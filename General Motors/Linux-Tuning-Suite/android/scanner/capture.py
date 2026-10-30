"""Record the CAN bus through a connected ELM327 transport, receive only. No Kivy.

Shared by the phone's Car tab and tools/capture_can.py, so both listen the same way: the adapter prints
what it hears and sends nothing to the car, and it is left as the OBD link expects afterwards.
"""

import contextlib
import time

from tunertoolpro.canbus.monitor import ElmMonitor, MonitorError

PROTOCOL = '6'         # CAN 500 kbit/s, 11-bit IDs: the GM default
STEP_SECONDS = 0.2     # how long each read waits for the adapter


def record(transport, seconds, protocol=PROTOCOL, rx_filter=None, lock=None, clock=time.monotonic,
           progress=None):
    """Listen for the given time. Returns a dict with frames, overruns, complete and error.

    lock, when given, is held for the whole recording so no other request reaches the adapter meanwhile.
    progress(elapsed, seconds) is called after each read. A link lost part way returns the frames heard
    so far with complete False and the reason in error."""
    monitor = ElmMonitor(transport, clock=clock)
    frames, error = [], ''
    with (lock if lock is not None else contextlib.nullcontext()):
        try:
            monitor.start(protocol, rx_filter)
            began = clock()
            end = began + seconds
            while clock() < end:
                frames += monitor.poll(STEP_SECONDS)
                if progress:
                    progress(min(clock() - began, seconds), seconds)
        except MonitorError as exc:
            error = str(exc)
        finally:
            try:
                monitor.stop()
            except MonitorError as exc:
                error = error or str(exc)
    return {'frames': frames, 'overruns': monitor.overruns, 'complete': not error, 'error': error}
