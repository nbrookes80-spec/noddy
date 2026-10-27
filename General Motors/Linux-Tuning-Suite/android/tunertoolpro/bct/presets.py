"""BC Trans preset tables: Trans_Presets.txt and Slope_Presets.txt.

Both are tab-separated. Lines starting with '#' are comments. The first
remaining line is the column header (the "legend" row). Cells equal to 'null'
mean "leave unchanged" and load as None. Numeric cells load as floats.
"""

from pathlib import Path


def _cell(text):
    text = text.strip()
    if text == '' or text.lower() == 'null':
        return None
    try:
        return float(text)
    except ValueError:
        return text


def load_table(path):
    """Return a list of dicts keyed by the header row. Rows with an empty name are skipped."""
    text = Path(path).read_bytes().decode('latin-1')
    header = None
    rows = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        cells = raw.split('\t')
        if header is None:
            header = [c.strip() for c in cells]
            continue
        row = {name: _cell(cells[i]) if i < len(cells) else None
               for i, name in enumerate(header) if name}
        if row.get('Name'):
            rows.append(row)
    return rows


def transmission_ratios(row):
    """Ratio1..Ratio12 from a Trans_Presets row, dropping unused (None) positions."""
    out = []
    for i in range(1, 13):
        value = row.get(f'Ratio{i}')
        if value is None:
            break
        out.append(value)
    return out
