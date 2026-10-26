"""BC Trans data-format tests against the shipped tune and preset files."""

import glob
import os
import unittest

from tunertoolpro.bct import shiftmath
from tunertoolpro.bct.presets import load_table, transmission_ratios
from tunertoolpro.bct.tune import BtcTune

BCT_DIR = os.environ.get(
    'BCT_DIR', '/home/nathan/Downloads/BCT+1.42/Bluecat Transmission Tool')
TUNES = sorted(glob.glob(os.path.join(BCT_DIR, '*.BTC')))


@unittest.skipUnless(TUNES, 'BC Trans folder not present (set BCT_DIR)')
class TuneFileTests(unittest.TestCase):
    def test_all_tunes_round_trip_byte_for_byte(self):
        for path in TUNES:
            with self.subTest(path=os.path.basename(path)):
                with open(path, 'rb') as fh:
                    original = fh.read().decode('latin-1')
                self.assertEqual(BtcTune.load(path).to_text(), original)

    def test_all_tunes_have_required_keys_and_matching_gear_count(self):
        for path in TUNES:
            with self.subTest(path=os.path.basename(path)):
                tune = BtcTune.load(path)
                self.assertEqual(tune.missing_required(), [])
                self.assertEqual(len(tune.ratios()), tune.gear_count())
                self.assertNotIn(None, tune.ratios())

    def test_set_then_save_round_trip(self):
        import tempfile
        tune = BtcTune.load(TUNES[0])
        tune.set('Idle', '600')
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, 'edited.BTC')
            tune.save(out)
            again = BtcTune.load(out)
        self.assertEqual(again.getint('Idle'), 600)
        self.assertEqual(again.to_text().count('\r\n'), len(again.pairs()) * 2)


@unittest.skipUnless(os.path.exists(os.path.join(BCT_DIR, 'Trans_Presets.txt')),
                     'BC Trans presets not present')
class PresetTests(unittest.TestCase):
    def test_trans_presets(self):
        rows = load_table(os.path.join(BCT_DIR, 'Trans_Presets.txt'))
        self.assertEqual(len(rows), 5)
        self.assertTrue(all(transmission_ratios(r) for r in rows))

    def test_slope_presets(self):
        rows = load_table(os.path.join(BCT_DIR, 'Slope_Presets.txt'))
        self.assertEqual(len(rows), 13)
        self.assertEqual(rows[0]['Name'], '78-85mm Cable TB')
        self.assertEqual(rows[0]['Factor'], 1.35)


class ShiftMathTests(unittest.TestCase):
    def test_speed_uses_literal_pi_314(self):
        # 2000 rpm, ratio 1, final 1, 26 in tire: 2000 / 1 * 26 * 3.14 * 60 / 12 / 5280
        expected = 2000 * 26 * 3.14 * 60 / 12 / 5280
        self.assertAlmostEqual(shiftmath.speed_mph(2000, 1.0, 1.0, 26.0), expected)

    def test_speed_and_rpm_are_inverse(self):
        mph = shiftmath.speed_mph(3000, 3.06, 3.15, 26)
        self.assertAlmostEqual(shiftmath.rpm_for_speed(mph, 3.06, 3.15, 26), 3000)

    def test_stall_slip(self):
        self.assertAlmostEqual(shiftmath.stall_slip(2000), (2.0 ** 1.7) / 100)


if __name__ == '__main__':
    unittest.main()
