import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import demo, pids  # noqa: E402
from scanner.session import DEMO, LIVE, OFFLINE, Session  # noqa: E402


class CatalogTests(unittest.TestCase):
    def test_catalogue_is_ported_whole(self):
        self.assertGreaterEqual(len(pids.CATALOG), 100)
        self.assertIn('Transmission (GM - Probable)', pids.categories())

    def test_every_pid_is_a_mode_01_or_mode_22_read(self):
        for pid in pids.CATALOG.values():
            self.assertIn(pid.mode, ('01', '22'))
            self.assertEqual(pid.command[:2], pid.mode)
            self.assertIn(pid.header, ('Auto', '7E0', '7E2', '7E3'))
            self.assertLess(pid.low, pid.high)

    def test_decoding_matches_the_standard_formulas(self):
        self.assertEqual(pids.get('010C').parse('1AF8'), 1726.0)        # (A*256+B)/4
        self.assertEqual(pids.get('0105').parse('78'), 80.0)             # A-40
        self.assertAlmostEqual(pids.get('010B').parse('FF'), 300.0)      # scaled for the 3 bar sensor
        self.assertAlmostEqual(pids.get('0111').parse('80'), 50.2, places=1)
        self.assertAlmostEqual(pids.get('0114').parse('90'), 0.72)       # A/200 volts
        self.assertAlmostEqual(pids.get('0114').parse('FF'), 1.275)      # top of its range

    def test_short_or_bad_data_gives_none(self):
        self.assertIsNone(pids.get('010C').parse('1A'))
        self.assertIsNone(pids.get('0105').parse(''))
        self.assertIsNone(pids.get('0105').parse('ZZ'))

    def test_reply_echo_differs_by_mode(self):
        self.assertEqual(pids.get('010C').echo, '410C')
        self.assertEqual(pids.get('22194F').echo, '62194F')

    def test_unconfirmed_pids_are_flagged(self):
        self.assertTrue(pids.get('010C').verified)
        self.assertFalse(pids.get('221999').verified)

    def test_dashboard_pages_hold_four_catalogue_pids(self):
        pages = pids.monitor_pages()
        self.assertTrue(all(1 <= len(page) <= pids.PAGE_SIZE for page in pages))
        self.assertEqual(sum(len(page) for page in pages), len(pids.MONITOR_PIDS))

    def test_stored_codes_decode(self):
        self.assertEqual(pids.decode_dtcs('03010420'), ['P0301', 'P0420'])
        self.assertEqual(pids.decode_dtcs('C1230000'), ['U0123'])
        self.assertEqual(pids.decode_dtcs('00000000'), [])


class DemoTests(unittest.TestCase):
    def test_every_pid_stays_inside_its_own_range(self):
        for pid in pids.CATALOG.values():
            for step in range(0, 160):
                reading = demo.value(pid, step * 0.5)
                self.assertGreaterEqual(reading, pid.low, pid.pid)
                self.assertLessEqual(reading, pid.high, pid.pid)

    def test_drive_idles_then_launches_through_the_gears(self):
        self.assertLess(demo.drive(1)['speed'], 1)
        self.assertGreater(demo.drive(15)['speed'], 100)
        gears = [demo.drive(4 + 0.25 * i)['gear'] for i in range(49)]
        self.assertEqual(gears, sorted(gears))
        self.assertEqual(gears[0], 1)
        self.assertGreaterEqual(gears[-1], 3)
        self.assertLessEqual(max(demo.drive(4 + 0.25 * i)['rpm'] for i in range(49)), 6200)

    def test_drive_repeats_every_cycle(self):
        self.assertEqual(demo.drive(7.5), demo.drive(7.5 + demo.CYCLE_SECONDS))

    def test_source_reads_like_the_adapter_link(self):
        clock = iter(range(0, 1000))
        source = demo.DemoSource(clock=lambda: next(clock) * 1.0)
        values, errors = source.poll(['010C', '010D', '22199A'])
        self.assertEqual(errors, {})
        self.assertEqual(set(values), {'010C', '010D', '22199A'})
        value, unit = source.read('010C')
        self.assertEqual(unit, 'RPM')
        self.assertEqual(source.read_dtcs(), demo.DEMO_CODES)
        self.assertTrue(all('simulated' in text or direction == 'TX' for direction, text in source.traffic))

    def test_unknown_pid_is_refused(self):
        with self.assertRaises(KeyError):
            demo.DemoSource().read('0902')


class FakeLink:
    label = 'Live'

    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class SessionTests(unittest.TestCase):
    def test_starts_offline_with_nothing_to_read(self):
        session = Session()
        self.assertEqual(session.status, OFFLINE)
        self.assertIsNone(session.active())

    def test_demo_works_without_an_adapter(self):
        session = Session()
        session.set_demo(True)
        self.assertEqual(session.status, DEMO)
        value, _unit = session.active().read('010C')
        self.assertGreater(value, 0)

    def test_demo_takes_priority_but_keeps_the_adapter_connected(self):
        session, link = Session(), FakeLink()
        session.attach(link)
        self.assertEqual(session.status, LIVE)
        session.set_demo(True)
        self.assertIsNot(session.active(), link)
        session.set_demo(False)
        self.assertIs(session.active(), link)
        self.assertFalse(link.closed)

    def test_detach_closes_the_adapter_and_tells_listeners(self):
        session, link, seen = Session(), FakeLink(), []
        session.listeners.append(seen.append)
        session.attach(link)
        session.detach()
        self.assertTrue(link.closed)
        self.assertEqual(seen, [LIVE, OFFLINE])


if __name__ == '__main__':
    unittest.main()
