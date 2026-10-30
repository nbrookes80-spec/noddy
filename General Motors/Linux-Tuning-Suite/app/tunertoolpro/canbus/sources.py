"""Frame sources that need no adapter: a simulated bus for trying the sniffer, and log-file replay.

Each source has poll() -> list of Frame, called often. The simulated bus uses made-up IDs and is not
any real car's traffic; it exists so the screen can be learned (and tested) with nothing plugged in.
"""

import math
import time

from .frames import Frame


class DemoBus:
    """Five invented messages that behave the way real ones do, to practise notching on.

    0x0C9  100 Hz  engine speed (bytes 0-1), throttle (byte 2), a constant, a rolling counter
    0x0F1   50 Hz  road speed (bytes 0-1), slowly climbing
    0x1E5   20 Hz  steering angle (bytes 0-1), signed, swings left and right
    0x3C1   10 Hz  gear (byte 0) stepping 1 to 6 every three seconds
    0x4C9    1 Hz  a fixed status message that never changes
    """

    label = 'Simulated bus'
    PLAN = ((0x0C9, 0.010), (0x0F1, 0.020), (0x1E5, 0.050), (0x3C1, 0.100), (0x4C9, 1.000))

    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self._start = clock()
        self._next = {can_id: 0.0 for can_id, _ in self.PLAN}
        self._counter = 0

    def poll(self):
        elapsed = self.clock() - self._start
        frames = []
        for can_id, period in self.PLAN:
            while self._next[can_id] <= elapsed:
                frames.append(Frame(can_id, self._payload(can_id, self._next[can_id]), False, self._next[can_id]))
                self._next[can_id] += period
        frames.sort(key=lambda f: f.timestamp)
        return frames

    def _payload(self, can_id, t):
        if can_id == 0x0C9:
            rpm = int((1500 + 1300 * (1 + math.sin(t / 2.0))) * 4)
            throttle = int(40 + 35 * math.sin(t / 2.0 - 0.4))
            self._counter = (self._counter + 1) & 0x0F
            return bytes([rpm >> 8, rpm & 0xFF, throttle, 0x80, self._counter, 0, 0, 0])
        if can_id == 0x0F1:
            speed = int(min(250 * 100, 800 + t * 150))
            return bytes([speed >> 8, speed & 0xFF, 0, 0, 0, 0, 0, 0])
        if can_id == 0x1E5:
            angle = int(4500 * math.sin(t / 3.0)) & 0xFFFF
            return bytes([angle >> 8, angle & 0xFF, 0, 0])
        if can_id == 0x3C1:
            return bytes([1 + int(t / 3.0) % 6, 0])
        return bytes([0xA5, 0x5A, 0x00, 0x01])


class LogPlayer:
    """Plays a list of Frames back at the speed they were recorded. loop=True starts over at the end."""

    label = 'Log file'

    def __init__(self, frames, clock=time.monotonic, loop=True, speed=1.0):
        self.frames = sorted(frames, key=lambda f: f.timestamp)
        self.clock, self.loop, self.speed = clock, loop, speed
        self._origin = self.frames[0].timestamp if self.frames else 0.0
        self._length = (self.frames[-1].timestamp - self._origin) if self.frames else 0.0
        self._start = clock()
        self._index = 0
        self._lap = 0.0
        self.finished = False

    def poll(self):
        if not self.frames or self.finished:
            return []
        elapsed = (self.clock() - self._start) * self.speed - self._lap
        out = []
        while self._index < len(self.frames) and self.frames[self._index].timestamp - self._origin <= elapsed:
            out.append(self.frames[self._index])
            self._index += 1
        if self._index >= len(self.frames):
            if self.loop:
                self._index = 0
                self._lap += self._length + 0.001
            else:
                self.finished = True
        return out
