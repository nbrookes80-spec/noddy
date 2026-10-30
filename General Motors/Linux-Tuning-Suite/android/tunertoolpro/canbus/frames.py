"""CAN frames and the text formats they travel in: ELM327 monitor lines, SLCAN, candump logs and CSV.

Everything here is plain Python with no hardware and no Qt, so it runs the same on Linux, Windows and
Android. Parsers return None for a line that is not a frame (prompts, "BUFFER FULL", blank lines),
so a noisy stream can be fed straight in.
"""

import re
from dataclasses import dataclass

HEX = re.compile(r'^[0-9A-Fa-f]+$')
MAX_STANDARD = 0x7FF
MAX_EXTENDED = 0x1FFFFFFF


@dataclass(frozen=True)
class Frame:
    can_id: int
    data: bytes
    extended: bool = False
    timestamp: float = 0.0   # seconds; only differences between frames matter

    def id_text(self):
        return f'{self.can_id:08X}' if self.extended else f'{self.can_id:03X}'

    def data_text(self):
        return ' '.join(f'{b:02X}' for b in self.data)


def _make(can_id, data, extended, timestamp):
    limit = MAX_EXTENDED if extended else MAX_STANDARD
    if not 0 <= can_id <= limit or len(data) > 8:
        return None
    return Frame(can_id, bytes(data), extended, timestamp)


def parse_elm_line(line, timestamp=0.0):
    """One line of ELM327 monitor output with headers and spaces on: '7E8 06 41 0C 1A F8 00 00 00'."""
    tokens = line.strip().upper().split()
    if not tokens or not all(HEX.match(t) for t in tokens):
        return None
    if len(tokens) == 1:   # headers on, spaces off: 3 hex digits of ID, then whole bytes
        text = tokens[0]
        if len(text) >= 3 and (len(text) - 3) % 2 == 0:
            tokens = [text[:3]] + [text[i:i + 2] for i in range(3, len(text), 2)]
        else:
            return None
    head, rest = tokens[0], tokens[1:]
    if len(head) not in (3, 8) or any(len(t) != 2 for t in rest):
        return None
    return _make(int(head, 16), bytes(int(t, 16) for t in rest), len(head) == 8, timestamp)


def parse_slcan_line(line, timestamp=0.0):
    """SLCAN / Lawicel: 't1238AABBCCDDEEFF00' (11-bit) or 'T123456788AABBCCDDEEFF00' (29-bit)."""
    text = line.strip()
    if not text or text[0] not in 'tT':
        return None
    extended = text[0] == 'T'
    id_digits = 8 if extended else 3
    body = text[1:]
    if len(body) < id_digits + 1 or not HEX.match(body):
        return None
    length = int(body[id_digits], 16)
    payload = body[id_digits + 1:id_digits + 1 + 2 * length]
    if length > 8 or len(payload) != 2 * length:
        return None
    return _make(int(body[:id_digits], 16), bytes.fromhex(payload), extended, timestamp)


_CANDUMP_HASH = re.compile(r'^\((?P<ts>[\d.]+)\)\s+\S+\s+(?P<id>[0-9A-Fa-f]{3,8})#(?P<data>[0-9A-Fa-f]*)\s*$')
_CANDUMP_PLAIN = re.compile(r'^\s*\S+\s+(?P<id>[0-9A-Fa-f]{3,8})\s+\[(?P<len>\d)\]\s*(?P<data>(?:[0-9A-Fa-f]{2}\s*)*)$')


def parse_candump_line(line, timestamp=0.0):
    """can-utils: '(1436509052.249713) can0 123#DEADBEEF' or the plain 'can0  123   [4]  DE AD BE EF'."""
    text = line.strip()
    match = _CANDUMP_HASH.match(text)
    if match:
        digits = match['data']
        if len(digits) % 2:
            return None
        return _make(int(match['id'], 16), bytes.fromhex(digits), len(match['id']) == 8, float(match['ts']))
    match = _CANDUMP_PLAIN.match(text)
    if match:
        payload = bytes.fromhex(match['data'].replace(' ', ''))
        if len(payload) != int(match['len']):
            return None
        return _make(int(match['id'], 16), payload, len(match['id']) == 8, timestamp)
    return None


def parse_csv_line(line, timestamp=0.0):
    """'time,id,extended,data' as written by format_csv, with the ID and data in hex."""
    parts = [p.strip() for p in line.strip().split(',')]
    if len(parts) != 4 or not HEX.match(parts[1] or 'x'):
        return None
    try:
        when = float(parts[0])
    except ValueError:
        return None
    digits = parts[3].replace(' ', '')
    if len(digits) % 2 or (digits and not HEX.match(digits)):
        return None
    return _make(int(parts[1], 16), bytes.fromhex(digits), parts[2] in ('1', 'true', 'True'), when)


def parse_line(line, timestamp=0.0):
    """Try each known format. Useful for log files whose format is not known in advance."""
    for parser in (parse_candump_line, parse_csv_line, parse_slcan_line, parse_elm_line):
        frame = parser(line, timestamp)
        if frame is not None:
            return frame
    return None


def read_log(text):
    """Frames from the text of a log file in any supported format. Lines that are not frames are skipped.

    Frames with no timestamp of their own (plain candump, ELM output) are spaced 1 ms apart so that
    replay keeps their order.
    """
    frames = []
    for number, line in enumerate(text.splitlines()):
        frame = parse_line(line, timestamp=number * 0.001)
        if frame is not None:
            frames.append(frame)
    return frames


def format_candump(frames, channel='can0'):
    lines = []
    for frame in frames:
        lines.append(f'({frame.timestamp:.6f}) {channel} {frame.id_text()}#{frame.data.hex().upper()}')
    return '\n'.join(lines) + ('\n' if lines else '')


def format_csv(frames):
    lines = ['time,id,extended,data']
    for frame in frames:
        lines.append(f'{frame.timestamp:.6f},{frame.id_text()},{int(frame.extended)},{frame.data.hex().upper()}')
    return '\n'.join(lines) + '\n'
