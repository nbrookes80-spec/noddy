import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from link.devices import normalise_address, rank_devices  # noqa: E402


class AddressTests(unittest.TestCase):
    def test_accepts_the_usual_spellings_of_a_bluetooth_address(self):
        self.assertEqual(normalise_address('00:1d:a5:68:98:8b'), '00:1D:A5:68:98:8B')
        self.assertEqual(normalise_address(' 00-1D-A5-68-98-8B '), '00:1D:A5:68:98:8B')
        self.assertEqual(normalise_address('001DA568988B'), '00:1D:A5:68:98:8B')

    def test_refuses_anything_that_is_not_an_address(self):
        for bad in ('', 'OBDII', '00:1D:A5:68:98', '00:1D:A5:68:98:8B:FF', '00:1D:A5:68:98:ZZ', None):
            self.assertIsNone(normalise_address(bad), bad)


class RankingTests(unittest.TestCase):
    def test_scan_adapters_come_before_headphones_and_watches(self):
        paired = [('JBL Flip 5', '11:22:33:44:55:66'), ('OBDII', '00:1D:A5:68:98:8B'),
                  ('Galaxy Watch', 'AA:BB:CC:DD:EE:FF'), ('Veepeak OBDCheck BLE', '10:21:3E:00:00:01'),
                  ('V-LINK', '66:12:34:56:78:9A')]
        names = [d['name'] for d in rank_devices(paired)]
        self.assertEqual(set(names[:3]), {'OBDII', 'Veepeak OBDCheck BLE', 'V-LINK'})
        self.assertEqual(set(names[3:]), {'JBL Flip 5', 'Galaxy Watch'})

    def test_each_entry_says_whether_it_looks_like_a_scan_adapter(self):
        ranked = rank_devices([('Car Stereo', '11:22:33:44:55:66'), ('ELM327', '00:1D:A5:68:98:8B')])
        self.assertTrue(ranked[0]['likely'])
        self.assertFalse(ranked[1]['likely'])
        self.assertEqual(ranked[0]['address'], '00:1D:A5:68:98:8B')

    def test_duplicates_and_bad_addresses_are_dropped_and_blank_names_filled(self):
        ranked = rank_devices([('OBDII', '00:1d:a5:68:98:8b'), ('OBDII', '00:1D:A5:68:98:8B'),
                               ('Broken', 'nope'), (None, '12:34:56:78:9A:BC')])
        self.assertEqual([d['address'] for d in ranked], ['00:1D:A5:68:98:8B', '12:34:56:78:9A:BC'])
        self.assertEqual(ranked[1]['name'], 'Unnamed device')

    def test_nothing_paired_gives_an_empty_list(self):
        self.assertEqual(rank_devices([]), [])


if __name__ == '__main__':
    unittest.main()
