import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import gmlan  # noqa: E402
from tunertoolpro.canbus import Frame, Sniffer  # noqa: E402


class GearTests(unittest.TestCase):
    def test_each_readme_example_decodes_to_its_gear(self):
        for payload, gear in (('0F0F000100000300', 'Park'), ('0F0F000200000300', 'Reverse'),
                              ('0F0F000300000300', 'Neutral'), ('0F0F000400000300', 'Drive')):
            with self.subTest(gear=gear):
                self.assertEqual(gmlan.decode(0x1F5, bytes.fromhex(payload)), {'gear': gear})

    def test_the_park_frame_from_the_capture_decodes(self):
        # 199 times in GMLAN data capture 1.csv
        self.assertEqual(gmlan.decode(0x1F5, bytes.fromhex('0F0F000100000300')), {'gear': 'Park'})

    def test_other_1f5_layouts_are_not_decoded(self):
        # 0101000400000900 is the most common 1F5 frame in the capture; its layout is not confirmed
        for payload in ('0101000400000900', '0E0D002200000300', '0F0F002100000300', '0F0F000100000800'):
            with self.subTest(payload=payload):
                self.assertEqual(gmlan.decode(0x1F5, bytes.fromhex(payload)), {})

    def test_the_same_payload_on_another_id_is_not_decoded(self):
        self.assertEqual(gmlan.decode(0x1F6, bytes.fromhex('0F0F000100000300')), {})


class ReadingsTests(unittest.TestCase):
    def test_the_gear_follows_the_latest_1f5_frame(self):
        sniffer = Sniffer()
        sniffer.feed([Frame(0x1F5, bytes.fromhex('0F0F000100000300'), False, 0.0)])
        self.assertEqual(gmlan.readings(sniffer.items), {'gear': 'Park'})
        sniffer.feed([Frame(0x1F5, bytes.fromhex('0F0F000400000300'), False, 0.1)])
        self.assertEqual(gmlan.readings(sniffer.items), {'gear': 'Drive'})

    def test_no_frames_means_no_readings(self):
        self.assertEqual(gmlan.readings(Sniffer().items), {})

    def test_an_unknown_1f5_frame_leaves_no_gear(self):
        sniffer = Sniffer()
        sniffer.feed([Frame(0x1F5, bytes.fromhex('0101000400000900'), False, 0.0)])
        self.assertEqual(gmlan.readings(sniffer.items), {})


if __name__ == '__main__':
    unittest.main()
