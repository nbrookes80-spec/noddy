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


if __name__ == '__main__':
    unittest.main()
