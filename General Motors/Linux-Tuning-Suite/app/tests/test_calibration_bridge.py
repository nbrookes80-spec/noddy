"""The AI snapshot includes the imported EFILive export summary, and leaves it out when none is loaded."""

import os
import tempfile
import unittest

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

from tunertoolpro import efilive_export  # noqa: E402

EXPORT = ('"EFILive Calibration Export"\r\n"File","Bridge test.csv"\r\n"Exported","Aug 15,2026","01:00:00"\r\n'
          '\r\nH0122,3.910034,Ratio,"Axle Ratio"\r\n')

try:
    from PyQt6.QtWidgets import QApplication
    HAVE_QT = True
except ImportError:  # pragma: no cover
    HAVE_QT = False


@unittest.skipUnless(HAVE_QT, 'PyQt6 not installed')
class CalibrationBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self._old = os.environ.get('TUNERTOOLPRO_HOME')
        self._tmp = tempfile.TemporaryDirectory()
        os.environ['TUNERTOOLPRO_HOME'] = self._tmp.name
        from tunertoolpro.gui.main_window import MainWindow
        self.window = MainWindow()
        self.vehicle = self.window.centralWidget().widget(1).widget()

    def tearDown(self):
        self.window.close()
        self._tmp.cleanup()
        if self._old is None:
            os.environ.pop('TUNERTOOLPRO_HOME', None)
        else:
            os.environ['TUNERTOOLPRO_HOME'] = self._old

    def test_no_export_means_no_text(self):
        self.assertIsNone(self.vehicle.calibration_text())
        self.assertEqual(self.window.ai_tab._bridge.snapshot()['calibration_export'], 'No EFILive export is loaded.')

    def test_loaded_export_reaches_the_snapshot(self):
        self.vehicle.calibration = efilive_export.parse(EXPORT)
        text = self.window.ai_tab._bridge.snapshot()['calibration_export']
        self.assertIn('H0122 Axle Ratio: 3.910034 Ratio', text)
        self.assertIn('Bridge test.csv', text)


if __name__ == '__main__':
    unittest.main()
