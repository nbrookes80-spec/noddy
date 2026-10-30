import csv
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import pid_view, pids, storage  # noqa: E402
from scanner.data_log import DataLogger  # noqa: E402

COLUMNS = [('010C', '010C Engine RPM (rpm)'), ('0105', '0105 Coolant (C)')]


class DataLoggerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.now = 1_800_000_000.0
        self.log = DataLogger(os.path.join(self.tmp.name, 'Data logs'), clock=lambda: self.now)

    def rows(self):
        with open(self.log.path, newline='') as handle:
            return list(csv.reader(handle))

    def test_file_is_named_by_date_and_time_and_starts_with_a_header(self):
        path = self.log.start(COLUMNS)
        self.assertRegex(os.path.basename(path), r'^\d{4}-\d\d-\d\d_\d\d-\d\d-\d\d\.csv$')
        self.assertEqual(self.rows()[0], ['time_s', 'clock'] + [label for _p, label in COLUMNS])

    def test_a_sensor_keeps_its_last_value_until_it_is_read_again(self):
        self.log.start(COLUMNS)
        self.log.update({'010C': (800.0, 'rpm')})
        self.now += 0.5
        self.log.update({'0105': (71.0, 'C')})
        rows = self.rows()
        self.assertEqual(rows[1][2:], ['800', ''])
        self.assertEqual(rows[2][2:], ['800', '71'])
        self.assertEqual(rows[2][0], '0.500')

    def test_nothing_is_written_when_not_recording(self):
        self.log.update({'010C': (800.0, 'rpm')})
        self.assertEqual(self.log.rows, 0)
        self.assertFalse(self.log.running)

    def test_a_sensor_without_a_column_is_counted_not_misplaced(self):
        self.log.start(COLUMNS)
        self.log.update({'010D': (50.0, 'km/h'), '010C': (900.0, 'rpm')})
        self.assertEqual(self.log.skipped, {'010D'})
        self.assertEqual(self.rows()[1][2:], ['900', ''])

    def test_stop_ends_the_recording_and_a_new_one_gets_a_new_file(self):
        self.log.start(COLUMNS)
        first = self.log.stop()
        self.assertFalse(self.log.running)
        self.now += 5
        self.assertNotEqual(self.log.start(COLUMNS), first)
        self.assertEqual(self.log.stop(), self.log.path)
        self.assertEqual(self.log.stop(), '')


class StorageTests(unittest.TestCase):
    def test_folders_follow_the_requested_layout(self):
        self.assertEqual(storage.folder('/base', storage.DATA_LOGS), '/base/Tuner Tool Info/Data logs')
        self.assertEqual(storage.folder('/base', storage.DEBUG_LOGS), '/base/Tuner Tool Info/Debug logs')

    def test_stamp_is_date_and_time(self):
        self.assertRegex(storage.stamp(), r'^\d{4}-\d\d-\d\d_\d\d-\d\d-\d\d$')

    def test_publishing_off_the_phone_says_so_and_does_not_raise(self):
        with tempfile.NamedTemporaryFile(suffix='.csv') as handle:
            done, message = storage.publish(handle.name, storage.DATA_LOGS)
        self.assertFalse(done)
        self.assertIn('phone', message)
        self.assertFalse(storage.publish('/no/such/file', storage.DATA_LOGS)[0])


class PidViewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, 'pid_view.json')

    def test_choices_survive_a_restart(self):
        views = pid_view.PidViews(self.path)
        views.update('010C', mode='analogue', redline=6300.0, name='Revs')
        again = pid_view.PidViews(self.path)
        self.assertEqual(again.mode('010C'), 'analogue')
        self.assertEqual(again.get('010C')['redline'], 6300.0)
        self.assertEqual(again.mode('0105'), pid_view.DEFAULT_MODE)

    def test_bad_values_are_dropped(self):
        views = pid_view.PidViews(self.path)
        views.update('010C', mode='sparkle', redline=float('nan'), unit='x' * 50)
        self.assertEqual(views.get('010C'), {'unit': 'x' * 12})

    def test_removing_a_choice_with_none_and_reset(self):
        views = pid_view.PidViews(self.path)
        views.update('010C', mode='graph', redline=5000.0, name='Revs')
        views.update('010C', redline=None)
        self.assertNotIn('redline', views.get('010C'))
        views.reset('010C')
        self.assertEqual(views.get('010C'), {'mode': 'graph'})

    def test_apply_uses_the_catalogue_unless_changed_and_ignores_a_bad_range(self):
        views = pid_view.PidViews(self.path)
        pid = pids.get('010C')
        self.assertEqual(views.apply(pid)['name'], pid.name)
        views.update('010C', low=500.0, high=100.0, redline=6000.0)    # low is not below high
        shown = views.apply(pid)
        self.assertEqual((shown['low'], shown['high']), (pid.low, pid.high))
        self.assertEqual(shown['redline'], 6000.0)

    def test_a_damaged_file_gives_defaults(self):
        Path(self.path).write_text('{not json')
        self.assertEqual(pid_view.PidViews(self.path).data, {})


if __name__ == '__main__':
    unittest.main()
