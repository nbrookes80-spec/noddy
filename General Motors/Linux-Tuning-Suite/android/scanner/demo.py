"""Demo mode: a simulated drive for trying the app with no adapter and no car.

Nothing here talks to hardware. DemoSource has the same read methods as the real adapter link, so
the screens treat it the same way. Values follow a repeating 40 second drive (idle, a launch through
four gears, a cruise, a stop) so the readings move together the way a real car's would.
"""

import math
import time
import zlib

from . import pids

CYCLE_SECONDS = 40.0
# (end_speed_kmh, shift_up_at_rpm) for each gear of the launch phase.
GEARS = [(55, 6000), (95, 6000), (135, 6000), (175, 6000)]
DEMO_CODES = ['P0301', 'P0420']   # sample codes so the Codes screen has something to show


def drive(t):
    """Engine and driveline signals at time t (seconds): a dict of floats."""
    t = t % CYCLE_SECONDS
    if t < 4:                                   # idle
        speed, rpm, throttle, gear = 0.0, 720 + 25 * math.sin(t * 3), 3.0, 1
    elif t < 16:                                # launch, wide open through the gears
        p = (t - 4) / 12.0
        speed = 175.0 * (p ** 0.9)
        gear = 1 + sum(speed > end for end, _ in GEARS[:-1])
        low = GEARS[gear - 2][0] if gear > 1 else 0.0
        high = GEARS[gear - 1][0]
        span = (speed - low) / max(high - low, 1e-9)
        rpm = 2800 + (GEARS[gear - 1][1] - 2800) * span
        throttle = 100.0
    elif t < 28:                                # cruise in top gear
        speed = 175.0 - 55.0 * min((t - 16) / 3.0, 1.0)
        gear, rpm, throttle = 4, 1500 + speed * 4.0, 22.0 + 4 * math.sin(t)
    elif t < 36:                                # coast down to a stop
        speed = 120.0 * (1 - (t - 28) / 8.0)
        gear = 4 if speed > 60 else (3 if speed > 35 else (2 if speed > 15 else 1))
        rpm, throttle = max(720.0, 700 + speed * 14), 0.0
    else:
        speed, rpm, throttle, gear = 0.0, 720 + 20 * math.sin(t * 2), 3.0, 1
    return {
        'speed': speed, 'rpm': rpm, 'throttle': throttle, 'gear': gear,
        'load': 15 + 0.85 * throttle,
        'coolant': 88 + 3 * math.sin(t / 7.0),
    }


def _smooth(pid, t, low, high):
    """A slow wander inside [low, high], stable for a given pid, for PIDs with no drive model."""
    seed = zlib.crc32(pid.encode('ascii')) % 1000 / 1000.0
    wave = 0.5 + 0.28 * math.sin(t / (4 + 5 * seed) + 6.28 * seed) + 0.12 * math.sin(t / 1.7 + seed)
    return low + (high - low) * min(max(wave, 0.0), 1.0)


def value(pid, t):
    """A simulated reading for catalogue Pid `pid` at time t. Always inside the PID's own range."""
    s = drive(t)
    known = {
        '010C': s['rpm'], '010D': s['speed'], '0111': s['throttle'], '0105': s['coolant'],
        '0143': s['load'], '0104': s['load'], '010B': 100 + 1.2 * s['throttle'] + (s['rpm'] / 8000) * 20,
        '010F': 32 + 0.06 * s['load'], '0133': 101.0, '0146': 24.0,
        '010E': 38 - 0.2 * s['load'] - 4 * (s['rpm'] / 8000), '0152': 85.0,
        '010A': 420 + 0.8 * s['throttle'], '0106': 1.5 * math.sin(t / 3), '0107': -1.0 + 0.3 * math.sin(t / 9),
        '0114': 0.45 + 0.4 * math.sin(t * 2.5), '22199A': float(s['gear']),
        '22194F': 82 + 6 * (1 - math.exp(-(t % CYCLE_SECONDS) / 20.0)),
        '22001F': 380 + 6 * s['throttle'] + s['rpm'] / 40,
        '221991': 0.0 if s['throttle'] < 30 else 40 + 20 * math.sin(t * 4),
    }
    raw = known[pid.pid] if pid.pid in known else _smooth(pid.pid, t, pid.low, pid.high)
    return min(max(raw, pid.low), pid.high)


class DemoSource:
    """Same read methods as the adapter link: read(), poll(), read_dtcs(). Sends nothing anywhere."""

    label = 'Demo'

    def __init__(self, clock=time.monotonic):
        self._clock = clock
        self._start = clock()
        self.traffic = []

    def now(self):
        return self._clock() - self._start

    def read(self, pid_id):
        pid = pids.get(pid_id)
        if pid is None:
            raise KeyError(pid_id)
        self.traffic.append(('TX', pid.command))
        reading = value(pid, self.now())
        self.traffic.append(('RX', f'{pid.echo} (simulated)'))
        return reading, pid.unit

    def poll(self, pid_ids):
        return {p: self.read(p) for p in pid_ids if pids.get(p) is not None}, {}

    def read_dtcs(self):
        self.traffic.append(('TX', '03'))
        self.traffic.append(('RX', '43 (simulated)'))
        return list(DEMO_CODES)

    def close(self):
        pass
