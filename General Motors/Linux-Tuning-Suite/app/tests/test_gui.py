"""Offscreen GUI smoke tests. They build each tab and drive the main actions."""

import os
import unittest

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

try:
    from PyQt6.QtWidgets import QApplication
    HAVE_QT = True
except ImportError:  # pragma: no cover
    HAVE_QT = False


@unittest.skipUnless(HAVE_QT, 'PyQt6 not installed')
class GuiSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        from tunertoolpro.gui.main_window import MainWindow
        self.window = MainWindow()
        self.tabs = self.window.centralWidget()

    def tearDown(self):
        self.window.close()

    def test_all_tabs_present(self):
        names = [self.tabs.tabText(i) for i in range(self.tabs.count())]
        self.assertEqual(names, ['Shift Points', 'Pressure & Timing', 'Dyno & Drag',
                                 'Datalog', 'XDF / BIN', 'BCT Tunes'])

    def test_shift_calculate_fills_tables(self):
        tab = self.tabs.widget(0)
        tab.calculate()
        self.assertEqual(tab.tables['upshift'].columnCount(), 17)
        self.assertGreater(tab.tables['upshift'].rowCount(), 0)

    def test_pressure_tables_switch(self):
        tab = self.tabs.widget(1)
        tab.kind_box.setCurrentText('Shift time 4-speed')
        self.assertEqual((tab.table.rowCount(), tab.table.columnCount()), (3, 17))
        tab.kind_box.setCurrentText('TCC duty maximum')
        self.assertEqual((tab.table.rowCount(), tab.table.columnCount()), (5, 17))
        tab.kind_box.setCurrentText('Base shift pressure 4-speed')
        self.assertEqual((tab.table.rowCount(), tab.table.columnCount()), (3, 33))
        tab.kind_box.setCurrentText('TCC apply ramp')
        self.assertTrue(tab.era_box.isEnabled())
        tab.era_box.setCurrentText('2015+')
        self.assertEqual((tab.table.rowCount(), tab.table.columnCount()), (9, 17))
        self.assertFalse(tab.torque.isEnabled())

    def test_dyno_and_drag_with_synthetic_curve(self):
        from tunertoolpro.engines.torque_curve import TorqueCurve
        tab = self.tabs.widget(2)
        tab.curve = TorqueCurve([(1000, 150, 790), (3000, 280, 490), (5000, 320, 336),
                                 (6200, 300, 254)])
        tab.refresh_dyno()
        tab.run_drag()
        self.assertGreater(tab.drag_table.rowCount(), 0)

    def test_bct_tab_opens_tune_when_available(self):
        from tunertoolpro.bct.tune import BtcTune
        import glob
        bct_dir = os.environ.get('BCT_DIR', '/home/nathan/Downloads/BCT+1.42/Bluecat Transmission Tool')
        tunes = sorted(glob.glob(os.path.join(bct_dir, '*.BTC')))
        if not tunes:
            self.skipTest('no BC Trans tunes')
        tab = self.tabs.widget(5)
        tab.tune = BtcTune.load(tunes[0])
        tab._show_keys()
        tab.show_speeds()
        self.assertGreater(tab.speeds.rowCount(), 0)
        self.assertEqual(tab.speeds.columnCount(), tab.tune.gear_count())


if __name__ == '__main__':
    unittest.main()
