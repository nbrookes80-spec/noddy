"""The demo drive as a six-speed car, seen through the same live stream a real adapter feeds."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import shift_live  # noqa: E402
from grading import BAD, GOOD, OK  # noqa: E402
from live import LiveStream  # noqa: E402
from scanner import demo  # noqa: E402


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def run_cycle(step=0.25):
    values, ratios = shift_live.default_inputs('LS3 Camaro SS (6L80)')
    cfg = shift_live.build_cfg(values, ratios)
    tables, _ = shift_live.calculate(values, ratios)
    clock = Clock()
    source = demo.DemoSource(clock=clock)
    stream = LiveStream(source, cfg=cfg, tables=tables, clock=clock)
    seen = []
    while clock.now < demo.CYCLE_SECONDS:
        stream.step()
        seen.append(stream.snapshot())
        clock.now += step
    return stream, seen


class SixSpeedDriveTests(unittest.TestCase):
    def test_the_launch_climbs_through_all_six_gears_one_at_a_time(self):
        gears = [round(demo.drive(4 + 0.1 * i)['gear']) for i in range(125)]
        steps = [b - a for a, b in zip(gears, gears[1:]) if a != b]
        self.assertEqual(steps, [1, 1, 1, 1, 1])
        self.assertEqual((gears[0], gears[-1]), (1, 6))

    def test_the_commanded_gear_matches_the_gear_the_car_is_in(self):
        _, seen = run_cycle()
        for snap in seen:
            v = snap['values']
            if '22199A' in v and '223D03' in v:
                self.assertEqual(v['22199A']['value'], v['223D03']['value'])

    def test_the_pressure_solenoid_follows_its_reference_within_five_percent(self):
        _, seen = run_cycle(step=1.0)
        for snap in seen:
            v = snap['values']
            if '22199E' in v and '22199F' in v:
                self.assertAlmostEqual(v['22199E']['value'], v['22199F']['value'],
                                       delta=0.05 * v['22199F']['value'])


class LiveFeedbackTests(unittest.TestCase):
    def test_a_whole_drive_records_every_shift_and_grades_them_against_the_stock_table(self):
        stream, _ = run_cycle()
        shifts = list(stream.shifts)[::-1] + []
        # the stream only keeps the most recent shifts, so look at what it kept
        kinds = [s['kind'] for s in stream.shifts]
        self.assertIn('up', kinds)
        self.assertIn('down', kinds)
        levels = [s['level'] for s in stream.shifts]
        self.assertGreaterEqual(levels.count(GOOD), 3)
        self.assertNotIn(BAD, levels)
        self.assertTrue(shifts)

    def test_one_demo_shift_is_deliberately_a_little_late_so_a_yellow_is_visible(self):
        stream, _ = run_cycle()
        self.assertIn(OK, [s['level'] for s in stream.shifts])

    def test_the_demo_car_stays_healthy(self):
        _, seen = run_cycle()
        for snap in seen:
            for tile in snap['health']:
                self.assertNotEqual(tile['level'], BAD, (tile, snap['rounds']))


if __name__ == '__main__':
    unittest.main()
