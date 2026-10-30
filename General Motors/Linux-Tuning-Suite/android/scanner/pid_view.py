"""How each sensor is shown, saved between runs. No Kivy.

Per sensor the user can choose a display (text, digital, graph, histogram or analogue gauge), colour bands
(blue below a cold limit, green from a good limit, red from the red line) and, by long pressing, a different
name, unit or range. These are display choices only: they never change what is sent to the car or how a reply is
decoded (that stays in the PID's own definition).

Ranges and limits are saved in the sensor's own unit and converted for the screen, so changing between C and F
(scanner/units.py) never moves a red line. A sensor given a unit of its own is shown, and edited, unconverted.
"""

import json
import math
from pathlib import Path

from . import units

MODES = ('text', 'digital', 'graph', 'histogram', 'analogue')
MODE_NAMES = {'text': 'Text', 'digital': 'Digital gauge', 'graph': 'Graph', 'histogram': 'Histogram',
              'analogue': 'Analogue gauge'}
DEFAULT_MODE = 'digital'
NUMBERS = ('low', 'high', 'redline', 'cold', 'good')
TEXTS = ('name', 'unit')


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        return None
    return float(value)


def zone(value, shown):
    """Which colour band a reading is in: 'red', 'cold', 'good', or None for the ordinary colour."""
    if value is None:
        return None
    if shown.get('redline') is not None and value >= shown['redline']:
        return 'red'
    if shown.get('cold') is not None and value < shown['cold']:
        return 'cold'
    if shown.get('good') is not None and value >= shown['good']:
        return 'good'
    return None


class Stats:
    """Lowest, highest and average of what a sensor has read since it was last reset."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.low = self.high = None
        self.total, self.count = 0.0, 0

    def add(self, value):
        if value is None or not math.isfinite(value):
            return
        self.low = value if self.low is None else min(self.low, value)
        self.high = value if self.high is None else max(self.high, value)
        self.total += value
        self.count += 1

    @property
    def average(self):
        return self.total / self.count if self.count else None


def clean(entry):
    """One sensor's saved choices, keeping only values that make sense."""
    out = {}
    if isinstance(entry, dict):
        if entry.get('mode') in MODES:
            out['mode'] = entry['mode']
        for key in NUMBERS:
            if key in entry and _number(entry[key]) is not None:
                out[key] = _number(entry[key])
        for key, limit in (('name', 80), ('unit', 12)):
            if isinstance(entry.get(key), str) and entry[key].strip():
                out[key] = entry[key].strip()[:limit]
    return out


class PidViews:
    """The saved display choices for every sensor, kept in one JSON file."""

    def __init__(self, path):
        self.path = Path(path)
        self.data = {}
        self.default_mode = DEFAULT_MODE    # what a sensor shows until its own card is changed
        self.units = units.clean(None)      # the user's temperature, pressure and speed units
        try:
            raw = json.loads(self.path.read_text(encoding='utf-8'))
            if isinstance(raw, dict):
                self.data = {pid: clean(entry) for pid, entry in raw.items() if isinstance(pid, str)}
        except (OSError, ValueError):
            pass

    def get(self, pid_id):
        return dict(self.data.get(pid_id, {}))

    def mode(self, pid_id):
        return self.data.get(pid_id, {}).get('mode', self.default_mode)

    def update(self, pid_id, **changes):
        """Change some choices for a sensor. A value of None removes that choice. Saves at once."""
        entry = dict(self.data.get(pid_id, {}))
        for key, value in changes.items():
            if value is None:
                entry.pop(key, None)
            else:
                entry[key] = value
        entry = clean(entry)
        if entry:
            self.data[pid_id] = entry
        else:
            self.data.pop(pid_id, None)
        self.save()

    def reset(self, pid_id):
        """Back to the sensor's own name, unit and range, keeping the chosen display."""
        keep = {'mode': self.data[pid_id]['mode']} if 'mode' in self.data.get(pid_id, {}) else {}
        self.data.pop(pid_id, None)
        if keep:
            self.data[pid_id] = keep
        self.save()

    def set_units(self, choices):
        """Show temperatures, pressures and speeds in these units (see scanner/units.py). Nothing is saved here."""
        self.units = units.clean(choices)

    def conversion(self, pid):
        """How a reading of this sensor is converted for the screen. A unit the user typed in is shown as it is."""
        if self.data.get(pid.pid, {}).get('unit', pid.unit) != pid.unit:
            return units.Conversion(self.data[pid.pid]['unit'], units.identity, units.identity)
        return units.conversion(pid.unit, self.units)

    def set_default(self, mode):
        """Choose how every sensor is drawn until it has its own choice. An unknown mode is ignored."""
        if mode in MODES:
            self.default_mode = mode

    def clear_modes(self):
        """Every sensor back to the default display. Names, units, ranges and red lines are kept."""
        for pid_id in list(self.data):
            self.data[pid_id].pop('mode', None)
            if not self.data[pid_id]:
                del self.data[pid_id]
        self.save()

    def save(self):
        try:
            self.path.write_text(json.dumps(self.data), encoding='utf-8')
        except OSError:
            pass   # a display choice is not worth stopping the app for

    def apply(self, pid):
        """What to show for a catalogue Pid: its own name, unit, range and limits unless the user changed them,
        in the user's units. `convert` turns a reading of the sensor into the shown unit and `back` reverses it."""
        mine = self.data.get(pid.pid, {})
        conv = self.conversion(pid)
        low, high = mine.get('low', pid.low), mine.get('high', pid.high)
        if not low < high:
            low, high = pid.low, pid.high

        def shown(value):
            return None if value is None else conv.forward(value)
        return {'name': mine.get('name', pid.name), 'unit': conv.unit, 'low': shown(low), 'high': shown(high),
                'redline': shown(mine.get('redline')), 'cold': shown(mine.get('cold')), 'good': shown(mine.get('good')),
                'mode': mine.get('mode', self.default_mode), 'convert': conv.forward, 'back': conv.back}
