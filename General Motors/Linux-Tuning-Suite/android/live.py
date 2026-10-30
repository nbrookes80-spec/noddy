"""Live streaming of the engine (ECU) and transmission (TCM) readings, with green/yellow/red health.

LiveStream sits on any source with poll(pids, headers=None): the demo drive or a real adapter link.
Each step() reads one round of readings. Fast readings (speed, throttle, gear) come every round;
slow ones (temperatures, pressures) every fourth round, so the screen stays quick on a slow adapter.

When the Shift Points settings and their calculated tables are supplied, every gear change the car
makes is compared with what the tables said it should do, and shown as green, yellow or red.
No Kivy here, so it can be tested on a desktop.
"""

import time
from collections import deque

import grading
from link import obd
from scanner import pids
from tunertoolpro import core

# Engine (ECU, answers on the broadcast address) first, then the transmission (TCM, 7E2) grouped
# together so the adapter only switches module once per round.
FAST_PIDS = ['010C', '010D', '0111', '22199A', '223D03', '221991']
SLOW_PIDS = ['0105', '0104', '010B', '010E', '22194F', '22001F', '221941', '221942', '22199E', '22199F']
STREAM_PIDS = FAST_PIDS + SLOW_PIDS
TCM_PIDS = {'22199A', '223D03', '22194F', '221991', '22001F', '221941', '221942', '22199E', '22199F'}
TCM_HEADER = '7E2'
SLOW_EVERY = 4
HISTORY = 60
KMH_TO_MPH = 0.621371
RATE_WINDOW = 10
SHIFT_LOG = 12

HEALTH = [('trans_temp', 'Transmission fluid'), ('engine_rpm', 'Engine speed'),
          ('coolant', 'Coolant'), ('pc_current', 'Line pressure solenoid'),
          ('gear_follow', 'Gear follows command')]


def _ordered(pid_list):
    """Engine readings first, transmission readings last, so the module address changes once."""
    return sorted(pid_list, key=lambda p: (p in TCM_PIDS, STREAM_PIDS.index(p)))


class LiveStream:
    def __init__(self, source, cfg=None, tables=None, clock=time.monotonic, transmission=True):
        self.source = source
        self.cfg = cfg
        self.tables = tables
        self.clock = clock
        self.transmission = transmission   # False: ask only the engine, so the TCM is never polled
        self.rounds = 0
        self.error = None
        self.latest = {}
        self.history = {p: deque(maxlen=HISTORY) for p in STREAM_PIDS}
        self.shifts = deque(maxlen=SHIFT_LOG)
        self._stamps = deque(maxlen=RATE_WINDOW)
        self._last_gear = None
        self._prev_speed = None
        self._mismatch_now = 0.0
        self._mismatch_since = None

    def set_model(self, cfg, tables):
        """Give the stream the current settings and tables, so live shifts are compared with them."""
        self.cfg, self.tables = cfg, tables

    # --- reading ---------------------------------------------------------------------------------

    def step(self):
        wanted = STREAM_PIDS if self.rounds % SLOW_EVERY == 0 else FAST_PIDS
        if not self.transmission:
            wanted = [p for p in wanted if p not in TCM_PIDS]
        wanted = _ordered(wanted)
        headers = {p: TCM_HEADER for p in wanted if p in TCM_PIDS}
        try:
            values, _errors = self.source.poll(wanted, headers=headers)
        except obd.OBDError as exc:
            self.error = str(exc)
            return
        self.error = None
        now = self.clock()
        self.rounds += 1
        self._stamps.append(now)
        for pid, (value, unit) in values.items():
            self.latest[pid] = (value, unit)
            self.history[pid].append(value)
        self._track_gear(now)
        self._prev_speed = self._value('010D')

    def _value(self, pid):
        reading = self.latest.get(pid)
        return None if reading is None else reading[0]

    def _track_gear(self, now):
        gear, commanded = self._value('22199A'), self._value('223D03')
        if gear is not None and commanded is not None and round(gear) != round(commanded):
            if self._mismatch_since is None:
                self._mismatch_since = now
        else:
            self._mismatch_since = None
        self._mismatch_now = now
        if gear is None:
            return
        previous, self._last_gear = self._last_gear, round(gear)
        if previous is not None and self._last_gear != previous:
            self._record_shift(previous, self._last_gear)

    def _record_shift(self, before, after):
        kind = 'up' if after > before else 'down'
        kmh, tps = self._value('010D'), self._value('0111')
        shift = {'kind': kind, 'from': before, 'to': after, 'mph': None, 'tps': tps,
                 'predicted_mph': None, 'delta_pct': None, 'level': grading.OFF, 'text': ''}
        if kmh is not None:
            # the shift happened between two readings, so use the speed halfway between them
            before_kmh = self._prev_speed if self._prev_speed is not None else kmh
            shift['mph'] = (before_kmh + kmh) / 2 * KMH_TO_MPH
        row = (before if kind == 'up' else after) - 1
        table = self.tables.get('upshift' if kind == 'up' else 'downshift') if self.tables else None
        if table and tps is not None and 0 <= row < len(table):
            shift['predicted_mph'] = _interpolate(table[row], tps)
        if shift['mph'] is not None and shift['predicted_mph']:
            shift['delta_pct'] = (shift['mph'] - shift['predicted_mph']) / shift['predicted_mph'] * 100
            shift['level'] = grading.grade_shift_delta(shift['delta_pct'])
            shift['text'] = (f'{before}-{after} at {shift["mph"]:.0f} mph, {tps:.0f}% throttle: your table '
                             f'says {shift["predicted_mph"]:.0f} mph ({shift["delta_pct"]:+.0f}%)')
        elif shift['mph'] is not None:
            shift['text'] = f'{before}-{after} at {shift["mph"]:.0f} mph'
        self.shifts.appendleft(shift)

    # --- reporting -------------------------------------------------------------------------------

    def rate_hz(self):
        if len(self._stamps) < 2:
            return 0.0
        span = self._stamps[-1] - self._stamps[0]
        return (len(self._stamps) - 1) / span if span > 0 else 0.0

    def health(self):
        tiles = []
        shift_rpm = self.cfg['shift_rpm'] if self.cfg else None
        graded = {
            'trans_temp': lambda v: grading.grade_trans_temp(v) if v is not None else None,
            'coolant': lambda v: grading.grade_coolant(v) if v is not None else None,
            'engine_rpm': lambda v: (grading.grade_engine_rpm(v, shift_rpm)
                                     if v is not None and shift_rpm else None),
        }
        sources = {'trans_temp': '22194F', 'coolant': '0105', 'engine_rpm': '010C'}
        for key, label in HEALTH:
            result = None
            if key in graded:
                result = graded[key](self._value(sources[key]))
            elif key == 'pc_current':
                actual, ref = self._value('22199E'), self._value('22199F')
                if actual is not None and ref is not None:
                    result = grading.grade_pc_current(actual, ref)
            elif key == 'gear_follow':
                seconds = (self._mismatch_now - self._mismatch_since
                           if self._mismatch_since is not None else 0.0)
                gear, commanded = self._value('22199A'), self._value('223D03')
                if gear is not None and commanded is not None:
                    result = grading.grade_gear_follow(gear, commanded, seconds)
            level, text = result if result else (grading.OFF, 'no reading yet')
            tiles.append({'key': key, 'label': label, 'level': level, 'text': text})
        return tiles

    def cursor(self):
        """Where the car is on the shift tables: {'gear': 1-based, 'tps': percent}, or None if unknown."""
        gear, tps = self._value('22199A'), self._value('0111')
        if gear is None or tps is None or round(gear) < 1:
            return None
        return {'gear': round(gear), 'tps': tps}

    def snapshot(self):
        values = {}
        for pid in STREAM_PIDS:
            reading = self.latest.get(pid)
            if reading is None:
                continue
            info = pids.get(pid)
            values[pid] = {'name': info.name if info else pid, 'value': reading[0], 'unit': reading[1],
                           'history': list(self.history[pid])}
        return {'values': values, 'health': self.health(), 'shifts': list(self.shifts),
                'rate_hz': self.rate_hz(), 'error': self.error, 'rounds': self.rounds}


def _interpolate(row, tps):
    """Table value at a throttle percentage, between the two nearest columns of the TPS axis."""
    axis = core.tps_axis()
    tps = min(max(tps, axis[0]), axis[-1])
    for i in range(len(axis) - 1):
        if tps <= axis[i + 1]:
            span = axis[i + 1] - axis[i]
            return row[i] + (row[i + 1] - row[i]) * (tps - axis[i]) / span
    return row[-1]
