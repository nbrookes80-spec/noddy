import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from recorder import Recorder  # noqa: E402
from scanner.session import Session  # noqa: E402

COLUMNS = [('010C', '010C Engine RPM (rpm)'), ('010D', '010D Vehicle Speed (km/h)')]


class RecorderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.session = Session()
        self.recorder = Recorder(self.session, self.tmp.name, lambda: COLUMNS)

    def test_it_will_not_start_with_nothing_to_read(self):
        self.assertIn('Nothing to record', self.recorder.toggle())
        self.assertFalse(self.recorder.running)

    def test_folders_are_under_tuner_tool_info(self):
        self.assertTrue(self.recorder.data_folder.endswith(os.path.join('Tuner Tool Info', 'Data logs')))
        self.assertTrue(self.recorder.debug_folder.endswith(os.path.join('Tuner Tool Info', 'Debug logs')))

    def test_the_demo_drive_is_recorded_through_the_session(self):
        self.session.set_demo(True)
        self.assertIn('Recording to Data logs/', self.recorder.toggle())
        self.assertTrue(self.recorder.running)
        self.session.active().poll(['010C', '010D'])
        self.session.active().poll(['010C'])
        message = self.recorder.toggle()
        self.assertIn('Saved 2 rows', message)
        self.assertFalse(self.recorder.running)
        files = os.listdir(self.recorder.data_folder)
        self.assertEqual(len(files), 1)
        self.assertRegex(files[0], r'^\d{4}-\d\d-\d\d_\d\d-\d\d-\d\d\.csv$')

    def test_the_elapsed_time_reads_as_minutes_and_seconds(self):
        self.assertEqual(self.recorder.elapsed_text(), '00:00')


if __name__ == '__main__':
    unittest.main()
