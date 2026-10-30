import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import capture, car_scan, profiles  # noqa: E402
from tunertoolpro.canbus.frames import read_log  # noqa: E402


class FakeClock:
    """Each call moves time on by 0.1 s, so a 1 s recording takes about ten polls."""

    def __init__(self):
        self.now = 0.0

    def __call__(self):
        self.now += 0.1
        return self.now


class FakeAdapter:
    def __init__(self, fail_after=None):
        self.sent = []
        self.fail_after = fail_after
        self.reads = 0
        self.closed = False

    def open(self):
        pass

    def write(self, data):
        self.sent.append(data.decode().strip())

    def read_until(self, prompt=b'>'):
        return b'OK\r'

    def read_chunk(self, timeout=0.2):
        self.reads += 1
        if self.fail_after is not None and self.reads > self.fail_after:
            raise OSError('link dropped')
        return b'7E8 04 41 0C 1A F8 00 00 00\r'

    def close(self):
        self.closed = True


class RecordTests(unittest.TestCase):
    def test_frames_are_recorded_and_the_adapter_is_left_as_the_obd_link_expects(self):
        adapter = FakeAdapter()
        result = capture.record(adapter, 1.0, clock=FakeClock())
        self.assertTrue(result['complete'])
        self.assertGreater(len(result['frames']), 0)
        self.assertEqual(result['frames'][0].can_id, 0x7E8)
        self.assertIn('ATMA', adapter.sent)
        self.assertIn('ATH0', adapter.sent)   # headers back off after listening

    def test_a_lock_is_held_for_the_whole_recording(self):
        events = []

        class Lock:
            def __enter__(self):
                events.append('lock')

            def __exit__(self, *exc):
                events.append('unlock')

        capture.record(FakeAdapter(), 0.3, lock=Lock(), clock=FakeClock())
        self.assertEqual(events, ['lock', 'unlock'])

    def test_progress_is_reported_up_to_the_full_time(self):
        seen = []
        capture.record(FakeAdapter(), 0.5, clock=FakeClock(), progress=lambda e, total: seen.append((e, total)))
        self.assertTrue(seen)
        self.assertLessEqual(seen[-1][0], 0.5)
        self.assertTrue(all(total == 0.5 for _, total in seen))

    def test_a_link_lost_part_way_keeps_what_was_heard_and_says_why(self):
        result = capture.record(FakeAdapter(fail_after=3), 5.0, clock=FakeClock())
        self.assertFalse(result['complete'])
        self.assertIn('stopped', result['error'])
        self.assertGreater(len(result['frames']), 0)

    def test_the_frames_can_be_saved_and_read_back(self):
        from tunertoolpro.canbus.frames import format_candump
        result = capture.record(FakeAdapter(), 0.5, clock=FakeClock())
        again = read_log(format_candump(result['frames']))
        self.assertEqual([f.can_id for f in again], [f.can_id for f in result['frames']])


class DescribeTests(unittest.TestCase):
    def test_a_scan_reads_as_plain_text_with_modules_and_silent_readings(self):
        result = {
            'tried': ['010C', '010D', '22194F'], 'complete': True, 'silent': ['010D'],
            'answered': {'010C': {'name': 'Engine RPM', 'header': 'Auto', 'unit': 'RPM', 'sample': 1726},
                         '22194F': {'name': 'Trans Fluid Temp', 'header': '7E2', 'unit': 'C', 'sample': 80}},
        }
        text = car_scan.describe(result)
        self.assertIn('2 of 3 readings answered.', text)
        self.assertIn('yes  010C  Engine RPM', text)
        self.assertIn('22194F  Trans Fluid Temp on module 7E2', text)
        self.assertIn('No reply to 1: 010D', text)

    def test_an_incomplete_scan_says_it_is_not_used(self):
        result = {'tried': ['010C'], 'complete': False, 'silent': [], 'answered': {}}
        self.assertIn('not used', car_scan.describe(result))


class CarCheckTests(unittest.TestCase):
    def tearDown(self):
        profiles.activate(profiles.built_in()[-1])

    def test_a_check_scans_records_and_saves_all_four_files(self):
        import tempfile
        from scanner import car_check
        from tests.test_car_scan import StubElm

        class CheckElm(StubElm):
            def __init__(self):
                super().__init__({'010C': (1726.0, '7E0')})
                self.transport = FakeAdapter()
                self._lock = __import__('threading').RLock()

        data = tempfile.mkdtemp()
        result = car_check.check(CheckElm(), profiles.built_in()[-1], data, seconds=0.5,
                                 when=datetime(2026, 10, 30, 12, 0, 0), capture_progress=None)
        self.assertTrue(result['scan_saved'])
        self.assertIn('010C', result['scan_text'])
        self.assertGreater(result['frames'], 0)
        for path in (result['raw'], result['report_path'], result['csv']):
            self.assertTrue(Path(path).exists(), path)
        self.assertIn('car-20261030-120000', result['raw'])
        self.assertIsNotNone(car_scan.load_scan(Path(data) / 'car_scans', 'obd2'))


if __name__ == '__main__':
    unittest.main()


class DroppingTransport:
    """Streams frames, but leaves monitor mode with BUFFER FULL and a prompt until ATMA is sent again."""

    def __init__(self):
        self.listening, self.atma_sent, self.drops = False, 0, 0

    def open(self):
        pass

    def write(self, data):
        text = data.decode().strip()
        if text == 'ATMA':
            self.listening = True
            self.atma_sent += 1

    def read_until(self, prompt=b'>'):
        return b'OK\r'

    def read_chunk(self, timeout=0.2):
        if not self.listening:
            return b''
        if self.drops < 3:
            self.drops += 1
            self.listening = False
            return b'1EB 01 82\r1ED C1 90\rBUFFER FULL\r\r>'
        return b'1EB 01 7D\r'


class LongRecordingTests(unittest.TestCase):
    def test_monitoring_starts_again_after_the_adapter_drops_out(self):
        transport = DroppingTransport()
        result = capture.record(transport, 0.3)
        self.assertEqual(result['restarts'], 3)
        self.assertEqual(transport.atma_sent, 4)          # the first start plus three restarts
        self.assertGreater(len(result['frames']), 6)
        self.assertTrue(result['complete'])
