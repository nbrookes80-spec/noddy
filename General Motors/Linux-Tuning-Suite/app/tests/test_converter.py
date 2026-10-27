import unittest

from tunertoolpro import converter as conv

BASE = {'stall_rpm': 2000, 'idle_rpm': 700, 'shift_rpm': 6300, 'min_tcc_rpm': 1650}


class TypesTest(unittest.TestCase):
    def test_five_types_with_labels(self):
        self.assertEqual(conv.type_keys(), ['stock', 'mild', 'high', 'triple', 'other'])
        self.assertEqual(conv.key_for_label('Stock'), 'stock')
        with self.assertRaises(KeyError):
            conv.key_for_label('nonsense')

    def test_unknown_type_is_refused(self):
        with self.assertRaises(KeyError):
            conv.adjust(BASE, 'bogus')


class AdjustTest(unittest.TestCase):
    def test_stock_changes_nothing(self):
        changes, stall_logic, _ = conv.adjust(BASE, 'stock')
        self.assertEqual(changes, BASE)
        self.assertFalse(stall_logic)

    def test_high_stall_matches_blue_cat_step_on_a_6_speed(self):
        # Blue Cat 2012 C6 6L80: stall 2000 -> 3400 field, idle +100, shift +200, min lock +200
        changes, stall_logic, _ = conv.adjust(BASE, 'high', stall_rpm=3400, n_gears=6)
        self.assertEqual(changes, {'stall_rpm': 3400, 'idle_rpm': 800, 'shift_rpm': 6500, 'min_tcc_rpm': 1850})
        self.assertTrue(stall_logic)

    def test_four_speed_min_lock_step_is_100(self):
        base = dict(BASE, min_tcc_rpm=1300)
        changes, _, _ = conv.adjust(base, 'high', stall_rpm=3400, n_gears=4)
        self.assertEqual(changes['min_tcc_rpm'], 1400)

    def test_mild_is_half_the_step(self):
        changes, _, _ = conv.adjust(BASE, 'mild', stall_rpm=2600, n_gears=6)
        self.assertEqual((changes['idle_rpm'], changes['shift_rpm'], changes['min_tcc_rpm']), (750, 6400, 1750))

    def test_choosing_twice_does_not_stack(self):
        first, _, _ = conv.adjust(BASE, 'high', stall_rpm=3200)
        again, _, _ = conv.adjust(first, 'high', stall_rpm=3200, base=BASE)
        self.assertEqual(first, again)

    def test_lock_gears_are_never_returned(self):
        changes, _, _ = conv.adjust(BASE, 'triple', stall_rpm=3200)
        for key in ('min_tcc_gear', 'accel_lock_gear', 'wot_lock_gear'):
            self.assertNotIn(key, changes)

    def test_other_scales_with_the_stall_figure(self):
        small, _, _ = conv.adjust(BASE, 'other', stall_rpm=2100)
        big, _, _ = conv.adjust(BASE, 'other', stall_rpm=3200)
        self.assertLess(small['shift_rpm'], big['shift_rpm'])
        self.assertEqual(big['shift_rpm'], 6500)

    def test_stall_is_clamped_to_the_form_range(self):
        changes, _, _ = conv.adjust(BASE, 'high', stall_rpm=9000)
        self.assertEqual(changes['stall_rpm'], conv.STALL_MAX)

    def test_min_lock_stays_inside_the_form_range(self):
        changes, _, _ = conv.adjust(dict(BASE, min_tcc_rpm=2950), 'high', stall_rpm=3400)
        self.assertEqual(changes['min_tcc_rpm'], 3000)

    def test_notes_are_tagged_with_a_source(self):
        _, _, notes = conv.adjust(BASE, 'high', stall_rpm=3400)
        self.assertTrue(notes and all(n.startswith('[') for n in notes))

    def test_classify(self):
        self.assertEqual(conv.classify(2100, 2000), 'stock')
        self.assertEqual(conv.classify(2500, 2000), 'mild')
        self.assertEqual(conv.classify(3400, 2000), 'high')


class AdviceTest(unittest.TestCase):
    def test_high_stall_advice_covers_the_blog_steps(self):
        text = ' '.join(conv.tcm_advice('high'))
        for phrase in ('TCC Desired Slip', 'Use DoD Slip', 'Apply/Release', 'Trans Input Max', 'Speed Control Terminate'):
            self.assertIn(phrase, text)

    def test_triple_plate_adds_a_line(self):
        self.assertEqual(len(conv.tcm_advice('triple')), len(conv.tcm_advice('high')) + 1)

    def test_stock_advice_is_short(self):
        self.assertEqual(len(conv.tcm_advice('stock')), 1)


class DiffTest(unittest.TestCase):
    RATIOS = [4.03, 2.36, 1.53, 1.15, 0.85, 0.67]

    def test_rpm_at_speed_worked_example(self):
        # 6L80 top 0.67, axle 3.42, 27.5 in tyre, 62.14 mph (100 km/h): 62.14*.67*3.42*63360/(60*pi*27.5) = 1740
        self.assertAlmostEqual(conv.rpm_at_speed(62.1371, 27.5, 0.67, 3.42), 1740, delta=3)

    def test_research_doc_example_shift_speed_ratio(self):
        # 2.73 vs 3.42 diff: 6500 rpm in 1st (4.03), 26.15 in tyre gives 45.9 and 36.7 mph
        for axle, mph in ((2.73, 45.9), (3.42, 36.7)):
            effect, _ = conv.diff_effect([4.03, 2.36], axle, 26.15, 6500)
            self.assertAlmostEqual(effect['first_gear_top_mph'], mph, delta=0.2)

    def test_options_include_the_current_ratio(self):
        self.assertIn(3.31, conv.diff_options(3.31))
        self.assertEqual(conv.diff_options(3.42).count(3.42), 1)

    def test_change_report_mentions_both_ratios(self):
        text = ' '.join(conv.diff_change(self.RATIOS, 3.08, 3.73, 27.5, 6300))
        self.assertIn('3.08', text)
        self.assertIn('3.73', text)

    def test_high_cruise_rpm_is_flagged(self):
        _, lines = conv.diff_effect(self.RATIOS, 4.88, 27.5, 6300)
        self.assertTrue(any('high' in l.lower() for l in lines))


if __name__ == '__main__':
    unittest.main()
