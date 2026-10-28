import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import shift_live  # noqa: E402
from grading import GOOD, OFF, OK, BAD, grade_tables  # noqa: E402

SIX_SPEED = 'LS3 Camaro SS (6L80)'
COLS = 17


def fixture():
    """The 6L80 starting tune: its own settings and its calculated tables."""
    values, ratios = shift_live.default_inputs(SIX_SPEED)
    cfg = shift_live.build_cfg(values, ratios)
    tables, error = shift_live.calculate(values, ratios)
    assert error == ''
    return cfg, tables


def mph_at(cfg, rpm, gear):
    """Road speed that puts the engine at rpm in a 1-based gear (worked out by hand from the ratios)."""
    return rpm * cfg['tire_dia'] / (cfg['axle'] * cfg['chain'] * cfg['ratios'][gear - 1] * 336.13)


class ShapeTests(unittest.TestCase):
    def test_every_table_gets_one_level_per_cell(self):
        cfg, tables = fixture()
        result = grade_tables(tables, cfg)
        for name in ('upshift', 'downshift', 'tcc_unlock', 'tcc_lock'):
            grid = result.levels[name]
            self.assertEqual(len(grid), len(tables[name]), name)
            self.assertTrue(all(len(row) == COLS for row in grid), name)

    def test_the_stock_6l80_tune_has_no_red_cells(self):
        cfg, tables = fixture()
        result = grade_tables(tables, cfg)
        reds = [(n, r, c) for n, grid in result.levels.items() for r, row in enumerate(grid)
                for c, level in enumerate(row) if level == BAD]
        self.assertEqual(reds, [])


class UpshiftTests(unittest.TestCase):
    def test_shifting_far_above_the_shift_rpm_is_red(self):
        cfg, tables = fixture()
        tables['upshift'][0][8] = mph_at(cfg, 7000, 1)       # 7000 rpm against a 6300 target
        self.assertEqual(grade_tables(tables, cfg).levels['upshift'][0][8], BAD)

    def test_shifting_just_above_the_shift_rpm_is_yellow(self):
        cfg, tables = fixture()
        tables['upshift'][0][8] = mph_at(cfg, 6400, 1)       # 1.6 percent over the target
        self.assertEqual(grade_tables(tables, cfg).levels['upshift'][0][8], OK)

    def test_a_shift_that_drops_the_engine_to_idle_is_red(self):
        cfg, tables = fixture()
        # 1000 rpm in gear 1 falls to 1000 * 2.364 / 4.027 = 587 rpm in gear 2, below idle plus 150
        tables['upshift'][0][2] = mph_at(cfg, 1000, 1)
        self.assertEqual(grade_tables(tables, cfg).levels['upshift'][0][2], BAD)

    def test_a_cell_lower_than_the_one_before_it_is_red(self):
        cfg, tables = fixture()
        tables['upshift'][2][10] = tables['upshift'][2][9] - 3.0
        self.assertEqual(grade_tables(tables, cfg).levels['upshift'][2][10], BAD)


class DownshiftTests(unittest.TestCase):
    def test_a_downshift_at_or_above_the_upshift_is_red(self):
        cfg, tables = fixture()
        tables['downshift'][1][6] = tables['upshift'][1][6] + 0.5       # the box would hunt
        self.assertEqual(grade_tables(tables, cfg).levels['downshift'][1][6], BAD)

    def test_a_narrow_gap_below_the_upshift_is_yellow(self):
        cfg, tables = fixture()
        tables['downshift'][1][6] = tables['upshift'][1][6] - 1.5
        self.assertEqual(grade_tables(tables, cfg).levels['downshift'][1][6], OK)

    def test_a_downshift_that_revs_past_the_shift_rpm_is_red(self):
        cfg, tables = fixture()
        tables['downshift'][0][12] = mph_at(cfg, 7000, 1)       # lands in gear 1 at 7000 rpm
        self.assertEqual(grade_tables(tables, cfg).levels['downshift'][0][12], BAD)


class ConverterLockTests(unittest.TestCase):
    def test_cells_where_the_converter_never_locks_are_off_not_red(self):
        cfg, tables = fixture()
        result = grade_tables(tables, cfg)
        self.assertTrue(all(level == OFF for level in result.levels['tcc_lock'][0]))
        self.assertTrue(all(level == OFF for level in result.levels['tcc_unlock'][0]))

    def test_locking_far_below_the_minimum_lock_rpm_is_red(self):
        cfg, tables = fixture()
        tables['tcc_lock'][2][8] = mph_at(cfg, 900, 3)            # minimum is 1300 rpm
        self.assertEqual(grade_tables(tables, cfg).levels['tcc_lock'][2][8], BAD)

    def test_unlocking_at_or_above_the_lock_speed_is_red(self):
        cfg, tables = fixture()
        tables['tcc_unlock'][3][9] = tables['tcc_lock'][3][9] + 1.0
        self.assertEqual(grade_tables(tables, cfg).levels['tcc_unlock'][3][9], BAD)

    def test_a_one_mph_gap_between_unlock_and_lock_is_yellow(self):
        cfg, tables = fixture()
        tables['tcc_unlock'][3][9] = tables['tcc_lock'][3][9] - 0.8
        self.assertEqual(grade_tables(tables, cfg).levels['tcc_unlock'][3][9], OK)


class SummaryTests(unittest.TestCase):
    def test_counts_and_worst_cells_describe_the_problems_in_words(self):
        cfg, tables = fixture()
        tables = copy.deepcopy(tables)
        tables['upshift'][0][16] = mph_at(cfg, 7000, 1)
        result = grade_tables(tables, cfg)
        self.assertEqual(result.counts[BAD], 1)
        self.assertGreater(result.counts[GOOD], 100)
        worst = result.worst[0]
        self.assertEqual((worst['table'], worst['row'], worst['col']), ('upshift', 0, 16))
        self.assertIn('7000', worst['message'])
        self.assertIn('6300', worst['message'])


if __name__ == '__main__':
    unittest.main()
