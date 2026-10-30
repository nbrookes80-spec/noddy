import sys
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner.session import Session  # noqa: E402


class FakeLink:
    def __init__(self, traffic):
        self._lock = threading.RLock()
        self.traffic = list(traffic)


class AdapterInfoTests(unittest.TestCase):
    def test_no_adapter_means_not_connected_and_nothing_recent(self):
        session = Session()
        self.assertEqual(session.adapter_info(), {'connected': False, 'demo': False, 'recent': []})

    def test_connected_adapter_shares_its_latest_traffic_only(self):
        session = Session()
        session.attach(FakeLink([('TX', f'01{n:02X}') for n in range(50)]))
        info = session.adapter_info(recent=3)
        self.assertTrue(info['connected'])
        self.assertEqual(info['recent'], [['TX', '012F'], ['TX', '0130'], ['TX', '0131']])

    def test_demo_is_reported_alongside_the_adapter(self):
        session = Session()
        session.set_demo(True)
        self.assertTrue(session.adapter_info()['demo'])


class FakeTransport:
    def __init__(self, reply=b'OK\r\r>', fail=None):
        self.reply, self.fail = reply, fail

    def write(self, data):
        pass

    def read_until(self, _end):
        if self.fail:
            raise self.fail
        return self.reply


class TrafficLogTests(unittest.TestCase):
    def test_traffic_refusals_and_errors_reach_the_log(self):
        from link import obd
        seen = []
        elm = obd.Elm327(FakeTransport())
        elm.on_traffic = lambda kind, text: seen.append((kind, text))
        elm.command('ATZ')
        with self.assertRaises(obd.UnsafeCommand):
            elm.command('2E0101')
        broken = obd.Elm327(FakeTransport(fail=obd.AdapterLost('gone')))
        broken.on_traffic = lambda kind, text: seen.append((kind, text))
        with self.assertRaises(obd.AdapterLost):
            broken.command('0100')
        self.assertEqual(seen, [('TX', 'ATZ'), ('RX', 'OK  >'), ('REFUSED', '2E0101'), ('TX', '0100'),
                                ('ERR', 'AdapterLost: gone')])

    def test_a_broken_log_does_not_stop_a_reading(self):
        from link import obd
        elm = obd.Elm327(FakeTransport())
        elm.on_traffic = lambda kind, text: 1 / 0
        self.assertEqual(elm.command('ATZ'), 'OK\n\n>')


if __name__ == '__main__':
    unittest.main()
