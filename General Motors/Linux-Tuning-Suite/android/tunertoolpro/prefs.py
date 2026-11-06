"""What the app remembers between runs: which link type and adapter the user picked last. No Kivy."""

import json
from pathlib import Path

from tunertoolpro.link import obd
from tunertoolpro.link.devices import normalise_address
from tunertoolpro.scanner import calais, dashboard_layout, page_layout, pid_view, pids, shift_light, themes, units

KINDS = ('Bluetooth', 'Wi-Fi')
# The start-up set for this version. A saved file from an older version gets it once, on the next start, and the
# owner's own choices after that are kept. Bump SETTINGS_VERSION to apply a new set again.
SETTINGS_VERSION = 1
START_SETTINGS = {'live_transmission': True,       # the TCM readings show on Live from the start
                  'scan_profile': calais.CAR_KEY,  # the CALAIS TURBO car is the one Live and Scan read
                  'intro_music': True}
DEFAULTS = {'link_kind': 'Bluetooth', 'bt_address': '', 'wifi': '192.168.0.10:35000', 'auto_connect': False,
            'live_transmission': START_SETTINGS['live_transmission'],   # read the transmission (7E2) on the Live screen
            'adaptive_timing': False,     # ATAT1: let the adapter adjust its wait to the car
            'timeout_ms': 0,              # 0 keeps the adapter's own response timeout; else ATST in 4 ms steps
            'scan_profile': START_SETTINGS['scan_profile'],   # the car Live and Scan read
            'settings_version': SETTINGS_VERSION,
            'debug_log': True,            # write a log file of each run, to bring back when something goes wrong
            'dash_columns': 0,            # sensor cards across: 0 fits as many as the screen allows
            'dash_page_size': dashboard_layout.DEFAULT_PAGE_SIZE,   # sensors per full-screen page: 4, 5 or 6
            'dash_order': [],             # the user's sensor order on the dashboard, by PID id (scanner/dashboard_layout.py)
            'dash_template': page_layout.DEFAULT,   # full-screen page layout for every page (scanner/page_layout.py)
            'dash_page_templates': {},    # {page index as a string: template id} for pages with their own layout
            'dash_theme': 'classic',      # gauge colours (scanner/themes.py)
            'dash_default_mode': 'digital',   # how a sensor is drawn until its own card is changed
            'dash_stats': True,           # show lowest, highest and average under each sensor's number
            'hud_mirror': False,          # full screen shows mirrored, to read as a reflection on the windscreen
            'unit_temperature': units.DEFAULTS['temperature'],   # how readings are shown (scanner/units.py)
            'unit_pressure': units.DEFAULTS['pressure'],
            'unit_speed': units.DEFAULTS['speed'],
            'log_scope': 'all',           # what a recording has columns for: all, live (the Live stream) or dashboard
            'log_rate': 0,                # most rows written per second; 0 writes a row for every round of readings
            'adapter_protocol': '0',      # ATSP choice: 0 automatic, or a CAN protocol number (link/obd.PROTOCOLS)
            'hidden_pids': {},            # {car profile key: [PID ids the user hid from the dashboard]}
            'intro_music': True,          # play the intro theme while the start-up pictures show
            'calais_saved': False,        # the CALAIS TURBO car has been set up once (scanner/calais.py)
            'light_on': False,            # the shift light on the Live screen (scanner/shift_light.py)
            **{f'light_{key}': value for key, value in shift_light.DEFAULTS.items()}}
TIMEOUT_CHOICES_MS = (0, 100, 200, 400)
COLUMN_CHOICES = (0, 2, 3, 4)
LOG_SCOPES = ('all', 'live', 'dashboard')
LOG_RATES = (0, 1, 2, 5, 10)


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
    for key in ('live_transmission', 'adaptive_timing', 'debug_log', 'dash_stats', 'hud_mirror', 'intro_music',
                'calais_saved'):
        if isinstance(data.get(key), bool):
            result[key] = data[key]
    if data.get('timeout_ms') in TIMEOUT_CHOICES_MS:
        result['timeout_ms'] = data['timeout_ms']
    if isinstance(data.get('scan_profile'), str):
        result['scan_profile'] = data['scan_profile'][:80]
    if data.get('dash_columns') in COLUMN_CHOICES and not isinstance(data.get('dash_columns'), bool):
        result['dash_columns'] = data['dash_columns']
    if data.get('dash_page_size') in dashboard_layout.PAGE_SIZES and not isinstance(data.get('dash_page_size'), bool):
        result['dash_page_size'] = data['dash_page_size']
    result['dash_order'] = dashboard_layout.clean_order(data.get('dash_order'))
    result['dash_template'] = page_layout.clean_choice(data.get('dash_template'))
    result['dash_page_templates'] = page_layout.clean_per_page(data.get('dash_page_templates'))
    if data.get('dash_theme') in themes.THEMES:
        result['dash_theme'] = data['dash_theme']
    if data.get('dash_default_mode') in pid_view.MODES:
        result['dash_default_mode'] = data['dash_default_mode']
    chosen = units.clean({group: data.get(f'unit_{group}') for group in units.CHOICES})
    for group in units.CHOICES:
        result[f'unit_{group}'] = chosen[group]
    if data.get('log_scope') in LOG_SCOPES:
        result['log_scope'] = data['log_scope']
    if data.get('log_rate') in LOG_RATES and not isinstance(data.get('log_rate'), bool):
        result['log_rate'] = data['log_rate']
    if data.get('adapter_protocol') in obd.PROTOCOLS:
        result['adapter_protocol'] = data['adapter_protocol']
    result['hidden_pids'] = _hidden(data.get('hidden_pids'))
    if isinstance(data.get('light_on'), bool):
        result['light_on'] = data['light_on']
    light = shift_light.clean({key: data.get(f'light_{key}') for key in shift_light.DEFAULTS})
    for key, value in light.items():
        result[f'light_{key}'] = value
    if data.get('settings_version') != SETTINGS_VERSION:
        result.update(START_SETTINGS)
    result['settings_version'] = SETTINGS_VERSION
    return result


def _hidden(raw):
    """The hidden-PID table, keeping only well formed entries."""
    out = {}
    if isinstance(raw, dict):
        for key, ids in raw.items():
            if isinstance(key, str) and isinstance(ids, list):
                kept = sorted({i.upper() for i in ids if isinstance(i, str) and pids.valid_id(i.upper())})
                if kept:
                    out[key[:80]] = kept
    return out


def save(path, choices):
    """Write the choices. A place that cannot be written is ignored: nothing here is essential."""
    clean = {key: choices.get(key, DEFAULTS[key]) for key in DEFAULTS}
    clean['hidden_pids'] = _hidden(clean['hidden_pids'])
    clean['dash_template'] = page_layout.clean_choice(clean['dash_template'])
    clean['dash_page_templates'] = page_layout.clean_per_page(clean['dash_page_templates'])
    try:
        Path(path).write_text(json.dumps(clean))
    except OSError:
        pass
