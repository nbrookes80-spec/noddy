"""Offscreen GUI smoke tests. They build each tab and drive the main actions."""

import os
import unittest


def tab_page(tabs, index):
    """The tab's own widget, even when the window wraps it in a scroll area."""
    from tunertoolpro.gui.main_window import tab_page as page_of
    return page_of(tabs, index)

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
        self.assertEqual(names, ['Shift Points', 'Vehicle', 'Pressure & Timing', 'Dyno & Drag',
                                 'Datalog', 'XDF / BIN', 'BCT Tunes', 'CAN Sniffer', 'AI Assistant'])

    def test_shift_calculate_fills_tables(self):
        tab = tab_page(self.tabs, 0)
        tab.calculate()
        self.assertEqual(tab.tables['upshift'].columnCount(), 17)
        self.assertGreater(tab.tables['upshift'].rowCount(), 0)

    def _bct_path(self, name):
        bct_dir = os.environ.get('BCT_DIR', '/home/nathan/Downloads/BCT+1.42/Bluecat Transmission Tool')
        path = os.path.join(bct_dir, name)
        if not os.path.exists(path):
            self.skipTest('BC Trans tune not present')
        return path

    def test_shift_engine_selector_switches_tables_source(self):
        from unittest import mock
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        from tunertoolpro import core
        from tunertoolpro.bct.calc_shifts import calc_shifts
        from tunertoolpro.bct.tune import BtcTune
        path = self._bct_path('(Base)2012_C6_6L80_Boltons.BTC')
        tab = tab_page(self.tabs, 0)
        with mock.patch.object(QMessageBox, 'warning') as warn:
            tab.engine_box.setCurrentText(core.ENGINE_BC)
            self.assertFalse(tab.form_box.isEnabled())
            tab.calculate()                      # no tune loaded yet
            self.assertEqual(warn.call_count, 1)
        with mock.patch.object(QFileDialog, 'getOpenFileName', return_value=(path, '')):
            tab.load_btc()
        self.assertTrue(tab.form_box.isEnabled() is False)  # still BC Trans mode
        tab.calculate()
        expected = calc_shifts(BtcTune.load(path)).upshift
        self.assertEqual(tab.tables['upshift'].rowCount(), len(expected))
        self.assertEqual(tab.tables['upshift'].columnCount(), 17)
        self.assertEqual(tab.tables['upshift'].item(0, 0).text(), f'{expected[0][0]:.1f}')
        self.assertIn('converged', tab.calc_note.text())
        # Back to CalcEngine: the form is editable and the BC tables are not used.
        tab.engine_box.setCurrentText(core.ENGINE_CALC)
        self.assertTrue(tab.form_box.isEnabled())
        tab.calculate()
        self.assertIsNotNone(tab._tables_data)
        self.assertNotIn('converged', tab.calc_note.text())

    def test_bc_engine_export_text_uses_bc_tables(self):
        from unittest import mock
        from PyQt6.QtWidgets import QFileDialog
        from tunertoolpro import core
        path = self._bct_path('(Base)2016_F_8L90_Boltons.BTC')
        tab = tab_page(self.tabs, 0)
        with mock.patch.object(QFileDialog, 'getOpenFileName', return_value=(path, '')):
            tab.load_btc()
        tab.engine_box.setCurrentText(core.ENGINE_BC)
        tab.calculate()
        text = core.tps_gear_text(tab._tables_data)
        self.assertIn('Upshift MPH', text)
        self.assertIn('TCC lock MPH', text)
        self.assertEqual(tab._tables_data['n_gears'], 8)

    def test_pressure_tables_switch(self):
        tab = tab_page(self.tabs, 2)
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
        tab = tab_page(self.tabs, 3)
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
        tab = tab_page(self.tabs, 6)
        tab.tune = BtcTune.load(tunes[0])
        tab._show_keys()
        tab.show_speeds()
        self.assertGreater(tab.speeds.rowCount(), 0)
        self.assertEqual(tab.speeds.columnCount(), tab.tune.gear_count())


if __name__ == '__main__':
    unittest.main()


@unittest.skipUnless(HAVE_QT, 'PyQt6 not installed')
class WindowFitsSmallScreenTests(unittest.TestCase):
    """Regression: the window once needed 1551x892, which cannot fit a 1366x768 screen."""

    @classmethod
    def setUpClass(cls):
        from tunertoolpro.gui import theme
        cls.app = QApplication.instance() or QApplication([])
        theme.apply(cls.app)  # the app runs with the theme; fonts and padding change the sizes

    def test_minimum_size_fits_a_1366_by_768_screen(self):
        from tunertoolpro.gui.main_window import MainWindow
        window = MainWindow()
        window.show()  # layout is only computed once the window is shown, as in the app
        self.app.processEvents()
        hint = window.minimumSizeHint()
        self.assertLessEqual(hint.width(), 1366)
        self.assertLessEqual(hint.height(), 768)
        window.close()

    def test_default_size_is_clamped_to_the_screen(self):
        from tunertoolpro.gui.main_window import fit_to_screen
        from PyQt6.QtWidgets import QMainWindow
        window = QMainWindow()
        fit_to_screen(window, 4000, 3000)
        available = self.app.primaryScreen().availableGeometry()
        self.assertLessEqual(window.width(), available.width())
        self.assertLessEqual(window.height(), available.height())
