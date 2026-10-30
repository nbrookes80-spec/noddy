"""Record the CAN bus for a set time through an ELM327 adapter, then save it as a candump log.

Run from the android/ folder:

    python3 tools/capture_can.py --seconds 60 --out capture.log
    python3 tools/capture_can.py --seconds 60 --prefs ~/.local/share/tunertoolpro/prefs.json

The monitor is receive-only: the adapter prints what it hears and sends nothing, so this cannot disturb the
car. Turn the ignition on first. Then decode the file with tools/decode_can.py.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from link.obd import OBDError  # noqa: E402
from scanner import capture, car_scan  # noqa: E402
from tunertoolpro.canbus.frames import format_candump  # noqa: E402
from tunertoolpro.canbus.monitor import PROTOCOLS  # noqa: E402


def build_parser():
    parser = argparse.ArgumentParser(description='Record CAN frames from the car to a log file.')
    parser.add_argument('--seconds', type=float, default=30.0, help='how long to listen (default %(default)s)')
    parser.add_argument('--out', default='capture.log', help='the log file to write (default %(default)s)')
    parser.add_argument('--protocol', default='6', choices=sorted(PROTOCOLS),
                        help='CAN protocol: 6 = 500 kbit/s 11-bit, the GM default (default %(default)s)')
    parser.add_argument('--rx-filter', help='only record this CAN ID, in hex, e.g. 7E8')
    parser.add_argument('--link', choices=('auto',) + car_scan.LINKS, default='auto',
                        help='how to reach the adapter (default: the saved app link, or wifi)')
    parser.add_argument('--prefs', help="the app's prefs.json, for the saved link and adapter address")
    parser.add_argument('--wifi', help='Wi-Fi adapter as host:port')
    parser.add_argument('--bluetooth', help='Bluetooth adapter address (Android only)')
    parser.add_argument('--serial', help='cable port, e.g. /dev/ttyUSB0 or COM3; implies --link cable')
    parser.add_argument('--baud', type=int, default=38400, help='cable baud rate (default %(default)s)')
    return parser


def open_transport(args):
    """The opened transport for the chosen link. Raises OBDError when it cannot connect."""
    saved = car_scan.saved_prefs(args.prefs)
    if args.wifi:
        saved['wifi'] = args.wifi
    if args.bluetooth:
        saved['bt_address'] = args.bluetooth
    link = car_scan.pick_link(args.link, args.serial, saved if args.prefs else None)
    transport = car_scan.transport_for(link, bt_address=saved['bt_address'], wifi=saved['wifi'],
                                       serial_port=args.serial, baud=args.baud)
    transport.open()
    return transport


def run(args, out=print):
    try:
        transport = open_transport(args)
    except OBDError as exc:
        out(str(exc))
        return 1
    try:
        out(f'Listening for {args.seconds:g} s on protocol {args.protocol}. Ignition on, please.')
        result = capture.record(transport, args.seconds, args.protocol, args.rx_filter)
    finally:
        transport.close()
    if result['error']:
        out(f'Capture stopped early: {result["error"]}')
    Path(args.out).write_text(format_candump(result['frames']), encoding='utf-8')
    out(f'Saved {len(result["frames"])} frames to {args.out}. Overruns (adapter buffer full): {result["overruns"]}.')
    out(f'Decode it with: python3 tools/decode_can.py {args.out}')
    return 0 if result['frames'] else 1


if __name__ == '__main__':
    sys.exit(run(build_parser().parse_args()))
