"""Print a plain-text report of a CAN capture: module readings, broadcast traffic and missing readings.

Run from the android/ folder:

    python3 tools/decode_can.py capture.log
    python3 tools/decode_can.py capture.log --out report.txt

The file can be a candump log (from tools/capture_can.py), SLCAN, ELM327 monitor text, or CSV.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import can_discovery  # noqa: E402
from tunertoolpro.canbus.frames import read_log  # noqa: E402


def build_parser():
    parser = argparse.ArgumentParser(description='Decode a CAN capture into a readable report.')
    parser.add_argument('capture', help='the capture file to read')
    parser.add_argument('--out', help='also save the report to this file')
    return parser


def run(args, out=print):
    text = Path(args.capture).read_text(encoding='utf-8', errors='replace')
    text_report = can_discovery.report(read_log(text))
    out(text_report)
    if args.out:
        Path(args.out).write_text(text_report + '\n', encoding='utf-8')
        out(f'Saved the report to {args.out}')
    return 0


if __name__ == '__main__':
    sys.exit(run(build_parser().parse_args()))
