"""The CAN Sniffer tab, driven offscreen with a fake clock and a fake adapter."""

import os
import tempfile
import unittest
from unittest import mock

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

try:
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QApplication
    HAVE_QT = True
except ImportError:  # pragma: no cover
    HAVE_QT = False

from tunertoolpro.canbus import Frame, read_log


class Clock:
    def __init__(self):
        self.now = 50.0

    def __call__(self):
        return self.now


class FakeAdapter:
    """Stands in for TcpTransport: answers OK to commands and hands over one block of monitor text."""

    instances = []

    def __init__(self, *args, **kwargs):
        self.sent = []
        self.chunks = [b'7E8 06 41 0C 1A F8 00 00 00\r7E8 06 41 0C 1B 00 00 00 00\r']
        self.closed = False
        FakeAdapter.instances.append(self)

    def open(self):
        pass

    def write(self, data):
        self.sent.append(data)

    def read_until(self, prompt=b'>'):
        return b'OK\r'

    def read_chunk(self, timeout=0.2):
        if self.chunks:
            return self.chunks.pop(0)
        import time
        time.sleep(min(timeout, 0.02))
        return b''

    def close(self):
        self.closed = True


@unittest.skipUnless(HAVE_QT, 'PyQt6 not installed')
class SnifferTabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        from tunertoolpro.gui.sniffer_tab import SnifferTab
        self.clock = Clock()
        self.tab = SnifferTab(clock=self.clock)

    def tearDown(self):
        self.tab.shutdown()

    def cell(self, r, c):
        return self.tab.table.item(r, c)

    def test_starts_stopped_with_the_simulated_bus_selected(self):
        self.assertEqual(self.tab.source_name, 'Simulated bus')
        self.assertFalse(self.tab.running)
        self.assertEqual(self.tab.start_btn.text(), 'Start')

    def test_simulated_bus_fills_the_table_and_stop_halts_it(self):
        self.tab.start()
        self.assertTrue(self.tab.running)
        self.assertEqual(self.tab.start_btn.text(), 'Stop')
        for _ in range(10):
            self.clock.now += 0.2
            self.tab.poll()
            self.tab.refresh()
        self.assertEqual(self.tab.table.rowCount(), 5)
        self.assertEqual(self.cell(0, 0).text(), '0x0C9')
        self.assertEqual(self.tab.id_list.count(), 5)
        self.tab.stop()
        self.assertFalse(self.tab.running)
        self.assertEqual(self.tab.start_btn.text(), 'Start')

    def test_changing_byte_is_coloured_and_idle_one_is_not(self):
        self.tab.feed([Frame(0x100, bytes([1, 5]))])
        self.tab.feed([Frame(0x100, bytes([2, 5]))])
        self.tab.sniffer.tick_notch()
        self.tab.refresh()
        self.assertNotEqual(self.cell(0, 3).background().style(), Qt.BrushStyle.NoBrush)   # byte 0 went up
        self.assertEqual(self.cell(0, 4).background().style(), Qt.BrushStyle.NoBrush)   # byte 1 did not move
        self.assertEqual(self.cell(0, 3).text(), '02')
        self.assertEqual(self.cell(0, 5).text(), '')                       # past the frame length

    def test_unchecking_an_id_hides_its_row(self):
        self.tab.feed([Frame(0x100, b'\x01'), Frame(0x200, b'\x01')])
        self.tab.refresh()
        self.assertEqual(self.tab.table.rowCount(), 2)
        self.tab.id_list.item(0).setCheckState(Qt.CheckState.Unchecked)
        self.tab.refresh()
        self.assertEqual(self.tab.table.rowCount(), 1)
        self.assertEqual(self.cell(0, 0).text(), '0x200')
        self.tab._hide_all()
        self.tab.refresh()
        self.assertEqual(self.tab.table.rowCount(), 0)
        self.tab._show_all()
        self.tab.refresh()
        self.assertEqual(self.tab.table.rowCount(), 2)

    def test_expired_ids_leave_the_table_and_the_list(self):
        self.tab.feed([Frame(0x100, b'\x01')])
        self.tab.refresh()
        self.clock.now += 6
        self.tab.refresh()
        self.assertEqual(self.tab.table.rowCount(), 0)
        self.assertEqual(self.tab.id_list.count(), 0)

    def test_option_checkboxes_reach_the_sniffer(self):
        self.tab.never_expire.setChecked(True)
        self.tab.mute.setChecked(True)
        self.tab.fade.setChecked(True)
        self.tab.expire_spin.setValue(9)
        s = self.tab.sniffer
        self.assertEqual((s.never_expire, s.mute_notched, s.fade_inactive, s.expire_seconds), (True, True, True, 9.0))

    def test_bits_view_switches_the_delegate_and_back(self):
        self.tab.view_bits.setChecked(True)
        self.assertIs(self.tab.table.itemDelegateForColumn(3), self.tab.bits_delegate)
        self.tab.view_bits.setChecked(False)
        self.assertIsNot(self.tab.table.itemDelegateForColumn(3), self.tab.bits_delegate)

    def test_adapter_source_listens_and_hands_the_adapter_back(self):
        FakeAdapter.instances.clear()
        self.tab.source_box.setCurrentIndex(2)
        with mock.patch('tunertoolpro.gui.sniffer_tab.TcpTransport', FakeAdapter):
            self.tab.start()
            self.assertTrue(self.tab.running)
            for _ in range(50):
                self.tab.poll()
                if self.tab.sniffer.frames_seen:
                    break
                import time
                time.sleep(0.02)
            self.tab.stop()
        self.assertEqual(self.tab.sniffer.frames_seen, 2)
        adapter = FakeAdapter.instances[0]
        sent = [s.decode().strip() for s in adapter.sent]
        self.assertIn('ATMA', sent)
        self.assertEqual(sent[-1], 'ATSP0')                  # handed back as the OBD link expects
        self.assertTrue(adapter.closed)
        self.assertFalse(self.tab.running)

    def test_adapter_rejects_a_bad_filter_without_leaving_it_open(self):
        FakeAdapter.instances.clear()
        self.tab.source_box.setCurrentIndex(2)
        self.tab.filter_edit.setText('ZZZ')
        with mock.patch('tunertoolpro.gui.sniffer_tab.TcpTransport', FakeAdapter), \
                mock.patch('tunertoolpro.gui.sniffer_tab.QMessageBox.warning') as warning:
            self.tab.start()
        warning.assert_called_once()
        self.assertFalse(self.tab.running)
        self.assertTrue(FakeAdapter.instances[0].closed)

    def test_serial_source_passes_the_port_and_baud_and_rejects_a_bad_baud(self):
        seen = []

        class Recorder(FakeAdapter):
            def __init__(self, port, baud=38400):
                super().__init__()
                seen.append((port, baud))

        self.tab.source_box.setCurrentIndex(3)
        self.tab.port_box.setCurrentText('/dev/rfcomm0')
        self.tab.baud_box.setCurrentText('115200')
        with mock.patch('tunertoolpro.gui.sniffer_tab.SerialTransport', Recorder):
            self.tab.start()
            self.tab.stop()
        self.assertEqual(seen, [('/dev/rfcomm0', 115200)])
        self.tab.baud_box.setCurrentText('fast')
        with mock.patch('tunertoolpro.gui.sniffer_tab.SerialTransport', Recorder), \
                mock.patch('tunertoolpro.gui.sniffer_tab.QMessageBox.warning') as warning:
            self.tab.start()
        warning.assert_called_once()
        self.assertFalse(self.tab.running)

    def test_serial_source_needs_a_port(self):
        self.tab.source_box.setCurrentIndex(3)
        self.tab.port_box.setCurrentText('')
        with mock.patch('tunertoolpro.gui.sniffer_tab.QMessageBox.warning') as warning:
            self.tab.start()
        warning.assert_called_once()

    def test_log_file_source_replays_a_saved_capture(self):
        frames = [Frame(0x123, b'\x01\x02', False, 0.0), Frame(0x456, b'\x03', False, 0.5)]
        from tunertoolpro.canbus import format_candump
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, 'x.log')
            with open(path, 'w') as handle:
                handle.write(format_candump(frames))
            with mock.patch('tunertoolpro.gui.sniffer_tab.QFileDialog.getOpenFileName', return_value=(path, '')):
                self.tab.source_box.setCurrentIndex(1)
                self.tab.start()
        self.clock.now += 1
        self.tab.poll()
        self.tab.refresh()
        self.assertEqual(self.tab.table.rowCount(), 2)

    def test_log_file_with_no_frames_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, 'x.log')
            with open(path, 'w') as handle:
                handle.write('nothing useful here\n')
            with mock.patch('tunertoolpro.gui.sniffer_tab.QFileDialog.getOpenFileName', return_value=(path, '')), \
                    mock.patch('tunertoolpro.gui.sniffer_tab.QMessageBox.warning') as warning:
                self.tab.source_box.setCurrentIndex(1)
                self.tab.start()
        warning.assert_called_once()
        self.assertFalse(self.tab.running)

    def test_save_log_writes_what_was_captured_in_both_formats(self):
        self.tab.feed([Frame(0x123, b'\x01\x02', False, 1.0)])
        with tempfile.TemporaryDirectory() as folder:
            for name, chosen in (('a.log', 'candump log (*.log)'), ('b.csv', 'CSV (*.csv)')):
                path = os.path.join(folder, name)
                with mock.patch('tunertoolpro.gui.sniffer_tab.QFileDialog.getSaveFileName', return_value=(path, chosen)):
                    self.tab.save_log()
                with open(path) as handle:
                    back = read_log(handle.read())
                self.assertEqual([(f.can_id, f.data) for f in back], [(0x123, b'\x01\x02')])

    def test_clear_empties_everything(self):
        self.tab.feed([Frame(0x100, b'\x01')])
        self.tab.refresh()
        self.tab.clear()
        self.assertEqual((self.tab.table.rowCount(), self.tab.id_list.count(), len(self.tab.captured)), (0, 0, 0))

    def test_tab_is_in_the_main_window(self):
        from tunertoolpro.gui.main_window import MainWindow
        window = MainWindow()
        titles = [window.centralWidget().tabText(i) for i in range(window.centralWidget().count())]
        self.assertIn('CAN Sniffer', titles)
        window.sniffer_tab.shutdown()


if __name__ == '__main__':
    unittest.main()
