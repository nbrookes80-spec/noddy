"""What the app remembers between runs: which link type and adapter the user picked last. No Kivy."""

import json
from pathlib import Path

from link.devices import normalise_address

KINDS = ('Bluetooth', 'Wi-Fi')
DEFAULTS = {'link_kind': 'Bluetooth', 'bt_address': '', 'wifi': '192.168.0.10:35000'}


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
    if isinstance(data.get('wifi'), str) and data['wifi'].strip():
        result['wifi'] = data['wifi'].strip()
    return result


def save(path, choices):
    """Write the choices. A place that cannot be written is ignored: nothing here is essential."""
    clean = {key: choices.get(key, DEFAULTS[key]) for key in DEFAULTS}
    try:
        Path(path).write_text(json.dumps(clean))
    except OSError:
        pass
