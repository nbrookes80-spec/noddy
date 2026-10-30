"""What the app remembers between runs: which link type and adapter the user picked last. No Kivy."""

import json
from pathlib import Path

from link.devices import normalise_address

KINDS = ('Bluetooth', 'Wi-Fi')
DEFAULTS = {'link_kind': 'Bluetooth', 'bt_address': '', 'wifi': '192.168.0.10:35000', 'auto_connect': False,
            'live_transmission': False,   # read the transmission (7E2) on the Live screen
            'adaptive_timing': False,     # ATAT1: let the adapter adjust its wait to the car
            'timeout_ms': 0,              # 0 keeps the adapter's own response timeout; else ATST in 4 ms steps
            'scan_profile': '',
            'debug_log': True}            # write a log file of each run, to bring back when something goes wrong           # the car profile Live and Scan read (its key); '' for the built-in list
TIMEOUT_CHOICES_MS = (0, 100, 200, 400)


def load(path):
    """The saved choices, or the defaults when there is no file or it is damaged."""
    result = dict(DEFAULTS)
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return result
    if not isinstance(data, dict):
        return result
    if data.get('link_kind') in KINDS:
        result['link_kind'] = data['link_kind']
    address = normalise_address(data.get('bt_address'))
    if address:
        result['bt_address'] = address
    if isinstance(data.get('auto_connect'), bool):
        result['auto_connect'] = data['auto_connect']
    if isinstance(data.get('wifi'), str) and data['wifi'].strip():
        result['wifi'] = data['wifi'].strip()
    for key in ('live_transmission', 'adaptive_timing', 'debug_log'):
        if isinstance(data.get(key), bool):
            result[key] = data[key]
    if data.get('timeout_ms') in TIMEOUT_CHOICES_MS:
        result['timeout_ms'] = data['timeout_ms']
    if isinstance(data.get('scan_profile'), str):
        result['scan_profile'] = data['scan_profile'][:80]
    return result


def save(path, choices):
    """Write the choices. A place that cannot be written is ignored: nothing here is essential."""
    clean = {key: choices.get(key, DEFAULTS[key]) for key in DEFAULTS}
    try:
        Path(path).write_text(json.dumps(clean))
    except OSError:
        pass
