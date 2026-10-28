"""Transmission choices and per-transmission Blue Cat data, tested through the core only."""

import tempfile
import unittest
from pathlib import Path

from tunertoolpro import core, trans_data, vehicles


def data(name):
    return trans_data.for_transmission(vehicles.find(name))


def values_for(profile):
    """The Shift tab's inputs as text, from a starter profile."""
    cfg = core.shift_cfg_from_profile(profile)
    keys = ('tire_dia', 'axle', 'chain', 'weight', 'rwhp', 'idle_rpm', 'stall_rpm', 'shift_rpm', 'downshift_rpm',
            'min_tcc_rpm', 'min_tcc_gear', 'accel_lock_gear', 'wot_lock_gear', 'lead_value')
    return {k: str(cfg[k]) for k in keys}


class ChoiceTests(unittest.TestCase):
    def test_all_four_makes_are_offered(self):
        self.assertEqual(vehicles.MAKES, ('GM', 'Holden', 'Pontiac', 'Ford'))

    def test_each_make_lists_automatics_and_gm_is_not_limited_to_the_4l60e(self):
        for make in vehicles.MAKES:
            self.assertGreaterEqual(len(vehicles.transmissions(make)), 4, make)
        names = [t.name for t in vehicles.transmissions('GM')]
        self.assertTrue(any(n.startswith('6L80') for n in names))
        self.assertTrue(any(n.startswith('10L90') for n in names))

    def test_holden_and_pontiac_g8_list_the_6l80(self):
        for make in ('Holden', 'Pontiac'):
            self.assertTrue(any(t.name.startswith('6L80') for t in vehicles.transmissions(make)), make)

    def test_ford_lists_its_own_automatics(self):
        names = [t.name for t in vehicles.transmissions('Ford')]
        for code in ('4R70W', '6R80', '10R80', 'ZF 6HP26'):
            self.assertTrue(any(n.startswith(code) for n in names), code)

    def test_ratios_fall_with_each_gear_and_the_checked_state_is_stated(self):
        for make in vehicles.MAKES:
            for t in vehicles.transmissions(make):
                self.assertEqual(t.ratios, sorted(t.ratios, reverse=True), t.name)
        self.assertFalse(vehicles.find('4R70W (1993-2003)').verified)
        self.assertEqual(vehicles.find('6L80 (2006-Current)').ratios[0], 4.027)

    def test_ratio_text_and_unknown_name(self):
        self.assertEqual(vehicles.ratios_text(vehicles.find('4R70W (1993-2003)')), '2.84, 1.55, 1, 0.7')
        self.assertIsNone(vehicles.find('Powerglide'))


class FitAndRemember(unittest.TestCase):
    def test_lock_gears_never_exceed_the_gears_the_transmission_has(self):
        values = {'min_tcc_gear': '6', 'accel_lock_gear': '5', 'wot_lock_gear': '4', 'idle_rpm': '700'}
        fitted = vehicles.fit_gears(values, 4)
        self.assertEqual((fitted['min_tcc_gear'], fitted['accel_lock_gear'], fitted['wot_lock_gear']), ('4', '4', '4'))
        self.assertEqual(values['min_tcc_gear'], '6')

    def test_a_saved_choice_comes_back_and_damage_is_dropped(self):
        path = Path(tempfile.mkdtemp()) / 'vehicle.json'
        self.assertEqual(vehicles.load(path), {'make': 'GM', 'transmission': '', 'profile': ''})
        vehicles.save(path, {'make': 'Ford', 'transmission': '6R80 (2009-Current)', 'profile': ''})
        self.assertEqual(vehicles.load(path)['transmission'], '6R80 (2009-Current)')
        path.write_text('{"make": "Mazda", "transmission": "Powerglide", "profile": 5}')
        self.assertEqual(vehicles.load(path), {'make': 'GM', 'transmission': '', 'profile': ''})


class BlueCatValues(unittest.TestCase):
    def test_the_6l80_gets_the_blue_cat_preset(self):
        d = data('6L80 (2006-Current)')
        self.assertEqual(d.delays, [(0.45, 0.15), (0.45, 0.15), (0.5, 0.15), (0.45, 0.15), (0.45, 0.15)])
        self.assertEqual((d.lead_mode, d.lead_value, d.vss), ('torque', 2.5, 36))
        self.assertEqual((d.min_tcc_rpm, d.min_tcc_gear, d.accel_lock_gear, d.wot_lock_gear), (1250, 3, 3, 3))
        self.assertFalse(d.derived)
        self.assertEqual(d.torque_rating, 440)

    def test_other_gm_units_have_their_own_delays(self):
        self.assertEqual(data('4L60E (1993-2013)').delays, [(0, 0.35), (0, 0.4), (0, 0.35)])
        self.assertEqual(data('4L80E (1991-2013)').delays, [(0, 0.45), (0, 0.45), (0, 0.4)])
        self.assertEqual(data('4L70E (2006-2013)').delays, [(0, 0)] * 3)
        self.assertEqual(len(data('8L90 (2014-Current)').delays), 7)
        self.assertEqual(len(data('10L90 (2017-Current)').delays), 9)

    def test_no_blue_cat_data_means_derived_and_says_so(self):
        for name in ('6R80 (2009-Current)', '4R70W (1993-2003)', '10R80 (2017-Current)', '5L40E (2003-2009)'):
            d = data(name)
            self.assertTrue(d.derived, name)
            self.assertIn('derived', d.source.lower(), name)
        self.assertIsNone(data('6R80 (2009-Current)').torque_rating)


class EveryTransmission(unittest.TestCase):
    def test_each_has_one_delay_pair_per_shift_and_gives_valid_tables(self):
        values = values_for('LS3 Camaro SS (6L80)')
        for t in vehicles.ALL:
            d = trans_data.for_transmission(t)
            self.assertEqual(len(d.delays), len(t.ratios) - 1, t.name)
            for gear in (d.min_tcc_gear, d.accel_lock_gear, d.wot_lock_gear):
                self.assertLessEqual(gear, len(t.ratios), t.name)
            cfg = core.shift_cfg_from_profile('LS3 Camaro SS (6L80)')
            cfg['ratios'] = list(t.ratios)
            cfg['delays'] = list(d.delays)
            for key in ('min_tcc_gear', 'accel_lock_gear', 'wot_lock_gear'):
                cfg[key] = min(int(values[key]), len(t.ratios))
            tables = core.calc_shift_tables(cfg)
            self.assertEqual(len(tables['upshift']), len(t.ratios) - 1, t.name)


class ApplyTests(unittest.TestCase):
    def test_apply_sets_lock_and_lead_and_leaves_the_cars_own_values(self):
        values = values_for('LS1 Camaro / Trans Am (4L60E)')
        applied = trans_data.apply(values, data('6L80 (2006-Current)'))
        self.assertEqual((applied['min_tcc_rpm'], applied['min_tcc_gear'], applied['lead_value']), ('1250', '3', '2.5'))
        for key in ('tire_dia', 'axle', 'weight', 'rwhp', 'idle_rpm', 'stall_rpm', 'shift_rpm'):
            self.assertEqual(applied[key], values[key], key)

    def test_summary_names_the_source(self):
        text = trans_data.summary(data('6L80 (2006-Current)'))
        self.assertIn('0.45', text)
        self.assertIn('Blue Cat', text)


if __name__ == '__main__':
    unittest.main()
