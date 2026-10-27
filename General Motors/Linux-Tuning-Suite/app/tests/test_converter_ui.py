"""The Shift tab's converter and differential pickers, driven offscreen."""

import os
import unittest

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

try:
    from PyQt6.QtWidgets import QApplication
    HAVE_QT = True
except ImportError:  # pragma: no cover
    HAVE_QT = False


@unittest.skipUnless(HAVE_QT, 'PyQt6 not installed')
class ConverterPickerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        from tunertoolpro.gui.shift_tab import ShiftTab
        self.tab = ShiftTab()

    def test_high_stall_moves_the_four_inputs_and_turns_stall_logic_on(self):
        before = {k: self.tab.value(k) for k in ('stall_rpm', 'idle_rpm', 'shift_rpm', 'min_tcc_rpm')}
        self.tab.converter_box.setCurrentText('High stall, single plate')
        after = {k: self.tab.value(k) for k in before}
        self.assertGreater(after['stall_rpm'], before['stall_rpm'])
        self.assertEqual(after['idle_rpm'], before['idle_rpm'] + 100)
        self.assertEqual(after['shift_rpm'], before['shift_rpm'] + 200)
        self.assertEqual(self.tab.stall_logic.currentIndex(), 1)

    def test_going_back_to_stock_restores_the_numbers(self):
        before = {k: self.tab.value(k) for k in ('stall_rpm', 'idle_rpm', 'shift_rpm', 'min_tcc_rpm')}
        self.tab.converter_box.setCurrentText('High stall, triple plate')
        self.tab.converter_box.setCurrentText('Stock')
        self.assertEqual({k: self.tab.value(k) for k in before}, before)
        self.assertEqual(self.tab.stall_logic.currentIndex(), 0)

    def test_a_typed_stall_is_used(self):
        self.tab.set_value('stall_rpm', 3100)
        self.tab.converter_box.setCurrentText('Other / custom')
        self.assertEqual(self.tab.value('stall_rpm'), 3100)

    def test_notes_list_the_tcm_settings(self):
        self.tab.converter_box.setCurrentText('High stall, single plate')
        self.assertIn('TCC Desired Slip', self.tab.advice.toPlainText())

    def test_diff_preset_sets_the_axle_and_reports_the_change(self):
        self.tab.diff_box.setCurrentText('3.73')
        self.tab._diff_picked()
        self.assertAlmostEqual(self.tab.value('axle'), 3.73)
        self.assertIn('3.73', self.tab.advice.toPlainText())

    def test_typing_an_axle_not_in_the_list_adds_it(self):
        self.tab.set_value('axle', 3.31)
        items = [self.tab.diff_box.itemText(i) for i in range(self.tab.diff_box.count())]
        self.assertIn('3.31', items)

    def test_calculation_still_runs_after_a_converter_change(self):
        self.tab.converter_box.setCurrentText('High stall, single plate')
        self.tab.calculate()
        self.assertIsNotNone(self.tab._tables_data)


if __name__ == '__main__':
    unittest.main()
