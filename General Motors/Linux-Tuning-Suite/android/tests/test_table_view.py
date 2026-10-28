import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from table_view import HEX, table_blocks  # noqa: E402

COLS = 17


def tables():
    return {'n_gears': 3,
            'upshift': [[10.0] * COLS, [20.0] * COLS],
            'downshift': [[6.0] * COLS, [12.0] * COLS],
            'tcc_unlock': [[255.0] * COLS, [12.0] * COLS, [18.0] * COLS],
            'tcc_lock': [[255.0] * COLS, [14.0] * COLS, [20.0] * COLS]}


def levels(changes=None):
    grid = {'upshift': [['good'] * COLS for _ in range(2)], 'downshift': [['good'] * COLS for _ in range(2)],
            'tcc_unlock': [['off'] * COLS] + [['good'] * COLS for _ in range(2)],
            'tcc_lock': [['off'] * COLS] + [['good'] * COLS for _ in range(2)]}
    for (name, row, col), level in (changes or {}).items():
        grid[name][row][col] = level
    return grid


class PlainTests(unittest.TestCase):
    def test_four_titled_blocks_with_a_header_and_a_line_per_row(self):
        blocks = table_blocks(tables())
        self.assertEqual([t for t, _ in blocks],
                         ['Upshift MPH', 'Downshift MPH', 'TCC unlock MPH', 'TCC lock MPH'])
        self.assertEqual([len(text.splitlines()) for _, text in blocks], [3, 3, 4, 4])
        self.assertIn('1-2', blocks[0][1])
        self.assertIn('Gear 3', blocks[2][1])
        self.assertNotIn('[color', blocks[0][1])


class ColourTests(unittest.TestCase):
    def test_cells_get_the_colour_and_the_marker_of_their_level(self):
        grid = levels({('upshift', 0, 2): 'bad', ('upshift', 0, 3): 'ok'})
        text = dict(table_blocks(tables(), grid))['Upshift MPH']
        self.assertIn(f'[color=#{HEX["bad"]}]  10.0![/color]', text)
        self.assertIn(f'[color=#{HEX["ok"]}]  10.0~[/color]', text)
        self.assertIn(f'[color=#{HEX["good"]}]  10.0 [/color]', text)

    def test_cells_where_the_converter_never_locks_show_dashes_not_255(self):
        text = dict(table_blocks(tables(), levels()))['TCC lock MPH']
        self.assertNotIn('255', text)
        self.assertIn('    -- ', text)


class CursorTests(unittest.TestCase):
    def cursor_cells(self, cursor):
        out = {}
        for title, text in table_blocks(tables(), levels(), cursor):
            lines = text.splitlines()[1:]
            out[title] = [(r, line.count('*')) for r, line in enumerate(lines) if '*' in line]
        return out

    def test_the_car_is_marked_in_the_row_for_its_current_gear(self):
        marks = self.cursor_cells({'gear': 2, 'tps': 50.0})
        self.assertEqual(marks['Upshift MPH'], [(1, 1)])        # the 2-3 upshift is the row for second gear
        self.assertEqual(marks['Downshift MPH'], [(0, 1)])      # the 1-2 downshift would take it out of second
        self.assertEqual(marks['TCC lock MPH'], [(1, 1)])
        self.assertEqual(marks['TCC unlock MPH'], [(1, 1)])

    def test_the_marker_sits_in_the_column_nearest_the_throttle(self):
        _, text = table_blocks(tables(), levels(), {'gear': 1, 'tps': 50.0})[0]
        row = text.splitlines()[1]
        cells = row[8:].split('[/color]')                       # eight characters of row label first
        stars = [i for i, c in enumerate(cells) if '*' in c]
        self.assertEqual(stars, [8])                            # 50 percent is column 8 on a 6.25 step axis

    def test_top_gear_has_no_upshift_to_mark_and_first_gear_no_downshift(self):
        top = self.cursor_cells({'gear': 3, 'tps': 10.0})
        self.assertNotIn('Upshift MPH', {k for k, v in top.items() if v})
        first = self.cursor_cells({'gear': 1, 'tps': 10.0})
        self.assertNotIn('Downshift MPH', {k for k, v in first.items() if v})


if __name__ == '__main__':
    unittest.main()
