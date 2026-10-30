"""Scan a car through a Wi-Fi ELM327 adapter and save which readings it answers for one profile.

Run from the android/ folder:

    python3 tools/scan_car.py --list
    python3 tools/scan_car.py holden-ve
    python3 tools/scan_car.py user-2011-holden-commodore --user-dir ~/.local/share/tunertoolpro/cars

The scan only sends the read-only Mode 01 and Mode 22 requests the app already allows, one per reading,
so it cannot change the car. Turn the ignition on before you start, and connect to the adapter's Wi-Fi.
The result is saved to <folder>/<profile key>.scan.json. The app loads it when that profile is chosen and
then offers only the readings the car answered.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from link.obd import DEFAULT_WIFI, Elm327, OBDError, WifiTransport  # noqa: E402
from scanner import car_scan, profiles  # noqa: E402


def build_parser():
    parser = argparse.ArgumentParser(description='Scan a car and save what it answers for a profile.')
    parser.add_argument('profile', nargs='?', help='profile key, from --list')
    parser.add_argument('--list', action='store_true', help='list the profile keys and exit')
    parser.add_argument('--host', default=DEFAULT_WIFI[0], help='adapter address (default %(default)s)')
    parser.add_argument('--port', type=int, default=DEFAULT_WIFI[1], help='adapter port (default %(default)s)')
    parser.add_argument('--folder', default='car_scans', help='where to save the scan (default %(default)s)')
    parser.add_argument('--user-dir', help='folder holding the saved user cars, so their profiles are listed too')
    return parser


def run(args, out=print):
    available = profiles.everything(args.user_dir) if args.user_dir else profiles.built_in()
    if args.list:
        for profile in available:
            out(f'{profile.key:<32} {profile.name}')
        return 0
    chosen = next((p for p in available if p.key == args.profile), None)
    if chosen is None:
        out(f'No profile called {args.profile!r}. Use --list to see the keys.')
        return 2

    profiles.activate(chosen)
    extras = [p.pid for p in profiles.load_pids(chosen)[0]]
    ids = car_scan.scan_ids(extras, mode01_only=chosen.mode01_only)

    elm = Elm327(WifiTransport(args.host, args.port))
    try:
        elm.open()
    except (OSError, OBDError) as exc:
        out(f'Could not reach the adapter at {args.host}:{args.port}: {exc}')
        return 1
    try:
        result = car_scan.scan(elm, ids, progress=lambda i, n, pid: out(f'[{i + 1}/{n}] {pid}'))
    finally:
        elm.close()

    for pid, info in result['answered'].items():
        out(f'  yes  {pid}  {info["name"]}  on {info["header"]}')
    out(f'Answered {len(result["answered"])} of {len(ids)} readings; {len(result["silent"])} gave no reply.')
    if not result['complete']:
        out('The adapter stopped answering part way through, so the scan is incomplete.')
    path = car_scan.save_scan(args.folder, chosen.key, result)
    if path is None:
        out('Kept the earlier complete scan, because this one was cut short.')
    else:
        out(f'Saved {path}')
    return 0 if result['complete'] else 1


if __name__ == '__main__':
    sys.exit(run(build_parser().parse_args()))
