import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import session_log  # noqa: E402
from scanner.session_log import NullLog, SessionLog  # noqa: E402


class SessionLogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_lines_have_a_kind_and_newlines_are_folded(self):
        log = SessionLog(self.tmp.name)
        log.write('TX', '010C')
        log.write('NOTE', 'one\ntwo')
        lines = Path(log.path).read_text().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn(' TX 010C', lines[0])
        self.assertTrue(lines[1].endswith('NOTE one | two'))

    def test_nothing_is_created_until_something_is_written(self):
        SessionLog(self.tmp.name)
        self.assertEqual(os.listdir(self.tmp.name), [])

    def test_disabled_log_writes_nothing(self):
        log = SessionLog(self.tmp.name, enabled=False)
        log.write('TX', '0100')
        self.assertEqual(os.listdir(self.tmp.name), [])

    def test_old_runs_are_pruned(self):
        for n in range(session_log.KEEP_FILES + 3):
            Path(self.tmp.name, f'2020-01-01_00-00-{n:02d}.txt').write_text('x')
        SessionLog(self.tmp.name).write('APP', 'start')
        logs = [n for n in os.listdir(self.tmp.name) if n.endswith('.txt')]
        self.assertEqual(len(logs), session_log.KEEP_FILES)

    def test_size_cap_stops_writing(self):
        original = session_log.MAX_BYTES
        session_log.MAX_BYTES = 200
        self.addCleanup(setattr, session_log, 'MAX_BYTES', original)
        log = SessionLog(self.tmp.name)
        for _ in range(50):
            log.write('TX', '0100')
        self.assertLess(os.path.getsize(log.path), 400)

    def test_unwritable_folder_never_raises(self):
        blocker = Path(self.tmp.name, 'file')
        blocker.write_text('x')
        log = SessionLog(str(blocker / 'sub'))
        log.write('TX', '0100')
        log.write('TX', '0100')

    def test_tail_returns_the_end(self):
        log = SessionLog(self.tmp.name)
        for n in range(100):
            log.write('NOTE', f'line {n}')
        text = log.tail(max_bytes=200)
        self.assertIn('line 99', text)
        self.assertNotIn('line 0\n', text)

    def test_new_file_starts_a_separate_log_and_turns_logging_on(self):
        ticks = iter(range(1000, 2000, 5))
        log = SessionLog(self.tmp.name, enabled=False, clock=lambda: next(ticks))
        log.new_file()
        first = log.path
        log.write('TX', '0100')
        log.new_file()
        self.assertNotEqual(first, log.path)
        self.assertEqual(len(os.listdir(self.tmp.name)), 2)

    def test_null_log_accepts_everything(self):
        log = NullLog()
        log.write('TX', 'x')
        log.set_enabled(True)
        self.assertEqual(log.tail(), '')


if __name__ == '__main__':
    unittest.main()
