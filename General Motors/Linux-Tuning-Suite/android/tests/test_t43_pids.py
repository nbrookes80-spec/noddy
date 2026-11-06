import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import pids  # noqa: E402
from scanner import t43_pids  # noqa: E402


class T43PidTests(unittest.TestCase):
    """The formulas from the confirmed T43 list (26_LATEST_TorquePro_PIDs_E38_T43_v5.csv)."""

    def test_fluid_temperature_is_the_confirmed_pid_and_the_guess_is_gone(self):
        pid = pids.get('221940')
        self.assertEqual((pid.header, pid.echo, pid.verified), ('7E2', '621940', True))
        self.assertEqual(pid.parse('78'), 80.0)          # 120 - 40
        self.assertIsNone(pids.get('22194F'))

    def test_tcc_slip_is_signed(self):
        pid = pids.get('221991')
        self.assertEqual(pid.parse('FFF8'), -1.0)        # -8 / 8
        self.assertEqual(pid.parse('0008'), 1.0)
        self.assertEqual(pid.parse('7FF8'), 4095.0)

    def test_last_shift_time_is_a_byte_divided_by_40(self):
        self.assertEqual(pids.get('221992').parse('50'), 2.0)

    def test_input_and_output_shaft_speeds(self):
        self.assertEqual(pids.get('221941').parse('0C80'), 800.0)   # (3200) / 4
        self.assertEqual(pids.get('221942').parse('0C80'), 400.0)   # 3200 * 0.125

    def test_current_gear_is_the_raw_byte(self):
        self.assertEqual(pids.get('22199A').parse('03'), 3.0)

    def test_the_t43_rows_read_the_transmission_module(self):
        for row in t43_pids.ROWS:
            with self.subTest(pid=row[0]):
                self.assertEqual(pids.get(row[0]).header, '7E2')

    def test_the_dashboard_and_the_live_stream_only_name_catalogued_pids(self):
        from live import STREAM_PIDS
        for pid_id in list(pids.MONITOR_PIDS) + list(STREAM_PIDS):
            with self.subTest(pid=pid_id):
                self.assertIn(pid_id, pids.CATALOG)
        self.assertNotIn('22194F', STREAM_PIDS)


if __name__ == '__main__':
    unittest.main()
