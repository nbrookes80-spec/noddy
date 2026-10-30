import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import sniffer_view as view  # noqa: E402
from tunertoolpro.canbus import Frame, Sniffer, SnifferSession  # noqa: E402


class Clock:
    now = 10.0

    def __call__(self):
        return self.now


def make_rows(*frame_sets, fade=False):
    clock = Clock()
    sniffer = Sniffer(clock)
    sniffer.fade_inactive = fade
    for frames in frame_sets:
        sniffer.feed(frames)
        sniffer.tick_notch()
    return sniffer, sniffer.rows()


class TableTextTests(unittest.TestCase):
    def test_rising_and_falling_bytes_carry_markers_and_colours(self):
        _s, rows = make_rows([Frame(0x100, bytes([0x10, 0x10, 0x10]), False, 0.0)],
                             [Frame(0x100, bytes([0x20, 0x08, 0x10]), False, 0.1)])
        text = view.table_text(rows)
        self.assertIn('[color=#66cc8c]20+[/color]', text)
        self.assertIn('[color=#ff6661]08-[/color]', text)
        self.assertIn('[color=#ffffff]10 [/color]', text)       # unchanged: no marker

    def test_rate_is_compact_and_ids_are_right_aligned(self):
        _s, rows = make_rows([Frame(0x0C9, b'\x01', False, 0.0), Frame(0x0C9, b'\x01', False, 0.01)],
                             [Frame(0x18DAF110, b'\x01', True, 0.0)])
        lines = view.table_text(rows).splitlines()
        self.assertTrue(lines[1].startswith('     0C9  100hz'))
        self.assertTrue(lines[2].startswith('18DAF110    0hz'))

    def test_notched_byte_gets_a_dot_and_missing_bytes_are_blank(self):
        sniffer, _rows = make_rows([Frame(0x100, b'\x00', False, 0.0)], [Frame(0x100, b'\x01', False, 0.1)])
        sniffer.notch()
        sniffer.feed([Frame(0x100, b'\x01', False, 0.2)])
        sniffer.tick_notch()
        sniffer.tick_notch()           # the changed window has passed: no colour, but still notched
        text = view.table_text(sniffer.rows())
        self.assertIn('01.', text)

    def test_stale_id_is_red(self):
        clock = Clock()
        sniffer = Sniffer(clock)
        sniffer.feed([Frame(0x100, b'\x01', False, 0.0)])
        clock.now += 4.5
        self.assertIn('[color=#ff6661]     100[/color]', view.table_text(sniffer.rows()))

    def test_faded_byte_goes_grey(self):
        sniffer, _ = make_rows([Frame(0x100, b'\x01', False, 0.0)], fade=True)
        for _ in range(10):
            sniffer.tick()
            sniffer.feed([Frame(0x100, b'\x01', False, 0.0)])
        self.assertIn('[color=#9b9b9b]01 [/color]', view.table_text(sniffer.rows()))

    def test_long_lists_are_cut_with_a_hint(self):
        frames = [Frame(i, b'\x01', False, 0.0) for i in range(1, 80)]
        _s, rows = make_rows(frames)
        text = view.table_text(rows, limit=10)
        self.assertEqual(len(text.splitlines()), 12)
        self.assertIn('and 69 more IDs', text)

    def test_header_digits_sit_over_each_byte(self):
        import re
        _s, rows = make_rows([Frame(0x100, bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]), False, 0.0)])
        header, row = view.table_text(rows).splitlines()
        plain = re.sub(r'\[/?color[^\]]*\]', '', row)
        start = view.ID_WIDTH + 1 + view.RATE_WIDTH + 1
        for i in range(8):
            self.assertEqual(header[start + 4 * i + 1], str(i))
            self.assertEqual(plain[start + 4 * i:start + 4 * i + 2], f'{0x11 * (i + 1):02X}')


class BitsTextTests(unittest.TestCase):
    def test_bits_show_set_unset_rose_fell_and_notched(self):
        sniffer, _ = make_rows([Frame(0x1E5, b'\xA0', False, 0.0)], [Frame(0x1E5, b'\xC0', False, 0.1)])
        text = view.bits_text(sniffer.row_for(0x1E5))
        self.assertIn('byte 0  C0  ', text)
        self.assertIn('[color=#ffffff]1[/color][color=#66cc8c]1[/color][color=#ff6661]0[/color]', text)

    def test_missing_id(self):
        self.assertIn('not on the bus', view.bits_text(None))


class ParseIdsTests(unittest.TestCase):
    def test_accepts_commas_spaces_and_0x(self):
        self.assertEqual(view.parse_ids('7E8, 0c9 0x18DAF110'), {0x7E8, 0xC9, 0x18DAF110})
        self.assertEqual(view.parse_ids('  '), set())

    def test_rejects_junk_naming_it(self):
        with self.assertRaisesRegex(ValueError, 'zz'):
            view.parse_ids('7E8 zz')
        with self.assertRaises(ValueError):
            view.parse_ids('123456789')


class SaveTests(unittest.TestCase):
    def test_save_capture_writes_a_candump_file(self):
        session = SnifferSession(Clock())
        session.feed([Frame(0x123, b'\x01\x02', False, 1.0)])
        with tempfile.TemporaryDirectory() as folder:
            path, count = view.save_capture(session, str(Path(folder) / 'sub'), now=0)
            self.assertEqual(count, 1)
            self.assertTrue(path.endswith('.log'))
            self.assertIn('123#0102', Path(path).read_text())


if __name__ == '__main__':
    unittest.main()
