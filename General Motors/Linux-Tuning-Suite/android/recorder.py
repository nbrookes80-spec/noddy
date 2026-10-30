"""Start and stop the data log, and keep both kinds of log copied to the phone's Documents folder. No Kivy.

The data log is the sensor recording (scanner/data_log.py). The debug log is the app's own diary
(scanner/session_log.py). Both live under "Tuner Tool Info" (scanner/storage.py): "Data logs" and "Debug logs".
"""

import os
import threading

from scanner import storage
from scanner.data_log import DataLogger


class Recorder:
    def __init__(self, session, base, columns, rate=lambda: 0):
        """columns is a callable giving the [(pid, label), ...] a new recording should have. rate is a callable
        giving the most rows to write per second (0 writes a row for every round of readings)."""
        self.session = session
        self.columns = columns
        self.rate = rate
        self.data_folder = storage.folder(base, storage.DATA_LOGS)
        self.debug_folder = storage.folder(base, storage.DEBUG_LOGS)
        self.logger = DataLogger(self.data_folder)
        session.data_log = self.logger
        self.copy_message = ''

    @property
    def running(self):
        return self.logger.running

    def toggle(self):
        """Start recording, or stop. Returns the sentence to show the user."""
        return self.stop() if self.running else self.start()

    def start(self):
        if self.session.active() is None:
            return 'Nothing to record yet. Connect to the adapter on the Link tab, or start the demo, then record.'
        per_second = self.rate()
        self.logger.min_interval = 1.0 / per_second if per_second else 0.0
        path = self.logger.start(self.columns())
        self.session.log.write('DATA', f'recording started: {os.path.basename(path)}, '
                                       f'{len(self.columns())} sensors, '
                                       f'{per_second or "every"} rows per second, source {self.session.status}')
        return f'Recording to Data logs/{os.path.basename(path)}'

    def stop(self):
        rows, skipped = self.logger.rows, sorted(self.logger.skipped)
        path = self.logger.stop()
        if not path:
            return 'Not recording.'
        self.session.log.write('DATA', f'recording stopped: {os.path.basename(path)}, {rows} rows'
                                       + (f', no column for {", ".join(skipped)}' if skipped else ''))
        self._publish_in_background(path, storage.DATA_LOGS)
        return f'Saved {rows} rows to Tuner Tool Info/Data logs/{os.path.basename(path)}'

    def elapsed_text(self):
        seconds = int(self.logger.elapsed())
        return f'{seconds // 60:02d}:{seconds % 60:02d}'

    def publish_debug(self):
        """Copy the debug log to Documents/Tuner Tool Info/Debug logs. Called now and then, and when the app stops."""
        path = self.session.log.path
        if path:
            self._publish_in_background(path, storage.DEBUG_LOGS)

    def publish_now(self, path, kind):
        """Copy and wait for the answer. Used when the app is closing."""
        done, message = storage.publish(path, kind)
        self.copy_message = message
        return done

    def _publish_in_background(self, path, kind):
        def work():
            self.copy_message = storage.publish(path, kind)[1]
        threading.Thread(target=work, daemon=True).start()
