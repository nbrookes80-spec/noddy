"""One check of a car: which readings it answers, then a bus capture decoded. No Kivy.

This is what the Sniff tab's button runs. Everything is saved in the app's folders, and the summary is
returned for the screen:
  car_scans/<profile>.scan.json   the readings the car answered (used when this profile is chosen)
  captures/car-<stamp>.log        the raw capture, in candump format
  captures/car-<stamp>.txt        the readable report
  captures/car-<stamp>.csv        the same readings as a spreadsheet
"""

import os
from datetime import datetime
from pathlib import Path

from scanner import can_discovery, capture, car_scan, profiles
from tunertoolpro.canbus.frames import format_candump


def check(elm, profile, data_dir, seconds=60, scan_progress=None, capture_progress=None, when=None):
    """Scan the profile's readings, then record the bus. Returns a dict of the summary and the file paths."""
    stamp = (when or datetime.now()).strftime('%Y%m%d-%H%M%S')
    profiles.activate(profile)
    extras = [p.pid for p in profiles.load_pids(profile)[0]]
    ids = car_scan.scan_ids(extras, mode01_only=profile.mode01_only)
    scan = car_scan.scan(elm, ids, progress=scan_progress)
    saved = car_scan.save_scan(os.path.join(data_dir, 'car_scans'), profile.key, scan)
    if scan['complete']:
        profiles.activate(profile, scan=scan)   # the dashboard now shows only what this car answered

    recorded = capture.record(elm.transport, seconds, lock=elm._lock, progress=capture_progress)
    base = Path(data_dir) / 'captures' / f'car-{stamp}'
    base.parent.mkdir(parents=True, exist_ok=True)
    raw = base.with_suffix('.log')
    raw.write_text(format_candump(recorded['frames']), encoding='utf-8')
    report = can_discovery.report(recorded['frames'])
    report_path = base.with_suffix('.txt')
    report_path.write_text(report + '\n', encoding='utf-8')
    csv_path = base.with_suffix('.csv')
    csv_path.write_text(_csv_text(recorded['frames']), encoding='utf-8')
    return {
        'scan_text': car_scan.describe(scan),
        'scan_saved': saved is not None,
        'frames': len(recorded['frames']),
        'capture_error': recorded['error'],
        'report': report,
        'raw': str(raw),
        'report_path': str(report_path),
        'csv': str(csv_path),
    }


def _csv_text(frames):
    import csv
    import io
    buffer = io.StringIO()
    csv.writer(buffer).writerows(can_discovery.csv_rows(frames))
    return buffer.getvalue()
