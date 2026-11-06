import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import prefs  # noqa: E402
from scanner import dashboard_layout as layout  # noqa: E402
from scanner import pids  # noqa: E402


def pid(code):
    found = pids.get(code)
    assert found is not None, code
    return found


class GroupTests(unittest.TestCase):
    def test_engine_sensors_are_ecu(self):
        for code in ('010C', '0105', '010E', '0143'):
            self.assertEqual(layout.group_of(pid(code)), 'ECU', code)

    def test_transmission_sensors_are_tcm(self):
        for code in ('221940', '22199A', '221941'):
            self.assertEqual(layout.group_of(pid(code)), 'TCM', code)

    def test_boost_sensors_are_boost(self):
        for code in ('010B', '01BB'):
            self.assertEqual(layout.group_of(pid(code)), 'Boost', code)

    def test_intake_and_throttle_sensors_are_air(self):
        for code in ('010F', '0110', '0133', '0111'):
            self.assertEqual(layout.group_of(pid(code)), 'Air', code)

    def test_fuel_sensors_are_fuel(self):
        for code in ('0106', '012F'):
            self.assertEqual(layout.group_of(pid(code)), 'Fuel', code)


class ArrangeTests(unittest.TestCase):
    def test_groups_come_in_the_fixed_order(self):
        mixed = [pid(c) for c in ('010C', '221940', '0106', '010B', '010F')]
        self.assertEqual([p.pid for p in layout.arrange(mixed, order=[])],
                         ['221940', '010C', '0106', '010F', '010B'])

    def test_the_user_order_holds_inside_a_group(self):
        ecu = [pid(c) for c in ('010C', '0105')]
        self.assertEqual([p.pid for p in layout.arrange(ecu, order=['0105', '010C'])], ['0105', '010C'])

    def test_sensors_the_order_does_not_mention_follow_the_listed_ones(self):
        ecu = [pid(c) for c in ('0105', '010C')]
        self.assertEqual([p.pid for p in layout.arrange(ecu, order=['010C'])], ['010C', '0105'])


class PageTests(unittest.TestCase):
    def sizes(self, count, size):
        return [len(p) for p in layout.pages(list(range(count)), size)]

    def test_pages_hold_four_five_or_six(self):
        self.assertEqual(self.sizes(13, 4), [4, 4, 4, 1])
        self.assertEqual(self.sizes(13, 5), [5, 5, 3])
        self.assertEqual(self.sizes(13, 6), [6, 6, 1])

    def test_any_other_size_falls_back_to_four(self):
        self.assertEqual(self.sizes(9, 7), [4, 4, 1])

    def test_an_empty_list_has_no_pages(self):
        self.assertEqual(layout.pages([]), [])

    def test_the_configured_size_is_used_when_none_is_given(self):
        try:
            layout.configure([], 6)
            self.assertEqual(self.sizes(13, None), [6, 6, 1])
        finally:
            layout.configure([], layout.DEFAULT_PAGE_SIZE)

    def test_runs_keep_each_group_together_in_order(self):
        seq = [pid(c) for c in ('221940', '010C', '0105', '010F')]
        self.assertEqual([(g, [p.pid for p in members]) for g, members in layout.runs(seq)],
                         [('TCM', ['221940']), ('ECU', ['010C', '0105']), ('Air', ['010F'])])


class SavedOrderTests(unittest.TestCase):
    def test_a_saved_order_keeps_only_valid_unique_ids(self):
        self.assertEqual(layout.clean_order(['010c', 'zz', '010C', '22199a', 5]), ['010C', '22199A'])

    def test_a_damaged_order_is_empty(self):
        self.assertEqual(layout.clean_order('010C'), [])


class PrefsTests(unittest.TestCase):
    def round_trip(self, **changes):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'prefs.json'
            choices = dict(prefs.DEFAULTS, **changes)
            prefs.save(path, choices)
            return prefs.load(path)

    def test_page_size_and_order_are_kept(self):
        saved = self.round_trip(dash_page_size=5, dash_order=['010C', '221940'])
        self.assertEqual(saved['dash_page_size'], 5)
        self.assertEqual(saved['dash_order'], ['010C', '221940'])

    def test_a_page_size_outside_four_to_six_is_replaced(self):
        self.assertEqual(self.round_trip(dash_page_size=9)['dash_page_size'], layout.DEFAULT_PAGE_SIZE)


if __name__ == '__main__':
    unittest.main()
