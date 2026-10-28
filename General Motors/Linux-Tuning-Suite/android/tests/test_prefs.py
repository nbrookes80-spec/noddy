import json
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
