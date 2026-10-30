"""One running sniffer: a frame source, the Sniffer that tracks it, and the frames kept for saving.

Screens on every platform use this so they only draw. The source is the simulated bus, a log file, or
an adapter heard through ElmMonitor on a background thread. An adapter's transport may be owned by
someone else (the Android app's open Bluetooth link): pass owns_transport=False and a lock, and the
session holds that lock for as long as it listens, then hands the adapter back as the OBD link expects.
"""

import queue
import threading
import time

from .frames import format_candump, format_csv
from .monitor import DEFAULT_PROTOCOL, ElmMonitor, MonitorError
from .sniffer import Sniffer
from .sources import DemoBus, LogPlayer

CAPTURE_LIMIT = 500_000
READY_TIMEOUT = 10.0


class SnifferSession:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.sniffer = Sniffer(clock)
        self.captured = []
        self.error = ''
        self.label = ''
        self.monitor = None
        self._source = None
        self._thread = None
        self._stop = threading.Event()
        self._inbox = queue.Queue()

    # --- state -----------------------------------------------------------------------------------
    @property
    def running(self):
        return self._source is not None or self._thread is not None

    @property
    def listening_to_adapter(self):
        return self._thread is not None

    @property
    def overruns(self):
        return self.monitor.overruns if self.monitor else 0

    # --- starting --------------------------------------------------------------------------------
    def start_demo(self):
        self._begin()
        self._source, self.label = DemoBus(self.clock), 'Simulated bus'

    def start_log(self, frames, label='Log file'):
        if not frames:
            raise MonitorError('That log has no CAN frames in a format the sniffer reads.')
        self._begin()
        self._source, self.label = LogPlayer(frames, self.clock), label

    def start_adapter(self, transport, protocol=DEFAULT_PROTOCOL, rx_filter=None, lock=None,
                      owns_transport=True, label='Adapter'):
        """Listen through transport (already open if owns_transport is False). Raises MonitorError."""
        self._begin()
        monitor = ElmMonitor(transport, self.clock)
        ready, failure = threading.Event(), []
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._listen, args=(monitor, transport, protocol, rx_filter, lock, owns_transport, ready, failure),
            daemon=True)
        self._thread.start()
        if not ready.wait(READY_TIMEOUT):
            self._stop.set()
            self._thread.join(timeout=2)
            self._thread = None
            raise MonitorError('The adapter did not answer in time.')
        if failure:
            self._thread.join(timeout=2)
            self._thread = None
            raise failure[0]
        self.monitor, self.label = monitor, label

    def _begin(self):
        if self.running:
            self.stop()
        self.error = ''
        self.monitor = None

    def _listen(self, monitor, transport, protocol, rx_filter, lock, owns_transport, ready, failure):
        held = False
        try:
            if lock is not None:
                if not lock.acquire(timeout=5):
                    raise MonitorError('The adapter is busy with another screen. Try again in a moment.')
                held = True
            if owns_transport:
                transport.open()
            monitor.start(protocol, rx_filter)
        except Exception as exc:
            failure.append(exc if isinstance(exc, MonitorError) else MonitorError(str(exc)))
            ready.set()
            self._finish(monitor, transport, lock, held, owns_transport, started=False)
            return
        ready.set()
        try:
            while not self._stop.is_set():
                frames = monitor.poll(0.1)
                if frames:
                    self._inbox.put(frames)
        except Exception as exc:
            self._inbox.put(str(exc))
        finally:
            self._finish(monitor, transport, lock, held, owns_transport, started=True)

    @staticmethod
    def _finish(monitor, transport, lock, held, owns_transport, started):
        try:
            if started:
                monitor.stop()
            elif monitor.traffic:      # a failed start may have left headers on: put the adapter back
                monitor.restore()
        except Exception:
            pass
        if owns_transport:
            try:
                transport.close()
            except Exception:
                pass
        if held:
            lock.release()

    # --- running ---------------------------------------------------------------------------------
    def poll(self):
        """Move waiting frames into the sniffer. Returns how many arrived. Call every 50 ms or so."""
        incoming = []
        if self._source is not None:
            incoming = self._source.poll()
            if getattr(self._source, 'finished', False):
                self.stop()
        while True:
            try:
                item = self._inbox.get_nowait()
            except queue.Empty:
                break
            if isinstance(item, str):
                self.error = f'Stopped: {item}'
                self.stop()
                break
            incoming.extend(item)
        if incoming:
            self.feed(incoming)
        return len(incoming)

    def feed(self, frames):
        self.sniffer.feed(frames)
        room = CAPTURE_LIMIT - len(self.captured)
        if room > 0:
            self.captured.extend(frames[:room])

    def tick(self):
        """Age the list (about every 200 ms). Returns the IDs that dropped off."""
        return self.sniffer.tick()

    def stop(self):
        self._source = None
        if self._thread is not None:
            self._stop.set()
            self._thread.join(timeout=5)
            self._thread = None

    def clear(self):
        self.sniffer.clear()
        self.captured.clear()

    # --- saving ----------------------------------------------------------------------------------
    def log_text(self, csv=False):
        return format_csv(self.captured) if csv else format_candump(self.captured)

    def save(self, path):
        """Write the captured frames to path (CSV if it ends in .csv, otherwise candump). Returns the count."""
        text = self.log_text(csv=str(path).lower().endswith('.csv'))
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(text)
        return len(self.captured)
