"""Builds scanner/pid_table.py from the VE CALAIS Scanner's Kotlin PID database.

Run from the android/ folder:  python3 tools/gen_pid_table.py

It only reads the Kotlin source (it never runs it). The decode formulas in the Kotlin file are either
named parsers in OBD2Protocol.kt or short inline lambdas; both are translated to Python lambdas of
one value: x is the first data byte for kind "byte" and the first two data bytes (A*256+B) for kind
"word".
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SOURCE = (HERE.parents[1] / 'E38' / 'Diagnostic Tools' / 'VE_CALAIS_Scanner' / 'app' / 'src' / 'main'
          / 'java' / 'com' / 'brookes' / 've_calais_obd2' / 'PIDDatabase.kt')
OUTPUT = HERE / 'scanner' / 'pid_table.py'

# Named parsers from OBD2Protocol.kt: name -> (kind, python expression of x).
NAMED = {
    'parseRPM': ('word', 'x / 4.0'),
    'parseCoolantTemp': ('byte', 'x - 40'),
    'parseIntakeAirTemp': ('byte', 'x - 40'),
    'parseEngineLoad': ('word', 'x * 100.0 / 65536.0'),
    'parseCalculatedLoad': ('byte', 'x * 100.0 / 255.0'),
    'parseMAP': ('byte', 'x / 255.0 * 300.0'),
    'parseThrottlePosition': ('byte', 'x * 100.0 / 255.0'),
    'parseMAF': ('word', 'x / 100.0'),
    'parseOilTemp': ('byte', 'x - 40'),
    'parseAmbientTemp': ('byte', 'x - 40'),
    'parseBaroPressure': ('byte', 'x'),
    'parseFuelLevel': ('byte', 'x * 100.0 / 255.0'),
    'parseFuelPressure': ('byte', 'x * 3'),
    'parseIgnitionTiming': ('byte', 'x / 2.0 - 64.0'),
    'parseO2Voltage': ('byte', 'x * 8.0 / 65535.0'),
    'parseShortFuelTrim': ('byte', '(x - 128) * 100.0 / 128.0'),
    'parseLongFuelTrim': ('byte', '(x - 128) * 100.0 / 128.0'),
    'parseVehicleSpeed': ('byte', 'x'),
    'parseTransmissionTemp': ('byte', 'x - 40'),
    'parseRawByte': ('byte', 'x'),
}

CYLINDER_NOTE = "probable - from Car Scanner's generic export, NOT yet DID-confirmed on this VIN"


def convert_lambda(text):
    """Translate `{ r -> OBD2Protocol.byte(r)?.let { EXPR } }` (or the .word / .toDouble forms)."""
    match = re.match(r'\{ r -> OBD2Protocol\.(byte|word)\(r\)\?\.(?:let \{ (.*) \}|toDouble\(\)) \}$', text)
    if not match:
        raise ValueError(f'unrecognised parse lambda: {text}')
    kind, expr = match.group(1), match.group(2) or 'it'
    expr = expr.replace('.toInt()', '').replace('.toDouble()', '')
    expr = re.sub(r'\bit\b', 'x', expr)
    return kind, expr


def parse_entries(source):
    entries = []
    for block in re.finditer(r'"([0-9A-F]{4,6})" to PIDParameter\((.*?)\n        \),?', source, re.S):
        body = block.group(2)

        def field(name, quoted=True):
            if quoted:
                found = re.search(rf'{name} = "((?:[^"\\]|\\.)*)"', body)
            else:
                found = re.search(rf'{name} = ([^,\n]+),', body)
            return found.group(1) if found else None

        parse_text = re.search(r'parse = (.*)$', body, re.M).group(1).strip()
        if parse_text.startswith('OBD2Protocol::'):
            kind, expr = NAMED[parse_text.split('::')[1]]
        else:
            kind, expr = convert_lambda(parse_text)
        entries.append((
            block.group(1), field('name'), field('category'), field('unit'),
            float(field('min', False)), float(field('max', False)),
            field('description').replace('\\"', '"'), field('header') or 'Auto', kind, expr))
    return entries


def cylinder_entries():
    groups = [
        ('Misfire Cylinder {n} (Current)', 'Engine', 'count', 0.0, 1000.0,
         'Current-trip misfire count, cylinder {n} (%s)' % CYLINDER_NOTE, 'byte', 'x',
         ['221205', '221206', '221207', '221208', '2211EA', '2211EB', '2211EC', '2211ED']),
        ('Misfire Cylinder {n} (History)', 'Engine', 'count', 0.0, 1000.0,
         'Historical misfire count, cylinder {n} (%s)' % CYLINDER_NOTE, 'word', 'x',
         ['221201', '221202', '221203', '221204', '2211F8', '2211F9', '2211FA', '2211FB']),
        ('Injector Pulse Width Cyl {n}', 'Fuel', 'ms', 0.0, 20.0,
         'Injector pulse width, cylinder {n} (%s)' % CYLINDER_NOTE, 'word', 'x / 65.535',
         ['221193', '221194', '221195', '221196', '221197', '221198', '221199', '22119A']),
        ('Fuel Balance Rate Cyl {n}', 'Fuel', '%', -100.0, 100.0,
         'Cylinder fuel balance / trim contribution, cylinder {n} (%s)' % CYLINDER_NOTE, 'word',
         '(x - 32768) * 0.15625 / 10.0',
         ['22162F', '221630', '221631', '221632', '221633', '221634', '221635', '221636']),
    ]
    entries = []
    for name, category, unit, lo, hi, description, kind, expr, addresses in groups:
        for n, address in enumerate(addresses, start=1):
            entries.append((address, name.format(n=n), category, unit, lo, hi, description.format(n=n),
                            'Auto', kind, expr))
    return entries


def main():
    entries = parse_entries(SOURCE.read_text(encoding='utf-8')) + cylinder_entries()
    seen = {}
    for entry in entries:
        seen[entry[0]] = entry
    lines = [
        '"""PID catalogue generated from the VE CALAIS Scanner. Do not edit: run tools/gen_pid_table.py.',
        '',
        'Each row: pid, name, category, unit, min, max, description, header, kind, decode.',
        'kind "byte": decode(x) takes the first data byte. kind "word": x is A*256+B.',
        '"""',
        '',
        'ROWS = [',
    ]
    for pid, name, category, unit, lo, hi, description, header, kind, expr in seen.values():
        lines.append(f'    ({pid!r}, {name!r}, {category!r}, {unit!r}, {lo!r}, {hi!r},')
        lines.append(f'     {description!r},')
        lines.append(f'     {header!r}, {kind!r}, lambda x: {expr}),')
    lines.append(']')
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'wrote {len(seen)} PIDs to {OUTPUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
