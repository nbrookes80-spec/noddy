"""Bluecat .BTC tune files.

A .BTC file is a flat list of key line / value line pairs, each terminated by
CRLF. The key set varies by file (331 keys are common to all 33 shipped tunes,
the rest are per-gear TCC and lock fields), so this reader keeps every pair in
file order and does not impose a schema. Reading then writing an unmodified
tune gives back the same bytes.
"""

from pathlib import Path

REQUIRED_KEYS = ('Gears', 'Ratio1', 'Gear', 'Tire', 'Idle', 'Stall')


class BtcTune:
    def __init__(self, pairs=None, source=None):
        self._pairs = [list(p) for p in (pairs or [])]
        self.source = source

    @classmethod
    def from_text(cls, text):
        lines = text.split('\r\n')
        if lines and lines[-1] == '':
            lines = lines[:-1]
        if len(lines) % 2:
            raise ValueError('BTC data has an odd number of lines; expected key/value pairs')
        pairs = [(lines[i], lines[i + 1]) for i in range(0, len(lines), 2)]
        return cls(pairs)

    @classmethod
    def load(cls, path):
        # Latin-1 maps every byte to one character, so unknown bytes survive a round trip.
        text = Path(path).read_bytes().decode('latin-1')
        tune = cls.from_text(text)
        tune.source = str(path)
        return tune

    def to_text(self):
        return ''.join(f'{k}\r\n{v}\r\n' for k, v in self._pairs)

    def save(self, path):
        Path(path).write_bytes(self.to_text().encode('latin-1'))
        self.source = str(path)

    def keys(self):
        return [k for k, _ in self._pairs]

    def pairs(self):
        return [(k, v) for k, v in self._pairs]

    def get(self, key, default=None):
        for k, v in self._pairs:
            if k == key:
                return v
        return default

    def getfloat(self, key, default=None):
        raw = self.get(key)
        if raw is None:
            return default
        try:
            return float(raw)
        except ValueError:
            return default

    def getint(self, key, default=None):
        value = self.getfloat(key)
        return default if value is None else int(value)

    def set(self, key, value):
        value = str(value)
        for pair in self._pairs:
            if pair[0] == key:
                pair[1] = value
                return
        self._pairs.append([key, value])

    def gear_count(self):
        return self.getint('Gears', 0)

    def ratios(self):
        """Gear ratios Ratio1..Ratio<Gears> in gear order."""
        return [self.getfloat(f'Ratio{i}') for i in range(1, self.gear_count() + 1)]

    def missing_required(self):
        return [k for k in REQUIRED_KEYS if self.get(k) is None]
