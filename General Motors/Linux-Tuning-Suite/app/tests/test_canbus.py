import unittest

from tunertoolpro.canbus import (DemoBus, ElmMonitor, Frame, LogPlayer, MonitorError, Sniffer, UnsafeCommand,
                                 format_candump, format_csv, is_allowed, read_log)
from tunertoolpro.canbus import frames as fr
from tunertoolpro.canbus import monitor as mon
from tunertoolpro.canbus.sniffer import DEC, INC, NONE


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def frame(can_id, *data, extended=False):
    return Frame(can_id, bytes(data), extended)


class ParseTests(unittest.TestCase):
    def test_elm_standard_and_extended(self):
        f = fr.parse_elm_line('7E8 06 41 0C 1A F8 00 00 00')
        self.assertEqual((f.can_id, f.extended, f.data.hex()), (0x7E8, False, '06410c1af8000000'))
        g = fr.parse_elm_line('18DAF110 03 7F 22 11')
        self.assertEqual((g.can_id, g.extended, g.data.hex()), (0x18DAF110, True, '037f2211'))

    def test_elm_compact_form(self):
        f = fr.parse_elm_line('7E80641')
        self.assertEqual((f.can_id, f.data.hex()), (0x7E8, '0641'))

    def test_elm_non_frames_are_ignored(self):
        for text in ('', 'OK', 'BUFFER FULL', 'SEARCHING...', '?', '>', 'STOPPED', 'ATMA', '7E8 1 2 3'):
            self.assertIsNone(fr.parse_elm_line(text), text)

    def test_elm_too_many_bytes_or_bad_id(self):
        self.assertIsNone(fr.parse_elm_line('7E8 ' + ' '.join(['00'] * 9)))
        self.assertIsNone(fr.parse_elm_line('7E 00'))

    def test_slcan(self):
        f = fr.parse_slcan_line('t1232AABB')
        self.assertEqual((f.can_id, f.data.hex(), f.extended), (0x123, 'aabb', False))
        g = fr.parse_slcan_line('T123456781FF')
        self.assertEqual((g.can_id, g.data.hex(), g.extended), (0x12345678, 'ff', True))
        self.assertIsNone(fr.parse_slcan_line('t1232AA'))      # shorter than its length says
        self.assertIsNone(fr.parse_slcan_line('r1230'))

    def test_candump_formats(self):
        f = fr.parse_candump_line('(1436509052.249713) vcan0 123#DEADBEEF')
        self.assertEqual((f.can_id, f.data.hex(), f.timestamp), (0x123, 'deadbeef', 1436509052.249713))
        g = fr.parse_candump_line('  can0  1F334455   [3]  11 22 33')
        self.assertEqual((g.can_id, g.extended, g.data.hex()), (0x1F334455, True, '112233'))
        self.assertIsNone(fr.parse_candump_line('can0 123 [3] 11 22'))   # length mismatch

    def test_round_trips(self):
        frames = [Frame(0x123, b'\x01\x02', False, 1.5), Frame(0x18DAF110, b'\xff', True, 2.25)]
        self.assertEqual(read_log(format_candump(frames)), frames)
        self.assertEqual(read_log(format_csv(frames)), frames)

    def test_read_log_skips_junk_and_mixes_formats(self):
        text = 'header line\n(1.0) can0 100#01\n\nnot a frame\n7E8 02 41 00\n'
        frames = read_log(text)
        self.assertEqual([f.can_id for f in frames], [0x100, 0x7E8])


class SnifferTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.s = Sniffer(self.clock)

    def row(self, can_id):
        return next(r for r in self.s.rows() if r['id'] == can_id)

    def test_new_id_shows_no_change(self):
        self.s.feed([frame(0x100, 1, 2, 3)])
        cells = self.row(0x100)['bytes']
        self.assertEqual([c['change'] for c in cells[:3]], [NONE, NONE, NONE])
        self.assertEqual(cells[3], None)

    def test_rising_and_falling_bytes_are_coloured(self):
        self.s.feed([frame(0x100, 0x10, 0x10)])
        self.clock.advance(0.1)
        self.s.feed([frame(0x100, 0x20, 0x08)])
        self.s.tick_notch()
        cells = self.row(0x100)['bytes']
        self.assertEqual((cells[0]['change'], cells[1]['change']), (INC, DEC))

    def test_unchanged_window_clears_colour(self):
        self.s.feed([frame(0x100, 1)])
        self.s.feed([frame(0x100, 2)])
        self.s.tick_notch()
        self.assertEqual(self.row(0x100)['bytes'][0]['change'], INC)
        self.s.feed([frame(0x100, 2)])
        self.s.tick_notch()
        self.assertEqual(self.row(0x100)['bytes'][0]['change'], NONE)

    def test_notch_ignores_busy_bits(self):
        self.s.feed([frame(0x100, 0x00)])
        for value in (0x01, 0x00, 0x01):       # the low bit flaps all the time
            self.s.feed([frame(0x100, value)])
        self.s.tick_notch()
        self.s.notch()
        self.s.feed([frame(0x100, 0x00)])
        self.s.tick_notch()
        self.s.feed([frame(0x100, 0x01)])
        self.s.tick_notch()
        self.assertEqual(self.row(0x100)['bytes'][0]['change'], NONE)
        self.s.feed([frame(0x100, 0x41)])      # a different bit moves: that one still shows
        self.s.tick_notch()
        self.assertEqual(self.row(0x100)['bytes'][0]['change'], INC)

    def test_unnotch_restores_colouring(self):
        self.s.feed([frame(0x100, 0)])
        self.s.feed([frame(0x100, 1)])
        self.s.tick_notch()
        self.s.notch()
        self.assertEqual(self.row(0x100)['bytes'][0]['notched'], 1)
        self.s.unnotch()
        self.assertEqual(self.row(0x100)['bytes'][0]['notched'], 0)

    def test_mute_notched_hides_notched_bit_changes(self):
        self.s.mute_notched = True
        self.s.feed([frame(0x100, 0)])
        self.s.feed([frame(0x100, 1)])
        self.s.tick_notch()
        self.s.notch()
        self.s.feed([frame(0x100, 0)])          # only the notched bit changed
        self.assertEqual(self.row(0x100)['bytes'][0]['text'], '01')

    def test_ids_expire_unless_told_not_to(self):
        self.s.feed([frame(0x100, 1), frame(0x200, 1)])
        self.clock.advance(3)
        self.s.feed([frame(0x200, 1)])
        self.clock.advance(3)
        self.assertEqual(self.s.tick(), [0x100])
        self.assertEqual(self.s.ids(), [0x200])
        self.s.never_expire = True
        self.clock.advance(60)
        self.assertEqual(self.s.tick(), [])
        self.assertEqual(self.s.ids(), [0x200])

    def test_stale_flag_before_expiry(self):
        self.s.feed([frame(0x100, 1)])
        self.clock.advance(4.5)
        self.assertTrue(self.row(0x100)['stale'])

    def test_delta_and_frequency_come_from_the_frames_own_times(self):
        self.s.feed([Frame(0x100, b'\x01', False, 5.0), Frame(0x100, b'\x01', False, 5.1)])   # one burst
        row = self.row(0x100)
        self.assertAlmostEqual(row['delta'], 0.1)
        self.assertEqual(row['freq'], '10 hz')

    def test_first_frame_and_backwards_time_show_zero_hz(self):
        self.s.feed([Frame(0x100, b'\x01', False, 5.0)])
        self.assertEqual(self.row(0x100)['freq'], '0 hz')
        self.s.feed([Frame(0x100, b'\x01', False, 4.0)])      # a looping log restarted
        self.assertEqual((self.row(0x100)['delta'], self.row(0x100)['freq']), (0.0, '0 hz'))

    def test_fade_grows_each_tick_and_resets_on_change(self):
        self.s.fade_inactive = True
        self.s.feed([frame(0x100, 1, 1)])
        for _ in range(5):
            self.s.tick()
        self.s.feed([frame(0x100, 2, 1)])
        cells = self.row(0x100)['bytes']
        self.assertEqual((cells[0]['fade'], cells[1]['fade']), (0, 50))
        self.s.never_expire = True
        for _ in range(40):                     # the ID keeps arriving, byte 1 never changes
            self.s.tick()
            self.s.feed([frame(0x100, 2, 1)])
        self.assertEqual(self.row(0x100)['bytes'][1]['fade'], 225)

    def test_fade_off_by_default(self):
        self.s.feed([frame(0x100, 1)])
        for _ in range(5):
            self.s.tick()
        self.assertEqual(self.row(0x100)['bytes'][0]['fade'], 0)

    def test_filter_hide_all_then_show_some(self):
        self.s.feed([frame(0x100, 1), frame(0x200, 1), frame(0x300, 1)])
        self.s.hide_all()
        self.assertEqual(self.s.rows(), [])
        self.s.set_visible(0x200, True)
        self.assertEqual([r['id'] for r in self.s.rows()], [0x200])
        self.s.show_all()
        self.assertEqual(len(self.s.rows()), 3)

    def test_hiding_one_id_keeps_the_rest(self):
        self.s.feed([frame(0x100, 1), frame(0x200, 1)])
        self.s.set_visible(0x100, False)
        self.assertEqual([r['id'] for r in self.s.rows()], [0x200])

    def test_notch_only_touches_visible_ids(self):
        self.s.feed([frame(0x100, 0), frame(0x200, 0)])
        self.s.feed([frame(0x100, 1), frame(0x200, 1)])
        self.s.tick_notch()
        self.s.set_visible(0x100, False)
        self.s.notch()
        self.assertEqual(self.s.items[0x100].notch[0], 0)
        self.assertEqual(self.s.items[0x200].notch[0], 1)

    def test_bits_view_states(self):
        self.s.feed([frame(0x100, 0b10100000)])
        self.s.feed([frame(0x100, 0b11000000)])
        bits = self.row(0x100)['bytes'][0]['bits']
        self.assertEqual(bits[:3], ['set', 'rose', 'fell'])
        self.assertEqual(bits[3:], ['unset'] * 5)

    def test_rows_sorted_by_id_and_extended_ids_padded(self):
        self.s.feed([frame(0x300, 1), Frame(0x18DAF110, b'\x01', True), frame(0x100, 1)])
        self.assertEqual([r['id_text'] for r in self.s.rows()], ['100', '300', '18DAF110'])

    def test_clear(self):
        self.s.feed([frame(0x100, 1)])
        self.s.clear()
        self.assertEqual(self.s.rows(), [])
        self.assertEqual(self.s.frames_seen, 0)


class FakeTransport:
    def __init__(self, chunks=()):
        self.sent = []
        self.chunks = list(chunks)
        self.prompt_replies = 0

    def write(self, data):
        self.sent.append(data)

    def read_until(self, prompt=b'>'):
        return b'OK\r'

    def read_chunk(self, timeout=0.2):
        return self.chunks.pop(0) if self.chunks else b''


class MonitorTests(unittest.TestCase):
    def make(self, chunks=()):
        self.t = FakeTransport(chunks)
        self.clock = Clock()
        return ElmMonitor(self.t, self.clock)

    def sent(self):
        return [s.decode() for s in self.t.sent]

    def test_allowlist_is_receive_only(self):
        for ok in ('ATZ', 'ATMA', 'atsp6', 'ATCRA7E8', 'ATCRA18DAF110', 'ATH1', 'ATCAF0', 'ATAR'):
            self.assertTrue(is_allowed(ok), ok)
        for bad in ('0100', '03', '2101', '22F190', 'ATSH7E0', 'ATCRA7E', 'ATCRA7E8X', 'ATFI', 'ATPC',
                    'ATTP6', 'ATSP', 'ATSPZ', '0104', '04', 'ATMA7E8', 'ATWS;03'):
            self.assertFalse(is_allowed(bad), bad)

    def test_unsafe_command_is_refused_before_sending(self):
        m = self.make()
        with self.assertRaises(UnsafeCommand):
            m.command('0100')
        self.assertEqual(self.t.sent, [])

    def test_start_sends_the_setup_in_order_then_atma(self):
        m = self.make()
        m.start('6', '7E8')
        self.assertEqual(self.sent(), ['ATE0\r', 'ATL0\r', 'ATH1\r', 'ATS1\r', 'ATCAF0\r', 'ATSP6\r',
                                       'ATCRA7E8\r', 'ATMA\r'])
        self.assertTrue(m.running)

    def test_every_command_start_sends_is_allowed(self):
        for command in mon.monitor_commands('A', '18DAF110') + list(mon.RESTORE_COMMANDS):
            self.assertTrue(is_allowed(command), command)

    def test_start_rejects_a_bad_filter_or_protocol(self):
        m = self.make()
        with self.assertRaises(MonitorError):
            m.start('6', 'ZZZ')
        with self.assertRaises(MonitorError):
            m.start('Q')
        self.assertEqual(self.t.sent, [])

    def test_start_fails_if_adapter_says_no(self):
        m = self.make()
        self.t.read_until = lambda prompt=b'>': b'?\r'
        with self.assertRaises(MonitorError):
            m.start()
        self.assertFalse(m.running)

    def test_poll_parses_frames_split_across_chunks(self):
        m = self.make([b'7E8 06 41 0C 1A F8 00 00 00\r7E8 03 41', b' 0D 40\r\r'])
        m.start()
        first = m.poll()
        self.assertEqual(len(first), 1)
        second = m.poll()
        self.assertEqual([f.data.hex() for f in second], ['03410d40'])

    def test_frames_in_one_block_are_spread_over_the_time_since_the_last_one(self):
        m = self.make()
        m.start()
        self.clock.advance(0.2)
        frames = m.parse('7E8 01\r7E8 02\r7E8 03\r7E8 04\r')
        self.assertEqual([round(f.timestamp, 3) for f in frames], [0.05, 0.1, 0.15, 0.2])
        self.clock.advance(0.2)
        later = m.parse('7E8 05\r')
        self.assertAlmostEqual(later[0].timestamp, 0.4)

    def test_poll_counts_buffer_full_and_ignores_noise(self):
        m = self.make([b'BUFFER FULL\r7E8 01 02\rSTOPPED\r'])
        m.start()
        frames = m.poll()
        self.assertEqual(len(frames), 1)
        self.assertEqual(m.overruns, 1)

    def test_poll_when_not_running_returns_nothing(self):
        m = self.make([b'7E8 01\r'])
        self.assertEqual(m.poll(), [])

    def test_stop_interrupts_then_restores_obd_settings(self):
        m = self.make()
        m.start()
        self.t.sent.clear()
        m.stop()
        self.assertEqual(self.sent(), ['\r', 'ATAR\r', 'ATH0\r', 'ATS0\r', 'ATCAF1\r', 'ATSP0\r'])
        self.assertFalse(m.running)
        m.stop()                                   # second call does nothing
        self.assertEqual(len(self.t.sent), 6)

    def test_nothing_the_monitor_ever_sends_is_a_request(self):
        m = self.make()
        m.start('6', '7E8')
        m.stop()
        for text in self.sent():
            command = text.strip()
            self.assertTrue(command == '' or is_allowed(command), command)


class SourceTests(unittest.TestCase):
    def test_demo_bus_rates(self):
        clock = Clock()
        bus = DemoBus(clock)
        clock.advance(1.0)
        frames = bus.poll()
        counts = {}
        for f in frames:
            counts[f.can_id] = counts.get(f.can_id, 0) + 1
        self.assertAlmostEqual(counts[0x0C9], 100, delta=2)
        self.assertAlmostEqual(counts[0x1E5], 20, delta=2)
        self.assertEqual(counts[0x4C9], 2)       # at 0 s and at 1 s

    def test_demo_bus_sniffs_the_way_the_help_describes(self):
        clock = Clock()
        sniffer = Sniffer(clock)
        bus = DemoBus(clock)
        for _ in range(30):
            clock.advance(0.2)
            sniffer.feed(bus.poll())
            sniffer.tick()
            sniffer.tick_notch()
        self.assertEqual(sniffer.ids(), [0x0C9, 0x0F1, 0x1E5, 0x3C1, 0x4C9])
        status = sniffer.items[0x4C9]
        self.assertEqual(status.change(0), NONE)     # the fixed message never lights up
        self.assertEqual(status.current[:4], [0xA5, 0x5A, 0x00, 0x01])

    def test_log_player_replays_at_recorded_speed_and_loops(self):
        clock = Clock()
        frames = [Frame(1, b'\x01', False, 10.0), Frame(2, b'\x02', False, 10.5), Frame(3, b'\x03', False, 11.0)]
        player = LogPlayer(frames, clock)
        self.assertEqual([f.can_id for f in player.poll()], [1])
        clock.advance(0.6)
        self.assertEqual([f.can_id for f in player.poll()], [2])
        clock.advance(0.5)
        self.assertEqual([f.can_id for f in player.poll()], [3])
        clock.advance(0.1)
        self.assertEqual([f.can_id for f in player.poll()], [1])      # looped

    def test_log_player_stops_without_loop(self):
        clock = Clock()
        player = LogPlayer([Frame(1, b'', False, 0.0)], clock, loop=False)
        self.assertEqual(len(player.poll()), 1)
        self.assertTrue(player.finished)
        clock.advance(5)
        self.assertEqual(player.poll(), [])

    def test_empty_log(self):
        self.assertEqual(LogPlayer([]).poll(), [])


if __name__ == '__main__':
    unittest.main()
