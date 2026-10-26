"""Port of BC_Trans Calc_Shifts (bct/calc_shifts.py) on the shipped .BTC tunes.

These tests check the port against hand-worked values and the invariants the original
relies on. They do not compare with BC Trans output, because BC Trans cannot be run here.
See recovered/bct-csharp/CALC_SHIFTS_NOTES.md.
"""

import glob
import math
import os
import unittest

from tunertoolpro.bct import calc_shifts as cs
from tunertoolpro.bct.tune import BtcTune

BCT_DIR = os.environ.get(
    'BCT_DIR', '/home/nathan/Downloads/BCT+1.42/Bluecat Transmission Tool')
TUNES = sorted(glob.glob(os.path.join(BCT_DIR, '*.BTC')))
SIX_SPEED = os.path.join(BCT_DIR, '(Base)2012_C6_6L80_Boltons.BTC')
FOUR_SPEED = os.path.join(BCT_DIR, '(Base)2008_GMT900_4L70_Boltons.BTC')


@unittest.skipUnless(TUNES, 'BC Trans folder not present (set BCT_DIR)')
class CalcShiftsTests(unittest.TestCase):
    def test_first_gear_speed_matches_hand_calculation(self):
        r = cs.calc_shifts(BtcTune.load(SIX_SPEED))
        # 6400 RPM, ratio 4.03, final drive 2.73, tire 26.15, pi as 3.14.
        expected = 6400 / (4.03 * 2.73) * (26.15 * 3.14) * 60 / 12 / 5280
        self.assertAlmostEqual(r.speed[0][0], expected, places=3)

    def test_stall_column_is_slipped_speed(self):
        r = cs.calc_shifts(BtcTune.load(SIX_SPEED))
        slip = (2000 / 1000.0) ** 1.7 / 100.0
        self.assertAlmostEqual(r.speed[0][1], r.speed[0][0] * (1 - slip), places=3)

    def test_every_tune_converges_with_no_logic_error(self):
        for path in TUNES:
            with self.subTest(tune=os.path.basename(path)):
                r = cs.calc_shifts(BtcTune.load(path))
                self.assertEqual(r.logic_error, 0)
                self.assertLess(r.iterations, 32)
                self.assertTrue(all(count == 0 for _, count in r.last_pass_log))

    def test_grid_shapes_and_values(self):
        for path in TUNES:
            with self.subTest(tune=os.path.basename(path)):
                tune = BtcTune.load(path)
                n = tune.gear_count()
                r = cs.calc_shifts(tune)
                self.assertEqual(len(r.upshift), n - 1)
                self.assertEqual(len(r.downshift), n - 1)
                self.assertEqual(len(r.tcc_lock), n)
                self.assertEqual(len(r.tcc_unlock), n)
                self.assertEqual(len(r.speed), n)
                self.assertEqual(len(r.slope), 3)
                for grid in (r.upshift, r.downshift, r.tcc_lock, r.tcc_unlock, r.slope):
                    for row in grid:
                        self.assertEqual(len(row), 17)
                        self.assertTrue(all(math.isfinite(x) and x >= 0 for x in row))

    def test_slope_ends_are_fixed(self):
        r = cs.calc_shifts(BtcTune.load(SIX_SPEED))
        for row in r.slope:
            self.assertEqual(row[0], 0.0)
        self.assertEqual(r.slope[0][16], 1.0)
        self.assertEqual(r.slope[1][16], 1.0)
        self.assertEqual(r.slope[2][16], 1.0)

    def test_disabled_markers_depend_on_gear_count(self):
        six = cs.calc_shifts(BtcTune.load(SIX_SPEED))       # 6 gears, MinLockGear 3
        self.assertEqual(six.tcc_lock[0][0], 318.0)
        self.assertEqual(six.tcc_unlock[0][0], 317.0)
        four = cs.calc_shifts(BtcTune.load(FOUR_SPEED))     # 4 gears, MinLockGear 3
        self.assertEqual(four.tcc_lock[0][0], 255.0)
        self.assertEqual(four.tcc_unlock[0][0], 254.0)

    def test_wot_lock_uses_auto_wot_rpm(self):
        # AUTOWOT sets WOTLockRPM from gear 1's RPM: floor(6400 * 0.8 / 50) * 50 = 5100.
        r = cs.calc_shifts(BtcTune.load(SIX_SPEED))
        tcc_delay = 0.5
        accel_rpm = 6400.0
        accel = 380 * 0.75 * 375.0 / r.speed[2][0] / 3300 * 21.93685
        # Gear 3 is the WOT lock gear. Row 3, column 17.
        expected = r.speed[2][0] * (5100.0 / accel_rpm) - accel * tcc_delay
        self.assertAlmostEqual(r.tcc_lock[2][16], expected, delta=0.05)

    def test_negative_values_are_clamped(self):
        for path in TUNES:
            with self.subTest(tune=os.path.basename(path)):
                r = cs.calc_shifts(BtcTune.load(path))
                for grid in (r.upshift, r.downshift, r.tcc_lock, r.tcc_unlock):
                    for row in grid:
                        self.assertTrue(all(x >= 0 for x in row))

    def test_input_tune_is_not_changed(self):
        tune = BtcTune.load(SIX_SPEED)
        before = tune.to_text()
        cs.calc_shifts(tune)
        self.assertEqual(tune.to_text(), before)

    def test_override_grid_replaces_the_slope(self):
        base = cs.calc_shifts(BtcTune.load(SIX_SPEED))
        tune = BtcTune.load(SIX_SPEED)
        tune.set('SlopeOverride', '1')
        for row in range(1, 2 * (tune.gear_count() - 1) + 1):
            for col in range(1, 18):
                tune.set(f'SlopeOverride{col}-{row}', '0.5')
        over = cs.calc_shifts(tune)
        self.assertNotEqual(base.upshift[0][8], over.upshift[0][8])
        # With every override slope at 0.5, upshift = MinSpeed + S + ((Speed1 - MinSpeed) - S) * 0.5.
        s = tune.getfloat('ShiftSpread')
        expected = over.min_speed[0] + s + ((over.speed[0][0] - over.min_speed[0]) - s) * 0.5
        self.assertAlmostEqual(over.upshift[0][8], expected, delta=0.02)

    def test_bc_shift_tables_has_calc_engine_keys(self):
        from tunertoolpro import core
        tables = core.bc_shift_tables(BtcTune.load(SIX_SPEED))
        for key in ('upshift', 'downshift', 'tcc_unlock', 'tcc_lock', 'n_gears'):
            self.assertIn(key, tables)
        self.assertEqual(tables['n_gears'], 6)
        self.assertEqual(len(tables['upshift']), 5)
        self.assertEqual(len(tables['tcc_lock']), 6)
        self.assertIn('TCC lock MPH', core.tps_gear_text(tables))

    def test_missing_key_is_named(self):
        tune = BtcTune.load(SIX_SPEED)
        pairs = [(k, v) for k, v in tune.pairs() if k != 'Prep1']
        with self.assertRaises(ValueError) as ctx:
            cs.calc_shifts(BtcTune(pairs))
        self.assertIn('Prep1', str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
