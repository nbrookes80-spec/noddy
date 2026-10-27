"""PID catalogue and response decoding, ported from the VE CALAIS Scanner. No Kivy, no I/O.

The catalogue (pid_table.py) is generated from that app's Kotlin source. Rows marked "probable" or
"unverified" in their description have not been confirmed against a real vehicle.
"""

from dataclasses import dataclass
from typing import Callable

from . import pid_table

DEFAULT_HEADER = '7DF'   # standard CAN functional request address
KNOWN_HEADERS = ('7DF', '7E0', '7E2', '7E3')

# Shown on the live dashboard by default, four to a page (same list as the original scanner).
MONITOR_PIDS = [
    '010C', '0105', '010B', '0133',
    '010A', '010E', '0143', '010F',
    '0146', '010D', '0114', '0152',
    '0106', '0107', '22194F', '22001F',
    '221991', '22199A', '0101', '0103',
]
PAGE_SIZE = 4


@dataclass(frozen=True)
class Pid:
    pid: str
    name: str
    category: str
    unit: str
    low: float
    high: float
    description: str
    header: str
    kind: str
    decode: Callable[[int], float]

    @property
    def mode(self):
        return '22' if self.pid.startswith('22') else '01'

    @property
    def command(self):
        """The text sent to the adapter: 01XX for Mode 01, 22XXXX for Mode 22."""
        return self.pid

    @property
    def echo(self):
        """What a good reply starts with: 41XX for Mode 01, 62XXXX for Mode 22."""
        return ('62' if self.mode == '22' else '41') + self.pid[2:]

    @property
    def verified(self):
        text = self.description.lower()
        return 'probable' not in text and 'unverified' not in text

    def parse(self, data):
        """Decode the data bytes (hex text, after the reply echo). None when too short or invalid."""
        width = 4 if self.kind == 'word' else 2
        if len(data) < width:
            return None
        try:
            raw = int(data[:width], 16)
        except ValueError:
            return None
        return float(self.decode(raw))


CATALOG = {row[0]: Pid(*row) for row in pid_table.ROWS}


def get(pid):
    return CATALOG.get(pid)


def categories():
    return sorted({p.category for p in CATALOG.values()})


def in_category(category):
    return [p for p in CATALOG.values() if p.category == category]


def monitor_pages(pids=None, size=PAGE_SIZE):
    """The dashboard pages: lists of Pid, `size` to a page, skipping ids that are not in the catalogue."""
    chosen = [CATALOG[p] for p in (pids or MONITOR_PIDS) if p in CATALOG]
    return [chosen[i:i + size] for i in range(0, len(chosen), size)]


def decode_dtcs(data):
    """Mode 03 data bytes (hex text, after the 43 echo) -> codes like P0301. 0000 pairs are padding."""
    codes = []
    for i in range(0, len(data) - 3, 4):
        pair = data[i:i + 4]
        if pair == '0000':
            continue
        try:
            first = int(pair[:2], 16)
        except ValueError:
            continue
        prefix = 'PCBU'[(first >> 6) & 3]
        codes.append(f'{prefix}{(first >> 4) & 3}{first & 0xF:X}{pair[2:]}')
    return codes
