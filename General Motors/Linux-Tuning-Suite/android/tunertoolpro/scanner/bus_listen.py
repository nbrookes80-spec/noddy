"""Short listening windows on the CAN bus, for the bus readings on the Live screen.

On a real adapter this uses monitor mode (ATMA): the adapter prints what it hears and sends nothing. The
window holds the adapter's lock, so the OBD reads wait, and the adapter is handed back the way the OBD link
expects it. A window that fails part-way still hands the adapter back before the error goes up.
"""

import time

from tunertoolpro.link.obd import Elm327
from tunertoolpro.canbus import ElmMonitor


def listen_adapter(elm, seconds, clock=time.monotonic):
    """Frames the bus sends in the next `seconds` seconds, heard through the adapter. Sends nothing to the car."""
    monitor = ElmMonitor(elm.transport, clock)
    frames = []
    with elm._lock:
        started = False
        try:
            monitor.start()
            started = True
            end = clock() + seconds
            while clock() < end:
                frames.extend(monitor.poll(0.1))
        finally:
            if started:
                monitor.stop()
            elif monitor.traffic:      # a failed start may have left headers on
                monitor.restore()
    return frames


def bus_reader(source):
    """The function that listens for a source's bus, taking the window length in seconds. None if it has no bus."""
    if isinstance(source, Elm327):
        return lambda seconds: listen_adapter(source, seconds)
    if hasattr(source, 'listen'):
        return source.listen
    return None
