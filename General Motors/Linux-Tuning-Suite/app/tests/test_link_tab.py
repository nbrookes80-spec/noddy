"""The Link tab, driven offscreen against the shared fake ELM327.

The fake is a real TCP server speaking the adapter's own line protocol, so these tests exercise the
whole round trip -- the tab builds a transport, the worker thread opens the link, sends the command and
decodes the reply -- without a car or a dongle. That is the part worth testing: that the tab actually
holds a two-way conversation, rather than drawing a number it made up.
"""

import os
import time
import unittest

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

try:
    from PyQt6.QtWidgets import QApplication
    HAVE_QT = True
except ImportError:                                   # pragma: no cover
    HAVE_QT = False

from tunertoolpro.link.testing import FakeElm327

if HAVE_QT:
    from tunertoolpro.gui.link_tab import SERIAL, WIFI, LinkTab, describe_ports


class Port:
    """Stands in for a pyserial ListPortInfo."""

    def __init__(self, device, description='', hwid=''):
        self.device, self.description, self.hwid = device, description, hwid


class DescribePorts(unittest.TestCase):

    def test_no_pyserial_or_no_ports_is_an_empty_list(self):
        self.assertEqual(describe_ports([]), [])

    def test_the_label_carries_the_description(self):
        """COM5 on its own does not tell a Windows user which port is the dongle."""
        got = describe_ports([Port('COM5', 'Standard Serial over Bluetooth link')])
        self.assertEqual(got, [('COM5 - Standard Serial over Bluetooth link', 'COM5')])

    def test_a_port_with_no_description_keeps_its_bare_name(self):
        self.assertEqual(describe_ports([Port('COM1')]), [('COM1', 'COM1')])
        self.assertEqual(describe_ports([Port('COM1', 'n/a')]), [('COM1', 'COM1')])

    def test_a_bluetooth_port_is_offered_before_an_ordinary_one(self):
        ports = [Port('COM1', 'Communications Port'),
                 Port('COM7', 'Standard Serial over Bluetooth link')]
        self.assertEqual([device for _, device in describe_ports(ports)], ['COM7', 'COM1'])

    def test_a_named_obd_adapter_is_offered_first_too(self):
        ports = [Port('/dev/ttyS0', 'Serial port'),
                 Port('/dev/ttyUSB0', 'OBDLink SX', 'USB VID:PID=0403:6001')]
        self.assertEqual([device for _, device in describe_ports(ports)], ['/dev/ttyUSB0', '/dev/ttyS0'])

    def test_ports_with_no_device_name_are_dropped(self):
        self.assertEqual(describe_ports([Port('')]), [])


def pump_until(tab, done, timeout=20.0):
    """Drain the worker's results until `done()` or the time runs out. Stands in for the Qt timer."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        tab.pump()
        if done():
            return True
        time.sleep(0.02)
    tab.pump()
    return done()


@unittest.skipUnless(HAVE_QT, 'PyQt6 is not installed')
class TalkingToTheAdapter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.fake = FakeElm327()
        self.tab = LinkTab()
        self.tab.source_box.setCurrentText(WIFI)
        self.tab.host_edit.setText(f'127.0.0.1:{self.fake.port}')
        self.addCleanup(self.fake.close)
        self.addCleanup(self.tab.shutdown)

    def connect(self):
        self.tab.open_link()
        self.assertTrue(pump_until(self.tab, lambda: self.tab.connected or 'not connect' in self.tab.status.text()),
                        f'never settled; status was {self.tab.status.text()!r}')
        self.assertTrue(self.tab.connected, self.tab.status.text())

    def test_it_connects_and_reports_what_the_adapter_said(self):
        self.connect()
        self.assertEqual(self.tab.firmware_label.text(), 'ELM327 v1.5')
        self.assertEqual(self.tab.adapter_volts_label.text(), '12.6V')
        self.assertEqual(self.tab.protocol_label.text(), 'ISO 15765-4 (CAN 11/500)')

    def test_it_reads_the_car_battery_through_the_catalogue(self):
        self.connect()
        self.assertEqual(self.tab.car_volts_label.text(), '12.6 V')

    def test_reading_a_pid_asks_the_car_and_decodes_the_answer(self):
        """010C returns 0x1AF8, which is 1726 rpm once divided by four."""
        self.connect()
        self.tab.pid_box.setCurrentText('010C')
        self.tab.read_pid()
        self.assertTrue(pump_until(self.tab, lambda: 'rpm' in self.tab.answer.text().lower()),
                        f'answer was {self.tab.answer.text()!r}')
        self.assertIn('1726', self.tab.answer.text())
        self.assertIn('010C', self.fake.received)

    def test_reading_trouble_codes_lists_what_is_stored(self):
        self.connect()
        self.tab.read_codes()
        self.assertTrue(pump_until(self.tab, lambda: 'P0' in self.tab.answer.text()),
                        f'answer was {self.tab.answer.text()!r}')
        self.assertIn('P0301', self.tab.answer.text())
        self.assertIn('P0420', self.tab.answer.text())

    def test_the_traffic_log_shows_both_directions(self):
        """The point of the log: what went out and what came back, not a story about it."""
        self.connect()
        text = self.tab.traffic_view.toPlainText()
        self.assertIn('TX', text)
        self.assertIn('RX', text)

    def test_the_link_is_opened_read_only(self):
        self.connect()
        self.assertIs(self.tab.worker.elm.allow_clear, False)

    def test_closing_the_link_stops_the_worker(self):
        self.connect()
        self.tab.close_link()
        self.assertFalse(self.tab.connected)
        self.assertFalse(self.tab.worker.running)
        self.assertIsNone(self.tab.worker.elm)


@unittest.skipUnless(HAVE_QT, 'PyQt6 is not installed')
class BeforeAnythingIsConnected(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.tab = LinkTab()
        self.addCleanup(self.tab.shutdown)

    def test_requests_are_disabled_until_a_link_is_open(self):
        self.assertFalse(self.tab.read_btn.isEnabled())
        self.assertFalse(self.tab.codes_btn.isEnabled())

    def test_a_serial_source_with_no_port_explains_itself(self):
        self.tab.source_box.setCurrentText(SERIAL)
        self.tab.port_box.setCurrentText('')
        with self.assertRaises(ValueError) as caught:
            self.tab.build_transport()
        self.assertIn('COM3', str(caught.exception))

    def test_a_wifi_source_with_no_address_explains_itself(self):
        self.tab.source_box.setCurrentText(WIFI)
        self.tab.host_edit.setText('')
        with self.assertRaises(ValueError):
            self.tab.build_transport()

    def test_the_port_list_offers_the_device_name_not_the_label(self):
        self.tab.source_box.setCurrentText(SERIAL)
        self.tab.refresh_ports([Port('COM5', 'Standard Serial over Bluetooth link')])
        self.assertEqual(self.tab.chosen_port(), 'COM5')

    def test_a_port_that_has_been_unplugged_stops_looking_selected(self):
        """Pick a port, unplug it, refresh: the box must not still offer the one that is gone."""
        self.tab.refresh_ports([Port('COM5', 'Standard Serial over Bluetooth link'),
                                Port('COM1', 'Communications Port')])
        self.assertEqual(self.tab.chosen_port(), 'COM5')
        self.tab.refresh_ports([Port('COM1', 'Communications Port')])
        self.assertEqual(self.tab.chosen_port(), 'COM1')

    def test_a_port_that_is_still_there_stays_selected_across_a_refresh(self):
        self.tab.refresh_ports([Port('COM5', 'Standard Serial over Bluetooth link'),
                                Port('COM1', 'Communications Port')])
        self.tab.port_box.setCurrentIndex(1)
        self.assertEqual(self.tab.chosen_port(), 'COM1')
        self.tab.refresh_ports([Port('COM1', 'Communications Port'),
                                Port('COM5', 'Standard Serial over Bluetooth link')])
        self.assertEqual(self.tab.chosen_port(), 'COM1')

    def test_a_typed_port_is_used_as_typed(self):
        self.tab.source_box.setCurrentText(SERIAL)
        self.tab.refresh_ports([Port('COM5', 'Standard Serial over Bluetooth link')])
        self.tab.port_box.setCurrentText('/dev/rfcomm0')
        self.assertEqual(self.tab.chosen_port(), '/dev/rfcomm0')

    def test_there_is_no_control_that_writes_to_the_car(self):
        """The read-only promise, enforced on the window rather than only in the docs."""
        from PyQt6.QtWidgets import QPushButton
        labels = [b.text().lower() for b in self.tab.findChildren(QPushButton)]
        for forbidden in ('clear', 'flash', 'write', 'erase', 'reset'):
            self.assertFalse([t for t in labels if forbidden in t], f'a button offers to {forbidden}: {labels}')


if __name__ == '__main__':
    unittest.main()
