"""The live stream through the real ELM327 link, talking to a fake adapter over a local socket."""

import socket
import sys
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from link import obd  # noqa: E402
from live import STREAM_PIDS, LiveStream  # noqa: E402

# What a car would say, as the hex after the adapter echo. Expected values below come from the
# standard formulas, worked by hand.
ECU = {'010C': '410C1AF8',      # (0x1A*256 + 0xF8) / 4 = 1726 rpm
       '010D': '410D3C',        # 60 km/h
       '0111': '411180',        # 128 * 100 / 255 = 50.2 percent
       '0105': '410578',        # 0x78 - 40 = 80 C
       '0104': '410480', '010B': '410B64', '010E': '410E90'}
TCM = {'22194F': '62194F78',    # 0x78 - 40 = 80 C
       '22199A': '62199A03',    # third gear
       '221991': '6219910032', '22001F': '62001F0190', '221941': '6219410BB8',
       '221942': '62194201F4'}


class FakeAdapter:
    """An ELM327 on a local port. Remembers every command it was sent and which module it was aimed at."""

    def __init__(self, tcm_header='7E2', silent=()):
        self.tcm_header = tcm_header     # the module address the transmission answers on
        self.silent = set(silent)        # PIDs that never get an answer
        self.log = []                    # (header, command)
        self.header = '7DF'
        self.server = socket.socket()
        self.server.bind(('127.0.0.1', 0))
        self.server.listen(1)
        self.port = self.server.getsockname()[1]
        threading.Thread(target=self._serve, daemon=True).start()

    def _serve(self):
        conn, _ = self.server.accept()
        buffer = b''
        while True:
            try:
                chunk = conn.recv(256)
            except OSError:
                return
            if not chunk:
                return
            buffer += chunk
            while b'\r' in buffer:
                line, _, buffer = buffer.partition(b'\r')
                conn.sendall(self._answer(line.decode().strip()).encode() + b'\r\r>')

    def _answer(self, command):
        self.log.append((self.header, command))
        if command.startswith('ATSH'):
            self.header = command[4:]
            return 'OK'
        if command.startswith('AT'):
            return 'OK'
        if command in self.silent:
            return 'NO DATA'
        if command in ECU and self.header in ('7DF', '7E0'):
            return ECU[command]
        if command in TCM and self.header == self.tcm_header:
            return TCM[command]
        return 'NO DATA'

    def link(self):
        self.elm = obd.Elm327(obd.WifiTransport('127.0.0.1', self.port, timeout=3.0))
        self.elm.open()
        return self.elm

    def close(self):
        if getattr(self, 'elm', None):
            self.elm.close()
        self.server.close()

    def sent(self):
        return [command for _, command in self.log]


class StreamOverTheWireTests(unittest.TestCase):
    def test_engine_and_transmission_readings_both_arrive(self):
        adapter = FakeAdapter()
        self.addCleanup(adapter.close)
        stream = LiveStream(adapter.link())
        stream.step()
        values = stream.snapshot()['values']
        self.assertEqual(values['010C']['value'], 1726.0)
        self.assertAlmostEqual(values['0111']['value'], 50.2, places=1)
        self.assertEqual(values['22194F']['value'], 80.0)
        self.assertEqual(values['22199A']['value'], 3.0)

    def test_the_adapter_switches_to_the_transmission_once_per_round(self):
        adapter = FakeAdapter()
        self.addCleanup(adapter.close)
        stream = LiveStream(adapter.link())
        stream.step()
        stream.step()
        switches = [c for c in adapter.sent() if c.startswith('ATSH')]
        # to 7E2 for the transmission, back to 7DF for the engine, once each round
        self.assertEqual(switches, ['ATSH7E2', 'ATSH7DF', 'ATSH7E2'])
        sent = adapter.sent()
        first_tcm = sent.index('22199A')
        self.assertLess(sent.index('010C'), sent.index('ATSH7E2'))
        self.assertLess(sent.index('ATSH7E2'), first_tcm)

    def test_a_transmission_that_only_answers_on_the_broadcast_address_still_streams(self):
        adapter = FakeAdapter(tcm_header='7DF')
        self.addCleanup(adapter.close)
        stream = LiveStream(adapter.link())
        stream.step()
        self.assertEqual(stream.snapshot()['values']['22199A']['value'], 3.0)
        asked_before = adapter.sent().count('22199A')
        stream.step()
        # it remembered which address worked, so the second round asks once, not twice
        self.assertEqual(adapter.sent().count('22199A') - asked_before, 1)

    def test_a_reading_the_car_never_answers_stops_costing_adapter_time(self):
        adapter = FakeAdapter(silent={'221991'})
        self.addCleanup(adapter.close)
        stream = LiveStream(adapter.link())
        for _ in range(7):
            stream.step()
        asked = adapter.sent().count('221991')
        self.assertLessEqual(asked, 6)          # 7 rounds, but it is skipped once it keeps failing
        self.assertNotIn('221991', stream.snapshot()['values'])

    def test_only_read_only_commands_ever_reach_the_adapter(self):
        adapter = FakeAdapter()
        self.addCleanup(adapter.close)
        stream = LiveStream(adapter.link())
        for _ in range(5):
            stream.step()
        self.assertTrue(adapter.sent())
        for command in adapter.sent():
            self.assertTrue(obd.is_allowed(command), command)
        self.assertTrue(set(STREAM_PIDS) >= {c for c in adapter.sent() if c[:2] in ('01', '22')})


class SharedAdapterTests(unittest.TestCase):
    def test_two_screens_reading_at_once_do_not_scramble_each_others_replies(self):
        adapter = FakeAdapter()
        self.addCleanup(adapter.close)
        elm = adapter.link()
        failures = []

        def read_loop(pids, expected):
            for _ in range(40):
                values, errors = elm.poll(pids, headers={p: '7E2' for p in pids if p[:2] == '22'})
                if errors or {p: v[0] for p, v in values.items()} != expected:
                    failures.append((values, errors))

        engine = threading.Thread(target=read_loop, args=(['010C', '0105'], {'010C': 1726.0, '0105': 80.0}))
        trans = threading.Thread(target=read_loop, args=(['22199A', '22194F'], {'22199A': 3.0, '22194F': 80.0}))
        engine.start(), trans.start()
        engine.join(20), trans.join(20)
        self.assertEqual(failures, [])


if __name__ == '__main__':
    unittest.main()
