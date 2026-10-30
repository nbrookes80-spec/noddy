import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import prefs  # noqa: E402


class PrefsTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(tempfile.mkdtemp()) / 'prefs.json'

    def test_a_first_run_defaults_to_bluetooth_and_the_usual_wifi_address(self):
        loaded = prefs.load(self.path)
        self.assertEqual(loaded['link_kind'], 'Bluetooth')
        self.assertEqual(loaded['bt_address'], '')
        self.assertEqual(loaded['wifi'], '192.168.0.10:35000')

    def test_what_was_saved_comes_back(self):
        prefs.save(self.path, {'link_kind': 'Wi-Fi', 'bt_address': '00:1d:a5:68:98:8b', 'wifi': '10.0.0.5:2000'})
        loaded = prefs.load(self.path)
        self.assertEqual((loaded['link_kind'], loaded['bt_address'], loaded['wifi']),
                         ('Wi-Fi', '00:1D:A5:68:98:8B', '10.0.0.5:2000'))

    def test_a_damaged_or_odd_file_falls_back_to_the_defaults(self):
        self.path.write_text('{not json')
        self.assertEqual(prefs.load(self.path)['link_kind'], 'Bluetooth')
        self.path.write_text(json.dumps({'link_kind': 'Carrier pigeon', 'bt_address': 'nope', 'wifi': 5, 'x': 1}))
        loaded = prefs.load(self.path)
        self.assertEqual((loaded['link_kind'], loaded['bt_address'], loaded['wifi']),
                         ('Bluetooth', '', '192.168.0.10:35000'))
        self.assertNotIn('x', loaded)

    def test_saving_to_a_place_that_cannot_be_written_does_not_crash(self):
        prefs.save(Path('/proc/nowhere/prefs.json'), {'link_kind': 'Wi-Fi'})


if __name__ == '__main__':
    unittest.main()


class AutoConnectPrefTests(unittest.TestCase):
    def test_the_auto_connect_choice_survives_saving_the_link(self):
        import tempfile
        from pathlib import Path as P
        path = P(tempfile.mkdtemp()) / 'prefs.json'
        prefs.save(path, dict(prefs.load(path), auto_connect=True))
        self.assertTrue(prefs.load(path)['auto_connect'])
        prefs.save(path, dict(prefs.load(path), link_kind='Wi-Fi'))
        self.assertTrue(prefs.load(path)['auto_connect'])


class MenuSettingsPrefTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.path = Path(self.folder, 'prefs.json')

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def test_menu_settings_default_to_off(self):
        result = prefs.load(self.path)
        self.assertFalse(result['live_transmission'])
        self.assertFalse(result['adaptive_timing'])
        self.assertEqual(result['timeout_ms'], 0)

    def test_menu_settings_round_trip(self):
        prefs.save(self.path, dict(prefs.DEFAULTS, live_transmission=True, adaptive_timing=True, timeout_ms=200))
        result = prefs.load(self.path)
        self.assertTrue(result['live_transmission'])
        self.assertTrue(result['adaptive_timing'])
        self.assertEqual(result['timeout_ms'], 200)

    def test_a_bad_timeout_or_flag_falls_back_to_the_default(self):
        self.path.write_text(json.dumps({'live_transmission': 'yes', 'adaptive_timing': 1, 'timeout_ms': 999}))
        result = prefs.load(self.path)
        self.assertFalse(result['live_transmission'])
        self.assertFalse(result['adaptive_timing'])
        self.assertEqual(result['timeout_ms'], 0)

    def test_the_chosen_scanner_profile_is_remembered(self):
        self.assertEqual(prefs.load(self.path)['scan_profile'], '')
        prefs.save(self.path, dict(prefs.DEFAULTS, scan_profile='holden-ve'))
        self.assertEqual(prefs.load(self.path)['scan_profile'], 'holden-ve')
        self.path.write_text(json.dumps({'scan_profile': 7}))
        self.assertEqual(prefs.load(self.path)['scan_profile'], '')
