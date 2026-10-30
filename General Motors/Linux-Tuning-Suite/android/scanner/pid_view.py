"""How each sensor is shown, saved between runs. No Kivy.

Per sensor the user can choose a display (text, digital, graph, histogram or analogue gauge), a red line
(the value the gauge marks in red from) and, by long pressing, a different name, unit or range. These are
display choices only: they never change what is sent to the car or how a reply is decoded (that stays in the
PID's own definition).
"""

import json
import math
from pathlib import Path

MODES = ('text', 'digital', 'graph', 'histogram', 'analogue')
MODE_NAMES = {'text': 'Text', 'digital': 'Digital gauge', 'graph': 'Graph', 'histogram': 'Histogram',
              'analogue': 'Analogue gauge'}
DEFAULT_MODE = 'digital'
NUMBERS = ('low', 'high', 'redline')
TEXTS = ('name', 'unit')


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        return None
    return float(value)


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
        """The name, unit, range and red line to show for a catalogue Pid: its own, unless the user changed them."""
        mine = self.data.get(pid.pid, {})
        low, high = mine.get('low', pid.low), mine.get('high', pid.high)
        if not low < high:
            low, high = pid.low, pid.high
        return {'name': mine.get('name', pid.name), 'unit': mine.get('unit', pid.unit), 'low': low,
                'high': high, 'redline': mine.get('redline'), 'mode': mine.get('mode', self.default_mode)}
