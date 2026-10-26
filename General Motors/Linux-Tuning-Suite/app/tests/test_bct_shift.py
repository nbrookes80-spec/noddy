"""BC Trans tune to Shift Points tab mapping, against the shipped .BTC files."""

import glob
import math
import os
import unittest
from unittest import mock

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

from tunertoolpro.bct.shift_cfg import shift_cfg_from_btc
from tunertoolpro.bct.tune import BtcTune
from tunertoolpro.engines.calc_engine import CalcEngine

BCT_DIR = os.environ.get(
    'BCT_DIR', '/home/nathan/Downloads/BCT+1.42/Bluecat Transmission Tool')
TUNES = sorted(glob.glob(os.path.join(BCT_DIR, '*.BTC')))
SIX_SPEED = os.path.join(BCT_DIR, '(Base)2012_C6_6L80_Boltons.BTC')


def _flatten(value):
    if isinstance(value, (list, tuple)):
        for item in value:
            yield from _flatten(item)
    else:
        yield value


@unittest.skipUnless(TUNES, 'BC Trans folder not present (set BCT_DIR)')
class BtcShiftMappingTests(unittest.TestCase):
    def test_six_speed_tune_maps_to_expected_values(self):
        cfg = shift_cfg_from_btc(BtcTune.load(SIX_SPEED))
        self.assertEqual(cfg['ratios'], [4.03, 2.36, 1.53, 1.15, 0.85, 0.67])
        self.assertEqual(cfg['axle'], 2.73)     # Gear is the final drive
        self.assertEqual(cfg['chain'], 1.0)
        self.assertEqual(cfg['tire_dia'], 26.15)
        self.assertEqual((cfg['idle_rpm'], cfg['stall_rpm']), (550, 2000))
        self.assertEqual(cfg['downshift_rpm'], 9900)
        self.assertEqual(cfg['per_gear_rpm'], [6400.0] * 6)
        self.assertEqual(cfg['shift_rpm'], 6400)
        self.assertEqual(cfg['min_tcc_rpm'], 1250)   # TCC_MinRpm, not the MinLockRPM grid cell
        self.assertEqual((cfg['min_tcc_gear'], cfg['accel_lock_gear'], cfg['wot_lock_gear']),
                         (3, 3, 3))
        self.assertEqual(cfg['lead_mode'], 'torque')  # AdvancedLead = 1
        self.assertEqual(cfg['lead_value'], 2.5)
        self.assertEqual((cfg['spread_up'], cfg['spread_lock'],
                          cfg['spread_lock_up'], cfg['spread_unlock_dn']), (3, 2, 4, 1))
        self.assertTrue(cfg['stall_lock_logic'])     # StallLogic = 1
        self.assertEqual((cfg['weight'], cfg['rwhp'], cfg['down_time']), (3300, 380, 0.5))
        self.assertEqual((cfg['tps_factor'], cfg['tps_offset']), (1.3, 10))
        self.assertEqual((cfg['up_firmness'], cfg['down_firmness']), (5, 5))

    def test_delays_are_prep_and_react_pairs(self):
        cfg = shift_cfg_from_btc(BtcTune.load(SIX_SPEED))
        self.assertEqual(len(cfg['delays']), 5)      # one pair per shift; top gear has none
        self.assertEqual(cfg['delays'][0], (0.45, 0.15))

    def test_rpm_lead_when_advanced_lead_is_zero(self):
        tune = BtcTune.load(SIX_SPEED)
        tune.set('AdvancedLead', '0')
        self.assertEqual(shift_cfg_from_btc(tune)['lead_mode'], 'rpm')

    def test_every_tune_maps_and_calculates(self):
        for path in TUNES:
            with self.subTest(tune=os.path.basename(path)):
                tune = BtcTune.load(path)
                n = tune.gear_count()
                cfg = shift_cfg_from_btc(tune)
                self.assertEqual(len(cfg['ratios']), n)
                self.assertEqual(len(cfg['per_gear_rpm']), n)
                self.assertEqual(len(cfg['delays']), n - 1)
                tables = CalcEngine.calculate(cfg)
                values = list(_flatten([tables['upshift'], tables['downshift'],
                                        tables['tcc_unlock'], tables['tcc_lock']]))
                self.assertTrue(values)
                self.assertTrue(all(math.isfinite(v) for v in values))

    def test_mapping_does_not_change_the_tune(self):
        tune = BtcTune.load(SIX_SPEED)
        before = tune.to_text()
        shift_cfg_from_btc(tune)
        self.assertEqual(tune.to_text(), before)

    def test_missing_key_is_named_in_the_error(self):
        tune = BtcTune.load(SIX_SPEED)
        pairs = [(k, v) for k, v in tune.pairs() if k != 'Prep1']
        with self.assertRaises(ValueError) as ctx:
            shift_cfg_from_btc(BtcTune(pairs))
        self.assertIn('Prep1', str(ctx.exception))


try:
    from PyQt6.QtWidgets import QApplication
    from tunertoolpro import core
    HAVE_QT = True
except ImportError:  # pragma: no cover
    HAVE_QT = False


@unittest.skipUnless(HAVE_QT and TUNES, 'PyQt6 or BC Trans folder not present')
class ShiftTabBtcTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_load_btc_fills_form_and_keeps_per_shift_data(self):
        from tunertoolpro.gui.shift_tab import ShiftTab
        tab = ShiftTab()
        with mock.patch('tunertoolpro.gui.shift_tab.QFileDialog.getOpenFileName',
                        return_value=(SIX_SPEED, '')):
            tab.load_btc()
        self.assertEqual(tab.intent_box.currentText(), core.CUSTOM_INTENT)
        self.assertEqual(tab.ratios.text(), '4.03, 2.36, 1.53, 1.15, 0.85, 0.67')
        self.assertEqual(tab._widgets['axle'].value(), 2.73)
        self.assertEqual(tab.lead_box.currentText(), 'torque')
        cfg = tab.build_cfg()
        self.assertEqual(cfg['delays'][0], (0.45, 0.15))
        self.assertEqual(cfg['per_gear_rpm'], [6400.0] * 6)
        tab.calculate()
        self.assertEqual(tab.tables['upshift'].rowCount(), 5)

    def test_changing_profile_clears_the_tune_data(self):
        from tunertoolpro.gui.shift_tab import ShiftTab
        tab = ShiftTab()
        with mock.patch('tunertoolpro.gui.shift_tab.QFileDialog.getOpenFileName',
                        return_value=(SIX_SPEED, '')):
            tab.load_btc()
        tab.load_profile()
        cfg = tab.build_cfg()
        self.assertNotIn('per_gear_rpm', cfg)
        self.assertEqual(cfg['delays'][0], core.DEFAULT_DELAY)


if __name__ == '__main__':
    unittest.main()
