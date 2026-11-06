"""Units, colour bands and lowest/highest/average: the dashboard additions that need no screen."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import prefs  # noqa: E402
from scanner import pid_view, pids, units  # noqa: E402


def pid_with_unit(unit):
    return next(p for p in pids.CATALOG.values() if p.unit == unit)


class UnitTests(unittest.TestCase):
    def test_celsius_to_fahrenheit_and_back(self):
        conv = units.conversion('°C', {'temperature': '°F'})
        self.assertEqual(conv.unit, '°F')
        self.assertAlmostEqual(conv.forward(90), 194)
        self.assertAlmostEqual(conv.forward(-40), -40)
        self.assertAlmostEqual(conv.back(conv.forward(37.5)), 37.5)

    def test_pressure_goes_both_ways_between_kpa_psi_and_bar(self):
        self.assertAlmostEqual(units.conversion('kPa', {'pressure': 'psi'}).forward(689.4757), 100, places=3)
        self.assertAlmostEqual(units.conversion('psi', {'pressure': 'kPa'}).forward(100), 689.4757, places=3)
        self.assertAlmostEqual(units.conversion('kPa', {'pressure': 'bar'}).forward(250), 2.5)
        self.assertAlmostEqual(units.conversion('Pa', {'pressure': 'kPa'}).forward(2000), 2)

    def test_distance_follows_the_speed_choice(self):
        self.assertEqual(units.conversion('km', {'speed': 'mph'}).unit, 'mi')
        self.assertAlmostEqual(units.conversion('km/h', {'speed': 'mph'}).forward(100), 62.1371, places=3)
        self.assertEqual(units.conversion('km', {'speed': 'km/h'}).unit, 'km')

    def test_a_unit_it_does_not_know_is_left_alone(self):
        for unit in ('RPM', '%', 'V', 'g/s', ''):
            with self.subTest(unit=unit):
                conv = units.conversion(unit, {'temperature': '°F', 'pressure': 'psi', 'speed': 'mph'})
                self.assertEqual((conv.unit, conv.forward(42.5), conv.back(42.5)), (unit, 42.5, 42.5))

    def test_the_default_changes_nothing(self):
        for unit in ('°C', 'kPa', 'km/h', 'km'):
            self.assertEqual(units.conversion(unit, None).forward(12.5), 12.5)

    def test_choices_that_are_not_offered_fall_back_to_the_defaults(self):
        self.assertEqual(units.clean({'temperature': 'kelvin', 'pressure': 'psi', 'speed': 5}),
                         {'temperature': '°C', 'pressure': 'psi', 'speed': 'km/h'})
        self.assertEqual(units.clean('nonsense'), units.DEFAULTS)


class ViewUnitTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(tempfile.mkdtemp()) / 'pid_view.json'
        self.views = pid_view.PidViews(self.path)
        self.temp = pid_with_unit('°C')

    def test_a_sensor_is_shown_in_the_chosen_unit(self):
        self.views.set_units({'temperature': '°F'})
        shown = self.views.apply(self.temp)
        self.assertEqual(shown['unit'], '°F')
        self.assertAlmostEqual(shown['convert'](100), 212)
        self.assertAlmostEqual(shown['low'], self.temp.low * 1.8 + 32)

    def test_limits_are_saved_in_the_sensors_own_unit_so_changing_units_never_moves_them(self):
        self.views.update(self.temp.pid, redline=110.0, cold=40.0)
        self.assertEqual(self.views.get(self.temp.pid)['redline'], 110.0)
        self.views.set_units({'temperature': '°F'})
        shown = self.views.apply(self.temp)
        self.assertAlmostEqual(shown['redline'], 230)
        self.assertAlmostEqual(shown['cold'], 104)
        self.assertAlmostEqual(shown['back'](shown['redline']), 110)
        self.views.set_units({'temperature': '°C'})
        self.assertAlmostEqual(self.views.apply(self.temp)['redline'], 110)

    def test_a_unit_typed_in_by_hand_is_not_converted(self):
        self.views.update(self.temp.pid, unit='deg')
        self.views.set_units({'temperature': '°F'})
        shown = self.views.apply(self.temp)
        self.assertEqual((shown['unit'], shown['convert'](100)), ('deg', 100))

    def test_an_old_saved_unit_that_matches_the_sensors_own_does_not_stop_conversion(self):
        self.views.update(self.temp.pid, unit=self.temp.unit)    # the editor used to save the unit every time
        self.views.set_units({'temperature': '°F'})
        self.assertEqual(self.views.apply(self.temp)['unit'], '°F')

    def test_the_new_limits_survive_a_restart_and_junk_is_dropped(self):
        self.views.update(self.temp.pid, cold=50.0, good=70.0, redline=105.0)
        again = pid_view.PidViews(self.path).get(self.temp.pid)
        self.assertEqual((again['cold'], again['good'], again['redline']), (50.0, 70.0, 105.0))
        self.path.write_text(json.dumps({self.temp.pid: {'cold': 'cold', 'good': True, 'redline': float('inf')}}))
        self.assertEqual(pid_view.PidViews(self.path).get(self.temp.pid), {})


class ZoneTests(unittest.TestCase):
    SHOWN = {'cold': 50.0, 'good': 70.0, 'redline': 110.0}

    def test_each_band(self):
        zone = lambda v: pid_view.zone(v, self.SHOWN)    # noqa: E731
        self.assertEqual([zone(40), zone(50), zone(69.9), zone(70), zone(109.9), zone(110), zone(200)],
                         ['cold', None, None, 'good', 'good', 'red', 'red'])

    def test_red_wins_over_the_others(self):
        self.assertEqual(pid_view.zone(100, {'cold': 150.0, 'good': 10.0, 'redline': 90.0}), 'red')

    def test_a_sensor_with_no_limits_has_no_bands(self):
        self.assertIsNone(pid_view.zone(55, {}))
        self.assertIsNone(pid_view.zone(None, self.SHOWN))


class StatsTests(unittest.TestCase):
    def test_lowest_highest_and_average(self):
        stats = pid_view.Stats()
        self.assertIsNone(stats.average)
        for value in (10, 30, 20):
            stats.add(value)
        self.assertEqual((stats.low, stats.high, stats.average, stats.count), (10, 30, 20, 3))

    def test_reset_and_bad_readings(self):
        stats = pid_view.Stats()
        for value in (5, None, float('nan'), float('inf'), 7):
            stats.add(value)
        self.assertEqual((stats.low, stats.high, stats.count), (5, 7, 2))
        stats.reset()
        self.assertEqual((stats.low, stats.high, stats.average, stats.count), (None, None, None, 0))


class PrefsTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(tempfile.mkdtemp()) / 'prefs.json'

    def test_new_installs_get_the_new_defaults(self):
        loaded = prefs.load(self.path)
        self.assertEqual((loaded['dash_stats'], loaded['hud_mirror']), (True, False))
        self.assertEqual((loaded['unit_temperature'], loaded['unit_pressure'], loaded['unit_speed']),
                         ('°C', 'kPa', 'km/h'))

    def test_choices_come_back_and_bad_ones_fall_back(self):
        prefs.save(self.path, {'unit_temperature': '°F', 'unit_pressure': 'psi', 'unit_speed': 'mph',
                               'dash_stats': False, 'hud_mirror': True})
        loaded = prefs.load(self.path)
        self.assertEqual((loaded['unit_temperature'], loaded['unit_pressure'], loaded['unit_speed'],
                          loaded['dash_stats'], loaded['hud_mirror']), ('°F', 'psi', 'mph', False, True))
        self.path.write_text(json.dumps({'unit_temperature': 'K', 'unit_pressure': 3, 'hud_mirror': 'yes'}))
        loaded = prefs.load(self.path)
        self.assertEqual((loaded['unit_temperature'], loaded['unit_pressure'], loaded['hud_mirror']),
                         ('°C', 'kPa', False))


if __name__ == '__main__':
    unittest.main()
