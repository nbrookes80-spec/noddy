"""The sniffer talking to a fake ELM327 over a real localhost socket, and the OBD link still working after."""

import socket
import sys
import threading
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from link import obd  # noqa: E402
from tunertoolpro.canbus import SnifferSession  # noqa: E402


class FakeMonitorElm:
    """Answers commands like an ELM327; after ATMA it streams CAN frames until it receives any byte."""

    def __init__(self):
        self.received = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('127.0.0.1', 0))
        self.server.listen(1)
        self.port = self.server.getsockname()[1]
        threading.Thread(target=self._serve, daemon=True).start()

    def _serve(self):
        conn, _ = self.server.accept()
        try:
            self._talk(conn)
        finally:
            conn.close()

    def _talk(self, conn):
        conn.settimeout(0.05)
        buffer = b''
        monitoring = False
        sent = 0
        while True:
            try:
                data = conn.recv(256)
                if not data:
                    return
                buffer += data
            except socket.timeout:
                pass
            except OSError:
                return
            if monitoring:
                if buffer:
                    buffer = b''
                    monitoring = False
                    self.received.append('<interrupt>')
                    conn.sendall(b'STOPPED\r\r>')
                else:
                    sent += 1
                    try:
                        conn.sendall(b'1E5 02 %02X 00 00\r0C9 FF 00\r' % (sent & 0xFF))
                    except OSError:
                        return
                    time.sleep(0.02)
                continue
            while b'\r' in buffer:
                command, _, buffer = buffer.partition(b'\r')
                command = command.decode()
                self.received.append(command)
                if command == 'ATMA':
                    monitoring = True
                    break
                reply = {'010D': '410D3C', 'ATZ': 'ELM327 v1.5'}.get(command, 'OK')
                conn.sendall(reply.encode() + b'\r\r>')

    def close(self):
        self.server.close()


class WireTests(unittest.TestCase):
    def test_sniff_then_go_back_to_reading_the_car(self):
        fake = FakeMonitorElm()
        transport = obd.WifiTransport('127.0.0.1', fake.port, timeout=2.0)
        elm = obd.Elm327(transport)
        elm.open()
        session = SnifferSession()
        session.start_adapter(transport, '6', '1E5', lock=elm._lock, owns_transport=False)
        end = time.time() + 3
        while time.time() < end and session.sniffer.frames_seen < 10:
            session.poll()
            time.sleep(0.02)
        self.assertGreaterEqual(session.sniffer.frames_seen, 10)
        self.assertEqual(session.sniffer.ids(), [0x0C9, 0x1E5])
        session.stop()
        # The adapter is handed back in the OBD link's settings, and a normal read works again.
        self.assertEqual(elm.read('010D')[0], 60)
        self.assertIn('ATMA', fake.received)
        self.assertIn('ATCRA1E5', fake.received)
        self.assertLess(fake.received.index('ATMA'), fake.received.index('<interrupt>'))
        tail = fake.received[fake.received.index('<interrupt>') + 1:]
        self.assertEqual(tail[:5], ['ATAR', 'ATH0', 'ATS0', 'ATCAF1', 'ATSP0'])
        elm.close()
        fake.close()

    def test_nothing_sent_while_listening_is_a_request(self):
        fake = FakeMonitorElm()
        transport = obd.WifiTransport('127.0.0.1', fake.port, timeout=2.0)
        elm = obd.Elm327(transport)
        elm.open()
        session = SnifferSession()
        session.start_adapter(transport, lock=elm._lock, owns_transport=False)
        time.sleep(0.3)
        session.stop()
        elm.close()
        fake.close()
        from tunertoolpro.canbus import is_allowed
        for command in fake.received:
            self.assertTrue(command.startswith('<') or is_allowed(command) or command in obd.SETUP_COMMANDS, command)
            self.assertFalse(command[:2] in ('01', '02', '03', '04', '09', '22', '2E', '3B'), command)

    def test_read_chunk_returns_empty_on_a_quiet_line_and_keeps_the_link_timeout(self):
        fake = FakeMonitorElm()
        transport = obd.WifiTransport('127.0.0.1', fake.port, timeout=2.0)
        transport.open()
        start = time.time()
        self.assertEqual(transport.read_chunk(0.1), b'')
        self.assertLess(time.time() - start, 1.0)
        self.assertEqual(transport._sock.gettimeout(), 2.0)
        transport.close()
        fake.close()


if __name__ == '__main__':
    unittest.main()
