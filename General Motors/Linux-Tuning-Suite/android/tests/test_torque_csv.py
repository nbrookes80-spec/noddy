import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import pids, torque_csv  # noqa: E402

DATA = Path(__file__).parent / 'data'
HEAD = '"Name", "ShortName", "ModeAndPID", "Equation", "Min Value", "Max Value", "Units", "Header", "startDiagnostic", "stopDiagnostic", "scale","minimumRefreshDelayMillis"\n'


def row(name='Test', pid='0x221234', eq='A', header='Auto', start='', stop='', lo='0', hi='100', unit='x'):
    return f'"{name}","T","{pid}","{eq}",{lo},{hi},"{unit}","{header}","{start}","{stop}",1,0\n'


def parse(*rows):
    return torque_csv.parse(HEAD + ''.join(rows), source='test.csv')


class RealFileTests(unittest.TestCase):
    def test_both_phone_exports_load_and_only_repeated_ids_are_dropped(self):
        for name, total in (('torque_gm_predefined.csv', 87), ('torque_e38_t43_v5.csv', 30)):
            found, rejected = torque_csv.parse((DATA / name).read_text(), source=name)
            self.assertTrue(all('already' in r['reason'] for r in rejected), (name, rejected))
            self.assertEqual(len(found) + len(rejected), total, name)
            self.assertGreaterEqual(len(found), total - 2, name)

    def test_a_known_equation_decodes_like_torque_would(self):
        found, _ = torque_csv.parse((DATA / 'torque_gm_predefined.csv').read_text(), source='x')
        by_id = {p.pid: p for p in found}
        self.assertAlmostEqual(by_id['221997'].parse('50'), 2.0)   # A/40
        self.assertAlmostEqual(by_id['22162F'].parse('8100'), (0x8100 - 32768) * 0.15625 / 10)     # (A<8)+B form


class Accepted(unittest.TestCase):
    def test_mode_01_and_22_reads_are_accepted_with_their_details(self):
        found, rejected = parse(row('[GM]Coolant', '0x2212AB', 'A-40', unit='C', lo='-40', hi='215'))
        self.assertEqual(rejected, [])
        pid = found[0]
        self.assertEqual((pid.pid, pid.name, pid.unit, pid.low, pid.high), ('2212AB', 'Coolant', 'C', -40.0, 215.0))
        self.assertEqual(pid.parse('78'), 80.0)
        self.assertEqual(pid.mode, '22')
        self.assertEqual(pid.source, 'test.csv')
        self.assertFalse(pid.verified)

    def test_a_mode_01_id_without_the_0x_prefix_is_accepted(self):
        found, _ = parse(row('RPM', '010C', '((A*256)+B)/4'))
        self.assertEqual((found[0].pid, found[0].mode, found[0].kind), ('010C', '01', 'word'))
        self.assertEqual(found[0].parse('1AF8'), 1726.0)

    def test_the_number_of_bytes_follows_the_letters_used(self):
        found, _ = parse(row('One', '0x220001', 'A'), row('Two', '0x220002', '(A<8)+B'),
                         row('Three', '0x220003', '(A*65536)+(B*256)+C'), row('Four', '0x220004', 'A+D'))
        self.assertEqual([p.kind for p in found], ['byte', 'word', 'bytes3', 'dword'])
        self.assertEqual(found[2].parse('010203'), 65536 + 512 + 3)

    def test_signed_and_shifts_work(self):
        found, _ = parse(row('S', '0x220005', '((signed(A)*256)+B)/8'))
        self.assertEqual(found[0].parse('FF00'), -256 / 8)
        self.assertEqual(found[0].parse('0100'), 256 / 8)

    def test_a_module_the_app_knows_keeps_its_address_and_an_unknown_one_is_flagged(self):
        found, _ = parse(row('A', '0x220001', header='7E2'), row('B', '0x220002', header='ABS'),
                         row('C', '0x220003', header=''))
        self.assertEqual([p.header for p in found], ['7E2', 'Auto', 'Auto'])
        self.assertIn('ABS', found[1].description)       # says which module it wanted and that it is unconfirmed
        self.assertNotIn('ABS', found[2].description)

    def test_the_name_tag_becomes_the_category(self):
        found, _ = parse(row('[GM]Trans Temp', '0x22194F'), row('Plain', '0x220001'))
        self.assertEqual((found[0].name, found[0].category), ('Trans Temp', 'Torque import: GM'))
        self.assertEqual(found[1].category, 'Torque import')


class Refused(unittest.TestCase):
    def reason(self, **kw):
        found, rejected = parse(row(**kw))
        self.assertEqual(found, [], kw)
        self.assertEqual(len(rejected), 1, kw)
        return rejected[0]['reason']

    def test_anything_but_mode_01_and_22_is_refused(self):
        for pid in ('0x2E1234', '0x141234', '0x041234', '0x101234', '0x271234', '0x311234', '0x3B1234', '0x0900', '03'):
            self.assertIn('Mode', self.reason(pid=pid), pid)

    def test_a_malformed_id_is_refused(self):
        for pid in ('0x22', '0x22ZZZZ', '0x2212345', '', "0x22'; ATZ", '0x01', '0x01ABCD'):
            self.reason(pid=pid)

    def test_start_and_stop_commands_are_never_accepted(self):
        self.assertIn('startDiagnostic', self.reason(start='10 03'))
        self.assertIn('stopDiagnostic', self.reason(stop='ATZ'))

    def test_hostile_equations_are_refused_and_nothing_runs(self):
        for eq in ('__import__("os").system("x")', 'open("/etc/passwd")', 'A.__class__', '(lambda: 1)()', 'A**9999999',
                   'A if A else B', 'A<B', '[A]', 'A;B', 'exec("1")', 'E', 'A' * 300, 'signed(A, B)', 'A<<99', ''):
            self.reason(eq=eq)

    def test_a_divide_by_zero_reads_as_no_value_not_an_error(self):
        found, _ = parse(row('Z', '0x220009', 'A/(B-B)'))
        self.assertIsNone(found[0].parse('0102'))

    def test_bad_numbers_are_refused(self):
        self.reason(lo='abc')

    def test_a_good_row_survives_next_to_bad_ones_and_the_line_is_reported(self):
        found, rejected = parse(row('Good', '0x220001'), row('Bad', '0x2E0001'), row('Good2', '0x220002'))
        self.assertEqual([p.pid for p in found], ['220001', '220002'])
        self.assertEqual((rejected[0]['line'], rejected[0]['name']), (3, 'Bad'))

    def test_files_that_are_not_a_torque_csv_are_refused_whole(self):
        for text in ('', 'hello', 'a,b,c\n1,2,3\n', 'x' * 2_000_000):
            found, rejected = torque_csv.parse(text, source='x')
            self.assertEqual(found, [])
            self.assertTrue(rejected)

    def test_repeats_within_a_file_keep_the_first(self):
        found, rejected = parse(row('First', '0x220001'), row('Again', '0x220001'))
        self.assertEqual([p.name for p in found], ['First'])
        self.assertIn('already', rejected[0]['reason'])


class Catalogue(unittest.TestCase):
    def tearDown(self):
        pids.use_extras([])

    def test_imported_pids_join_the_catalogue_but_never_replace_a_built_in_one(self):
        found, _ = parse(row('Mine', '0x229999'), row('RPM again', '010C', 'A'))
        skipped = pids.use_extras(found)
        self.assertIn('229999', pids.CATALOG)
        self.assertEqual(pids.get('010C').name, 'Engine RPM')
        self.assertEqual(skipped, ['010C'])
        pids.use_extras([])
        self.assertNotIn('229999', pids.CATALOG)


if __name__ == '__main__':
    unittest.main()
