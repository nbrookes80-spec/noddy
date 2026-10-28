import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tunertoolpro import vehicles  # noqa: E402
from link import obd  # noqa: E402
from live import LiveStream  # noqa: E402
from scanner import pids, profiles  # noqa: E402
from tests.test_stream_wire import FakeAdapter  # noqa: E402
from tests.test_torque_csv import HEAD, row  # noqa: E402


def by_key(key):
    return next(p for p in profiles.built_in() if p.key == key)


class BuiltInTests(unittest.TestCase):
    def tearDown(self):
        pids.use_extras([])
        pids.MONITOR_PIDS[:] = pids.DEFAULT_MONITOR

    def test_holden_pontiac_gm_and_ford_each_have_a_profile(self):
        makes = {p.make for p in profiles.built_in()}
        self.assertTrue({'Holden', 'Pontiac', 'GM', 'Ford'} <= makes)
        keys = {p.key for p in profiles.built_in()}
        self.assertTrue({'holden-ve', 'holden-vf', 'pontiac-g8'} <= keys)

    def test_profile_transmissions_are_ones_the_settings_screen_offers(self):
        for profile in profiles.built_in():
            if profile.transmission:
                found = vehicles.find(profile.transmission)
                self.assertIsNotNone(found, profile.name)
                self.assertIn(profile.make, found.makes, profile.name)

    def test_the_holden_profile_adds_the_torque_lists_without_a_rejection(self):
        summary = profiles.activate(by_key('holden-ve'))
        self.assertEqual(summary['rejected'], [])
        self.assertGreaterEqual(summary['added'], 30)         # the 33 GM readings the scanner did not have
        self.assertIn('224051', pids.CATALOG)                 # ABS front-left wheel speed from Torque
        self.assertFalse(pids.get('224051').verified)
        self.assertIn('22119E', pids.CATALOG)
        self.assertEqual(pids.get('010C').name, 'Engine RPM')   # built-in definitions are untouched

    def test_readings_whose_module_is_unknown_are_listed_but_not_put_on_the_dashboard(self):
        profiles.activate(by_key('holden-ve'))
        self.assertIn('224051', pids.CATALOG)
        self.assertNotIn('224051', pids.MONITOR_PIDS)         # ABS: address unconfirmed
        self.assertIn('22119E', pids.MONITOR_PIDS)

    def test_a_ford_profile_shows_only_standard_readings(self):
        profiles.activate(by_key('ford-generic'))
        self.assertTrue(pids.MONITOR_PIDS)
        self.assertTrue(all(p.startswith('01') for p in pids.MONITOR_PIDS))

    def test_switching_back_removes_the_added_readings(self):
        profiles.activate(by_key('holden-ve'))
        profiles.activate(by_key('obd2'))
        self.assertNotIn('224051', pids.CATALOG)
        self.assertEqual(len(pids.CATALOG), len(pids.BUILT_IN))


class UserCarTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp()) / 'cars'
        self.csv = HEAD + row('[FORD]Trans Temp', '0x221E1C', 'A-40', header='7E1', unit='C', lo='-40', hi='150') \
            + row('Bad', '0x2E1234')

    def tearDown(self):
        pids.use_extras([])
        pids.MONITOR_PIDS[:] = pids.DEFAULT_MONITOR

    def test_a_car_is_saved_from_a_torque_file_and_comes_back(self):
        profile, rejected = profiles.save_user(self.dir, 'x', 'Ford', 'Falcon XR6T', 2010, '6R80 (2009-Current)', self.csv)
        self.assertEqual(profile.name, '2010 Ford Falcon XR6T')
        self.assertEqual([r['name'] for r in rejected], ['Bad'])
        again = profiles.list_user(self.dir)
        self.assertEqual([p.name for p in again], ['2010 Ford Falcon XR6T'])
        self.assertEqual(again[0].transmission, '6R80 (2009-Current)')
        profiles.activate(again[0])
        self.assertIn('221E1C', pids.CATALOG)
        self.assertNotIn('221E1C', pids.MONITOR_PIDS)          # unknown module 7E1, so not auto-polled

    def test_a_file_with_nothing_usable_saves_nothing(self):
        profile, rejected = profiles.save_user(self.dir, 'x', 'Ford', 'Ranger', 2015, '',
                                               HEAD + row('Bad', '0x2E0001'))
        self.assertIsNone(profile)
        self.assertTrue(rejected)
        self.assertEqual(profiles.list_user(self.dir), [])

    def test_a_name_cannot_write_outside_the_cars_folder(self):
        profiles.save_user(self.dir, 'x', '../../etc', '../passwd', 1, '', self.csv)
        files = [p for p in self.dir.parent.rglob('*') if p.is_file()]
        self.assertTrue(files)
        for path in files:
            self.assertEqual(path.parent, self.dir)

    def test_a_damaged_saved_car_is_skipped(self):
        self.dir.mkdir(parents=True)
        (self.dir / 'broken.json').write_text('{oops')
        self.assertEqual(profiles.list_user(self.dir), [])


class WireTests(unittest.TestCase):
    def tearDown(self):
        pids.use_extras([])
        pids.MONITOR_PIDS[:] = pids.DEFAULT_MONITOR

    def test_an_imported_reading_is_polled_on_its_module_and_a_write_service_never_is(self):
        text = HEAD + row('Mine', '0x225150', 'A-40', header='7E2') + row('Evil', '0x2E5151', 'A') \
            + row('Evil2', '0x105152', 'A', start='10 03')
        found, rejected = __import__('scanner.torque_csv', fromlist=['x']).parse(text, 'wire.csv')
        self.assertEqual(len(rejected), 2)
        pids.use_extras(found)
        adapter = FakeAdapter()
        self.addCleanup(adapter.close)
        from tests import test_stream_wire
        test_stream_wire.TCM['225150'] = '62515078'          # 0x78 - 40 = 80
        self.addCleanup(test_stream_wire.TCM.pop, '225150', None)
        elm = adapter.link()
        values, errors = elm.poll(['225150'], headers={'225150': '7E2'})
        self.assertEqual(values['225150'][0], 80.0)
        with self.assertRaises(obd.UnsafeCommand):
            elm.command('2E5151')
        self.assertNotIn('2E5151', adapter.sent())
        for command in adapter.sent():
            self.assertTrue(obd.is_allowed(command), command)


if __name__ == '__main__':
    unittest.main()
