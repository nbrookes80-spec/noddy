"""EFILive exports from other controllers and from comparisons. Synthetic text only."""

import unittest

from tunertoolpro import efilive_export as ef

COMPARISON = (
    '"EFILive Comparison Export"\r\n"File 1","New.csv"\r\n"File 2","Old.csv"\r\n"Exported","Oct 24,2026","16:59:16"\r\n'
    '\r\nD1100,-0.550391,KMH,"1>2 WOT Shift (a)"\r\n'
)

ESCALADE_STYLE = (
    '"EFILive Calibration Export"\r\n"File","L92 test.csv"\r\n"Exported","Oct 27,2026","01:31:58"\r\n'
    '\r\nA9021,"Primary Tank Axis 1"\r\n.,"Value (v)"\r\n1,0.000000\r\n2,1.400147\r\n'
    '\r\nB1000,"Some Table"\r\n.,"Value"\r\n"Row",2.5\r\n'
)


class ComparisonExportTests(unittest.TestCase):
    def test_comparison_is_flagged_and_its_files_are_named(self):
        export = ef.parse(COMPARISON)
        self.assertTrue(export.comparison)
        self.assertEqual(export.meta['File 1'], 'New.csv')
        self.assertEqual(export.meta['File 2'], 'Old.csv')

    def test_comparison_summary_says_what_the_values_mean(self):
        text = ef.parse(COMPARISON).readable()
        self.assertIn('New.csv compared with Old.csv', text)
        self.assertIn('File 1 minus File 2', text)
        self.assertIn('D1100 1>2 WOT Shift (a): -0.550391 KMH', text)

    def test_calibration_export_is_not_flagged(self):
        self.assertFalse(ef.parse(ESCALADE_STYLE).comparison)


class OtherControllerTests(unittest.TestCase):
    def test_records_outside_d_are_read(self):
        export = ef.parse(ESCALADE_STYLE)
        self.assertEqual(export.families(), {'A': 1, 'B': 1})
        axis = export.by_code('A9021')
        self.assertTrue(axis.is_table)
        header, rows = axis.table_rows()
        self.assertEqual(header, ['.', 'Value (v)'])
        self.assertEqual(len(rows), 2)

    def test_summary_lists_the_families_and_their_tables(self):
        text = ef.parse(ESCALADE_STYLE).readable()
        self.assertIn('Record families: A 1, B 1', text)
        self.assertIn('A9021 Primary Tank Axis 1', text)
        self.assertIn('B1000 Some Table', text)

    def test_wrong_header_is_still_refused(self):
        with self.assertRaises(ValueError):
            ef.parse('"Something else"\r\nD1100,1,KMH,"x"\r\n')


if __name__ == '__main__':
    unittest.main()
