"""A debug log: one text file for each run of the app, so a drive can be gone over afterwards. No Kivy.

Each line is `HH:MM:SS.mmm KIND text`. The kinds used by the app:
  APP      start-up details and the saved settings
  SCREEN   which screen was opened
  LINK     connecting, connected, failed, lost
  TX / RX  what the adapter was sent and what it answered
  REFUSED  a command the read-only guard would not send
  ERR      an adapter or app error
  CAR      the car profile that was made active
  NOTE     text the user added by hand while testing
  CRASH    an uncaught error, with its traceback

The log never raises: a place that cannot be written just stops logging. It holds nothing secret (the Agent
token is never written), and it can be switched off from the menu.
"""

import os
import threading
import time
from datetime import datetime

KEEP_FILES = 15            # older run logs are deleted when a new one starts
MAX_BYTES = 5_000_000      # one run stops writing past this, so a long drive cannot fill the phone
FILE_PREFIX = 'session-'


class NullLog:
    """What the screens use until a real log exists, so they never have to check."""

    path = ''
    enabled = False

    def write(self, kind, text=''):
        pass

    def tail(self, max_bytes=40000):
        return ''

    def set_enabled(self, on):
        pass

    def new_file(self):
        pass


class SessionLog:
    def __init__(self, folder, enabled=True, clock=time.time):
        self.folder = folder
        self.enabled = bool(enabled)
        self._clock = clock
        self._lock = threading.Lock()
        self._handle = None
        self._written = 0
        self._failed = False
        self.path = ''

    def write(self, kind, text=''):
        """Add one line. Safe to call from any thread, and never raises."""
        if not self.enabled or self._failed:
            return
        with self._lock:
            try:
                if self._handle is None:
                    self._open()
                if self._written >= MAX_BYTES:
                    return
                stamp = self._clock()
                moment = time.strftime('%H:%M:%S', time.localtime(stamp))
                line = f'{moment}.{int((stamp % 1) * 1000):03d} {kind} {str(text).replace(chr(10), " | ")}\n'
                self._handle.write(line)
                self._handle.flush()
                self._written += len(line)
                if self._written >= MAX_BYTES:
                    self._handle.write('--- log is full, nothing more is saved for this run ---\n')
                    self._handle.flush()
            except OSError:
                self._failed = True

    def set_enabled(self, on):
        """Switching off stops writing; switching on carries on in the same file."""
        self.enabled = bool(on)
        if self._handle is not None:
            self.write('APP', 'debug log on' if self.enabled else 'debug log off')

    def new_file(self):
        """Close this run's file and start a fresh one, so a drive can be logged on its own."""
        with self._lock:
            if self._handle is not None:
                try:
                    self._handle.close()
                except OSError:
                    pass
            self._handle, self._written, self._failed, self.path = None, 0, False, ''
        self.enabled = True
        self.write('APP', 'new log started')

    def tail(self, max_bytes=40000):
        """The end of this run's log as text, for copying out of the app."""
        if not self.path:
            return ''
        try:
            with open(self.path, 'rb') as handle:
                handle.seek(0, os.SEEK_END)
                size = handle.tell()
                handle.seek(max(0, size - max_bytes))
                return handle.read().decode('utf-8', 'replace')
        except OSError:
            return ''

    def _open(self):
        os.makedirs(self.folder, exist_ok=True)
        stamp = datetime.fromtimestamp(self._clock()).strftime('%Y%m%d-%H%M%S')
        self.path = os.path.join(self.folder, f'{FILE_PREFIX}{stamp}.log')
        self._handle = open(self.path, 'a', encoding='utf-8')
        self._prune()

    def _prune(self):
        names = sorted(n for n in os.listdir(self.folder) if n.startswith(FILE_PREFIX) and n.endswith('.log'))
        for name in names[:-KEEP_FILES]:
            try:
                os.remove(os.path.join(self.folder, name))
            except OSError:
                pass
