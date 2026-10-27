import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import shift_live  # noqa: E402
import vehicles  # noqa: E402


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
                self.assertIsInstance(t.verified, bool)
        self.assertFalse(vehicles.find('4R70W (1993-2003)').verified)    # Ford figures are unchecked
        self.assertEqual(vehicles.find('6L80 (2006-Current)').ratios[0], 4.027)

    def test_a_ratio_list_is_written_the_way_the_gear_box_expects(self):
        self.assertEqual(vehicles.ratios_text(vehicles.find('4R70W (1993-2003)')), '2.84, 1.55, 1, 0.7')

    def test_unknown_name_gives_none(self):
        self.assertIsNone(vehicles.find('Powerglide'))


class FitTests(unittest.TestCase):
    def test_lock_gears_never_exceed_the_gears_the_transmission_has(self):
        values = {'min_tcc_gear': '6', 'accel_lock_gear': '5', 'wot_lock_gear': '4', 'idle_rpm': '700'}
        fitted = vehicles.fit_gears(values, 4)
        self.assertEqual((fitted['min_tcc_gear'], fitted['accel_lock_gear'], fitted['wot_lock_gear']),
                         ('4', '4', '4'))
        self.assertEqual(fitted['idle_rpm'], '700')
        self.assertEqual(values['min_tcc_gear'], '6')        # the original is untouched

    def test_every_listed_transmission_gives_valid_shift_tables(self):
        values, _ = shift_live.default_inputs()
        for make in vehicles.MAKES:
            for t in vehicles.transmissions(make):
                tables, error = shift_live.calculate(vehicles.fit_gears(values, len(t.ratios)),
                                                     vehicles.ratios_text(t))
                self.assertEqual(error, '', t.name)
                self.assertEqual(len(tables['upshift']), len(t.ratios) - 1, t.name)


class RememberTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(tempfile.mkdtemp()) / 'vehicle.json'

    def test_the_first_run_starts_on_the_original_profile(self):
        self.assertEqual(vehicles.load(self.path), {'make': 'GM', 'transmission': '', 'profile': ''})

    def test_a_saved_choice_comes_back(self):
        vehicles.save(self.path, {'make': 'Ford', 'transmission': '6R80 (2009-Current)', 'profile': ''})
        self.assertEqual(vehicles.load(self.path)['transmission'], '6R80 (2009-Current)')

    def test_damaged_or_unknown_values_are_dropped(self):
        self.path.write_text('{"make": "Mazda", "transmission": "Powerglide", "profile": 5}')
        self.assertEqual(vehicles.load(self.path), {'make': 'GM', 'transmission': '', 'profile': ''})
        self.path.write_text('not json')
        self.assertEqual(vehicles.load(self.path)['make'], 'GM')


if __name__ == '__main__':
    unittest.main()
