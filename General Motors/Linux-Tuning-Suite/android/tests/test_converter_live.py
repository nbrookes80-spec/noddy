import unittest

import converter_live as cl

VALUES = {'stall_rpm': '2200', 'idle_rpm': '650', 'shift_rpm': '6300', 'min_tcc_rpm': '1300',
          'axle': '3.42', 'tire_dia': '27.5', 'chain': '1'}
RATIOS = '4.03, 2.36, 1.53, 1.15, 0.85, 0.67'


class ChooseTest(unittest.TestCase):
    def test_high_stall_gives_text_values_and_advice(self):
        base = cl.read_base(VALUES)
        changes, logic, notes, advice = cl.choose(VALUES, base, 'High stall, single plate', 6)
        self.assertEqual(changes['idle_rpm'], '750')
        self.assertEqual(changes['shift_rpm'], '6500')
        self.assertEqual(changes['min_tcc_rpm'], '1500')
        self.assertTrue(logic and notes and advice)

    def test_stock_returns_the_base(self):
        base = cl.read_base(VALUES)
        changes, logic, _, _ = cl.choose(VALUES, base, 'Stock', 6)
        self.assertEqual(changes['shift_rpm'], '6300')
        self.assertFalse(logic)

    def test_unreadable_values_change_nothing(self):
        bad = dict(VALUES, shift_rpm='')
        changes, _, notes, _ = cl.choose(bad, cl.read_base(VALUES), 'Stock', 6)
        self.assertEqual(changes, {})
        self.assertTrue(notes)

    def test_typed_stall_is_kept(self):
        base = cl.read_base(VALUES)
        typed = dict(VALUES, stall_rpm='3100')
        changes, _, _, _ = cl.choose(typed, base, 'Other / custom', 6)
        self.assertEqual(changes['stall_rpm'], '3100')


class DiffTest(unittest.TestCase):
    def test_values_include_current(self):
        self.assertIn('3.31', cl.diff_values('3.31'))
        self.assertIn('3.73', cl.diff_values('abc'))

    def test_report_and_summary(self):
        self.assertIn('3.73', ' '.join(cl.diff_report(RATIOS, '3.42', '3.73', VALUES)))
        self.assertTrue(cl.diff_summary(RATIOS, VALUES))
        self.assertEqual(cl.diff_summary('x', VALUES), [])


if __name__ == '__main__':
    unittest.main()
