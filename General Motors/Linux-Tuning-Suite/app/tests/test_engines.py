"""Engine tests. These check invariants and hand-computed values from the disassembly.

They do not compare against the original program. That differential check needs the
original to be run, which has not been approved (see README.md).
"""

import csv
import os
import tempfile
import unittest

from tunertoolpro import core
from tunertoolpro.engines import constants as C
from tunertoolpro.engines.calc_engine import CalcEngine
from tunertoolpro.engines.drag_simulator import DragSimulator
from tunertoolpro.engines.logimporter import LogImporter
from tunertoolpro.engines.pressure_engine import PressureEngine
from tunertoolpro.engines.shift_time_engine import ShiftTimeEngine
from tunertoolpro.engines.tcc_duty_engine import TCCDutyEngine
from tunertoolpro.engines.torque_curve import TorqueCurve
from tunertoolpro.engines.xdf import XDFDefinition

# tests/ -> app/ -> Linux-Tuning-Suite/ -> General Motors/ (reference material)
GM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
XDF_SAMPLE = os.path.join(GM_DIR, 'P01', 'Software', '12208322_Operating_System',
                          'Unvetted XDFs',
                          'No Password - XDF for Operating System 12208322 - 2001 512Kb PCM - Version 5.xdf')


class ShiftTimeTests(unittest.TestCase):
    def test_first_and_last_values(self):
        rows = ShiftTimeEngine.desired_shift_time_4spd('Normal')
        self.assertEqual(len(rows), 3)
        self.assertEqual(len(rows[0]), 17)
        self.assertAlmostEqual(rows[0][0], 0.575)     # no torque: max time
        self.assertAlmostEqual(rows[0][-1], 0.3)      # full torque: min time
        self.assertEqual(set(rows[2]), {0.0})         # 3-4 has zero max and min

    def test_rows_do_not_increase_with_torque(self):
        for intent in C.SHIFT_TIME_INTENTS_4SPD:
            for row in ShiftTimeEngine.desired_shift_time_4spd(intent)[:2]:
                self.assertTrue(all(a >= b - 1e-12 for a, b in zip(row, row[1:])), intent)

    def test_unknown_intent_falls_back_to_normal(self):
        self.assertEqual(ShiftTimeEngine.desired_shift_time_4spd('nope'),
                         ShiftTimeEngine.desired_shift_time_4spd('Normal'))


class TccDutyTests(unittest.TestCase):
    def test_hand_value_at_151f_zero_psi(self):
        table = TCCDutyEngine.max_duty_cycle()
        # temp_norm = 0.5, row_offset = -0.5, pressure_offset = -1.5, base 97 -> 95.0
        self.assertAlmostEqual(table[2][0], 95.0)

    def test_shape_and_clamp(self):
        table = TCCDutyEngine.max_duty_cycle()
        self.assertEqual((len(table), len(table[0])), (5, 17))
        flat = [v for row in table for v in row]
        self.assertTrue(all(90.0 <= v <= 98.0 for v in flat))


class PressureTests(unittest.TestCase):
    def test_torque_columns(self):
        self.assertEqual(PressureEngine.torque_cols(640), [0, 160, 320, 480, 640])

    def test_base_table_shape_and_regression_value(self):
        table = PressureEngine.base_shift_pressure('Daily', 640, '1-2', 296)
        self.assertEqual((len(table), len(table[0])), (5, 5))
        # Regression value from the first implementation run (68 F row, 160 lb-ft column).
        self.assertAlmostEqual(table[2][1], 121.5)
        self.assertTrue(all(0 <= v <= 296 for row in table for v in row))

    def test_four_speed_base_table_shape(self):
        table = PressureEngine.base_shift_pressure_4spd('Normal')
        self.assertEqual((len(table), len(table[0])), (3, 33))

    def test_tcc_ramp_shape_per_era(self):
        expected = {'2007-2010': (17, 17), '2011-2014': (17, 17), '2015+': (9, 17)}
        for era, shape in expected.items():
            table = PressureEngine.tcc_apply_pressure_ramp('Daily', era, 640.0)
            self.assertEqual((len(table), len(table[0])), shape, era)

    def test_shift_time_and_pressure_use_separate_intent_sets(self):
        self.assertIn('Normal', C.SHIFT_TIME_INTENTS_4SPD)
        self.assertIn('Daily', C.PRESSURE_INTENTS)


class CalcEngineTests(unittest.TestCase):
    def setUp(self):
        self.cfg = core.shift_cfg_from_profile('LS1 Camaro / Trans Am (4L60E)')

    def test_table_shapes(self):
        t = CalcEngine.calculate(self.cfg)
        n = len(self.cfg['ratios'])
        self.assertEqual(t['n_gears'], n)
        self.assertEqual(len(t['upshift']), n - 1)
        self.assertEqual(len(t['downshift']), n - 1)
        self.assertEqual(len(t['tcc_unlock']), n)
        self.assertEqual(len(t['tcc_lock']), n)
        self.assertEqual(len(t['upshift'][0]), 17)

    def test_downshift_stays_below_upshift_by_spread(self):
        t = CalcEngine.calculate(self.cfg)
        s_up = self.cfg['spread_up']
        for g, row in enumerate(t['upshift']):
            for col, up in enumerate(row):
                self.assertLessEqual(t['downshift'][g][col], up - s_up + 1e-9)

    def test_tcc_lock_is_not_below_unlock(self):
        t = CalcEngine.calculate(self.cfg)
        for g in range(t['n_gears']):
            for col in range(17):
                if t['tcc_unlock'][g][col] == C.TCC_DISABLED_MPH:
                    continue
                self.assertGreaterEqual(t['tcc_lock'][g][col], t['tcc_unlock'][g][col])

    def test_intent_changes_shift_rpm(self):
        base = core.shift_cfg_from_profile('LS1 Camaro / Trans Am (4L60E)', 'Eco')
        racing = core.shift_cfg_from_profile('LS1 Camaro / Trans Am (4L60E)', 'Racing')
        self.assertNotEqual(base['shift_rpm'], racing['shift_rpm'])
        self.assertGreaterEqual(racing['shift_rpm'], 3000)

    def test_tps_gear_text_has_four_blocks(self):
        text = core.tps_gear_text(CalcEngine.calculate(self.cfg))
        self.assertEqual(text.count('TPS %'), 4)
        self.assertIn('Upshift MPH', text)


class TorqueCurveTests(unittest.TestCase):
    def test_peaks_and_interpolation(self):
        curve = TorqueCurve([(2000, 100, 262), (4000, 300, 394), (6000, 280, 245)])
        self.assertEqual(curve.peak_hp, 300)
        self.assertEqual(curve.peak_hp_rpm, 4000)
        self.assertAlmostEqual(curve.hp_at(3000), 200)

    def test_csv_skips_header_and_drops_bad_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'dyno.csv')
            with open(path, 'w', newline='') as fh:
                w = csv.writer(fh)
                w.writerows([['rpm', 'hp', 'tq'], [2000, 100, 262], ['bad', 1, 2], [0, 5, 5],
                             [4000, 300, 394]])
            curve = TorqueCurve.from_csv(path)
        self.assertEqual(len(curve.points), 2)


class DragTests(unittest.TestCase):
    def test_zero_to_sixty_is_plausible(self):
        curve = TorqueCurve([(1000, 150, 790), (3000, 280, 490), (5000, 320, 336), (6200, 300, 254)])
        cfg = core.shift_cfg_from_profile('LS1 Camaro / Trans Am (4L60E)')
        result = core.run_drag(cfg, curve)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result['t_0_60'])
        self.assertTrue(3.0 < result['t_0_60'] < 9.0, result['t_0_60'])
        self.assertIsNotNone(result['t_quarter'])

    def test_empty_curve_returns_none(self):
        cfg = core.shift_cfg_from_profile('LS1 Camaro / Trans Am (4L60E)')
        self.assertIsNone(DragSimulator(dict(cfg, torque_curve=TorqueCurve())).simulate())


class LogImporterTests(unittest.TestCase):
    ROWS = [
        ['Datalog export'],
        ['Time', 'Engine RPM', 'Vehicle Speed (MPH)', 'TPS (%)', 'Current Gear', 'Trans Temp'],
        ['0.0', '800', '0', '0', '1', '150'],
        ['0.1', '1500', '8', '40', '1', '152'],
        ['0.2', '2600', '12', '95', '1', '154'],
        ['0.3', '3300', '20', '96', '1', '156'],
        ['0.4', '2700', '21', '50', '2', '156'],
        ['0.5', '3000', '30', '98', '2', '158'],
        ['0.6', '3400', '32', '97', '2', '158'],
        ['0.7', '2100', '33', '30', '3', '160'],
        ['0.8', '3100', '0', '98', '3', '161'],
    ]

    def _write(self, tmp):
        path = os.path.join(tmp, 'log.csv')
        with open(path, 'w', newline='') as fh:
            csv.writer(fh).writerows(self.ROWS)
        return path

    def test_detects_columns_and_sample_rate(self):
        with tempfile.TemporaryDirectory() as tmp:
            imp = LogImporter.from_csv(self._write(tmp))
        keys = {k for k, _ in imp.detected_columns()}
        self.assertTrue({'rpm', 'mph', 'tps', 'gear', 'trans_temp'} <= keys)
        self.assertEqual(imp.n_samples, 9)
        self.assertAlmostEqual(imp.sample_rate, 10.0)

    def test_analysis_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            imp = LogImporter.from_csv(self._write(tmp))
        result = imp.analyze({'ratios': [3.0, 2.0, 1.5], 'axle': 3.0, 'chain': 1.0, 'tire_dia': 28.0})
        self.assertEqual(result['stall_peak_rpm'], 3100.0)   # standstill WOT row
        self.assertEqual(result['temp_range'], (150.0, 161.0))
        self.assertIsNotNone(result['wot_slip_pct'])
        self.assertEqual(result['warnings'], [])

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'empty.csv')
            open(path, 'w').close()
            imp = LogImporter.from_csv(path)
        self.assertTrue(imp.is_empty)
        self.assertIn('Log is empty', imp.analyze()['warnings'])


@unittest.skipUnless(os.path.exists(XDF_SAMPLE), 'reference XDF not present')
class XdfTests(unittest.TestCase):
    def test_parses_reference_definition(self):
        xdf = XDFDefinition.from_file(XDF_SAMPLE)
        self.assertGreater(len(xdf.parameters), 300)
        self.assertTrue(xdf.categories())
        self.assertIsNotNone(xdf.find('shift'))


if __name__ == '__main__':
    unittest.main()
