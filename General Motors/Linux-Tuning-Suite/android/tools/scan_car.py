"""Scan a car through a Wi-Fi ELM327 adapter and save which readings it answers for one profile.

Run from the android/ folder:

    python3 tools/scan_car.py --list
    python3 tools/scan_car.py holden-ve
    python3 tools/scan_car.py user-2011-holden-commodore --user-dir ~/.local/share/tunertoolpro/cars

The link is the one the app uses. With --prefs pointing at the app's saved settings (prefs.json), the scan
uses the Wi-Fi or Bluetooth adapter the user picked last. Without it, or with --link, it uses Wi-Fi. A cable
is used when --serial is given (desktop only, needs pyserial).

    python3 tools/scan_car.py holden-ve --prefs ~/.local/share/tunertoolpro/prefs.json
    python3 tools/scan_car.py holden-ve --link cable --serial /dev/ttyUSB0

The scan only sends the read-only Mode 01 and Mode 22 requests the app already allows, one per reading,
so it cannot change the car. Turn the ignition on before you start. The result is saved to
<folder>/<profile key>.scan.json. The app loads it when that profile is chosen and then offers only the
readings the car answered.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from link.obd import OBDError  # noqa: E402
from scanner import car_scan, profiles  # noqa: E402


def build_parser():
    parser = argparse.ArgumentParser(description='Scan a car and save what it answers for a profile.')
    parser.add_argument('profile', nargs='?', help='profile key, from --list')
    parser.add_argument('--list', action='store_true', help='list the profile keys and exit')
    parser.add_argument('--link', choices=('auto',) + car_scan.LINKS, default='auto',
                        help='how to reach the adapter (default: the saved app link, or wifi)')
    parser.add_argument('--prefs', help="the app's prefs.json, for the saved link and adapter address")
    parser.add_argument('--wifi', help='Wi-Fi adapter as host:port (default: the saved one, else 192.168.0.10:35000)')
    parser.add_argument('--bluetooth', help='Bluetooth adapter address, e.g. 00:1D:A5:68:98:8B (default: the saved one)')
    parser.add_argument('--serial', help='cable port, e.g. /dev/ttyUSB0 or COM3; implies --link cable')
    parser.add_argument('--baud', type=int, default=38400, help='cable baud rate (default %(default)s)')
    parser.add_argument('--folder', default='car_scans', help='where to save the scan (default %(default)s)')
    parser.add_argument('--user-dir', help='folder holding the saved user cars, so their profiles are listed too')
    return parser


def link_for(args, saved):
    """(elm, owned) over the link the user asked for. --link auto follows the app: a cable when --serial is
    given, otherwise the link saved on the Link screen, otherwise Wi-Fi. A live app connection is reused."""
    if args.link == 'auto':
        link = car_scan.LINK_CABLE if args.serial else (car_scan.link_from_prefs(saved) if args.prefs
                                                       else car_scan.LINK_WIFI)
    else:
        link = args.link
    if link == car_scan.LINK_CABLE:
        return car_scan.choose_link(None, {}, serial_port=args.serial, baud=args.baud)
    return car_scan.choose_link(None, dict(saved, link_kind='Bluetooth' if link == car_scan.LINK_BLUETOOTH
                                           else 'Wi-Fi'))


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

    saved = car_scan.saved_prefs(args.prefs)
    if args.wifi:
        saved['wifi'] = args.wifi
    if args.bluetooth:
        saved['bt_address'] = args.bluetooth
    if args.serial:
        args.link = car_scan.LINK_CABLE
    profiles.activate(chosen)
    extras = [p.pid for p in profiles.load_pids(chosen)[0]]
    ids = car_scan.scan_ids(extras, mode01_only=chosen.mode01_only)

    try:
        elm, owned = link_for(args, saved)
    except OBDError as exc:
        out(str(exc))
        return 1
    try:
        result = car_scan.scan(elm, ids, progress=lambda i, n, pid: out(f'[{i + 1}/{n}] {pid}'))
    finally:
        if owned:
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
