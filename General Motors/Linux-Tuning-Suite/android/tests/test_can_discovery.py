import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scanner import can_discovery, pids  # noqa: E402
from tools import capture_can, decode_can  # noqa: E402
from tunertoolpro.canbus.frames import Frame, format_candump, read_log  # noqa: E402


def frame(can_id, hex_bytes, t=0.0):
    return Frame(can_id, bytes.fromhex(hex_bytes.replace(' ', '')), False, t)


class DecodeReplyTests(unittest.TestCase):
    def test_engine_speed_from_the_engine_module(self):
        reply = can_discovery.decode_reply(frame(0x7E8, '04 41 0C 1A F8 00 00 00'))
        self.assertEqual(reply[0], '010C')
        self.assertAlmostEqual(reply[1], 1726.0)
        self.assertEqual(reply[2], 'RPM')

    def test_transmission_fluid_temperature_from_the_transmission_module(self):
        reply = can_discovery.decode_reply(frame(0x7EA, '04 62 19 4F 78 00 00 00'))
        self.assertEqual(reply[0], '22194F')
        self.assertAlmostEqual(reply[1], 80.0)

    def test_a_reply_for_a_reading_the_catalogue_lacks_is_still_reported(self):
        reading, value, unit, name = can_discovery.decode_reply(frame(0x7E8, '03 41 C0 01 02 00 00 00'))
        self.assertEqual((reading, value), ('01C0', None))
        self.assertEqual(name, 'not in the catalogue')

    def test_other_traffic_is_not_a_reply(self):
        self.assertIsNone(can_discovery.decode_reply(frame(0x3E9, '02 01 0C 00 00 00 00 00')))
        self.assertIsNone(can_discovery.decode_reply(frame(0x7E8, '10 14 41 0C 1A F8 00 00')))   # multi-frame start


class ReportTests(unittest.TestCase):
    def capture(self):
        frames = []
        for i in range(101):   # 0x3E9 at 100 Hz, byte 0 counting, byte 1 steady
            frames.append(frame(0x3E9, f'{i % 256:02X} 55 00 00 00 00 00 00', i * 0.01))
        frames.append(frame(0x7E8, '04 41 0C 1A F8 00 00 00', 0.5))
        frames.append(frame(0x7E8, '04 41 0C 1A F8 00 00 00', 0.6))
        return frames

    def test_the_report_names_module_readings_and_broadcast_traffic(self):
        text = can_discovery.report(self.capture())
        self.assertIn('Module 7E0 Engine (ECM)', text)
        self.assertIn('010C', text)
        self.assertIn('1726 RPM', text)
        self.assertIn('3E9', text)
        self.assertIn('100.0', text)            # the broadcast rate
        self.assertIn('0', text.split('3E9')[1].split('\n')[0])   # byte 0 is listed as changing

    def test_dashboard_readings_the_capture_lacks_are_listed(self):
        text = can_discovery.report(self.capture())
        self.assertIn('Dashboard readings not in this capture', text)
        self.assertIn('0105', text.split('Dashboard readings not in this capture')[1])

    def test_an_empty_capture_says_what_to_check(self):
        self.assertIn('no CAN frames', can_discovery.report([]))

    def test_a_capture_survives_the_log_format_round_trip(self):
        frames = self.capture()
        again = read_log(format_candump(frames))
        self.assertEqual([(f.can_id, f.data) for f in again], [(f.can_id, f.data) for f in frames])


class FakeAdapter:
    """A transport that answers the monitor set-up and then sends two frames."""

    def __init__(self):
        self.sent = []
        self.sent_frames = False
        self.closed = False

    def open(self):
        pass

    def write(self, data):
        self.sent.append(data)

    def read_until(self, prompt=b'>'):
        return b'OK\r'

    def read_chunk(self, timeout=0.2):
        if self.sent_frames:
            return b''
        self.sent_frames = True
        return b'7E8 04 41 0C 1A F8 00 00 00\r3E9 00 55 00 00 00 00 00 00\r'

    def close(self):
        self.closed = True


class CaptureTests(unittest.TestCase):
    def test_a_capture_is_saved_as_a_log_the_decoder_reads(self):
        adapter = FakeAdapter()
        out_path = Path(tempfile.mkdtemp()) / 'capture.log'
        args = capture_can.build_parser().parse_args(['--seconds', '0.05', '--out', str(out_path)])
        with mock.patch.object(capture_can, 'open_transport', return_value=adapter):
            lines = []
            code = capture_can.run(args, out=lines.append)
        self.assertEqual(code, 0, lines)
        self.assertTrue(adapter.closed)
        frames = read_log(out_path.read_text())
        self.assertEqual({f.can_id for f in frames}, {0x7E8, 0x3E9})
        self.assertIn('ATMA', [s.decode().strip() for s in adapter.sent])   # listening, not requesting

    def test_no_adapter_is_reported_and_nothing_is_written(self):
        from link.obd import OBDError
        args = capture_can.build_parser().parse_args(['--seconds', '0.05', '--out', '/nonexistent/x.log'])
        with mock.patch.object(capture_can, 'open_transport', side_effect=OBDError('no adapter')):
            lines = []
            self.assertEqual(capture_can.run(args, out=lines.append), 1)
        self.assertEqual(lines, ['no adapter'])


class DecodeScriptTests(unittest.TestCase):
    def test_the_decoder_prints_and_saves_the_report(self):
        folder = Path(tempfile.mkdtemp())
        capture = folder / 'in.log'
        capture.write_text(format_candump([frame(0x7E8, '04 41 0C 1A F8 00 00 00', 0.0)]))
        report_path = folder / 'report.txt'
        args = decode_can.build_parser().parse_args([str(capture), '--out', str(report_path)])
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = decode_can.run(args, out=print)
        self.assertEqual(code, 0)
        self.assertIn('1726 RPM', buffer.getvalue())
        self.assertIn('1726 RPM', report_path.read_text())


class CsvRowsTests(unittest.TestCase):
    def test_module_readings_and_broadcast_ids_become_rows(self):
        frames = [frame(0x3E9, f'{i % 256:02X} 55 00 00 00 00 00 00', i * 0.01) for i in range(11)]
        frames.append(frame(0x7E8, '04 41 0C 1A F8 00 00 00', 0.5))
        rows = can_discovery.csv_rows(frames)
        self.assertEqual(rows[0], can_discovery.CSV_HEADER)
        reading = [r for r in rows if r[0] == 'module reading'][0]
        self.assertEqual(reading[1:4], ['7E0', '010C', 'Engine RPM'])
        self.assertEqual(reading[6:9], [1726.0, 1726.0, 'RPM'])
        broadcast = [r for r in rows if r[0] == 'broadcast'][0]
        self.assertEqual(broadcast[2], '3E9')
        self.assertEqual(broadcast[4], 11)
        self.assertEqual(broadcast[9], '0')

    def test_the_csv_text_parses_back_to_the_same_rows(self):
        import csv, io
        from scanner.can_discovery import csv_rows as rows_of
        frames = [frame(0x7E8, '04 41 0C 1A F8 00 00 00', 0.0)]
        buffer = io.StringIO()
        csv.writer(buffer).writerows(rows_of(frames))
        parsed = list(csv.reader(io.StringIO(buffer.getvalue())))
        self.assertEqual(parsed[0], can_discovery.CSV_HEADER)
        self.assertEqual(parsed[1][2], '010C')


if __name__ == '__main__':
    unittest.main()
