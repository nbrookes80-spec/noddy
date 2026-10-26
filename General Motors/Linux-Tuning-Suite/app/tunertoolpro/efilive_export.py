"""Reader for EFILive calibration exports: the comma-separated text that EFILive Tune writes.

Format, established from a real export (static analysis; EFILive was not run):

    "EFILive Calibration Export"            title line
    "File","<name>"                         meta rows, then a blank line
    "Exported","<date>","<time>"
    <blank>
    CODE,value,unit,"label"                 scalar: one value with a unit and a label
    CODE,"title"                            table: title, then one or more rows, then blank
    ,"subtitle"                             table body: the first row names the axes
    "TPS .",1->2,2->3,...                   header row (first cell is the row axis)
    0.00,11.007813,21.164063,...            data rows: axis value, then the cells
    E0101,"title"                           enable flag: title, then a header and value rows
    P0218,"C: Non Emissions"                DTC: code and its classification
    H0122,3.910034,Ratio,"Axis ratio"       vehicle constant: value, unit, label

A record runs from its code line to the next blank line or code line. Cells stay as text
until a caller asks for a number, so nothing is rounded or changed on the way in.
"""

import csv
import io
import re
from dataclasses import dataclass, field

CODE = re.compile(r'^[A-Z]\d{3,5}$')
KIND_NAMES = {'D': 'calibration', 'E': 'enable flag', 'P': 'trouble code', 'U': 'trouble code',
              'H': 'vehicle constant'}


def number(text):
    """The cell as a float, or None when it is not a number."""
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


@dataclass
class Record:
    code: str
    fields: list          # cells after the code on its own line
    body: list = field(default_factory=list)  # the rows that follow it

    @property
    def kind(self):
        return self.code[0]

    @property
    def is_scalar(self):
        """A value with a unit and a label, such as D1100 or H0122."""
        return len(self.fields) >= 3 and number(self.fields[0]) is not None

    @property
    def title(self):
        if self.is_scalar:
            return self.fields[2]
        return self.fields[0] if self.fields else ''

    @property
    def value(self):
        return number(self.fields[0]) if self.is_scalar else None

    @property
    def unit(self):
        return self.fields[1] if self.is_scalar else ''

    @property
    def is_table(self):
        return not self.is_scalar and bool(self.body)

    def table_rows(self):
        """For a table: (header, rows). The header row's first cell is the row axis label.

        A table may open with a subtitle row whose first cell is empty (for example ,"Gear Change").
        That row is skipped, so the header is the next row.
        """
        if not self.is_table:
            return [], []
        start = 1 if self.body[0][0] == '' and len(self.body) > 1 else 0
        return self.body[start], self.body[start + 1:]


@dataclass
class CalibrationExport:
    meta: dict
    records: list
    comparison: bool = False  # True for "EFILive Comparison Export": values are File 1 minus File 2

    def by_code(self, code):
        for record in self.records:
            if record.code == code:
                return record
        raise KeyError(code)

    def of_kind(self, kind):
        return [r for r in self.records if r.kind == kind]

    def scalars(self):
        return [r for r in self.records if r.is_scalar]

    def tables(self):
        return [r for r in self.records if r.is_table]

    def families(self):
        """Record letters present and how many records each has. The letters differ by controller: T43 uses D,
        the L92 Escalade uses A, B, C, F, G and H for its calibrations."""
        counts = {}
        for r in self.records:
            counts[r.kind] = counts.get(r.kind, 0) + 1
        return counts

    def readable(self, table_rows=4):
        """Plain-text summary for people and for the AI. Full tables stay in the export file."""
        if self.comparison:
            head = [f'Comparison export: {self.meta.get("File 1", "file 1")} compared with '
                    f'{self.meta.get("File 2", "file 2")}',
                    'Values are File 1 minus File 2 (negative means File 1 is lower).']
        else:
            head = [f'Calibration export: {self.meta.get("File", "unnamed")}']
        lines = head + [f'Exported: {self.meta.get("Exported", "unknown date")}',
                        'Record families: ' + ', '.join(f'{k} {n}' for k, n in sorted(self.families().items())), '']
        constants = [r for r in self.of_kind('H')]
        if constants:
            lines.append('Vehicle constants:')
            for r in constants:
                lines.append(f'  {r.code} {r.title}: {r.fields[0]} {r.unit}'.rstrip())
            lines.append('')
        scalars = [r for r in self.scalars() if r.kind != 'H']
        if scalars:
            lines.append(f'Calibration values ({len(scalars)}):')
            for r in scalars:
                lines.append(f'  {r.code} {r.title}: {r.fields[0]} {r.unit}'.rstrip())
            lines.append('')
        tables = self.tables()
        if tables:
            lines.append(f'Calibration tables ({len(tables)}):')
            for r in tables:
                header, rows = r.table_rows()
                lines.append(f'  {r.code} {r.title}: columns {", ".join(c for c in header[1:] if c) or "(none)"}')
                for row in rows[:table_rows]:
                    lines.append('    ' + ', '.join(c for c in row if c != '')[:200])
                if len(rows) > table_rows:
                    lines.append(f'    ... {len(rows) - table_rows} more rows')
            lines.append('')
        flags = [r for r in self.of_kind('E')]
        if flags:
            lines.append(f'Enable flags ({len(flags)}): ' + '; '.join(r.code + ' ' + r.title for r in flags[:12]))
            lines.append('')
        codes = self.of_kind('P') + self.of_kind('U')
        if codes:
            lines.append(f'Trouble codes listed: {len(codes)}')
        return '\n'.join(lines).rstrip() + '\n'


def parse(text):
    """Parse the text of an export. Raises ValueError when it does not start like an EFILive export."""
    rows = list(csv.reader(io.StringIO(text, newline='')))
    title = rows[0][0].strip() if rows and rows[0] else ''
    if title not in ('EFILive Calibration Export', 'EFILive Comparison Export'):
        raise ValueError('not an EFILive export: the first line should be "EFILive Calibration Export" '
                         'or "EFILive Comparison Export"')
    meta = {}
    records = []
    current = None
    for row in rows[1:]:
        cells = [c.strip() if c else '' for c in row]
        if not any(cells):
            current = None  # a blank line ends the record
            continue
        if CODE.match(cells[0]):
            current = Record(code=cells[0], fields=[c for c in cells[1:]])
            records.append(current)
        elif current is not None:
            current.body.append(cells)
        elif len(cells) >= 2 and not meta.get(cells[0]):
            meta[cells[0]] = cells[1]
    return CalibrationExport(meta=meta, records=records, comparison=(title == 'EFILive Comparison Export'))


def load(path):
    """Read and parse an export file. The file is read as text only; nothing in it is run."""
    with open(path, encoding='latin-1', newline='') as fh:
        return parse(fh.read())


if __name__ == '__main__':  # python3 -I -m tunertoolpro.efilive_export "<export file>"
    import sys
    print(load(sys.argv[1]).readable(table_rows=4))
