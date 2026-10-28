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
DEMO_CODES = ['P0301', 'P0420']   # sample codes so the Codes screen has something to show

# A six-speed automatic with the stock LS3 6L80 gearing. The car shifts up at the speeds that tune's
# table gives at 37.5 percent throttle, and down at the speeds it gives at closed throttle, so the
# live comparison with the shift tables has something real to show. The 3-4 shift is a little late
# on purpose, so a yellow result appears alongside the green ones.
RATIOS = [4.027, 2.364, 1.532, 1.152, 0.852, 0.667]
FINAL_DRIVE = 3.45
TIRE_INCHES = 27.5
UP_KMH = [24.9, 43.1, 66.1, 87.7, 118.0]
LATE = [1.0, 1.0, 1.0, 1.12, 1.0]
DOWN_KMH = [10.0, 16.9, 26.2, 34.8, 47.0]
KMH_TO_MPH = 0.621371
MPH_K = 336.13


def _wheel_rpm(speed_kmh, gear):
    """Engine speed the road speed asks for in a gear (1-based), before converter slip."""
    return speed_kmh * KMH_TO_MPH * FINAL_DRIVE * RATIOS[gear - 1] * MPH_K / TIRE_INCHES


def drive(t):
    """Engine and driveline signals at time t (seconds): a dict of floats."""
    t = t % CYCLE_SECONDS
    if t < 4:                                   # idle
        speed, throttle, gear = 0.0, 3.0, 1
    elif t < 16:                                # brisk acceleration at 37.5 percent throttle
        speed = 150.0 * (((t - 4) / 12.0) ** 0.9)
        gear = 1 + sum(speed > up * late for up, late in zip(UP_KMH, LATE))
        throttle = 37.5
    elif t < 28:                                # cruise in top gear
        speed = 150.0 - 40.0 * (t - 16) / 12.0
        gear, throttle = 6, 20.0 + 4 * math.sin(t)
    elif t < 36:                                # coast down to a stop, closed throttle
        speed = 110.0 * (1 - (t - 28) / 8.0)
        gear = 1 + sum(speed > down for down in DOWN_KMH)
        throttle = 0.0
    else:
        speed, throttle, gear = 0.0, 3.0, 1
    if speed < 0.5:
        rpm = 720 + 25 * math.sin(t * 3)
    else:
        rpm = max(_wheel_rpm(speed, gear) * 1.01 + 450 * math.exp(-speed / 15.0), 800.0)
    return {
        'speed': speed, 'rpm': rpm, 'throttle': throttle, 'gear': gear,
        'load': 15 + 0.85 * throttle,
        'coolant': 88 + 3 * math.sin(t / 7.0),
    }


def _tcc_slip(s):
    locked = s['gear'] >= 2 and s['speed'] > 35 and s['throttle'] < 80
    return 6 + 4 * math.sin(s['rpm']) if locked else 250 + 0.1 * s['rpm']


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
        '221991': _tcc_slip(s),
        '223D03': float(s['gear']),
        '221942': s['speed'] * KMH_TO_MPH * FINAL_DRIVE * MPH_K / TIRE_INCHES,
        '221941': max(s['rpm'] - _tcc_slip(s), 0.0),
        '22199F': 0.30 + 0.005 * s['throttle'] + 0.0002 * s['rpm'],
        '22199E': (0.30 + 0.005 * s['throttle'] + 0.0002 * s['rpm']) * (1 + 0.02 * math.sin(t * 3)),
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

    def poll(self, pid_ids, headers=None):
        return {p: self.read(p) for p in pid_ids if pids.get(p) is not None}, {}

    def read_dtcs(self):
        self.traffic.append(('TX', '03'))
        self.traffic.append(('RX', '43 (simulated)'))
        return list(DEMO_CODES)

    def close(self):
        pass
