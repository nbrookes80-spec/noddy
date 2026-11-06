"""The data log: a recording of every sensor reading the app takes, saved as a spreadsheet. No Kivy.

This is separate from the debug log (session_log.py), which records what the app and the adapter said.
One recording is one CSV file named by its start date and time. Each row is one moment: the seconds since
the recording began, the clock time, then one column per sensor. A sensor that has not been read yet is
left blank, and one that was read earlier keeps its last value until it is read again, so the file opens
cleanly in a spreadsheet and plots without gaps.

The columns are fixed when the recording starts (every sensor the app reads). A reading that turns up later
that has no column is counted in `skipped` rather than being written out of place.
"""

import csv
import os
import threading
import time

from . import storage


class DataLogger:
    def __init__(self, folder, clock=time.time):
        self.folder = folder
        self._clock = clock
        self._lock = threading.Lock()
        self._handle = None
        self._writer = None
        self._latest = {}
        self._columns = []
        self.path = ''
        self.rows = 0
        self.skipped = set()
        self.began = 0.0
        self.error = ''
        self.min_interval = 0.0    # seconds between rows; 0 writes a row for every round of readings
        self._last_row = None

    @property
    def running(self):
        return self._handle is not None

    def elapsed(self):
        return self._clock() - self.began if self.running else 0.0

    def start(self, columns):
        """Begin a recording. columns is a list of (pid, label) pairs, one for each sensor."""
        with self._lock:
            if self._handle is not None:
                return self.path
            self.error = ''
            os.makedirs(self.folder, exist_ok=True)
            self.began = self._clock()
            self.path = os.path.join(self.folder, f'{storage.stamp(self.began)}.csv')
            self._columns = [pid for pid, _label in columns]
            self._latest = {}
            self.rows, self.skipped, self._last_row = 0, set(), None
            self._handle = open(self.path, 'w', newline='', encoding='utf-8')
            self._writer = csv.writer(self._handle)
            self._writer.writerow(['time_s', 'clock'] + [label for _pid, label in columns])
            self._handle.flush()
            return self.path

    def update(self, values):
        """Take a round of readings, {pid: (value, unit)}, and write one row. Does nothing when not recording."""
        if self._handle is None or not values:
            return
        with self._lock:
            if self._handle is None:
                return
            for pid, reading in values.items():
                if pid in self._columns:
                    self._latest[pid] = reading[0]
                else:
                    self.skipped.add(pid)
            now = self._clock()
            if self._last_row is not None and now - self._last_row < self.min_interval:
                return    # the readings are kept, and go into the next row that is written
            self._last_row = now
            clock_text = time.strftime('%H:%M:%S', time.localtime(now)) + f'.{int((now % 1) * 1000):03d}'
            row = [f'{now - self.began:.3f}', clock_text]
            row += [f'{self._latest[pid]:.6g}' if pid in self._latest else '' for pid in self._columns]
            try:
                self._writer.writerow(row)
                self._handle.flush()
                self.rows += 1
            except OSError as exc:
                self.error = str(exc)
                self._close()

    def stop(self):
        """End the recording. Returns the file's path (empty if none was running)."""
        with self._lock:
            path = self.path if self._handle is not None else ''
            self._close()
            return path

    def _close(self):
        if self._handle is not None:
            try:
                self._handle.close()
            except OSError:
                pass
        self._handle = self._writer = None
