"""Load a CAN log and the DBC file that decodes it, ready to play on Live and Scan. No Kivy.

The log can be a candump text file (the sniffer's own captures are this format), a CSV or SLCAN file; the DBC
is the message and signal list for the car. Files are looked for in two folders: the sniffer's captures and the
"CAN imports" folder, where the user puts files from the computer.
"""

import os
import time
from dataclasses import dataclass

from tunertoolpro.canbus.frames import read_log

from . import can_replay, dbc

LOG_SUFFIXES = ('.log', '.csv', '.txt')
DBC_SUFFIX = '.dbc'
MAX_BYTES = 2 * 1024 * 1024       # a bigger file is refused: at the measured 0.5 s per 323 KB this keeps the load to a few
                                  # seconds, because it runs on the screen's own thread


class ImportProblem(Exception):
    """A file that cannot be played; the message is for the user."""


@dataclass
class Loaded:
    name: str                # the log's file name
    entries: list            # the PIDs for the signals, for pids.set_replay
    source: object           # the can_replay.ReplaySource to play
    frames: int              # frames read from the log
    readings: int            # readings across all signals
    seconds: float           # length of the log
    signals: int             # signals with readings in this log

    dbc: str = ''            # the DBC file that decoded them

    def describe(self):
        return (f'Playing {self.signals} signals from {self.name}, decoded with {self.dbc}: {self.readings} readings '
                f'over {self.seconds:.0f} s, looping.')


def files_in(folder, suffixes):
    """The file names in a folder with one of these suffixes, sorted. A missing folder has none."""
    try:
        names = os.listdir(folder)
    except OSError:
        return []
    return sorted(n for n in names if n.lower().endswith(tuple(suffixes)) and os.path.isfile(os.path.join(folder, n)))


def load(log_path, dbc_path, clock=time.monotonic):
    """Decode a log with its DBC. Raises ImportProblem with a message the user can act on."""
    log_text = _read(log_path)
    dbc_text = _read(dbc_path)
    try:
        frames = read_log(log_text)
    except (ValueError, OverflowError, MemoryError):
        raise ImportProblem(f'{os.path.basename(log_path)} could not be read as a CAN log. Use a candump (.log), '
                            'CSV or SLCAN file.')
    if not frames:
        raise ImportProblem(f'No CAN frames were found in {os.path.basename(log_path)}. Use a candump (.log), '
                            'CSV or SLCAN file.')
    try:
        signals = dbc.parse(dbc_text)
    except (ValueError, OverflowError, MemoryError):
        raise ImportProblem(f'{os.path.basename(dbc_path)} could not be read as a DBC file.')
    if not signals:
        raise ImportProblem(f'No signals were found in {os.path.basename(dbc_path)}. Check that it is a DBC file.')
    try:
        replay = can_replay.decode(frames, signals)
    except can_replay.TooLong as exc:
        raise ImportProblem(str(exc))
    if not replay.series:
        raise ImportProblem('None of the DBC signals appear in this log. Check that the DBC is for this car.')
    entries = can_replay.catalogue_entries(replay, source_name=os.path.basename(dbc_path))
    readings = sum(len(times) for _signal, times, _values in replay.series.values())
    return Loaded(name=os.path.basename(log_path), entries=entries,
                  source=can_replay.ReplaySource(replay, clock=clock), frames=len(frames), readings=readings,
                  seconds=replay.span, signals=len(replay.series), dbc=os.path.basename(dbc_path))


def _read(path):
    try:
        if os.path.getsize(path) > MAX_BYTES:
            raise ImportProblem(f'{os.path.basename(path)} is larger than 2 MB. Use a shorter capture.')
        with open(path, encoding='utf-8', errors='replace') as fh:
            return fh.read()
    except OSError as exc:
        raise ImportProblem(f'Could not read {os.path.basename(path)}: {exc.strerror or exc}')
