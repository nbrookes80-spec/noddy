import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import prefs  # noqa: E402
from scanner import calais, profiles  # noqa: E402
from tunertoolpro import core, vehicles  # noqa: E402
from tunertoolpro.engines import constants  # noqa: E402

EXPECTED_IDS = {'221564', '221171', '22114B', '221145', '221141', '2212C3', '2212C4',
                '221201', '221202', '221203', '221204', '2211F8', '2211F9', '2211FA', '2211FB', '22115C'}


class CalaisCarTests(unittest.TestCase):
    def setUp(self):
        self.folder = Path(tempfile.mkdtemp())
        self.cars = self.folder / 'cars'

    def test_the_car_is_saved_with_the_sixteen_missing_pids(self):
        saved = calais.ensure_car(str(self.cars))
        self.assertIsNotNone(saved)
        self.assertEqual(saved.key, calais.CAR_KEY)
        found, _rejected = profiles.load_pids(saved)
        self.assertEqual({p.pid.upper() for p in found}, EXPECTED_IDS)

    def test_the_car_is_only_saved_once(self):
        calais.ensure_car(str(self.cars))
        self.assertIsNone(calais.ensure_car(str(self.cars)))
        self.assertEqual(len(profiles.list_user(str(self.cars))), 1)

    def test_the_car_is_listed_under_its_name(self):
        calais.ensure_car(str(self.cars))
        names = [p.name for p in profiles.list_user(str(self.cars))]
        self.assertEqual(names, ['2011 Holden CALAIS TURBO'])


class CalaisVehicleTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(tempfile.mkdtemp()) / 'vehicle.json'

    def test_the_starter_profile_is_the_6l80_with_the_3_9_axle(self):
        calais.register_profile()
        profile = constants.STARTER_PROFILES[calais.PROFILE_NAME]
        self.assertEqual(profile['trans_name'], calais.CAR_TRANSMISSION)
        self.assertEqual(profile['axle'], 3.9)
        base = constants.STARTER_PROFILES[calais.BASE_PROFILE]
        self.assertEqual(base['axle'], 3.45)        # the profile it was copied from is untouched
        self.assertEqual({k: v for k, v in profile.items() if k != 'axle'},
                         {k: v for k, v in base.items() if k != 'axle'})

    def test_registering_twice_keeps_one_profile(self):
        calais.register_profile()
        calais.register_profile()
        self.assertEqual(core.profile_names().count(calais.PROFILE_NAME), 1)

    def test_a_new_install_gets_the_calais_turbo_vehicle(self):
        self.assertTrue(calais.ensure_vehicle(self.path))
        self.assertEqual(vehicles.load(self.path),
                         {'make': 'Holden', 'transmission': '6L80 (2006-Current)', 'profile': calais.PROFILE_NAME})

    def test_a_vehicle_already_chosen_is_not_replaced(self):
        vehicles.save(self.path, {'make': 'GM', 'transmission': '4L60E (1993-2013)', 'profile': ''})
        self.assertFalse(calais.ensure_vehicle(self.path))
        self.assertEqual(vehicles.load(self.path)['transmission'], '4L60E (1993-2013)')

    def test_the_calais_vehicle_is_kept_after_the_owner_changes_the_axle(self):
        calais.ensure_vehicle(self.path)
        self.assertFalse(calais.ensure_vehicle(self.path))      # a second start does nothing

    def test_a_folder_that_cannot_be_written_does_not_stop_the_start(self):
        blocked = Path(tempfile.mkdtemp()) / 'a-file'
        blocked.write_text('not a folder')
        calais.ensure_vehicle(blocked / 'vehicle.json')         # vehicles.save ignores a place it cannot write


class StartSettingsTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(tempfile.mkdtemp()) / 'prefs.json'

    def test_a_first_run_gets_the_start_settings(self):
        loaded = prefs.load(self.path)
        self.assertTrue(loaded['live_transmission'])
        self.assertEqual(loaded['scan_profile'], calais.CAR_KEY)
        self.assertTrue(loaded['intro_music'])

    def test_an_old_file_gets_the_start_settings_once(self):
        self.path.write_text(json.dumps({'live_transmission': False, 'scan_profile': 'holden-ve'}))
        loaded = prefs.load(self.path)
        self.assertTrue(loaded['live_transmission'])
        self.assertEqual(loaded['scan_profile'], calais.CAR_KEY)
        self.assertTrue(loaded['intro_music'])
        self.assertEqual(loaded['settings_version'], prefs.SETTINGS_VERSION)

    def test_a_current_file_keeps_the_owners_own_choices(self):
        saved = dict(prefs.DEFAULTS, live_transmission=False, scan_profile='holden-ve', intro_music=False)
        prefs.save(self.path, saved)
        loaded = prefs.load(self.path)
        self.assertFalse(loaded['live_transmission'])
        self.assertEqual(loaded['scan_profile'], 'holden-ve')
        self.assertFalse(loaded['intro_music'])

    def test_intro_music_must_be_a_real_yes_or_no(self):
        self.path.write_text(json.dumps({'settings_version': prefs.SETTINGS_VERSION, 'intro_music': 'yes'}))
        self.assertTrue(prefs.load(self.path)['intro_music'])


if __name__ == '__main__':
    unittest.main()
