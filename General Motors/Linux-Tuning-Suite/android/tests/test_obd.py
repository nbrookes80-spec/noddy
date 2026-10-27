import socket
import sys
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from link import obd  # noqa: E402


class FakeElm327:
    """A localhost TCP server that answers like an ELM327 with spaces and line feeds off."""

    REPLIES = {
        'ATZ': 'ELM327 v1.5',
        'ATE0': 'OK', 'ATL0': 'OK', 'ATH0': 'OK', 'ATS0': 'OK', 'ATSP0': 'OK',
        '0100': 'SEARCHING...\r4100BE3FA813',
        '010C': 'SEARCHING...\r410C1AF8',   # 0x1AF8 / 4 = 1726 rpm
        '010D': '410D3C',                   # 60 km/h
        '0105': '410578',                   # 120 - 40 = 80 C
        '0111': '411180',                   # 128 * 100 / 255 = 50.2 %
        '010F': 'NO DATA',
        'ATSH7DF': 'OK', 'ATSH7E0': 'OK', 'ATSH7E2': 'OK',
        '22194F': '62194F78',               # transmission fluid temperature: 120 - 40 = 80 C
        '03': '4303010420',                 # stored codes P0301 and P0420
    }

    def __init__(self):
        self.received = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('127.0.0.1', 0))
        self.server.listen(1)
        self.port = self.server.getsockname()[1]
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()

    def _serve(self):
        conn, _ = self.server.accept()
        conn.settimeout(5)
        buffer = b''
        with conn:
            while True:
                chunk = conn.recv(256)
                if not chunk:
                    return
                buffer += chunk
                while b'\r' in buffer:
                    line, _, buffer = buffer.partition(b'\r')
                    command = line.decode('ascii').strip()
                    self.received.append(command)
                    reply = self.REPLIES.get(command, '?')
                    conn.sendall((reply + '\r\r>').encode('ascii'))

    def close(self):
        self.server.close()


class ElmTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeElm327()
        self.elm = obd.Elm327(obd.WifiTransport('127.0.0.1', self.fake.port, timeout=3))
        self.elm.open()

    def tearDown(self):
        self.elm.close()
        self.fake.close()

    def test_setup_sends_only_the_setup_commands(self):
        self.assertEqual(self.fake.received[:len(obd.SETUP_COMMANDS)], list(obd.SETUP_COMMANDS))

    def test_engine_speed_decodes_over_wifi(self):
        value, unit = self.elm.read('010C')
        self.assertAlmostEqual(value, 1726.0)
        self.assertEqual(unit, 'rpm')

    def test_speed_coolant_and_throttle_decode(self):
        self.assertEqual(self.elm.read('010D'), (60, 'km/h'))
        self.assertEqual(self.elm.read('0105'), (80, 'C'))
        value, unit = self.elm.read('0111')
        self.assertAlmostEqual(value, 50.196, places=2)
        self.assertEqual(unit, '%')

    def test_no_data_reply_raises_a_clear_error(self):
        with self.assertRaises(obd.OBDError) as ctx:
            self.elm.read('010F')
        self.assertIn('Intake air temperature', str(ctx.exception))
        self.assertIn('NO DATA', str(ctx.exception))

    def test_poll_keeps_good_values_and_reports_bad_ones(self):
        values, errors = self.elm.poll(['010C', '010F', '010D'])
        self.assertEqual(set(values), {'010C', '010D'})
        self.assertEqual(set(errors), {'010F'})

    def test_write_commands_are_refused_before_sending(self):
        sent_before = len(self.fake.received)
        for command in ('0902', '0400', '04', 'ATSP6', '14FF00', '1902', '2201FF', 'ATSH7E1',
                        'ATSH7FF', '2F1234', '3101'):
            with self.subTest(command=command):
                with self.assertRaises(obd.UnsafeCommand):
                    self.elm.command(command)
        self.assertEqual(len(self.fake.received), sent_before)

    def test_only_listed_pids_can_be_read(self):
        for pid in ('0902', '2201FF', '04'):
            with self.subTest(pid=pid):
                with self.assertRaises(obd.UnsafeCommand):
                    self.elm.read(pid)

    def test_a_transmission_pid_switches_header_then_returns_to_broadcast(self):
        value, unit = self.elm.read('22194F')
        self.assertAlmostEqual(value, 80)
        self.elm.read('010D')
        sent = self.fake.received[len(obd.SETUP_COMMANDS):]
        self.assertEqual(sent, ['ATSH7E2', '22194F', 'ATSH7DF', '010D'])

    def test_stored_codes_are_decoded(self):
        self.assertEqual(self.elm.read_dtcs(), ['P0301', 'P0420'])

    def test_traffic_log_records_what_was_sent_and_received(self):
        self.elm.read('010D')
        self.assertIn(('TX', '010D'), self.elm.traffic)
        self.assertIn(('RX', '410D3C'), self.elm.traffic)

    def test_every_allowed_command_is_a_read(self):
        from scanner import pids
        for pid in pids.CATALOG:
            self.assertTrue(pid[:2] in ('01', '22'), pid)
        for command in obd.ALLOWED:
            self.assertFalse(command.startswith(('04', '08', '09', '10', '14', '27', '2E', '2F', '31', '34')),
                             command)

    def test_unreachable_wifi_adapter_gives_a_clear_error(self):
        probe = socket.socket()
        probe.bind(('127.0.0.1', 0))
        port = probe.getsockname()[1]
        probe.close()
        elm = obd.Elm327(obd.WifiTransport('127.0.0.1', port, timeout=1))
        with self.assertRaises(obd.OBDError) as ctx:
            elm.open()
        self.assertIn('Wi-Fi adapter', str(ctx.exception))


class BluetoothTests(unittest.TestCase):
    def test_bluetooth_says_it_needs_android_when_run_elsewhere(self):
        transport = obd.BluetoothTransport('00:11:22:33:44:55')
        with self.assertRaises(obd.OBDError) as ctx:
            transport.open()
        self.assertIn('needs the Android app', str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
