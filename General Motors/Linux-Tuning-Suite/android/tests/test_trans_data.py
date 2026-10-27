import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import shift_live  # noqa: E402
from tunertoolpro import trans_data  # noqa: E402
from tunertoolpro import vehicles  # noqa: E402


def data(name):
    return trans_data.for_transmission(vehicles.find(name))


class BlueCatValues(unittest.TestCase):
    def test_the_6l80_gets_the_blue_cat_preset_and_its_shipped_tunes(self):
        d = data('6L80 (2006-Current)')
        self.assertEqual(d.delays, [(0.45, 0.15), (0.45, 0.15), (0.5, 0.15), (0.45, 0.15), (0.45, 0.15)])
        self.assertEqual((d.lead_mode, d.lead_value, d.vss), ('torque', 2.5, 36))
        self.assertEqual((d.min_tcc_rpm, d.min_tcc_gear, d.accel_lock_gear, d.wot_lock_gear), (1250, 3, 3, 3))
        self.assertFalse(d.derived)
        self.assertIn('Blue Cat', d.source)
        self.assertEqual(d.torque_rating, 440)

    def test_the_4l60e_and_4l80e_have_their_own_delays(self):
        self.assertEqual(data('4L60E (1993-2013)').delays, [(0, 0.35), (0, 0.4), (0, 0.35)])
        self.assertEqual(data('4L80E (1991-2013)').delays, [(0, 0.45), (0, 0.45), (0, 0.4)])
        self.assertEqual(data('4L60E (1993-2013)').lead_value, 1.0)

    def test_the_4l70e_follows_its_shipped_tunes_which_use_no_delay(self):
        self.assertEqual(data('4L70E (2006-2013)').delays, [(0, 0)] * 3)

    def test_the_8l90_and_10l90_presets(self):
        d = data('8L90 (2014-Current)')
        self.assertEqual(d.delays[0], (0.45, 0.15))
        self.assertEqual(d.delays[1], (0.35, 0.1))
        self.assertEqual(len(d.delays), 7)
        self.assertEqual(d.vss, 68)
        self.assertEqual(len(data('10L90 (2017-Current)').delays), 9)


class DerivedValues(unittest.TestCase):
    def test_a_transmission_with_no_blue_cat_data_is_derived_from_its_gear_count_and_says_so(self):
        for name in ('6R80 (2009-Current)', '4R70W (1993-2003)', '10R80 (2017-Current)', '5L40E (2003-2009)',
                     '6L50 (2007-Current)'):
            d = data(name)
            self.assertTrue(d.derived, name)
            self.assertIn('derived', d.source.lower(), name)
        self.assertEqual(data('6R80 (2009-Current)').lead_value, 2.5)
        self.assertEqual(data('4R70W (1993-2003)').lead_value, 1.0)

    def test_an_unknown_torque_rating_is_none_not_a_guess(self):
        self.assertIsNone(data('6R80 (2009-Current)').torque_rating)
        self.assertEqual(data('10L90 (2017-Current)').torque_rating, 600)


class EveryTransmission(unittest.TestCase):
    def test_each_one_has_one_delay_pair_per_shift_and_values_inside_the_screens_ranges(self):
        ranges = {f[0]: (f[2], f[3]) for f in shift_live.FIELDS}
        for t in vehicles.ALL:
            d = trans_data.for_transmission(t)
            self.assertEqual(len(d.delays), len(t.ratios) - 1, t.name)
            for prep, react in d.delays:
                self.assertTrue(0 <= prep <= 2 and 0 <= react <= 2, t.name)
            for key, value in (('min_tcc_rpm', d.min_tcc_rpm), ('lead_value', d.lead_value),
                               ('min_tcc_gear', d.min_tcc_gear), ('accel_lock_gear', d.accel_lock_gear),
                               ('wot_lock_gear', d.wot_lock_gear)):
                low, high = ranges[key]
                self.assertTrue(low <= value <= high, (t.name, key, value))
            for gear in (d.min_tcc_gear, d.accel_lock_gear, d.wot_lock_gear):
                self.assertLessEqual(gear, len(t.ratios), t.name)

    def test_each_one_produces_valid_tables_with_its_data_applied(self):
        values, _ = shift_live.default_inputs('LS3 Camaro SS (6L80)')
        for t in vehicles.ALL:
            d = trans_data.for_transmission(t)
            applied = trans_data.apply(values, d)
            tables, error = shift_live.calculate(applied, vehicles.ratios_text(t), d.lead_mode, False, d.delays)
            self.assertEqual(error, '', t.name)

    def test_the_delays_change_the_torque_lead_result(self):
        values, ratios = shift_live.default_inputs('LS3 Camaro SS (6L80)')
        slow = shift_live.calculate(values, ratios, 'torque', False, [(0.9, 0.5)] * 5)[0]
        quick = shift_live.calculate(values, ratios, 'torque', False, [(0.0, 0.0)] * 5)[0]
        self.assertNotEqual(slow['upshift'], quick['upshift'])


class ApplyTests(unittest.TestCase):
    def test_apply_sets_lock_gears_and_lead_and_leaves_the_cars_own_values(self):
        values, _ = shift_live.default_inputs('LS1 Camaro / Trans Am (4L60E)')
        applied = trans_data.apply(values, data('6L80 (2006-Current)'))
        self.assertEqual((applied['min_tcc_rpm'], applied['min_tcc_gear'], applied['lead_value']), ('1250', '3', '2.5'))
        for key in ('tire_dia', 'axle', 'weight', 'rwhp', 'idle_rpm', 'stall_rpm', 'shift_rpm'):
            self.assertEqual(applied[key], values[key], key)
        self.assertNotEqual(values['min_tcc_gear'], applied['min_tcc_gear'])   # the original was not changed

    def test_the_summary_says_what_was_loaded_and_where_from(self):
        text = trans_data.summary(data('6L80 (2006-Current)'))
        self.assertIn('0.45', text)
        self.assertIn('Blue Cat', text)


if __name__ == '__main__':
    unittest.main()
