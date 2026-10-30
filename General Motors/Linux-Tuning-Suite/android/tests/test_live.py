import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import shift_live  # noqa: E402
from grading import BAD, GOOD, OK  # noqa: E402
from link import obd  # noqa: E402
from live import FAST_PIDS, SLOW_PIDS, STREAM_PIDS, TCM_PIDS, LiveStream  # noqa: E402


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


class ScriptedSource:
    """Answers each poll with whatever `readings` holds, and remembers what was asked for."""
    label = 'Scripted'

    def __init__(self):
        self.readings = {}
        self.asked = []
        self.fail = None

    def poll(self, pids, headers=None):
        self.asked.append(list(pids))
        if self.fail:
            raise obd.OBDError(self.fail)
        values = {p: (self.readings[p], '') for p in pids if p in self.readings}
        return values, {p: 'no reply' for p in pids if p not in self.readings}


def model():
    values, ratios = shift_live.default_inputs('LS3 Camaro SS (6L80)')
    cfg = shift_live.build_cfg(values, ratios)
    tables, _ = shift_live.calculate(values, ratios)
    return cfg, tables


def health(stream, key):
    return next(h for h in stream.snapshot()['health'] if h['key'] == key)


class PollingTests(unittest.TestCase):
    def test_the_stream_covers_the_engine_and_the_transmission(self):
        self.assertIn('010C', STREAM_PIDS)        # engine speed, from the ECU
        self.assertIn('22194F', STREAM_PIDS)      # transmission fluid temperature, from the TCM
        self.assertIn('22199A', STREAM_PIDS)      # current gear
        self.assertEqual(set(FAST_PIDS) | set(SLOW_PIDS), set(STREAM_PIDS))

    def test_slow_readings_are_asked_for_every_fourth_round(self):
        source, clock = ScriptedSource(), Clock()
        stream = LiveStream(source, clock=clock)
        for _ in range(5):
            stream.step()
        self.assertEqual(set(source.asked[0]), set(STREAM_PIDS))      # first round reads everything
        self.assertEqual(set(source.asked[1]), set(FAST_PIDS))
        self.assertEqual(set(source.asked[3]), set(FAST_PIDS))
        self.assertEqual(set(source.asked[4]), set(STREAM_PIDS))      # fifth round: slow ones again

    def test_engine_only_stream_never_asks_the_transmission(self):
        source, clock = ScriptedSource(), Clock()
        stream = LiveStream(source, clock=clock, transmission=False)
        for _ in range(5):
            stream.step()
        for asked in source.asked:
            self.assertFalse(set(asked) & TCM_PIDS)
        self.assertIn('010C', source.asked[0])

    def test_snapshot_gives_names_units_values_and_a_short_history(self):
        source, clock = ScriptedSource(), Clock()
        source.readings = {'010C': 1726.0}
        stream = LiveStream(source, clock=clock)
        for _ in range(3):
            clock.now += 0.5
            stream.step()
            source.readings['010C'] += 100
        entry = stream.snapshot()['values']['010C']
        self.assertEqual(entry['name'], 'Engine RPM')
        self.assertEqual(entry['value'], 1926.0)
        self.assertEqual(entry['history'], [1726.0, 1826.0, 1926.0])

    def test_rate_is_rounds_per_second(self):
        source, clock = ScriptedSource(), Clock()
        stream = LiveStream(source, clock=clock)
        for _ in range(5):
            clock.now += 0.5
            stream.step()
        self.assertAlmostEqual(stream.snapshot()['rate_hz'], 2.0, places=1)

    def test_a_lost_adapter_is_reported_not_raised(self):
        source, clock = ScriptedSource(), Clock()
        source.readings = {'010C': 900.0}
        stream = LiveStream(source, clock=clock)
        stream.step()
        source.fail = 'The adapter stopped answering'
        stream.step()
        snap = stream.snapshot()
        self.assertEqual(snap['error'], 'The adapter stopped answering')
        self.assertEqual(snap['values']['010C']['value'], 900.0)


class HealthTests(unittest.TestCase):
    def stream_with(self, **readings):
        source, clock = ScriptedSource(), Clock()
        source.readings = readings
        cfg, tables = model()
        stream = LiveStream(source, cfg=cfg, tables=tables, clock=clock)
        stream.clock, stream.source = clock, source
        stream.step()
        return stream

    def test_transmission_fluid_temperature(self):
        for celsius, level in ((95, GOOD), (110, OK), (125, BAD), (20, OK)):
            stream = self.stream_with(**{'22194F': float(celsius)})
            self.assertEqual(health(stream, 'trans_temp')['level'], level, celsius)

    def test_engine_speed_against_the_shift_rpm_setting(self):
        for rpm, level in ((6000, GOOD), (6400, OK), (6600, BAD)):      # target is 6300
            stream = self.stream_with(**{'010C': float(rpm)})
            self.assertEqual(health(stream, 'engine_rpm')['level'], level, rpm)

    def test_line_pressure_is_shown_as_read(self):
        self.assertEqual(health(self.stream_with(**{'22001F': 612.0}), 'line_pressure')['text'], '612 kPa')
        self.assertEqual(health(self.stream_with(), 'line_pressure')['level'], 'off')

    def test_the_gear_is_worked_out_from_the_shaft_speeds(self):
        for turbine, output, gear in ((4027, 1000, 1), (1532, 1000, 3), (1000, 1500, 6)):
            stream = self.stream_with(**{'221941': float(turbine), '221942': float(output)})
            self.assertEqual(stream.implied_gear(), gear)
        self.assertIsNone(self.stream_with(**{'221941': 800.0, '221942': 50.0}).implied_gear())   # crawling
        self.assertIsNone(self.stream_with(**{'221941': 1900.0, '221942': 1000.0}).implied_gear())  # mid-shift

    def test_a_gear_that_does_not_match_the_shaft_speeds_turns_yellow_then_red(self):
        shafts = {'221941': 1532.0, '221942': 1000.0}                  # the shafts say third
        stream = self.stream_with(**{'22199A': 3.0, **shafts})
        self.assertEqual(health(stream, 'gear_follow')['level'], GOOD)
        stream.source.readings['22199A'] = 4.0
        stream.step()
        stream.clock.now += 2.0
        stream.step()
        self.assertEqual(health(stream, 'gear_follow')['level'], OK)
        stream.clock.now += 3.0
        stream.step()
        self.assertEqual(health(stream, 'gear_follow')['level'], BAD)
        stream.source.readings['22199A'] = 3.0
        stream.step()
        self.assertEqual(health(stream, 'gear_follow')['level'], GOOD)

    def test_readings_that_have_not_arrived_are_not_graded(self):
        stream = self.stream_with()
        self.assertEqual(health(stream, 'trans_temp')['level'], 'off')


class ShiftComparisonTests(unittest.TestCase):
    def run_shift(self, before, after, kmh, tps):
        source, clock = ScriptedSource(), Clock()
        cfg, tables = model()
        stream = LiveStream(source, cfg=cfg, tables=tables, clock=clock)
        source.readings = {'22199A': float(before), '010D': kmh, '0111': tps, '010C': 3000.0}
        stream.step()
        clock.now += 0.5
        source.readings['22199A'] = float(after)
        stream.step()
        return stream.snapshot()['shifts'], tables

    def test_no_shift_is_recorded_for_the_first_reading(self):
        shifts, _ = self.run_shift(2, 2, 50.0, 30.0)
        self.assertEqual(shifts, [])

    def test_an_upshift_is_compared_with_the_table_at_that_throttle(self):
        shifts, tables = self.run_shift(2, 3, 80.0, 50.0)          # 80 km/h is 49.7 mph at half throttle
        self.assertEqual(len(shifts), 1)
        shift = shifts[0]
        self.assertEqual((shift['kind'], shift['from'], shift['to']), ('up', 2, 3))
        row = tables['upshift'][1]
        expected = row[8]          # 50 percent sits exactly on column 8 of the 6.25 percent axis
        self.assertAlmostEqual(shift['predicted_mph'], expected, places=2)
        self.assertAlmostEqual(shift['mph'], 80.0 * 0.621371, places=2)
        self.assertAlmostEqual(shift['delta_pct'], (80.0 * 0.621371 - expected) / expected * 100, places=1)

    def test_a_shift_close_to_the_table_is_green_and_far_from_it_is_red(self):
        _, tables = model()
        near_kmh = tables['upshift'][1][8] / 0.621371
        shifts, _ = self.run_shift(2, 3, near_kmh * 1.04, 50.0)
        self.assertEqual(shifts[0]['level'], GOOD)
        shifts, _ = self.run_shift(2, 3, near_kmh * 1.40, 50.0)
        self.assertEqual(shifts[0]['level'], BAD)
        shifts, _ = self.run_shift(2, 3, near_kmh * 1.15, 50.0)
        self.assertEqual(shifts[0]['level'], OK)

    def test_a_downshift_is_compared_with_the_downshift_table(self):
        shifts, tables = self.run_shift(4, 3, 60.0, 50.0)
        self.assertEqual((shifts[0]['kind'], shifts[0]['from'], shifts[0]['to']), ('down', 4, 3))
        self.assertAlmostEqual(shifts[0]['predicted_mph'], tables['downshift'][2][8], places=2)


class CursorTests(unittest.TestCase):
    def test_the_cursor_waits_for_both_the_gear_and_the_throttle(self):
        source, clock = ScriptedSource(), Clock()
        stream = LiveStream(source, clock=clock)
        self.assertIsNone(stream.cursor())
        source.readings = {'22199A': 4.0}
        stream.step()
        self.assertIsNone(stream.cursor())
        source.readings['0111'] = 37.5
        stream.step()
        self.assertEqual(stream.cursor(), {'gear': 4, 'tps': 37.5})

    def test_neutral_or_park_gives_no_cursor(self):
        source, clock = ScriptedSource(), Clock()
        source.readings = {'22199A': 0.0, '0111': 3.0}
        stream = LiveStream(source, clock=clock)
        stream.step()
        self.assertIsNone(stream.cursor())


if __name__ == '__main__':
    unittest.main()
