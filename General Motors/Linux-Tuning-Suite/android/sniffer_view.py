"""The CAN sniffer's rows as text for the phone screen. No Kivy here, so it can be tested.

A byte that went up gets a + after it and shows green, one that went down gets a - and shows red, and
a byte with notched bits gets a dot. The markers say what the colour says, for anyone who cannot tell
green from red (the Shift tables do the same with ~ and !).
"""

import os
import re
import time

HEX = {'inc': '66cc8c', 'dec': 'ff6661', 'stale': 'ff6661', 'notched': '6b7684', 'plain': 'ffffff',
       'unset': 'bcc9d6'}
MARKER = {'inc': '+', 'dec': '-', 'none': ' '}
ROW_LIMIT = 60
ID_WIDTH = 8
RATE_WIDTH = 6
LINE_CHARS = ID_WIDTH + 1 + RATE_WIDTH + 1 + 8 * 3 + 7 + 1    # the widest row, so the screen can size its font


def _tag(colour, text):
    return f'[color=#{colour}]{text}[/color]'


def _grey(fade):
    level = max(60, 255 - fade)
    return f'{level:02x}{level:02x}{level:02x}'


def header():
    return f'{"ID":>{ID_WIDTH}} {"rate":>{RATE_WIDTH}} ' + ' '.join(f'{i:>2} ' for i in range(8)).rstrip()


def _byte_cell(cell):
    if cell is None:
        return '   '
    if cell['change'] in ('inc', 'dec'):
        return _tag(HEX[cell['change']], cell['text'] + MARKER[cell['change']])
    marker = '.' if cell['notched'] else ' '
    colour = _grey(cell['fade']) if cell['fade'] else HEX['plain']
    return _tag(colour, cell['text'] + marker)


def table_text(rows, limit=ROW_LIMIT):
    """The header and one line per ID, with colour markup. Rows past the limit are summarised."""
    lines = [header()]
    for row in rows[:limit]:
        ident = f'{row["id_text"]:>{ID_WIDTH}}'
        if row['stale']:
            ident = _tag(HEX['stale'], ident)
        rate = f'{row["freq"].replace(" ", ""):>{RATE_WIDTH}}'
        lines.append(f'{ident} {rate} ' + ' '.join(_byte_cell(c) for c in row['bytes']).rstrip())
    if len(rows) > limit:
        lines.append(f'... and {len(rows) - limit} more IDs. Type IDs under "Only show these IDs" to narrow it.')
    return '\n'.join(lines)


def bits_text(row):
    """One line per byte of a single ID: the eight bits, green just set, red just cleared, grey notched."""
    if row is None:
        return 'That ID is not on the bus right now.'
    lines = [f'ID {row["id_text"]}   {row["freq"]}']
    for i, cell in enumerate(row['bytes']):
        if cell is None:
            continue
        value = int(cell['text'], 16)
        glyphs = []
        for position, state in enumerate(cell['bits']):
            bit = '1' if value & (0x80 >> position) else '0'
            colour = {'rose': HEX['inc'], 'fell': HEX['dec'], 'notched': HEX['notched'],
                      'set': HEX['plain'], 'unset': HEX['unset']}[state]
            glyphs.append(_tag(colour, bit))
        lines.append(f'byte {i}  {cell["text"]}  ' + ''.join(glyphs))
    return '\n'.join(lines)


def parse_ids(text):
    """'7E8, 0c9 18DAF110' -> {0x7E8, 0xC9, 0x18DAF110}. Raises ValueError naming the bad entry."""
    found = set()
    for token in re.split(r'[,\s]+', text.strip()):
        if not token:
            continue
        token = token[2:] if token.lower().startswith('0x') else token
        if not re.fullmatch(r'[0-9A-Fa-f]{1,8}', token):
            raise ValueError(f'"{token}" is not a hex CAN ID')
        found.add(int(token, 16))
    return found


def capture_name(now=None):
    return time.strftime('capture-%Y%m%d-%H%M%S.log', time.localtime(now))


def save_capture(session, folder, now=None):
    """Write the captured frames into folder. Returns (path, frame count)."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, capture_name(now))
    return path, session.save(path)
