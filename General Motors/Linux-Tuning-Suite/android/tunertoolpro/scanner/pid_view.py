"""How each sensor is shown, saved between runs. No Kivy.

Per sensor the user can choose a display (text, digital, graph, histogram or analogue gauge), colour zones
(red and yellow at either end, green between two limits, blue below a cold limit), an accent colour for the
number and gauge, and, by long pressing, a different name, unit or range. These are display choices only: they never change what is sent to the car or how a reply is
decoded (that stays in the PID's own definition).

Ranges and limits are saved in the sensor's own unit and converted for the screen, so changing between C and F
(scanner/units.py) never moves a red line. A sensor given a unit of its own is shown, and edited, unconverted.
"""

import json
import math
import re
from pathlib import Path

from . import units

MODES = ('text', 'digital', 'graph', 'histogram', 'analogue')
MODE_NAMES = {'text': 'Text', 'digital': 'Digital gauge', 'graph': 'Graph', 'histogram': 'Histogram',
              'analogue': 'Analogue gauge'}
DEFAULT_MODE = 'digital'
NUMBERS = ('low', 'high', 'redline', 'cold', 'good', 'red_low', 'warn_low', 'good_to', 'warn')
ZONE_KEYS = NUMBERS[2:]      # the limits that make up the zones, in the units of the sensor
TEXTS = ('name', 'unit')
ZONE_ORDER = ('red', 'yellow', 'good', 'cold')    # which zone wins when a reading is in more than one
ZONE_LABELS = {'red_low': 'Red at or below', 'warn_low': 'Yellow at or below', 'cold': 'Blue below',
               'good': 'Green from', 'good_to': 'Green up to', 'warn': 'Yellow from', 'redline': 'Red from'}
_COLOR = re.compile(r'#[0-9A-Fa-f]{6}')


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        return None
    return float(value)


def _limit(shown, key):
    value = shown.get(key)
    return None if value is None else _number(value)


def zone(value, shown):
    """Which zone a reading is in: 'red', 'yellow', 'good', 'cold', or None for the ordinary colour.

    Red comes first (`redline` or above, `red_low` or below), then yellow (`warn` or above, `warn_low` or below),
    then green (`good` up to `good_to`, either end may be missing), then blue (below `cold`)."""
    if value is None:
        return None
    limit = lambda key: _limit(shown, key)    # noqa: E731
    redline, red_low, warn, warn_low = limit('redline'), limit('red_low'), limit('warn'), limit('warn_low')
    if (redline is not None and value >= redline) or (red_low is not None and value <= red_low):
        return 'red'
    if (warn is not None and value >= warn) or (warn_low is not None and value <= warn_low):
        return 'yellow'
    good, good_to, cold = limit('good'), limit('good_to'), limit('cold')
    if (good is not None or good_to is not None) and (good is None or value >= good) \
            and (good_to is None or value <= good_to):
        return 'good'
    if cold is not None and value < cold:
        return 'cold'
    return None


def zone_problems(entry):
    """Plain-English problems with the order of a sensor's zone limits (empty when they make sense).

    Only the numbers that are set are compared, so a sensor with just a red line, or just a red low limit, is fine.
    The numbers can be in any one unit, as long as they are all in the same one."""
    mine = {key: _limit(entry, key) for key in ZONE_KEYS} if isinstance(entry, dict) else {}
    out = []

    def check(low_key, high_key, allow_equal, message):
        low, high = mine.get(low_key), mine.get(high_key)
        if low is not None and high is not None and (low > high if allow_equal else low >= high):
            out.append(message.format(low=ZONE_LABELS[low_key], high=ZONE_LABELS[high_key]))
    check('red_low', 'warn_low', False, '{low} must be lower than {high}.')
    check('warn', 'redline', False, '{low} must be lower than {high}.')
    check('good', 'good_to', True, '{high} must not be lower than {low}.')
    check('cold', 'good', True, '{low} must not be higher than {high}.')
    check('good', 'redline', False, '{low} must be lower than {high}.')
    for low_key in ('red_low', 'warn_low'):         # the low side of the scale must stay below the high side
        for high_key in ('warn', 'redline'):
            check(low_key, high_key, False, '{low} must be lower than {high}.')
    return out


def bands(shown, low, high):
    """The coloured stretches of a scale from `low` to `high` as (from, to, zone) in the same units as the limits.

    Each stretch has the zone that `zone` gives for it, so a picture of the bands always agrees with the colour
    of the number. Stretches with no zone are left out and neighbours in the same zone are joined."""
    if not (isinstance(low, (int, float)) and isinstance(high, (int, float)) and low < high):
        return []
    inside = {x for x in (_limit(shown, key) for key in ZONE_KEYS) if x is not None and low < x < high}
    edges = sorted(inside | {float(low), float(high)})
    out = []
    for start, end in zip(edges, edges[1:]):
        name = zone((start + end) / 2, shown)
        if name is None:
            continue
        if out and out[-1][2] == name and out[-1][1] == start:
            out[-1] = (out[-1][0], end, name)
        else:
            out.append((start, end, name))
    return out


def clean_color(value):
    """'#RRGGBB' in capitals, or None when the text is not a colour of that form."""
    if isinstance(value, str) and _COLOR.fullmatch(value.strip()):
        return value.strip().upper()
    return None


def rgba(color, alpha=1.0):
    """A '#RRGGBB' text as (red, green, blue, alpha) floats from 0 to 1, or None when it is not a colour."""
    color = clean_color(color)
    if color is None:
        return None
    return tuple(int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)) + (alpha,)


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
        if clean_color(entry.get('color')) is not None:
            out['color'] = clean_color(entry['color'])
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
        if pid.pid in units.BOOST_PIDS and pid.unit == 'kPa':
            return units.boost_conversion(pid.unit, self.units)
        return units.conversion(pid.unit, self.units)

    def set_default(self, mode):
        """Choose how every sensor is drawn until it has its own choice. An unknown mode is ignored."""
        if mode in MODES:
            self.default_mode = mode

    def clear_modes(self):
        """Every sensor back to the default display. Names, units, ranges, zones and colours are kept."""
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
        out = {'name': mine.get('name', pid.name), 'unit': conv.unit, 'low': shown(low), 'high': shown(high),
               'mode': mine.get('mode', self.default_mode), 'color': mine.get('color'),
               'convert': conv.forward, 'back': conv.back}
        for key in ZONE_KEYS:
            out[key] = shown(mine.get(key))
        return out
