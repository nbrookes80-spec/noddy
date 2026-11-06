"""DBC files: the messages and signals a CAN log is decoded with. Standard library only, no Kivy.

Only what a reading needs is kept: each message's ID, and each signal's bit position, length, byte order,
sign, scale (factor and offset), range, unit and multiplexing. Attribute, comment and value-table lines are
ignored. A signal's value is raw * factor + offset, the same as in every DBC reader.
"""

import re
from dataclasses import dataclass
from functools import lru_cache

EXTENDED_FLAG = 0x80000000       # DBC sets this bit on the ID of a 29-bit (extended) message

_MESSAGE = re.compile(r'^\s*BO_\s+(\d+)\s+(\S+?)\s*:\s*(\d+)')
_SIGNAL = re.compile(
    r'^\s*SG_\s+(\S+)\s+(M|m\d+M?)?\s*:\s*(\d+)\|(\d+)@([01])([+-])\s*'
    r'\(([^,\s]+),([^)\s]+)\)\s*\[([^|\s]+)\|([^\]\s]+)\]\s*"([^"]*)"')


@dataclass(frozen=True)
class Signal:
    message_id: int          # the ID as it appears on the bus (29-bit IDs without the DBC extended flag)
    extended: bool
    message: str
    name: str
    start: int               # DBC bit number of the signal's first bit
    length: int
    big_endian: bool         # DBC '@0': Motorola, most significant bit first
    signed: bool
    factor: float
    offset: float
    minimum: float
    maximum: float
    unit: str
    mux_role: str = ''       # '' not multiplexed, 'M' the multiplexer, or 'm' for a signal kept only for one value
    mux_value: int = 0       # for 'm' signals: the multiplexer value that carries this signal

    @property
    def key(self):
        return (self.message_id, self.extended)

    def physical(self, raw):
        return raw * self.factor + self.offset


def parse(text):
    """Every signal in a DBC file's text, in file order. Returns [] for text with no messages."""
    signals, message = [], None
    for line in text.splitlines():
        head = _MESSAGE.match(line)
        if head:
            raw_id = int(head.group(1))
            message = (raw_id & ~EXTENDED_FLAG, bool(raw_id & EXTENDED_FLAG), head.group(2))
            continue
        if message is None:
            continue
        found = _SIGNAL.match(line)
        if not found:
            continue
        signals.append(_signal(message, found))
    return signals


def _signal(message, found):
    """'M' marks the multiplexer, 'm3' a signal that is only present while the multiplexer reads 3."""
    role = found.group(2) or ''
    mux_role, mux_value = role, 0
    if role.startswith('m'):
        mux_role, mux_value = 'm', int(role[1:].rstrip('M'))
    return Signal(
        message_id=message[0], extended=message[1], message=message[2],
        name=found.group(1), start=int(found.group(3)), length=int(found.group(4)),
        big_endian=found.group(5) == '0', signed=found.group(6) == '-',
        factor=float(found.group(7)), offset=float(found.group(8)),
        minimum=_number(found.group(9)), maximum=_number(found.group(10)), unit=found.group(11),
        mux_role=mux_role, mux_value=mux_value)


def _number(text):
    try:
        return float(text)
    except ValueError:
        return 0.0


@lru_cache(maxsize=512)
def bit_positions(start, length, big_endian):
    """The bit numbers of a signal, most significant first, so the raw value is built by reading them in order."""
    if not big_endian:
        return tuple(start + i for i in range(length))
    positions = []
    byte, bit = divmod(start, 8)
    for _ in range(length):
        positions.append(byte * 8 + bit)
        if bit == 0:
            byte, bit = byte + 1, 7
        else:
            bit -= 1
    return tuple(positions)


def raw_value(signal, data):
    """The unsigned or signed raw integer of a signal in a frame's data bytes. None when the frame is too short."""
    positions = bit_positions(signal.start, signal.length, signal.big_endian)
    if not positions or max(positions) >= 8 * len(data):
        return None
    bits = int.from_bytes(bytes(data), 'little')
    if signal.big_endian:
        raw = 0
        for position in positions:
            raw = (raw << 1) | ((bits >> position) & 1)
    else:
        raw = (bits >> signal.start) & ((1 << signal.length) - 1)
    if signal.signed and raw >= 1 << (signal.length - 1):
        raw -= 1 << signal.length
    return raw
