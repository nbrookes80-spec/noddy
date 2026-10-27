import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import dyno_live as dyno  # noqa: E402
import shift_live  # noqa: E402


class SimulatedCurveTests(unittest.TestCase):
    def test_peak_power_matches_the_rwhp_entered(self):
        curve = dyno.simulated_curve(rwhp=400, shift_rpm=6000, idle_rpm=700)
        self.assertAlmostEqual(curve.peak_hp, 400, delta=1.0)
        self.assertAlmostEqual(curve.peak_hp_rpm, 0.89 * 6000, delta=150)

    def test_torque_follows_from_horsepower(self):
        curve = dyno.simulated_curve(rwhp=300, shift_rpm=5000, idle_rpm=700)
        rpm, hp, tq = curve.points[len(curve.points) // 2]
        self.assertAlmostEqual(tq, hp * 5252 / rpm, delta=0.5)


class RunTests(unittest.TestCase):
    def setUp(self):
        self.values, self.ratios = shift_live.default_inputs()
        self.curve = dyno.simulated_curve(float(self.values['rwhp']), float(self.values['shift_rpm']),
                                          float(self.values['idle_rpm']))

    def test_default_run_finishes_the_quarter_mile(self):
        result, error = dyno.run(self.values, self.ratios, self.curve)
        self.assertEqual(error, '')
        self.assertIsNotNone(result['t_quarter'])
        self.assertGreater(result['t_quarter'], 5)
        self.assertLess(result['t_quarter'], 30)

    def test_a_heavier_car_runs_a_slower_quarter_mile(self):
        light, _ = dyno.run(self.values, self.ratios, self.curve)
        heavy, _ = dyno.run(dict(self.values, weight='5200'), self.ratios, self.curve)
        self.assertGreater(heavy['t_quarter'], light['t_quarter'])

    def test_changing_a_ratio_changes_the_run(self):
        base, _ = dyno.run(self.values, self.ratios, self.curve)
        ratios = self.ratios.split(', ')
        ratios[0] = str(float(ratios[0]) - 0.4)
        changed, error = dyno.run(self.values, ', '.join(ratios), self.curve)
        self.assertEqual(error, '')
        self.assertNotEqual(base['t_quarter'], changed['t_quarter'])

    def test_no_curve_gives_a_message_not_a_crash(self):
        result, error = dyno.run(self.values, self.ratios, None)
        self.assertIsNone(result)
        self.assertIn('torque curve', error)

    def test_bad_shift_value_is_reported(self):
        result, error = dyno.run(dict(self.values, weight='99999'), self.ratios, self.curve)
        self.assertIsNone(result)
        self.assertIn('Weight', error)

    def test_result_rows_follow_the_desktop_order(self):
        result, _ = dyno.run(self.values, self.ratios, self.curve)
        labels = [label for label, _ in dyno.result_rows(result)]
        self.assertEqual(labels[0], '0-30 mph (s)')
        self.assertEqual(labels[-1], 'Top speed in run (mph)')
        self.assertEqual(len(labels), 8)


class CsvTests(unittest.TestCase):
    def test_loads_a_dyno_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'dyno.csv'
            path.write_text('rpm,hp,tq\n2000,150,394\n4000,300,394\n6000,350,306\n')
            curve = dyno.load_curve(str(path))
            self.assertEqual(len(curve.points), 3)
            self.assertAlmostEqual(curve.peak_hp, 350)

    def test_empty_csv_gives_a_readable_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'empty.csv'
            path.write_text('rpm,hp,tq\nabc,def,ghi\n')
            with self.assertRaises(ValueError) as ctx:
                dyno.load_curve(str(path))
            self.assertIn('no usable rows', str(ctx.exception))


class ChartTests(unittest.TestCase):
    def test_chart_series_cover_the_curve_range(self):
        curve = dyno.simulated_curve(400, 6000, 700)
        rpms, hp, tq = dyno.chart_series(curve)
        self.assertEqual(len(rpms), len(hp))
        self.assertEqual(len(rpms), len(tq))
        self.assertAlmostEqual(rpms[0], curve.rpm_range[0])
        self.assertAlmostEqual(rpms[-1], curve.rpm_range[1])

    def test_empty_curve_draws_nothing(self):
        from tunertoolpro.engines.torque_curve import TorqueCurve
        self.assertEqual(dyno.chart_series(TorqueCurve([])), ([], [], []))


if __name__ == '__main__':
    unittest.main()
