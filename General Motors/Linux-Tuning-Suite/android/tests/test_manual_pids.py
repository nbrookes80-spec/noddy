import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import manual_pids, profiles, torque_csv  # noqa: E402
from scanner import pids  # noqa: E402


def entry(**changes):
    row = {'pid': '2219AA', 'name': 'Test sensor', 'unit': 'kPa', 'equation': 'A*2', 'low': 0, 'high': 600,
           'header': 'Auto'}
    row.update(changes)
    return row


class BuildTests(unittest.TestCase):
    def test_a_good_entry_becomes_an_unconfirmed_pid(self):
        pid = manual_pids.build(entry())
        self.assertEqual(pid.pid, '2219AA')
        self.assertEqual(pid.unit, 'kPa')
        self.assertEqual(pid.kind, 'byte')
        self.assertEqual(pid.parse('10'), 32.0)
        self.assertFalse(pid.verified)
        self.assertEqual(pid.source, manual_pids.SOURCE)

    def test_a_formula_that_reads_two_bytes_is_a_word(self):
        pid = manual_pids.build(entry(equation='(A*256+B)/4'))
        self.assertEqual(pid.kind, 'word')
        self.assertEqual(pid.parse('1AF8'), 1726.0)

    def test_the_formula_cannot_run_code(self):
        for equation in ('__import__("os")', 'open("x")', ''):
            with self.subTest(equation=equation):
                with self.assertRaises(torque_csv.Refused):
                    manual_pids.build(entry(equation=equation))

    def test_only_mode_01_and_22_ids_are_accepted(self):
        for pid in ('0902', '04', '2F1234', 'XYZ'):
            with self.subTest(pid=pid):
                with self.assertRaises(torque_csv.Refused):
                    manual_pids.build(entry(pid=pid))

    def test_limits_must_be_in_order(self):
        with self.assertRaises(torque_csv.Refused):
            manual_pids.build(entry(low=10, high=5))

    def test_an_unknown_module_is_refused(self):
        with self.assertRaises(torque_csv.Refused):
            manual_pids.build(entry(header='7EF'))
        self.assertEqual(manual_pids.build(entry(header='7e2')).header, '7E2')


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def test_saved_entries_come_back_for_the_same_profile_only(self):
        manual_pids.save(self.folder, 'holden-ve', [entry()])
        self.assertEqual([p.pid for p in manual_pids.pids_for(self.folder, 'holden-ve')], ['2219AA'])
        self.assertEqual(manual_pids.pids_for(self.folder, 'obd2'), [])

    def test_one_bad_entry_saves_nothing(self):
        manual_pids.save(self.folder, 'holden-ve', [entry()])
        with self.assertRaises(torque_csv.Refused):
            manual_pids.save(self.folder, 'holden-ve', [entry(), entry(pid='2219AB', equation='open("x")')])
        self.assertEqual([p.pid for p in manual_pids.pids_for(self.folder, 'holden-ve')], ['2219AA'])

    def test_the_same_pid_twice_is_refused(self):
        with self.assertRaises(torque_csv.Refused):
            manual_pids.save(self.folder, 'holden-ve', [entry(), entry(pid='2219aa')])

    def test_a_damaged_file_is_treated_as_empty(self):
        Path(self.folder, manual_pids.FILE_NAME).write_text('{not json', encoding='utf-8')
        self.assertEqual(manual_pids.load(self.folder), {})
        self.assertEqual(manual_pids.pids_for(self.folder, 'holden-ve'), [])

    def test_an_entry_that_no_longer_checks_out_is_skipped(self):
        Path(self.folder, manual_pids.FILE_NAME).write_text(
            json.dumps({'holden-ve': [entry(), entry(pid='2219AB', equation='open("x")')]}), encoding='utf-8')
        self.assertEqual([p.pid for p in manual_pids.pids_for(self.folder, 'holden-ve')], ['2219AA'])


class ActivateTests(unittest.TestCase):
    def tearDown(self):
        pids.use_extras([])

    def test_a_manual_pid_is_added_and_replaces_an_imported_row(self):
        profile = profiles.built_in()[0]
        imported, _ = profiles.load_pids(profile)
        target = next(p.pid for p in imported if p.pid not in pids.BUILT_IN)   # built-in ids always win
        manual = [manual_pids.build(entry(pid=target, name='Mine'))]
        profiles.activate(profile, manual=manual)
        self.assertEqual(pids.get(target).name, 'Mine')

    def test_a_manual_pid_stays_on_the_dashboard_when_the_car_check_never_asked_for_it(self):
        profile = profiles.built_in()[0]
        car_check = {'complete': True, 'answered': {'010C': {'header': 'Auto'}}}   # ran before the PID existed
        manual = [manual_pids.build(entry(pid='2219AA', name='Mine'))]
        profiles.activate(profile, scan=car_check, manual=manual)
        self.assertIn('2219AA', pids.MONITOR_PIDS)
