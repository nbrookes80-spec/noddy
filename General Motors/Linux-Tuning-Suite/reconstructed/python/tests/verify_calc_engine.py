"""Differential test: reconstructed CalcEngine vs. the ORIGINAL bytecode.

Loads only the `CalcEngine` class body from the original PyInstaller module's
.pyc (no PyQt6, no GUI, no file or network access) and compares every public
method against the hand-written version in ../engines/calc_engine.py on random
inputs.

Usage:
    python3 -I verify_calc_engine.py "/path/to/Ewalts ... v2.0.pyc"

Exit status is 0 only if every comparison matches within 1e-9 relative tolerance.
"""

import marshal
import math
import os
import random
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tunertoolpro', 'engines'))
import calc_engine as ours  # noqa: E402


def load_original_engine(pyc_path):
    raw = open(pyc_path, 'rb').read()
    module_code = marshal.loads(raw[16:])
    class_code = next(c for c in module_code.co_consts
                      if isinstance(c, types.CodeType) and c.co_name == 'CalcEngine')
    glb = {
        '__name__': 'orig',
        '__builtins__': __builtins__,
        'math': math,
        'MPH_K': 336.13,
        'TPS_COLS': 17,
        'TPS_STEP': 6.25,
        'SLOPE_BLEND': (0.0, 0.1, 0.1, 0.1, 0.1, 0.125, 0.15, 0.225, 0.35, 0.5,
                        0.675, 0.825, 0.925, 0.95, 1.0, 1.0, 1.0),
        'MAX_SPREAD_ITERATIONS': 32,
        'TCC_DISABLED_MPH': 255.0,
    }
    ns = {}
    exec(class_code, glb, ns)          # builds the class namespace only
    glb['CalcEngine'] = type('CalcEngine', (), ns)
    return glb['CalcEngine']


def close(a, b, tol=1e-9):
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(close(a[k], b[k], tol) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, float) or isinstance(b, float):
        return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
    return a == b


class FakeCurve:
    def __init__(self, rng):
        self.rng = rng

    @property
    def is_empty(self):  # a property in the original TorqueCurve (LOAD_ATTR without CALL)
        return False

    def avg_hp(self, lo, hi):
        return 300.0 + 0.05 * (lo + hi) / 2.0


def random_cfg(rng):
    n = rng.randint(3, 9)
    ratios = sorted((rng.uniform(0.5, 4.5) for _ in range(n)), reverse=True)
    cfg = {
        'ratios': ratios,
        'tire_dia': rng.uniform(24.0, 34.0),
        'axle': rng.uniform(2.5, 4.1),
        'chain': rng.uniform(0.8, 1.2),
        'idle_rpm': rng.uniform(550, 900),
        'stall_rpm': rng.uniform(1500, 3200),
        'shift_rpm': rng.uniform(4500, 6200),
        'downshift_rpm': rng.uniform(4000, 5800),
        'weight': rng.uniform(3000, 5500),
        'rwhp': rng.uniform(250, 600),
        'tps_offset': rng.uniform(0, 10),
        'tps_factor': rng.uniform(0.6, 1.6),
        'up_firmness': rng.uniform(0, 10),
        'down_firmness': rng.uniform(0, 10),
        'spread_up': rng.uniform(0.5, 6),
        'spread_lock': rng.uniform(0.5, 5),
        'spread_lock_up': rng.uniform(0.5, 6),
        'spread_unlock_dn': rng.uniform(0.5, 6),
        'lead_mode': rng.choice(['rpm', 'other']),
        'lead_value': rng.uniform(0, 20),
        'down_time': rng.uniform(0.05, 0.6),
        'delays': [(rng.uniform(0.05, 0.5), rng.uniform(0.05, 0.5)) for _ in range(n)],
        'min_tcc_rpm': rng.uniform(1000, 1700),
        'min_tcc_gear': rng.randint(1, n),
        'accel_lock_gear': rng.randint(1, n),
        'wot_lock_gear': rng.randint(1, n),
        'stall_lock_logic': rng.random() < 0.5,
        'init_lock_logic': rng.random() < 0.5,
    }
    if rng.random() < 0.4:
        cfg['per_gear_rpm'] = [rng.uniform(1000, 6500) for _ in range(rng.randint(n - 2, n + 1))]
    if rng.random() < 0.3:
        cfg['torque_curve'] = FakeCurve(rng)
    return cfg


def main(pyc_path, trials=400, seed=1):
    Orig = load_original_engine(pyc_path)
    rng = random.Random(seed)
    failures = []
    checks = 0

    # Primitive helpers on random scalars
    for _ in range(2000):
        rpm, tire, ratio, fd = (rng.uniform(0, 7000), rng.uniform(20, 36),
                                rng.uniform(-0.5, 5), rng.uniform(0, 5))
        for name, args in [('mph', (rpm, tire, ratio, fd))]:
            checks += 1
            if not close(getattr(Orig, name)(*args), getattr(ours.CalcEngine, name)(*args)):
                failures.append((name, args))
        stall = rng.uniform(0, 4000)
        checks += 1
        if not close(Orig.stall_slip(stall), ours.CalcEngine.stall_slip(stall)):
            failures.append(('stall_slip', stall))
        tps, off, fac, up, dn = (rng.uniform(-5, 110), rng.uniform(0, 10),
                                 rng.uniform(0.5, 2), rng.uniform(0, 10), rng.uniform(0, 10))
        col = rng.randint(0, 16)
        for name, args in [('base_slope', (tps, off, fac)),
                           ('upshift_slope', (col, tps, off, fac, up)),
                           ('downshift_slope', (tps, off, fac, dn))]:
            checks += 1
            if not close(getattr(Orig, name)(*args), getattr(ours.CalcEngine, name)(*args)):
                failures.append((name, args))
        for mode in range(6):
            checks += 1
            args = (mode, rng.uniform(20, 36), rng.uniform(2, 5), rng.uniform(1, 8), rng.random() < 0.5)
            if not close(Orig.vss_calibration(*args), ours.CalcEngine.vss_calibration(*args)):
                failures.append(('vss_calibration', args))

    # Full calculate() on random configurations
    for t in range(trials):
        cfg = random_cfg(rng)
        checks += 1
        try:
            want = Orig.calculate(dict(cfg))
        except Exception as e:  # original raised: our version must raise too
            want = e
        try:
            got = ours.CalcEngine.calculate(dict(cfg))
        except Exception as e:
            got = e
        if isinstance(want, Exception) or isinstance(got, Exception):
            if type(want) is not type(got):
                failures.append(('calculate-exc', t, repr(want), repr(got)))
            continue
        if not close(want, got):
            failures.append(('calculate', t))

    print(f'checks={checks} failures={len(failures)}')
    for f in failures[:20]:
        print('FAIL', f)
    return 0 if not failures else 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
