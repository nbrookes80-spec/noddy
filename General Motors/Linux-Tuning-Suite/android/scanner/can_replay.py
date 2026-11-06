"""Play back a CAN log decoded with a DBC, as a data source the Live and Scan screens read. No Kivy.

A capture (candump text, CSV or SLCAN, read by tunertoolpro/canbus/frames.py) and a DBC are decoded once into a
time series for each signal. The ReplaySource then plays those series back in real time, looping at the end, and
answers poll() the way the adapter and the demo do. Each signal becomes a PID with an id that starts with CAN, so
it can never be sent to the car (pids.valid_id only accepts the Mode 01 and Mode 22 reads).
"""

import bisect
import time
from dataclasses import dataclass, field

from link import obd

from . import dbc, gmlan, pids

CATEGORY = 'Imported'
SOURCE = 'CAN import'
LABEL = 'CAN import'
MAX_SAMPLES = 200_000    # readings across all signals; a log needing more is refused (about 20 MB of Python objects)


def replay_id(signal, index):
    """The PID id for a signal: CAN, the message ID in hex (X when extended), then the signal's place in the DBC."""
    return f'CAN{signal.message_id:X}{"X" if signal.extended else ""}.{index}'


@dataclass
class Replay:
    """Decoded signals: each id maps to (signal, times, values), with times in seconds from the log's start."""
    series: dict = field(default_factory=dict)
    frames: list = field(default_factory=list)      # the log's own frames, for the bus (gear) reads
    stamps: list = field(default_factory=list)      # each frame's time from the log's start, in the same order
    first: float = 0.0
    last: float = 0.0

    @property
    def span(self):
        return self.last - self.first

    def ids(self):
        return list(self.series)


class TooLong(ValueError):
    pass


def decode(frames, signals):
    """Decode every signal the DBC defines that appears in the frames. Returns a Replay.

    Multiplexed signals (m<n>) only take a reading in the frames where their multiplexer reads n.
    Raises TooLong when the log would need more than MAX_SAMPLES readings.
    """
    frames = sorted(frames, key=lambda f: f.timestamp)
    by_key, muxers = {}, {}
    for index, signal in enumerate(signals):
        by_key.setdefault(signal.key, []).append((index, signal))
        if signal.mux_role == 'M':
            muxers[signal.key] = signal
    wanted = {key for key in by_key}
    # Keep only the frames the DBC decodes, plus the gear message for the bus reads, so memory is not spent on the
    # rest of the bus (a frame costs about 180 bytes of Python objects).
    keep = wanted | {(gmlan.GEAR_ID, False)}
    frames = [f for f in frames if (f.can_id, f.extended) in keep]
    replay = Replay(frames=frames)
    if not frames:
        return replay
    replay.first, replay.last = frames[0].timestamp, frames[-1].timestamp
    replay.stamps = [f.timestamp - replay.first for f in frames]
    count = 0
    for frame in frames:
        key = (frame.can_id, frame.extended)
        if key not in wanted:
            continue
        mux_raw = None
        if key in muxers:
            mux_raw = dbc.raw_value(muxers[key], frame.data)
        for index, signal in by_key[key]:
            if signal.mux_role == 'M':
                continue
            if signal.mux_role == 'm' and mux_raw != signal.mux_value:
                continue
            raw = dbc.raw_value(signal, frame.data)
            if raw is None:
                continue
            count += 1
            if count > MAX_SAMPLES:
                raise TooLong(f'more than {MAX_SAMPLES} readings; use a shorter capture')
            entry = replay.series.setdefault(replay_id(signal, index), (signal, [], []))
            entry[1].append(frame.timestamp - replay.first)
            entry[2].append(signal.physical(raw))
    return replay


def value_at(times, values, t):
    """The last reading at or before t, held until the next one. None before the first reading."""
    at = bisect.bisect_right(times, t) - 1
    return values[at] if at >= 0 else None


def pid_for(pid_id, signal, values, source_name=''):
    """The catalogue entry for one decoded signal. Its range is the DBC range, or the range seen in the log."""
    low, high = signal.minimum, signal.maximum
    if not high > low:
        low, high = (min(values), max(values)) if values else (0.0, 1.0)
    if not high > low:
        low, high = low - 1.0, high + 1.0
    return pids.Pid(pid=pid_id, name=signal.name, category=CATEGORY, unit=signal.unit, low=low, high=high,
                    description=(f'From the imported CAN log {source_name}: ' if source_name else 'From the imported CAN log: ')
                                 + f'message {signal.message} (ID {signal.message_id:X}).',
                    header='', kind='word', decode=lambda raw: raw, source=SOURCE, trusted=False)


def catalogue_entries(replay, source_name=''):
    """The PIDs for every decoded signal, in the order their first reading appears in the log. source_name (the DBC's file name)
    is put in each description, so the owner can see which file decoded the values."""
    return [pid_for(pid_id, signal, values, source_name)
            for pid_id, (signal, _times, values) in replay.series.items()]


class ReplaySource:
    """Same read methods as the adapter and the demo: read(), poll(), read_dtcs(), listen(), close().

    The log's time runs at real speed from the moment the replay starts, and starts again at the beginning when
    it reaches the end (unless loop is False, when it holds the last reading).
    """

    label = LABEL

    def __init__(self, replay, clock=time.monotonic, loop=True):
        self.replay = replay
        self._clock = clock
        self._start = clock()
        self._loop = loop
        self.traffic = []
        self.on_values = None

    def now(self):
        """The log's time now, in seconds from its first frame."""
        elapsed = self._clock() - self._start
        span = self.replay.span
        if span <= 0:
            return 0.0
        if self._loop:
            return elapsed % span
        return min(elapsed, span)

    def read(self, pid_id):
        entry = self.replay.series.get(pid_id)
        if entry is None:
            raise KeyError(pid_id)
        _signal, times, values = entry
        reading = value_at(times, values, self.now())
        return reading, entry[0].unit

    def poll(self, pid_ids, headers=None):
        now = self.now()
        values = {}
        for pid_id in pid_ids:
            entry = self.replay.series.get(pid_id)
            if entry is None:
                continue
            reading = value_at(entry[1], entry[2], now)
            if reading is not None:
                values[pid_id] = (reading, entry[0].unit)
        if self.on_values is not None and values:
            self.on_values(values)
        return values, {}

    def listen(self, seconds):
        """The log's own frames from the last few seconds, so a gear message in the capture still reads."""
        now = self.now()
        stamps = self.replay.stamps
        lo = bisect.bisect_right(stamps, now - seconds)
        hi = bisect.bisect_right(stamps, now)
        return self.replay.frames[lo:hi]

    def read_dtcs(self):
        raise obd.OBDError('A CAN log is playing, not the car. Stop the log to read codes.')

    def clear_dtcs(self):
        raise obd.OBDError('A CAN log is playing, not the car. Stop the log first.')

    def close(self):
        pass


