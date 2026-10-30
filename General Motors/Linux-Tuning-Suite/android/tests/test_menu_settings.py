"""The settings behind the menu: themes, pre-defined lists, new saved choices, hidden PIDs, log rate."""

import csv
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import prefs  # noqa: E402
from link import obd  # noqa: E402
from recorder import Recorder  # noqa: E402
from scanner import pid_view, pids, predefined, profiles, themes  # noqa: E402
from scanner.data_log import DataLogger  # noqa: E402
from scanner.session import Session  # noqa: E402


class ThemeTests(unittest.TestCase):
    def tearDown(self):
        themes.use(themes.DEFAULT)

    def test_an_unknown_theme_keeps_the_current_one(self):
        themes.use('green')
        themes.use('no-such-theme')
        self.assertEqual(themes.current().key, 'green')

    def test_every_theme_has_a_label_that_maps_back_to_it(self):
        for theme in themes.THEMES.values():
            self.assertEqual(themes.key_for(theme.label), theme.key)


class PredefinedListTests(unittest.TestCase):
    def test_a_list_is_made_of_real_rows_of_its_file(self):
        for item in predefined.LISTS:
            with self.subTest(item=item.key):
                self.assertGreater(predefined.count(item), 0)

    def test_the_gm_groups_cover_every_row_once(self):
        total = predefined.count(predefined.by_key('gm-all'))
        parts = sum(predefined.count(predefined.by_key(k))
                    for k in ('gm-transmission', 'gm-engine', 'gm-misfire', 'gm-abs'))
        self.assertEqual(parts, total)

    def test_the_holden_groups_cover_every_row_once(self):
        total = predefined.count(predefined.by_key('holden-e38-t43'))
        self.assertEqual(predefined.count(predefined.by_key('holden-t43'))
                         + predefined.count(predefined.by_key('holden-e38')), total)

    def test_the_text_is_a_csv_the_importer_accepts_with_nothing_rejected(self):
        from scanner import torque_csv
        for item in predefined.LISTS:
            with self.subTest(item=item.key):
                found, rejected = torque_csv.parse(predefined.csv_text(item))
                self.assertEqual([r for r in rejected if 'already' not in r['reason']], [])
                self.assertEqual(len({p.pid for p in found}), predefined.count(item))

    def test_transmission_lists_hold_only_transmission_rows(self):
        names = [r[0] for r in csv.reader(io.StringIO(predefined.csv_text(predefined.by_key('gm-transmission'))))][1:]
        self.assertTrue(names)
        self.assertFalse([n for n in names if 'Misfire' in n or 'ABS' in n or 'Injector' in n])

    def test_saving_makes_a_user_profile_for_the_car(self):
        with tempfile.TemporaryDirectory() as folder:
            item = predefined.by_key('holden-e38-t43')
            profile, rejected = predefined.save_to_profile(folder, item, '', 'Holden', 'VE Commodore SS', '2011',
                                                           '6L80 (2006-Current)')
            self.assertEqual(rejected, [])
            self.assertEqual((profile.make, profile.years, profile.transmission),
                             ('Holden', '2011', '6L80 (2006-Current)'))
            found = [p for p in profiles.list_user(folder) if p.key == profile.key]
            self.assertEqual(len(found), 1)
            extras, _ = profiles.load_pids(found[0])
            self.assertEqual(len(extras), predefined.count(item))
        pids.use_extras([])

    def test_a_car_with_no_name_is_not_saved(self):
        with tempfile.TemporaryDirectory() as folder:
            profile, rejected = predefined.save_to_profile(folder, predefined.LISTS[0], ' ', '', '', '', '')
            self.assertIsNone(profile)
            self.assertIn('Give the car', rejected[0]['reason'])
            self.assertEqual(list(Path(folder).iterdir()), [])


class PrefsTests(unittest.TestCase):
    def load(self, data):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, 'prefs.json')
            Path(path).write_text(json.dumps(data))
            return prefs.load(path)

    def test_new_choices_have_safe_defaults(self):
        got = self.load({})
        self.assertEqual((got['dash_columns'], got['dash_theme'], got['log_scope'], got['log_rate'],
                          got['adapter_protocol'], got['hidden_pids']), (0, 'classic', 'all', 0, '0', {}))

    def test_good_choices_are_kept_and_bad_ones_fall_back(self):
        got = self.load({'dash_columns': 3, 'dash_theme': 'ice', 'dash_default_mode': 'analogue', 'log_scope': 'live',
                         'log_rate': 5, 'adapter_protocol': '6'})
        self.assertEqual((got['dash_columns'], got['dash_theme'], got['dash_default_mode'], got['log_scope'],
                          got['log_rate'], got['adapter_protocol']), (3, 'ice', 'analogue', 'live', 5, '6'))
        bad = self.load({'dash_columns': 9, 'dash_theme': 'x', 'dash_default_mode': 'x', 'log_scope': 'x',
                         'log_rate': True, 'adapter_protocol': 'ATZ'})
        self.assertEqual((bad['dash_columns'], bad['dash_theme'], bad['dash_default_mode'], bad['log_scope'],
                          bad['log_rate'], bad['adapter_protocol']), (0, 'classic', 'digital', 'all', 0, '0'))

    def test_hidden_pids_keep_only_valid_ids(self):
        got = self.load({'hidden_pids': {'holden-ve': ['22194f', '0105', 'ATZ', 5, '2219'], 'bad': 'x'}})
        self.assertEqual(got['hidden_pids'], {'holden-ve': ['0105', '22194F']})

    def test_saving_and_loading_round_trips(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, 'prefs.json')
            choices = dict(prefs.DEFAULTS, dash_columns=4, hidden_pids={'k': ['0105']}, adapter_protocol='6')
            prefs.save(path, choices)
            got = prefs.load(path)
            self.assertEqual((got['dash_columns'], got['hidden_pids'], got['adapter_protocol']),
                             (4, {'k': ['0105']}, '6'))

    def test_the_protocol_choices_are_all_guarded_commands(self):
        for code in prefs.DEFAULTS and obd.PROTOCOLS:
            self.assertTrue(obd.is_allowed(f'ATSP{code}'))


class DefaultDisplayTests(unittest.TestCase):
    def test_the_default_applies_until_a_sensor_has_its_own_choice(self):
        with tempfile.TemporaryDirectory() as folder:
            views = pid_view.PidViews(os.path.join(folder, 'v.json'))
            views.update('010C', mode='graph')
            views.set_default('analogue')
            self.assertEqual(views.mode('010C'), 'graph')
            self.assertEqual(views.mode('0105'), 'analogue')
            views.set_default('nonsense')
            self.assertEqual(views.mode('0105'), 'analogue')

    def test_clearing_modes_keeps_names_and_red_lines(self):
        with tempfile.TemporaryDirectory() as folder:
            views = pid_view.PidViews(os.path.join(folder, 'v.json'))
            views.update('010C', mode='graph', redline=6500, name='Revs')
            views.update('0105', mode='text')
            views.clear_modes()
            self.assertEqual(views.get('010C'), {'redline': 6500.0, 'name': 'Revs'})
            self.assertEqual(views.get('0105'), {})
            self.assertEqual(pid_view.PidViews(os.path.join(folder, 'v.json')).get('0105'), {})


class RateTests(unittest.TestCase):
    COLUMNS = [('010C', 'rpm'), ('010D', 'speed')]

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.now = 1_800_000_000.0
        self.log = DataLogger(self.tmp.name, clock=lambda: self.now)

    def rows(self):
        with open(self.log.path, newline='') as handle:
            return list(csv.reader(handle))[1:]

    def test_rows_are_held_back_to_the_chosen_rate_but_readings_are_not_lost(self):
        self.log.min_interval = 1.0
        self.log.start(self.COLUMNS)
        self.log.update({'010C': (800.0, 'rpm')})
        self.now += 0.3
        self.log.update({'010D': (30.0, 'km/h')})        # too soon for a row
        self.now += 0.3
        self.log.update({'010C': (900.0, 'rpm')})        # still too soon
        self.now += 0.5
        self.log.update({'010C': (950.0, 'rpm')})        # a second has passed
        rows = self.rows()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][2:], ['950', '30'])     # the held back speed reading is in the next row

    def test_no_limit_writes_every_round(self):
        self.log.start(self.COLUMNS)
        for _ in range(5):
            self.log.update({'010C': (800.0, 'rpm')})
        self.assertEqual(len(self.rows()), 5)

    def test_the_recorder_turns_rows_per_second_into_an_interval(self):
        session = Session()
        session.demo_on = True
        recorder = Recorder(session, self.tmp.name, lambda: self.COLUMNS, rate=lambda: 5)
        recorder.start()
        self.assertAlmostEqual(recorder.logger.min_interval, 0.2)
        recorder.stop()


class HiddenPidTests(unittest.TestCase):
    def tearDown(self):
        pids.use_extras([])
        pids.MONITOR_PIDS[:] = pids.DEFAULT_MONITOR

    def profile(self):
        return next(p for p in profiles.built_in() if p.key == 'holden-ve')

    def test_hidden_pids_are_left_off_the_dashboard_but_stay_known(self):
        profile = self.profile()
        before = profiles.candidates(profile)
        gone = before[0]
        summary = profiles.activate(profile, user_hidden=[gone.lower()])
        self.assertNotIn(gone, pids.MONITOR_PIDS)
        self.assertIsNotNone(pids.get(gone))
        self.assertEqual(summary['turned_off'], 1)
        self.assertEqual(len(pids.MONITOR_PIDS), len(before) - 1)

    def test_nothing_hidden_changes_nothing(self):
        profile = self.profile()
        before = profiles.candidates(profile)
        profiles.activate(profile)
        self.assertEqual(pids.MONITOR_PIDS, before)

    def test_candidates_list_every_pid_before_the_car_check(self):
        profile = self.profile()
        self.assertTrue({'010C', '010D'} <= set(profiles.candidates(profile)))


if __name__ == '__main__':
    unittest.main()
