import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import shift_live as live  # noqa: E402
from tunertoolpro import core  # noqa: E402


class LiveShiftTests(unittest.TestCase):
    def setUp(self):
        self.values, self.ratios = live.default_inputs()

    def test_default_profile_calculates(self):
        tables, error = live.calculate(self.values, self.ratios)
        self.assertEqual(error, '')
        ratio_count = len(self.ratios.split(','))
        self.assertEqual(len(tables['upshift']), ratio_count - 1)
        for key in ('downshift', 'tcc_unlock', 'tcc_lock'):
            self.assertIn(key, tables)

    def test_changing_tire_diameter_changes_upshift_speeds(self):
        before, _ = live.calculate(self.values, self.ratios)
        changed = dict(self.values, tire_dia=str(float(self.values['tire_dia']) + 2.0))
        after, error = live.calculate(changed, self.ratios)
        self.assertEqual(error, '')
        self.assertNotEqual(before['upshift'], after['upshift'])

    def test_changing_a_ratio_changes_the_tables(self):
        before, _ = live.calculate(self.values, self.ratios)
        ratios = self.ratios.split(', ')
        ratios[0] = str(float(ratios[0]) + 0.2)
        after, error = live.calculate(self.values, ', '.join(ratios))
        self.assertEqual(error, '')
        self.assertNotEqual(before['upshift'], after['upshift'])

    def test_out_of_range_value_gives_a_clear_message(self):
        bad = dict(self.values, tire_dia='99')
        tables, error = live.calculate(bad, self.ratios)
        self.assertIsNone(tables)
        self.assertIn('Tire diameter', error)
        self.assertIn('between 20 and 40', error)

    def test_non_number_gives_a_clear_message(self):
        with self.assertRaises(ValueError) as ctx:
            live.parse_value('axle', 'abc')
        self.assertIn('enter a number', str(ctx.exception))

    def test_one_ratio_is_refused(self):
        tables, error = live.calculate(self.values, '3.06')
        self.assertIsNone(tables)
        self.assertIn('at least two gear ratios', error)

    def test_upshift_rows_have_header_and_one_row_per_shift(self):
        tables, _ = live.calculate(self.values, self.ratios)
        rows = live.upshift_rows(tables)
        self.assertEqual(rows[0][0], 'Shift')
        self.assertEqual(len(rows), 1 + len(tables['upshift']))


if __name__ == '__main__':
    unittest.main()
