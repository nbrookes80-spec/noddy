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
            'holden-ve', '--wifi', f'127.0.0.1:{fake.port}', '--folder', folder])
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


class FakeSerialPort:
    """Stands in for pyserial: replies come from a script, one prompt-terminated answer per command."""

    def __init__(self, replies):
        self.replies = replies
        self.pending = b''
        self.written = []
        self.in_waiting = 0
        self.timeout = None

    def write(self, data):
        self.written.append(data.decode('ascii').strip())
        self.pending += (self.replies.get(self.written[-1], '?') + '\r>').encode('ascii')

    def flush(self):
        pass

    def read(self, count):
        chunk, self.pending = self.pending[:count], self.pending[count:]
        return chunk

    def close(self):
        pass


class LinkChoiceTests(unittest.TestCase):
    def test_a_saved_bluetooth_or_wifi_link_maps_to_its_name(self):
        self.assertEqual(car_scan.link_from_prefs({'link_kind': 'Bluetooth'}), car_scan.LINK_BLUETOOTH)
        self.assertEqual(car_scan.link_from_prefs({'link_kind': 'Wi-Fi'}), car_scan.LINK_WIFI)

    def test_each_link_gets_its_own_transport(self):
        wifi = car_scan.transport_for(car_scan.LINK_WIFI, wifi='10.0.0.5:3500')
        self.assertIsInstance(wifi, obd.WifiTransport)
        self.assertEqual((wifi.host, wifi.port), ('10.0.0.5', 3500))
        self.assertIsInstance(car_scan.transport_for(car_scan.LINK_BLUETOOTH, bt_address='AA:BB'),
                              obd.BluetoothTransport)
        self.assertIsInstance(car_scan.transport_for(car_scan.LINK_CABLE, serial_port='COM3'), obd.SerialTransport)

    def test_a_link_without_its_address_says_what_is_missing(self):
        with self.assertRaisesRegex(obd.OBDError, 'Bluetooth adapter'):
            car_scan.transport_for(car_scan.LINK_BLUETOOTH)
        with self.assertRaisesRegex(obd.OBDError, 'cable port'):
            car_scan.transport_for(car_scan.LINK_CABLE)
        with self.assertRaisesRegex(obd.OBDError, 'port number'):
            car_scan.transport_for(car_scan.LINK_WIFI, wifi='192.168.0.10:abc')

    def test_a_live_app_connection_is_reused_and_not_reopened(self):
        live = StubElm({})
        elm, owned = car_scan.choose_link(live, {'link_kind': 'Bluetooth', 'bt_address': ''})
        self.assertIs(elm, live)
        self.assertFalse(owned)

    def test_with_no_connection_the_saved_wifi_link_is_opened_and_owned(self):
        fake = FakeElm327()
        self.addCleanup(fake.close)
        prefs = {'link_kind': 'Wi-Fi', 'bt_address': '', 'wifi': f'127.0.0.1:{fake.port}'}
        elm, owned = car_scan.choose_link(None, prefs)
        self.addCleanup(elm.close)
        self.assertTrue(owned)
        self.assertEqual(elm.read('010C')[0], 1726.0)

    def test_a_saved_bluetooth_link_without_an_adapter_is_refused(self):
        with self.assertRaisesRegex(obd.OBDError, 'Bluetooth adapter'):
            car_scan.choose_link(None, {'link_kind': 'Bluetooth', 'bt_address': '', 'wifi': ''})

    def test_a_cable_port_overrides_the_saved_link(self):
        sys.modules['serial'] = FakeSerialModule({'ATZ': 'ELM327 v1.5'})
        self.addCleanup(sys.modules.pop, 'serial', None)
        elm, owned = car_scan.choose_link(None, {'link_kind': 'Wi-Fi', 'wifi': ''}, serial_port='COM3')
        self.addCleanup(elm.close)
        self.assertTrue(owned)
        self.assertIsInstance(elm.transport, obd.SerialTransport)


class FakeSerialModule:
    """A stand-in for the pyserial module, so the cable path can be tested without a port."""

    class SerialException(Exception):
        pass

    def __init__(self, replies):
        self.replies = replies

    def Serial(self, port, baud, **kwargs):
        if port == 'NOPE':
            raise OSError('no such port')
        return FakeSerialPort(self.replies)


class SerialTransportTests(unittest.TestCase):
    def test_a_cable_reads_to_the_prompt_and_round_trips_a_command(self):
        sys.modules['serial'] = FakeSerialModule({'ATZ': 'ELM327 v1.5', '010C': '410C1AF8'})
        self.addCleanup(sys.modules.pop, 'serial', None)
        transport = obd.SerialTransport('COM3')
        transport.open()
        transport.write(b'ATZ\r')
        self.assertEqual(transport.read_until(b'>').strip(), b'ELM327 v1.5')
        transport.write(b'010C\r')
        self.assertEqual(transport.read_until(b'>').strip(), b'410C1AF8')
        transport.close()

    def test_a_port_that_will_not_open_is_an_obd_error(self):
        sys.modules['serial'] = FakeSerialModule({})
        self.addCleanup(sys.modules.pop, 'serial', None)
        with self.assertRaisesRegex(obd.OBDError, 'NOPE'):
            obd.SerialTransport('NOPE').open()

    def test_a_script_run_on_a_cable_without_pyserial_says_so(self):
        sys.modules['serial'] = None   # import fails, as on a machine without pyserial
        self.addCleanup(sys.modules.pop, 'serial', None)
        args = scan_car.build_parser().parse_args(['holden-ve', '--serial', 'COM3'])
        lines = []
        self.assertEqual(scan_car.run(args, out=lines.append), 1)
        self.assertIn('pyserial', lines[-1])


class BluetoothOnDesktopTests(unittest.TestCase):
    def test_bluetooth_is_refused_clearly_off_the_phone(self):
        args = scan_car.build_parser().parse_args(['holden-ve', '--link', 'bluetooth', '--bluetooth', 'AA:BB:CC:DD:EE:FF'])
        lines = []
        self.assertEqual(scan_car.run(args, out=lines.append), 1)
        self.assertIn('Android app', lines[-1])


class FollowsTheAppLinkTests(unittest.TestCase):
    def write_prefs(self, choices):
        path = Path(tempfile.mkdtemp()) / 'prefs.json'
        path.write_text(json.dumps(choices))
        return str(path)

    def test_the_saved_wifi_link_and_address_are_used(self):
        fake = FakeElm327()
        self.addCleanup(fake.close)
        prefs = self.write_prefs({'link_kind': 'Wi-Fi', 'bt_address': '', 'wifi': f'127.0.0.1:{fake.port}'})
        folder = tempfile.mkdtemp()
        args = scan_car.build_parser().parse_args(['holden-ve', '--prefs', prefs, '--folder', folder])
        lines = []
        self.assertEqual(scan_car.run(args, out=lines.append), 0, lines)
        self.assertTrue(car_scan.load_scan(folder, 'holden-ve')['complete'])

    def test_a_saved_bluetooth_link_is_used_when_the_app_chose_it(self):
        prefs = self.write_prefs({'link_kind': 'Bluetooth', 'bt_address': 'AA:BB:CC:DD:EE:FF', 'wifi': ''})
        args = scan_car.build_parser().parse_args(['holden-ve', '--prefs', prefs])
        lines = []
        self.assertEqual(scan_car.run(args, out=lines.append), 1)
        self.assertIn('Android app', lines[-1])


if __name__ == '__main__':
    unittest.main()
