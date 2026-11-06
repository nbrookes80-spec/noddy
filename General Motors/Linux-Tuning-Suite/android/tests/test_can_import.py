import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import can_import, can_replay, dbc, pids  # noqa: E402
from tunertoolpro.canbus.frames import Frame  # noqa: E402

DBC_TEXT = '''VERSION ""

BU_: ECM TCM

BO_ 201 ENGINE: 8 ECM
 SG_ RPM : 0|16@1+ (0.25,0) [0|16383.75] "rpm" TCM
 SG_ Coolant : 16|8@1- (1,-40) [-40|215] "C" TCM

BO_ 300 MUXED: 8 ECM
 SG_ Selector M : 0|8@1+ (1,0) [0|255] "" TCM
 SG_ Low m1 : 8|8@1+ (1,0) [0|255] "kPa" TCM
 SG_ High m2 : 8|8@1+ (2,0) [0|510] "kPa" TCM

BO_ 400 BIGENDIAN: 8 TCM
 SG_ Speed : 7|16@0+ (0.5,0) [0|32767] "rpm" ECM
'''


def frame(can_id, data, stamp, extended=False):
    return Frame(can_id, bytes(data), extended, stamp)


class DbcParseTests(unittest.TestCase):
    def setUp(self):
        self.signals = {s.name: s for s in dbc.parse(DBC_TEXT)}

    def test_messages_and_signals_are_read(self):
        self.assertEqual(sorted(self.signals), ['Coolant', 'High', 'Low', 'RPM', 'Selector', 'Speed'])
        rpm = self.signals['RPM']
        self.assertEqual((rpm.message_id, rpm.start, rpm.length, rpm.big_endian, rpm.signed), (201, 0, 16, False, False))
        self.assertAlmostEqual(rpm.factor, 0.25)
        self.assertEqual(rpm.unit, 'rpm')

    def test_signed_and_offset_signals_are_read(self):
        coolant = self.signals['Coolant']
        self.assertTrue(coolant.signed)
        self.assertEqual(coolant.offset, -40)

    def test_multiplexer_roles_are_read(self):
        self.assertEqual(self.signals['Selector'].mux_role, 'M')
        self.assertEqual((self.signals['Low'].mux_role, self.signals['Low'].mux_value), ('m', 1))
        self.assertEqual((self.signals['High'].mux_role, self.signals['High'].mux_value), ('m', 2))

    def test_big_endian_flag_and_extended_ids_are_read(self):
        self.assertTrue(self.signals['Speed'].big_endian)
        extended = dbc.parse('BO_ 2147483857 X: 8 ECM\n SG_ A : 0|8@1+ (1,0) [0|255] "" TCM\n')[0]
        self.assertTrue(extended.extended)
        self.assertEqual(extended.message_id, 209)   # 2147483857 is 0x80000000 plus 209


class RawValueTests(unittest.TestCase):
    def signal(self, start, length, big_endian=False, signed=False):
        return dbc.Signal(1, False, 'M', 'S', start, length, big_endian, signed, 1.0, 0.0, 0, 0, '')

    def test_intel_bytes_read_least_significant_first(self):
        self.assertEqual(dbc.raw_value(self.signal(0, 16), bytes([0x34, 0x12])), 0x1234)

    def test_intel_field_inside_a_byte(self):
        self.assertEqual(dbc.raw_value(self.signal(4, 4), bytes([0xA5])), 0xA)

    def test_motorola_bytes_read_most_significant_first(self):
        self.assertEqual(dbc.raw_value(self.signal(7, 16, big_endian=True), bytes([0x12, 0x34])), 0x1234)

    def test_signed_values_go_negative(self):
        self.assertEqual(dbc.raw_value(self.signal(0, 8, signed=True), bytes([0xFF])), -1)

    def test_a_short_frame_gives_no_value(self):
        self.assertIsNone(dbc.raw_value(self.signal(8, 16), bytes([0x01, 0x02])))


class DecodeTests(unittest.TestCase):
    def setUp(self):
        self.signals = dbc.parse(DBC_TEXT)

    def test_values_are_scaled_and_timed_from_the_first_frame(self):
        frames = [frame(201, [0x10, 0x27, 0x28], 5.0), frame(201, [0x20, 0x4E, 0x28], 6.0)]
        replay = can_replay.decode(frames, self.signals)
        entry = next(v for k, v in replay.series.items() if v[0].name == 'RPM')
        self.assertEqual(entry[1], [0.0, 1.0])
        self.assertEqual(entry[2], [0x2710 * 0.25, 0x4E20 * 0.25])

    def test_a_multiplexed_signal_only_reads_when_its_multiplexer_matches(self):
        frames = [frame(300, [1, 50, 0], 0.0), frame(300, [2, 60, 0], 1.0)]
        replay = can_replay.decode(frames, self.signals)
        by_name = {v[0].name: v for v in replay.series.values()}
        self.assertEqual(by_name['Low'][2], [50])
        self.assertEqual(by_name['High'][2], [120])

    def test_a_log_with_no_matching_message_has_no_series(self):
        replay = can_replay.decode([frame(0x7E8, [1, 2, 3], 0.0)], self.signals)
        self.assertEqual(replay.series, {})

    def test_a_log_over_the_reading_limit_is_refused(self):
        original = can_replay.MAX_SAMPLES
        can_replay.MAX_SAMPLES = 3
        try:
            frames = [frame(201, [0, 0, 0], float(i)) for i in range(5)]
            with self.assertRaises(can_replay.TooLong):
                can_replay.decode(frames, self.signals)
        finally:
            can_replay.MAX_SAMPLES = original


class ReplaySourceTests(unittest.TestCase):
    def make(self, loop=True):
        signals = dbc.parse(DBC_TEXT)
        frames = [frame(201, [0x10, 0x27, 0x28], 0.0), frame(201, [0x20, 0x4E, 0x28], 2.0)]
        replay = can_replay.decode(frames, signals)
        clock = {'now': 100.0}
        source = can_replay.ReplaySource(replay, clock=lambda: clock['now'], loop=loop)
        return source, clock, replay

    def test_poll_returns_the_reading_held_at_the_replay_time(self):
        source, clock, replay = self.make()
        pid_id = next(k for k, v in replay.series.items() if v[0].name == 'RPM')
        clock['now'] = 100.5
        values, errors = source.poll([pid_id])
        self.assertEqual(values[pid_id], (0x2710 * 0.25, 'rpm'))
        self.assertEqual(errors, {})

    def test_the_log_loops_back_to_its_start(self):
        source, clock, replay = self.make()
        pid_id = next(k for k, v in replay.series.items() if v[0].name == 'RPM')
        clock['now'] = 102.5     # 2.5 s in, span is 2 s: the log is at 0.5 s again
        self.assertEqual(source.poll([pid_id])[0][pid_id][0], 0x2710 * 0.25)

    def test_without_loop_the_last_reading_is_held(self):
        source, clock, replay = self.make(loop=False)
        pid_id = next(k for k, v in replay.series.items() if v[0].name == 'RPM')
        clock['now'] = 1000.0
        self.assertEqual(source.poll([pid_id])[0][pid_id][0], 0x4E20 * 0.25)

    def test_unknown_ids_are_ignored_and_the_adapter_never_gets_them(self):
        source, clock, replay = self.make()
        self.assertEqual(source.poll(['010C'])[0], {})
        for pid_id in replay.series:
            self.assertFalse(pids.valid_id(pid_id), pid_id)

    def test_listen_gives_the_log_frames_from_the_last_seconds(self):
        source, clock, replay = self.make()
        clock['now'] = 101.0    # replay time 1.0 s: the frame at 0 s is inside the last 1.5 s
        self.assertEqual([f.timestamp for f in source.listen(1.5)], [0.0])
        source, clock, replay = self.make(loop=False)
        clock['now'] = 102.0    # replay time 2.0 s: only the frame at 2 s is inside the last second
        self.assertEqual([f.timestamp for f in source.listen(1.0)], [2.0])


class CatalogueEntryTests(unittest.TestCase):
    def test_each_signal_gets_its_dbc_range_and_is_marked_imported(self):
        replay = can_replay.decode([frame(201, [0, 0, 0], 0.0)], dbc.parse(DBC_TEXT))
        entries = can_replay.catalogue_entries(replay)
        rpm = next(p for p in entries if p.name == 'RPM')
        self.assertEqual((rpm.low, rpm.high, rpm.unit), (0, 16383.75, 'rpm'))
        self.assertEqual(rpm.category, 'Imported')
        self.assertFalse(rpm.verified)

    def test_a_signal_with_no_range_takes_the_range_seen_in_the_log(self):
        text = 'BO_ 5 SENSOR: 8 ECM\n SG_ Level : 0|8@1+ (1,0) [0|0] "" TCM\n'
        replay = can_replay.decode([frame(5, [7], 0.0), frame(5, [9], 1.0)], dbc.parse(text))
        level = can_replay.catalogue_entries(replay)[0]
        self.assertEqual((level.low, level.high), (7, 9))


class LoadTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()

    def write(self, name, text):
        path = os.path.join(self.folder, name)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(text)
        return path

    def test_a_candump_log_and_its_dbc_load_together(self):
        log = self.write('capture.log', '(0.000000) can0 0C9#1027280000000000\n(0.500000) can0 0C9#2000280000000000\n')
        dbc_path = self.write('car.dbc', DBC_TEXT)
        loaded = can_import.load(log, dbc_path, clock=lambda: 0.0)
        self.assertEqual(loaded.name, 'capture.log')
        self.assertEqual(loaded.frames, 2)
        self.assertIn('Playing', loaded.describe())

    def test_a_log_with_no_frames_is_refused_with_a_message(self):
        log = self.write('empty.log', 'nothing here\n')
        with self.assertRaises(can_import.ImportProblem) as caught:
            can_import.load(log, self.write('car.dbc', DBC_TEXT))
        self.assertIn('No CAN frames', str(caught.exception))

    def test_a_dbc_with_no_signals_is_refused(self):
        log = self.write('capture.log', '(0.0) can0 0C9#00\n')
        with self.assertRaises(can_import.ImportProblem):
            can_import.load(log, self.write('bad.dbc', 'not a dbc\n'))

    def test_a_dbc_for_another_car_is_refused(self):
        log = self.write('capture.log', '(0.0) can0 7E8#00\n')
        with self.assertRaises(can_import.ImportProblem) as caught:
            can_import.load(log, self.write('car.dbc', DBC_TEXT))
        self.assertIn('None of the DBC signals', str(caught.exception))

    def test_a_missing_file_gives_a_message_not_a_crash(self):
        with self.assertRaises(can_import.ImportProblem):
            can_import.load(os.path.join(self.folder, 'gone.log'), self.write('car.dbc', DBC_TEXT))

    def test_files_are_listed_by_suffix_and_a_missing_folder_is_empty(self):
        self.write('a.log', '')
        self.write('b.dbc', '')
        self.write('c.bin', '')
        self.assertEqual(can_import.files_in(self.folder, can_import.LOG_SUFFIXES), ['a.log'])
        self.assertEqual(can_import.files_in(self.folder, [can_import.DBC_SUFFIX]), ['b.dbc'])
        self.assertEqual(can_import.files_in(os.path.join(self.folder, 'missing'), ['.log']), [])


class ReplayGuardTests(unittest.TestCase):
    def test_the_adapter_refuses_an_imported_signal(self):
        from link import obd
        replay = can_replay.decode([frame(201, [0x10, 0x27, 0x28], 0.0)], dbc.parse(DBC_TEXT))
        pids.set_replay(can_replay.catalogue_entries(replay))
        try:
            entry = next(iter(pids.REPLAY))
            self.assertFalse(obd.is_allowed(entry))
            self.assertFalse(obd.is_allowed('CAN0C9.0'))
        finally:
            pids.set_replay([])

    def test_live_only_asks_for_imported_signals_from_a_replay(self):
        from live import LiveStream

        class Adapter:
            def __init__(self):
                self.asked = []

            def poll(self, ids, headers=None):
                self.asked.append(list(ids))
                return {}, {}

        replay = can_replay.decode([frame(201, [0x10, 0x27, 0x28], 0.0)], dbc.parse(DBC_TEXT))
        pids.set_replay(can_replay.catalogue_entries(replay))
        try:
            adapter = Adapter()
            LiveStream(adapter, transmission=False).step()
            self.assertFalse(any(p in pids.REPLAY for p in adapter.asked[0]))
            source = can_replay.ReplaySource(replay, clock=lambda: 0.0)
            stream = LiveStream(source, transmission=False)
            stream.step()
            self.assertTrue(all(p in stream.latest for p in pids.REPLAY))
        finally:
            pids.set_replay([])

    def test_only_the_dbc_frames_and_the_gear_frame_are_kept(self):
        frames = [frame(201, [0x10, 0x27, 0x28], 0.0), frame(0x7E8, [1, 2, 3], 0.5), frame(0x1F5, [0] * 8, 1.0)]
        replay = can_replay.decode(frames, dbc.parse(DBC_TEXT))
        self.assertEqual(sorted(f.can_id for f in replay.frames), [201, 0x1F5])
        self.assertEqual(len(replay.stamps), len(replay.frames))



class HostileFileTests(unittest.TestCase):
    def test_a_signal_line_with_a_number_that_cannot_be_read_is_skipped(self):
        text = 'BO_ 201 M: 8 X\n SG_ Bad : 0|8@1+ (1.0e,0) [0|1] ""  X\n SG_ Good : 8|8@1+ (1,0) [0|255] "" X\n'
        self.assertEqual([s.name for s in dbc.parse(text)], ['Good'])

    def test_a_signal_longer_than_64_bits_or_with_a_non_finite_scale_is_skipped(self):
        text = ('BO_ 201 M: 8 X\n SG_ Long : 0|99999999@1+ (1,0) [0|1] "" X\n'
                ' SG_ Nan : 0|8@1+ (nan,0) [0|1] "" X\n SG_ Inf : 0|8@1+ (1,inf) [0|1] "" X\n'
                ' SG_ Good : 8|8@1+ (1,0) [0|255] "" X\n')
        self.assertEqual([s.name for s in dbc.parse(text)], ['Good'])

    def test_a_message_line_too_long_to_read_does_not_leave_its_signals_under_the_one_before(self):
        text = ('BO_ 201 First: 8 X\n SG_ A : 0|8@1+ (1,0) [0|255] "" X\n'
                'BO_ 202 Second' + ' ' * 2000 + ': 8 X\n SG_ B : 0|8@1+ (1,0) [0|255] "" X\n')
        self.assertEqual([(s.message, s.name) for s in dbc.parse(text)], [('First', 'A')])

    def test_a_message_line_that_cannot_be_read_does_not_leave_its_signals_under_the_one_before(self):
        text = ('BO_ 201 First: 8 X\n SG_ A : 0|8@1+ (1,0) [0|255] "" X\n'
                'BO_ notanumber Second: 8 X\n SG_ B : 0|8@1+ (1,0) [0|255] "" X\n')
        self.assertEqual([(s.message, s.name) for s in dbc.parse(text)], [('First', 'A')])

    def test_a_file_over_the_limit_is_refused_with_a_message(self):
        folder = tempfile.mkdtemp()
        log, dbc_path = os.path.join(folder, 'big.log'), os.path.join(folder, 'a.dbc')
        with open(log, 'w') as fh:
            fh.write('x' * (can_import.MAX_BYTES + 1))
        with open(dbc_path, 'w') as fh:
            fh.write(DBC_TEXT)
        with self.assertRaises(can_import.ImportProblem):
            can_import.load(log, dbc_path)

    def test_reading_or_clearing_codes_while_a_log_plays_says_so(self):
        from link import obd
        replay = can_replay.decode([frame(201, [0x10, 0x27, 0x28], 0.0)], dbc.parse(DBC_TEXT))
        source = can_replay.ReplaySource(replay)
        with self.assertRaises(obd.OBDError):
            source.read_dtcs()
        with self.assertRaises(obd.OBDError):
            source.clear_dtcs()

    def test_replacing_the_replay_table_does_not_change_one_a_reader_holds(self):
        replay = can_replay.decode([frame(201, [0x10, 0x27, 0x28], 0.0)], dbc.parse(DBC_TEXT))
        pids.set_replay(can_replay.catalogue_entries(replay))
        try:
            held = pids.REPLAY
            pids.set_replay([])
            self.assertTrue(held)
            self.assertEqual(pids.REPLAY, {})
        finally:
            pids.set_replay([])


class MalformedLogTests(unittest.TestCase):
    def test_a_log_with_an_unreadable_timestamp_gives_a_message_not_a_crash(self):
        folder = tempfile.mkdtemp()
        log, dbc_path = os.path.join(folder, 'bad.log'), os.path.join(folder, 'a.dbc')
        with open(log, 'w') as fh:
            fh.write('(1.2.3) can0 0C9#102728\n(.) can0 0C9#102728\n')
        with open(dbc_path, 'w') as fh:
            fh.write(DBC_TEXT)
        with self.assertRaises(can_import.ImportProblem):
            can_import.load(log, dbc_path)

    def test_the_live_snapshot_survives_new_readings_arriving(self):
        from live import LiveStream

        class Source:
            replay = object()

            def poll(self, wanted, headers=None):
                return {'CAN0C9.0': (1.0, '')}, {}
        stream = LiveStream(Source())
        stream.step()
        self.assertIn('CAN0C9.0', stream.snapshot()['values'])


if __name__ == '__main__':
    unittest.main()
