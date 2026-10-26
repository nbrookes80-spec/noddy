"""Tests for the EFILive calibration export reader, on a small synthetic export.

No user data is in the repository. A real export can be checked by setting EFILIVE_SAMPLE to its path.
"""

import os
import unittest

from tunertoolpro import efilive_export as ef

SAMPLE = (
    '"EFILive Calibration Export"\r\n'
    '"File","Test tune.csv"\r\n'
    '"Exported","Aug 15,2026","01:42:33"\r\n'
    '\r\n'
    'D1001,"Part Throttle Shift"\r\n'
    ',"Gear Change"\r\n'
    '"TPS .",1->2,2->3\r\n'
    '0.00,11.007813,21.164063\r\n'
    '6.25,12.000000,22.000000\r\n'
    '\r\n'
    'D1100,37.242188,KMH,"1>2 WOT Shift (a)"\r\n'
    '\r\n'
    'E0101,"Transmission DTC Fault Processing Enablers"\r\n'
    '.,Value\r\n'
    '"No Fault","X: Not Reported"\r\n'
    '\r\n'
    'P0218,"C: Non Emissions"\r\n'
    'U0073,"A: 1 Trip, Emissions Related"\r\n'
    '\r\n'
    'H0122,3.910034,Ratio,"Axle Ratio"\r\n'
)


class EfiLiveExportTests(unittest.TestCase):
    def setUp(self):
        self.export = ef.parse(SAMPLE)

    def test_meta_is_read(self):
        self.assertEqual(self.export.meta['File'], 'Test tune.csv')
        self.assertEqual(self.export.meta['Exported'], 'Aug 15,2026')

    def test_record_kinds(self):
        kinds = [r.code for r in self.export.records]
        self.assertEqual(kinds, ['D1001', 'D1100', 'E0101', 'P0218', 'U0073', 'H0122'])

    def test_table_axes_and_rows(self):
        table = self.export.by_code('D1001')
        self.assertTrue(table.is_table)
        header, rows = table.table_rows()
        self.assertEqual(header[:3], ['TPS .', '1->2', '2->3'])
        self.assertEqual(rows[0][1], '11.007813')
        self.assertEqual(len(rows), 2)

    def test_scalar_value_unit_and_title(self):
        scalar = self.export.by_code('D1100')
        self.assertTrue(scalar.is_scalar)
        self.assertAlmostEqual(scalar.value, 37.242188)
        self.assertEqual(scalar.unit, 'KMH')
        self.assertEqual(scalar.title, '1>2 WOT Shift (a)')

    def test_constant_is_a_scalar(self):
        constant = self.export.by_code('H0122')
        self.assertAlmostEqual(constant.value, 3.910034)
        self.assertEqual(constant.title, 'Axle Ratio')

    def test_trouble_code_classification_is_kept_as_text(self):
        self.assertEqual(self.export.by_code('P0218').title, 'C: Non Emissions')
        self.assertIsNone(self.export.by_code('P0218').value)

    def test_readable_summary_lists_each_section(self):
        text = self.export.readable()
        self.assertIn('Vehicle constants:', text)
        self.assertIn('H0122 Axle Ratio: 3.910034 Ratio', text)
        self.assertIn('D1100 1>2 WOT Shift (a): 37.242188 KMH', text)
        self.assertIn('D1001 Part Throttle Shift: columns 1->2, 2->3', text)
        self.assertIn('Trouble codes listed: 2', text)

    def test_rejects_a_file_that_is_not_an_export(self):
        with self.assertRaises(ValueError):
            ef.parse('"Something else"\r\nD1001,1,KMH,"x"\r\n')

    def test_missing_code_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.export.by_code('D9999')


@unittest.skipUnless(os.environ.get('EFILIVE_SAMPLE'), 'set EFILIVE_SAMPLE to a real export to run this check')
class RealExportTests(unittest.TestCase):
    def test_real_export_parses(self):
        export = ef.load(os.environ['EFILIVE_SAMPLE'])
        self.assertGreater(len(export.records), 500)
        self.assertGreater(len(export.tables()), 100)


if __name__ == '__main__':
    unittest.main()
