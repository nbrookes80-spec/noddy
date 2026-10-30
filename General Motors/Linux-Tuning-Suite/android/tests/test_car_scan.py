import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from link import obd  # noqa: E402
from scanner import car_scan, pids, profiles  # noqa: E402
from tests.test_obd import FakeElm327  # noqa: E402
from tools import scan_car  # noqa: E402


class StubElm:
    """Answers each reading from a table; anything missing gives no reply, and 'lost' stops the link."""

    def __init__(self, answers, lost_at=None):
        self.answers = answers
        self.lost_at = lost_at
        self.calls = []
        self.headers = {}

    def read(self, pid):
        self.calls.append(pid)
        if pid == self.lost_at:
            raise obd.AdapterLost('gone')
        if pid not in self.answers:
            raise obd.OBDError(f'{pid}: no reply')
        value, header = self.answers[pid]
        self.headers[pid] = header
        return value, 'unit'

    def header_for(self, pid):
        return self.headers.get(pid)


class FakeTransport:
    """An adapter that answers the reading only on the header it is listening to."""

    def __init__(self, answers_by_header):
        self.answers = answers_by_header
        self.header = '7DF'
        self.reply = ''

    def open(self):
        pass

    def close(self):
        pass

    def write(self, data):
        command = data.decode('ascii').strip()
        if command.startswith('ATSH'):
            self.header = command[4:]
            self.reply = 'OK'
        elif command.startswith('AT'):
            self.reply = 'OK'
        else:
            self.reply = self.answers.get(self.header, {}).get(command, 'NO DATA')

    def read_until(self, prompt=b'>'):
        return (self.reply + '\r>').encode('ascii')


class ScanIdsTests(unittest.TestCase):
    def test_only_valid_catalogued_readings_are_tried_once(self):
        ids = car_scan.scan_ids(['010C', 'not-a-pid', '010C', '99ZZ'])
        self.assertEqual(ids.count('010C'), 1)
        self.assertNotIn('not-a-pid', ids)
        self.assertTrue(all(pids.valid_id(p) for p in ids))

    def test_mode01_only_drops_mode22(self):
        ids = car_scan.scan_ids([], mode01_only=True)
        self.assertTrue(ids)
        self.assertTrue(all(p.startswith('01') for p in ids))


class ScanTests(unittest.TestCase):
    def test_answered_and_silent_readings_are_recorded_with_their_module(self):
        elm = StubElm({'010C': ((1726.0), '7E0'), '010D': (60, 'Auto')})
        result = car_scan.scan(elm, ['010C', '010D', '0105'])
        self.assertEqual(sorted(result['answered']), ['010C', '010D'])
        self.assertEqual(result['answered']['010C']['header'], '7E0')
        self.assertEqual(result['answered']['010D']['header'], 'Auto')
        self.assertEqual(result['silent'], ['0105'])
        self.assertTrue(result['complete'])

    def test_a_lost_adapter_stops_the_scan_and_marks_it_incomplete(self):
        elm = StubElm({'010C': (1, '7E0')}, lost_at='010D')
        result = car_scan.scan(elm, ['010C', '010D', '0105'])
        self.assertFalse(result['complete'])
        self.assertEqual(elm.calls, ['010C', '010D'])

    def test_progress_is_reported_for_each_reading(self):
        seen = []
        car_scan.scan(StubElm({}), ['010C', '010D'], progress=lambda i, n, pid: seen.append((i, n, pid)))
        self.assertEqual(seen, [(0, 2, '010C'), (1, 2, '010D')])

    def test_a_reading_on_the_transmission_module_is_found_and_its_header_kept(self):
        transport = FakeTransport({'7E2': {'22194F': '62194F78'}})
        elm = obd.Elm327(transport)
        elm.open()
        result = car_scan.scan(elm, ['22194F'])
        self.assertEqual(result['answered']['22194F']['header'], '7E2')
        self.assertEqual(car_scan.headers(result), {'22194F': '7E2'})


class SavedScanTests(unittest.TestCase):
    def setUp(self):
        self.folder = Path(tempfile.mkdtemp())

    def complete(self):
        return car_scan.scan(StubElm({'010C': (1, '7E0')}), ['010C'])

    def test_a_scan_comes_back_the_same_after_saving(self):
        car_scan.save_scan(self.folder, 'holden-ve', self.complete())
        again = car_scan.load_scan(self.folder, 'holden-ve')
        self.assertEqual(again['answered']['010C']['header'], '7E0')

    def test_a_cut_off_scan_does_not_replace_a_complete_one(self):
        car_scan.save_scan(self.folder, 'holden-ve', self.complete())
        cut = car_scan.scan(StubElm({}, lost_at='010C'), ['010C'])
        self.assertIsNone(car_scan.save_scan(self.folder, 'holden-ve', cut))
        self.assertTrue(car_scan.load_scan(self.folder, 'holden-ve')['complete'])

    def test_a_cut_off_scan_is_kept_when_nothing_is_saved_yet(self):
        cut = car_scan.scan(StubElm({}, lost_at='010C'), ['010C'])
        self.assertIsNotNone(car_scan.save_scan(self.folder, 'holden-ve', cut))
        self.assertFalse(car_scan.load_scan(self.folder, 'holden-ve')['complete'])

    def test_a_damaged_or_missing_scan_is_none(self):
        self.assertIsNone(car_scan.load_scan(self.folder, 'holden-ve'))
        (self.folder / f'holden-ve{car_scan.SCAN_SUFFIX}').write_text('{not json')
        self.assertIsNone(car_scan.load_scan(self.folder, 'holden-ve'))

    def test_a_scan_with_a_bad_reading_id_is_rejected(self):
        bad = self.complete()
        bad['answered']['zz'] = {'name': 'x', 'header': 'Auto', 'unit': '', 'sample': 0}
        (self.folder / f'holden-ve{car_scan.SCAN_SUFFIX}').write_text(json.dumps(bad))
        self.assertIsNone(car_scan.load_scan(self.folder, 'holden-ve'))


class EnforceTests(unittest.TestCase):
    def test_readings_the_car_did_not_answer_are_hidden(self):
        result = car_scan.scan(StubElm({'010C': (1, 'Auto')}), ['010C', '010D'])
        shown, hidden = car_scan.enforce(['010C', '010D'], result)
        self.assertEqual(shown, ['010C'])
        self.assertEqual(hidden, {'010D': 'no reply from this car'})

    def test_without_a_complete_scan_nothing_is_hidden(self):
        shown, hidden = car_scan.enforce(['010C', '010D'], None)
        self.assertEqual(shown, ['010C', '010D'])
        self.assertEqual(hidden, {})

    def test_a_cut_off_scan_does_not_hide_anything(self):
        cut = car_scan.scan(StubElm({}, lost_at='010C'), ['010C', '010D'])
        shown, _ = car_scan.enforce(['010C', '010D'], cut)
        self.assertEqual(shown, ['010C', '010D'])


class ActivateWithScanTests(unittest.TestCase):
    def tearDown(self):
        profiles.activate(profiles.built_in()[-1])   # back to the plain catalogue

    def test_the_dashboard_lists_only_what_the_car_answered(self):
        profile = profiles.built_in()[0]
        result = car_scan.scan(StubElm({'010C': (1, 'Auto'), '22194F': (80, '7E2')}),
                               ['010C', '010D', '22194F'])
        summary = profiles.activate(profile, scan=result)
        self.assertTrue(summary['checked'])
        self.assertIn('010C', pids.MONITOR_PIDS)
        self.assertNotIn('010D', pids.MONITOR_PIDS)
        self.assertEqual(summary['headers'], {'22194F': '7E2'})
        self.assertIn('010D', summary['hidden'])

    def test_without_a_scan_the_dashboard_is_unchanged(self):
        summary = profiles.activate(profiles.built_in()[0])
        self.assertFalse(summary['checked'])
        self.assertEqual(summary['hidden'], {})
        self.assertIn('010D', pids.MONITOR_PIDS)


class ScriptTests(unittest.TestCase):
    def test_the_script_scans_saves_and_reports_against_the_adapter(self):
        fake = FakeElm327()
        self.addCleanup(fake.close)
        folder = tempfile.mkdtemp()
        args = scan_car.build_parser().parse_args([
            'holden-ve', '--host', '127.0.0.1', '--port', str(fake.port), '--folder', folder])
        out = io.StringIO()
        with redirect_stdout(out):
            code = scan_car.run(args, out=print)
        self.assertEqual(code, 0, out.getvalue())
        saved = car_scan.load_scan(folder, 'holden-ve')
        self.assertTrue(saved['complete'])
        self.assertIn('010C', saved['answered'])
        self.assertIn('010F', saved['silent'])

    def test_an_unknown_profile_is_refused(self):
        args = scan_car.build_parser().parse_args(['no-such-car'])
        lines = []
        self.assertEqual(scan_car.run(args, out=lines.append), 2)
        self.assertIn('No profile', lines[0])

    def test_the_list_option_names_the_profiles(self):
        args = scan_car.build_parser().parse_args(['--list'])
        lines = []
        self.assertEqual(scan_car.run(args, out=lines.append), 0)
        self.assertTrue(any('holden-ve' in line for line in lines))


if __name__ == '__main__':
    unittest.main()
