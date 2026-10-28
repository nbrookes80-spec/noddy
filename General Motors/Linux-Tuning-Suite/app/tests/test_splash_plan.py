import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tunertoolpro.splash_plan import SplashPlan  # noqa: E402


class SplashPlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = SplashPlan(['side', 'bay'], hold_ms=1000, fade_ms=250)

    def test_total_time_is_every_picture_fading_in_holding_and_fading_out(self):
        self.assertEqual(self.plan.total_ms(), 2 * (250 + 1000 + 250))

    def test_first_picture_fades_in_from_nothing(self):
        self.assertEqual(self.plan.at(0), ('side', 0.0))
        self.assertEqual(self.plan.at(125), ('side', 0.5))

    def test_picture_is_fully_shown_while_held(self):
        self.assertEqual(self.plan.at(750), ('side', 1.0))

    def test_second_picture_follows_the_first(self):
        name, opacity = self.plan.at(1500 + 125)
        self.assertEqual((name, opacity), ('bay', 0.5))

    def test_picture_fades_out_before_the_next(self):
        self.assertEqual(self.plan.at(1500 - 125), ('side', 0.5))

    def test_nothing_is_shown_once_finished(self):
        self.assertIsNone(self.plan.at(self.plan.total_ms()))
        self.assertIsNone(self.plan.at(10_000))

    def test_no_pictures_means_nothing_to_show(self):
        empty = SplashPlan([])
        self.assertEqual(empty.total_ms(), 0)
        self.assertIsNone(empty.at(0))


if __name__ == '__main__':
    unittest.main()
