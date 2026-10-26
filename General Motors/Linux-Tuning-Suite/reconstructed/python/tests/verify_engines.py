"""Differential test: reconstructed engines vs. the ORIGINAL module, on random inputs.

Loads the original module with oracle.load_original() (PyQt6 replaced by inert stubs) and
compares it with the reconstructions in app/tunertoolpro/. Covers PressureEngine,
ShiftTimeEngine, TCCDutyEngine, TorqueCurve, BoostCurve and DragSimulator.

Usage (run from an empty folder, with no network):
    python3 -I verify_engines.py "/path/to/orig.pyc"

Exit status is 0 only if every comparison matches within 1e-9 relative tolerance.
"""

import math
import os
import random
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app'))

import oracle  # noqa: E402
from tunertoolpro.engines import constants as C  # noqa: E402
from tunertoolpro.engines.bin_reader import BinReader as OurBin  # noqa: E402
from tunertoolpro.engines.boost_curve import BoostCurve as OurBoost  # noqa: E402
from tunertoolpro.engines.logimporter import LogImporter as OurLog  # noqa: E402
from tunertoolpro.engines.xdf import XDFDefinition as OurXdf  # noqa: E402
from tunertoolpro.engines.drag_simulator import DragSimulator as OurDrag  # noqa: E402
from tunertoolpro.engines.pressure_engine import PressureEngine as OurPressure  # noqa: E402
from tunertoolpro.engines.shift_time_engine import ShiftTimeEngine as OurShift  # noqa: E402
from tunertoolpro.engines.tcc_duty_engine import TCCDutyEngine as OurTcc  # noqa: E402
from tunertoolpro.engines.torque_curve import TorqueCurve as OurCurve  # noqa: E402

TOL = 1e-9
RNG = random.Random(20261026)
RESULTS = {'checks': 0, 'failures': []}


def close(a, b):
    if isinstance(a, float) or isinstance(b, float):
        if a is None or b is None:
            return a is b
        return math.isclose(float(a), float(b), rel_tol=TOL, abs_tol=TOL)
    return a == b


def expect(label, got, want):
    RESULTS['checks'] += 1
    if not compare(got, want):
        RESULTS['failures'].append((label, got, want))


def compare(got, want):
    if isinstance(want, dict):
        if not isinstance(got, dict) or set(got) != set(want):
            return False
        return all(compare(got[k], want[k]) for k in want)
    if isinstance(want, (list, tuple)):
        if not isinstance(got, (list, tuple)) or len(got) != len(want):
            return False
        return all(compare(g, w) for g, w in zip(got, want))
    return close(got, want)


def check_pressure(orig):
    op = orig.PressureEngine
    intents = list(C.PRESSURE_INTENTS)
    for _ in range(300):
        intent = RNG.choice(intents)
        max_tq = RNG.uniform(100, 900)
        psi = RNG.uniform(120, 296)
        shift = RNG.choice(list(C.SHIFT_PRESSURE_MULT))
        expect(f'base {intent} {shift}', OurPressure.base_shift_pressure(intent, max_tq, shift, psi),
               op.base_shift_pressure(intent, max_tq, shift, psi))
        expect(f'tcc {intent}', OurPressure.tcc_apply_pressure(intent, max_tq, psi),
               op.tcc_apply_pressure(intent, max_tq, psi))
        expect(f'coast {intent}', OurPressure.coast_pressure(intent, max_tq, psi),
               op.coast_pressure(intent, max_tq, psi))
    for intent in intents:
        expect(f'garage {intent}', OurPressure.garage_shift_pressure(intent),
               op.garage_shift_pressure(intent))
    for intent in C.BRAKE_SHIFT_INTENTS_4SPD:
        expect(f'brake4 {intent}', OurPressure.brake_shift_pressure_4spd(intent),
               op.brake_shift_pressure_4spd(intent))
    for intent in list(C.PRESSURE_INTENTS_4SPD) + ["no-such-intent"]:
        expect(f'base4 {intent}', OurPressure.base_shift_pressure_4spd(intent),
               op.base_shift_pressure_4spd(intent))
    expect('force motor', OurPressure.force_motor_current(), op.force_motor_current())
    expect('torque cols', OurPressure.torque_cols(640.0), op.torque_cols(640.0))


def check_ramp(orig):
    op = orig.PressureEngine
    for era in C.TCC_RAMP_ERAS:
        for intent in C.TCC_APPLY_INTENTS:
            for mt in (200.0, 400.0, 640.0):
                try:
                    want = op.tcc_apply_pressure_ramp(intent, era, mt)
                except Exception as exc:  # the original may reject some combinations
                    want = ('raised', type(exc).__name__)
                try:
                    got = OurPressure.tcc_apply_pressure_ramp(intent, era, mt)
                except Exception as exc:
                    got = ('raised', type(exc).__name__)
                expect(f'ramp {era} {intent} {mt}', got, want)


def check_shift_and_tcc(orig):
    for intent in C.SHIFT_TIME_INTENTS_4SPD:
        expect(f'shift time {intent}', OurShift.desired_shift_time_4spd(intent),
               orig.ShiftTimeEngine.desired_shift_time_4spd(intent))
    expect('shift time unknown', OurShift.desired_shift_time_4spd('zzz'),
           orig.ShiftTimeEngine.desired_shift_time_4spd('zzz'))
    expect('tcc duty', OurTcc.max_duty_cycle(), orig.TCCDutyEngine.max_duty_cycle())


def check_torque_curve(orig):
    oc = orig.TorqueCurve
    for _ in range(200):
        n = RNG.randint(2, 12)
        rpms = sorted(RNG.sample(range(800, 9000, 50), n))
        pts = []
        for r in rpms:
            hp = RNG.uniform(50, 500)
            tq = RNG.choice([0, hp * 5252 / r, RNG.uniform(50, 600)])
            pts.append((float(r), hp, tq))
        ours = OurCurve(list(pts))
        theirs = oc(list(pts))
        expect('peak_hp', ours.peak_hp, theirs.peak_hp)
        expect('peak_tq', ours.peak_tq, theirs.peak_tq)
        expect('peak_hp_rpm', ours.peak_hp_rpm, theirs.peak_hp_rpm)
        expect('peak_tq_rpm', ours.peak_tq_rpm, theirs.peak_tq_rpm)
        expect('rpm_range', ours.rpm_range, theirs.rpm_range)
        for _ in range(10):
            x = RNG.uniform(rpms[0] - 200, rpms[-1] + 200)
            expect('hp_at', ours.hp_at(x), theirs.hp_at(x))
            expect('tq_at', ours.tq_at(x), theirs.tq_at(x))
        lo = RNG.uniform(rpms[0], rpms[-1])
        hi = RNG.uniform(lo, rpms[-1] + 500)
        expect('avg_hp', ours.avg_hp(lo, hi), theirs.avg_hp(lo, hi))
    empty_ours = OurCurve([(1000.0, 100.0, 0.0)])
    expect('empty is_empty', empty_ours.is_empty, oc([(1000.0, 100.0, 0.0)]).is_empty)
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'dyno.csv')
        with open(path, 'w') as fh:
            fh.write('rpm,hp,tq\n2000,100,262\n3000,200,350\nbad,1,2\n0,5,5\n4000,300,394\n')
        expect('from_csv points', OurCurve.from_csv(path).points, oc.from_csv(path).points)


def check_boost(orig):
    ob = orig.BoostCurve
    for _ in range(200):
        args = dict(spool_rpm=RNG.uniform(1500, 3500), peak_psi=RNG.uniform(0, 25),
                    peak_rpm=RNG.uniform(3000, 6000), redline_psi=RNG.uniform(0, 25),
                    torque_per_psi_pct=RNG.uniform(0, 15))
        ours = OurBoost(**args)
        theirs = ob(**args)
        expect('boost empty', ours.is_empty, theirs.is_empty)
        for _ in range(10):
            rpm = RNG.uniform(0, 9000)
            expect('psi_at', ours.psi_at(rpm), theirs.psi_at(rpm))
            expect('torque_mult', ours.torque_mult(rpm), theirs.torque_mult(rpm))


def drag_cfg(rng):
    ratios = [round(rng.uniform(0.6, 3.5), 3) for _ in range(rng.choice([4, 6]))]
    ratios.sort(reverse=True)
    return {
        'ratios': ratios,
        'axle': round(rng.uniform(2.7, 4.1), 2),
        'chain': 1.0,
        'tire_dia': round(rng.uniform(24, 30), 1),
        'weight': rng.randint(2800, 4800),
        'stall_rpm': rng.randint(1800, 3000),
        'idle_rpm': rng.randint(550, 800),
        'shift_rpm': rng.randint(4500, 6500),
        'per_gear_rpm': None,
    }


def check_drag(orig):
    od = orig.DragSimulator
    for _ in range(40):
        cfg = drag_cfg(RNG)
        pts = []
        for r in range(1000, 7000, 500):
            hp = RNG.uniform(120, 450)
            pts.append((float(r), hp, hp * 5252 / r))
        ours_cfg = dict(cfg, torque_curve=OurCurve(list(pts)))
        orig_cfg = dict(cfg, torque_curve=orig.TorqueCurve(list(pts)))
        ours = OurDrag(ours_cfg).simulate()
        theirs = od(orig_cfg).simulate()
        if theirs is None or ours is None:
            expect('drag none', ours is None, theirs is None)
            continue
        for key in ('t_0_30', 't_0_60', 't_0_100', 't_0_120', 't_eighth', 'v_eighth',
                    't_quarter', 'v_quarter', 'max_v'):
            expect(f'drag {key}', ours[key], theirs[key])
        expect('drag shifts', ours['shift_events'], theirs['shift_events'])
        expect('drag trace_v', ours['trace_v'], theirs['trace_v'])


XDF_SAMPLE = os.path.join(HERE, '..', '..', '..', '..', 'P01', 'Software',
                          '12208322_Operating_System', 'Unvetted XDFs',
                          'No Password - XDF for Operating System 12208322 - 2001 512Kb PCM - Version 5.xdf')


def check_readers(orig, xdf_path=XDF_SAMPLE):
    ox = orig.XDFDefinition
    ours_x = OurXdf.from_file(xdf_path)
    theirs_x = ox.from_file(xdf_path)
    expect('xdf title', ours_x.title, theirs_x.title)
    expect('xdf param count', len(ours_x.parameters), len(theirs_x.parameters))
    expect('xdf categories', ours_x.categories(), theirs_x.categories())
    bin_data = bytes(RNG.getrandbits(8) for _ in range(0x20000))
    ours_bin = OurBin(bin_data, ours_x)
    theirs_bin = orig.BinReader(bin_data, theirs_x)
    for p_ours, p_theirs in zip(ours_x.parameters, theirs_x.parameters):
        expect(f'xdf title {p_ours.title}', p_ours.title, p_theirs.title)
        expect(f'xdf kind {p_ours.title}', p_ours.kind, p_theirs.kind)
        expect(f'xdf units {p_ours.title}', p_ours.units, p_theirs.units)
        try:
            want = p_theirs.read(bin_data)
        except Exception as exc:
            want = ('raised', type(exc).__name__)
        try:
            got = p_ours.read(bin_data)
        except Exception as exc:
            got = ('raised', type(exc).__name__)
        expect(f'xdf read {p_ours.title}', got, want)
    for title in ('Shift', 'TCC', 'Pressure', 'Torque'):
        expect(f'bin find {title}', ours_bin.read(title), theirs_bin.read(title))
    expect('bin size', len(ours_bin.data), theirs_bin.size)


def check_log(orig):
    rows = ['Time,Engine RPM,Vehicle Speed (MPH),TPS (%),Current Gear,Trans Temp']
    for i in range(400):
        rpm = 800 + i * 12 + RNG.randint(0, 40)
        mph = max(0, i * 0.2)
        tps = RNG.choice([0, 30, 75, 95])
        gear = 1 + i // 60
        rows.append(f'{i * 0.1:.1f},{rpm},{mph:.2f},{tps},{min(gear, 4)},{150 + i % 10}')
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'log.csv')
        with open(path, 'w') as fh:
            fh.write('\n'.join(rows) + '\n')
        ours = OurLog.from_csv(path)
        theirs = orig.LogImporter.from_csv(path)
    expect('log samples', ours.n_samples, theirs.n_samples)
    expect('log rate', ours.sample_rate, theirs.sample_rate)
    expect('log cols', ours.col_map, theirs.col_map)
    cfg = {'ratios': [3.06, 1.63, 1.0, 0.7], 'axle': 3.42, 'chain': 1.0, 'tire_dia': 26.0}
    expect('log analyze', ours.analyze(cfg), theirs.analyze(cfg))


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    orig = oracle.load_original(argv[1])
    check_pressure(orig)
    check_ramp(orig)
    check_shift_and_tcc(orig)
    check_torque_curve(orig)
    check_boost(orig)
    check_drag(orig)
    if os.path.exists(XDF_SAMPLE):
        check_readers(orig)
    else:
        print('reader check skipped: XDF sample not found')
    check_log(orig)
    print(f"checks={RESULTS['checks']} failures={len(RESULTS['failures'])}")
    for label, got, want in RESULTS['failures'][:20]:
        print('MISMATCH', label, '\n  ours:', repr(got)[:300], '\n  orig:', repr(want)[:300])
    return 0 if not RESULTS['failures'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
