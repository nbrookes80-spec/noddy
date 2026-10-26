"""Offscreen tests for the Vehicle tab, the AI proposal flow and the settings bridge.

The settings folder is a temporary directory, so these tests never touch the user's real files.
"""

import json
import os
import tempfile
import unittest

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

try:
    from PyQt6.QtWidgets import QApplication
    HAVE_QT = True
except ImportError:  # pragma: no cover
    HAVE_QT = False


@unittest.skipUnless(HAVE_QT, 'PyQt6 not installed')
class VehicleAiGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self._old_home = os.environ.get('TUNERTOOLPRO_HOME')
        self._tmp = tempfile.TemporaryDirectory()
        os.environ['TUNERTOOLPRO_HOME'] = self._tmp.name
        from tunertoolpro.gui.main_window import MainWindow
        self.window = MainWindow()
        self.shift = self.window.centralWidget().widget(0)
        self.vehicle = self.window.centralWidget().widget(1)
        self.ai = self.window.ai_tab

    def tearDown(self):
        self.window.close()
        self._tmp.cleanup()
        if self._old_home is None:
            os.environ.pop('TUNERTOOLPRO_HOME', None)
        else:
            os.environ['TUNERTOOLPRO_HOME'] = self._old_home

    def _bridge(self):
        from tunertoolpro.gui.ai_tab import SettingsBridge
        return SettingsBridge(self.shift, self.vehicle)

    def test_tab_order(self):
        names = [self.window.centralWidget().tabText(i) for i in range(self.window.centralWidget().count())]
        self.assertEqual(names[:2], ['Shift Points', 'Vehicle'])
        self.assertEqual(names[-1], 'AI Assistant')

    def test_check_shows_findings_for_default_profile(self):
        self.vehicle.check()
        self.assertTrue(self.vehicle.status.text())

    def test_save_copies_tire_axle_and_weight_to_shift_tab(self):
        self.vehicle.final_drive.setValue(3.42)
        self.vehicle.tire.setValue(30.0)
        self.vehicle.weight.setValue(3800)
        self.vehicle.save()
        self.assertAlmostEqual(self.shift.value('axle'), 3.42, places=2)
        self.assertAlmostEqual(self.shift.value('tire_dia'), 30.0, places=2)
        self.assertEqual(self.shift.value('weight'), 3800)
        self.assertTrue(os.path.exists(os.path.join(self._tmp.name, 'vehicle.json')))

    def test_bridge_names_are_unique_and_routed(self):
        bridge = self._bridge()
        bounds = bridge.bounds()
        self.assertIn('shift_rpm', bounds)
        self.assertIn('vehicle.redline_rpm', bounds)
        # Tire, final drive and weight belong to the Shift Points tab only.
        self.assertNotIn('vehicle.final_drive', bounds)
        self.assertNotIn('vehicle.tire_dia', bounds)
        self.assertTrue(bridge.apply('shift_rpm', 6400))
        self.assertEqual(self.shift.value('shift_rpm'), 6400)
        self.assertTrue(bridge.apply('vehicle.redline_rpm', 6500))
        self.assertEqual(self.vehicle.spins()['redline_rpm'].value(), 6500)
        self.assertFalse(bridge.apply('vehicle.final_drive', 3.0))
        self.assertFalse(bridge.apply('no_such_setting', 1))

    def test_snapshot_is_json_serialisable(self):
        snap = self._bridge().snapshot()
        text = json.dumps(snap, default=str)
        self.assertIn('shift_inputs', text)
        self.assertIsInstance(snap['shift_inputs'], dict)

    def test_proposal_rows_show_questions_and_apply(self):
        proposal = {'field': 'shift_rpm', 'value': 6400.0, 'reason': 'Keep under the redline.'}
        self.ai._show_answer(('Use 6400.', [proposal], ['How many gears does the car have?']))
        self.assertEqual(self.ai.proposals.rowCount(), 1)
        self.assertIn('How many gears', self.ai.answer.toPlainText())
        holder = self.ai.proposals.cellWidget(0, 4)
        holder.layout().itemAt(0).widget().click()  # Apply
        self.assertEqual(self.shift.value('shift_rpm'), 6400)
        self.assertEqual(self.ai.proposals.item(0, 4).text(), 'Applied')

    def test_rejected_proposal_changes_nothing(self):
        before = self.shift.value('shift_rpm')
        proposal = {'field': 'shift_rpm', 'value': 7000.0, 'reason': 'Try higher.'}
        self.ai._show_answer(('Maybe.', [proposal], []))
        self.ai.proposals.cellWidget(0, 4).layout().itemAt(1).widget().click()  # Reject
        self.assertEqual(self.shift.value('shift_rpm'), before)
        self.assertEqual(self.ai.proposals.item(0, 4).text(), 'Rejected')


if __name__ == '__main__':
    unittest.main()
