import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from link.obd import Elm327  # noqa: E402
from live import LiveStream  # noqa: E402
from scanner import gmlan  # noqa: E402
from scanner.bus_listen import bus_reader, listen_adapter  # noqa: E402
from scanner.demo import DemoSource  # noqa: E402
from tunertoolpro.canbus import Frame, MonitorError  # noqa: E402

PARK = bytes.fromhex('0F0F000100000300')
DRIVE = bytes.fromhex('0F0F000400000300')


class FakeClock:
    """Moves forward a little on every call, so a listening window ends after a few polls."""

    def __init__(self, step=0.1):
        self.now = 0.0
        self.step = step

    def __call__(self):
        self.now += self.step
        return self.now


class FakeAdapter:
    """An ELM327 stand-in: answers every command with OK and hands out the chunks it is given."""

    def __init__(self, chunks=(), fail=False):
        self.chunks = list(chunks)
        self.fail = fail
        self.written = []

    def open(self):
        pass

    def close(self):
        pass

    def write(self, data):
        self.written.append(data.decode('ascii').strip())

    def read_until(self, prompt=b'>', timeout=5.0):
        if self.fail:
            raise OSError('link down')
        return b'OK\r>'

    def read_chunk(self, timeout=0.2):
        return self.chunks.pop(0) if self.chunks else b''


class FakeSource:
    """Engine readings only, as the OBD link would give them."""

    def poll(self, pids, headers=None):
        return {'010C': (800.0, 'rpm')}, {}


class LatestTests(unittest.TestCase):
    def test_a_gear_reading_goes_stale_after_three_seconds(self):
        latest = gmlan.Latest()
        latest.feed([Frame(0x1F5, PARK, False, 0.0)], now=10.0)
        self.assertEqual(latest.readings(now=12.9), {'gear': 'Park'})
        self.assertEqual(latest.readings(now=13.5), {})

    def test_the_newest_payload_wins(self):
        latest = gmlan.Latest()
        latest.feed([Frame(0x1F5, PARK, False, 0.0)], now=1.0)
        latest.feed([Frame(0x1F5, DRIVE, False, 0.0)], now=2.0)
        self.assertEqual(latest.readings(now=2.0), {'gear': 'Drive'})

    def test_gear_frame_gives_the_readme_payload(self):
        self.assertEqual(gmlan.gear_frame('Drive'), DRIVE)


class ListenAdapterTests(unittest.TestCase):
    def test_a_window_reads_frames_and_hands_the_adapter_back(self):
        adapter = FakeAdapter(chunks=[b'1F5 0F 0F 00 04 00 00 03 00\r'])
        elm = Elm327(adapter)
        frames = listen_adapter(elm, 0.5, clock=FakeClock())
        self.assertEqual([(f.can_id, f.data) for f in frames], [(0x1F5, DRIVE)])
        self.assertIn('ATMA', adapter.written)
        self.assertEqual(adapter.written[-5:], ['ATAR', 'ATH0', 'ATS0', 'ATCAF1', 'ATSP0'])
        self.assertTrue(elm._lock.acquire(blocking=False))   # the lock is released after the window
        elm._lock.release()

    def test_a_failed_window_still_raises_and_releases_the_lock(self):
        elm = Elm327(FakeAdapter(fail=True))
        with self.assertRaises(MonitorError):
            listen_adapter(elm, 0.5, clock=FakeClock())
        self.assertTrue(elm._lock.acquire(blocking=False))
        elm._lock.release()


class BusReaderTests(unittest.TestCase):
    def test_an_adapter_gets_the_listening_window(self):
        self.assertIsNotNone(bus_reader(Elm327(FakeAdapter())))

    def test_the_demo_source_listens_itself(self):
        self.assertIsNotNone(bus_reader(DemoSource()))

    def test_a_source_with_no_bus_gets_none(self):
        self.assertIsNone(bus_reader(FakeSource()))


class DemoBusTests(unittest.TestCase):
    def test_the_simulated_bus_shows_park_then_drive(self):
        now = [0.0]
        demo = DemoSource(clock=lambda: now[0])
        now[0] = 1.0
        self.assertEqual(demo.listen(0.8)[0].data, PARK)
        now[0] = 6.0
        self.assertEqual(demo.listen(0.8)[0].data, DRIVE)


class LiveTileTests(unittest.TestCase):
    def tile(self, stream, key='shift_lever'):
        return next(t for t in stream.health() if t['key'] == key)

    def run_rounds(self, stream, rounds=4):
        for _ in range(rounds):
            stream.step()

    def test_the_shift_lever_tile_names_the_gear_and_the_engine_still_reads(self):
        clock = FakeClock(step=0.0)
        stream = LiveStream(FakeSource(), clock=clock,
                            bus=lambda seconds: [Frame(0x1F5, DRIVE, False, 0.0)])
        self.run_rounds(stream)
        self.assertEqual(self.tile(stream)['text'], 'Drive')
        self.assertEqual(stream.latest['010C'], (800.0, 'rpm'))

    def test_a_bus_that_does_not_answer_leaves_the_engine_readings_running(self):
        def broken(seconds):
            raise MonitorError('The adapter did not answer in time.')
        stream = LiveStream(FakeSource(), clock=FakeClock(step=0.0), bus=broken)
        self.run_rounds(stream)
        self.assertEqual(self.tile(stream)['text'], 'bus not answering')
        self.assertEqual(stream.latest['010C'], (800.0, 'rpm'))

    def test_the_tile_says_no_reading_when_the_bus_has_gone_quiet(self):
        clock = FakeClock(step=0.0)
        stream = LiveStream(FakeSource(), clock=clock, bus=lambda seconds: [Frame(0x1F5, PARK, False, 0.0)])
        self.run_rounds(stream)
        clock.now += 10.0
        self.assertEqual(self.tile(stream)['text'], 'no reading yet')

    def test_without_a_bus_the_tile_waits_for_one(self):
        stream = LiveStream(FakeSource(), clock=FakeClock(step=0.0))
        self.run_rounds(stream)
        self.assertEqual(self.tile(stream)['text'], 'no reading yet')


if __name__ == '__main__':
    unittest.main()
