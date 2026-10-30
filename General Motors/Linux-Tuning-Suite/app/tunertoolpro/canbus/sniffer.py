"""Live CAN sniffer: list the IDs that are updating and show which bytes and bits just changed.

This is a port of the Sniffer window in SavvyCAN (Collin Kidder, MIT licence, see
docs/THIRD_PARTY.md), in the spirit of can-utils' cansniffer: an ID that goes quiet drops off the list,
a byte that went up shows green, one that went down shows red, and "notching" learns which bits
change all the time so they stop drawing the eye. Nothing here touches hardware or draws anything; a
screen asks for rows() and paints them.

Two clocks drive it, the same as SavvyCAN: feed() is called whenever frames arrive, tick() about
every 200 ms to age things, and tick_notch() every notch interval (also about 200 ms) to restart the
window in which changed bits are collected.
"""

import time

MAX_BYTES = 8
EXPIRE_SECONDS = 5.0        # an ID not seen for this long leaves the list
STALE_SECONDS = 4.0         # ...and its ID turns red after this long
FADE_STEP = 10              # grey level gained per tick since a byte last changed
FADE_MAX = 225

NONE, INC, DEC = 'none', 'inc', 'dec'


class SnifferItem:
    """What is known about one CAN ID: its latest and previous data, and when each byte last changed."""

    def __init__(self, frame, seq, now):
        self.can_id = frame.can_id
        self.extended = frame.extended
        self.length = len(frame.data)
        self.current = self._padded(frame.data)
        self.last = list(self.current)
        self.byte_seq = [seq] * MAX_BYTES        # tick number at which each byte last changed
        self.notch = [0] * MAX_BYTES             # bits to ignore
        self.marker = [0] * MAX_BYTES            # bits changed in the window being collected
        self.last_marker = [0] * MAX_BYTES       # bits changed in the previous window
        self.seq = seq
        self.current_time = self.last_time = frame.timestamp   # the frame's own time, as SavvyCAN does
        self.touched = now                       # when the latest frame arrived

    @staticmethod
    def _padded(data):
        return list(data[:MAX_BYTES]) + [0] * (MAX_BYTES - len(data[:MAX_BYTES]))

    def update(self, frame, seq, now, mute=False):
        """A new frame for this ID. mute leaves notched bits out of the comparison, as SavvyCAN does."""
        self.last = list(self.current)
        self.last_time = self.current_time
        self.seq = seq
        incoming = self._padded(frame.data)
        count = min(len(frame.data), MAX_BYTES)
        for i in range(count):
            new_value, old_value = incoming[i], self.current[i]
            if mute:
                new_value &= ~self.notch[i] & 0xFF
                old_value &= ~self.notch[i] & 0xFF
            if new_value != old_value:
                self.current[i] = incoming[i]
                self.byte_seq[i] = seq
        self.length = count
        self.current_time = frame.timestamp
        self.touched = now
        for i in range(MAX_BYTES):
            self.marker[i] |= self.last[i] ^ self.current[i]

    def update_marker(self):
        """Close the window of changed bits and start a new one."""
        self.last_marker = list(self.marker)
        self.marker = [0] * MAX_BYTES

    def set_notch(self, on):
        if on:
            self.notch = [n | m for n, m in zip(self.notch, self.last_marker)]
        else:
            self.notch = [0] * MAX_BYTES

    def delta(self):
        """Seconds between the last two frames of this ID (0 if a log looped or the clock stepped back)."""
        return max(0.0, self.current_time - self.last_time)

    def elapsed(self, now):
        return now - self.touched

    def change(self, i):
        """INC, DEC or NONE for byte i, as SavvyCAN's dataChange does."""
        if i >= self.length:
            return NONE
        notch, byte, last = self.notch[i], self.current[i], self.last[i]
        if not self.last_marker[i]:
            return NONE
        if not notch:
            return INC if byte >= last else DEC
        byte &= ~notch & 0xFF
        if byte == 0:
            return NONE
        last &= ~notch & 0xFF
        if last == byte:
            return NONE
        return INC if byte >= last else DEC

    def fade(self, i):
        """0 (just changed) to FADE_MAX (long quiet): how far to grey byte i out."""
        return max(0, min(FADE_MAX, (self.seq - self.byte_seq[i]) * FADE_STEP))

    def bits(self, i):
        """Eight (state) values for byte i, most significant bit first: notched, set, unset, rose, fell."""
        out = []
        for shift in range(7, -1, -1):
            mask = 1 << shift
            now_set, was_set = bool(self.current[i] & mask), bool(self.last[i] & mask)
            if self.notch[i] & mask:
                out.append('notched')
            elif now_set == was_set:
                out.append('set' if now_set else 'unset')
            else:
                out.append('rose' if now_set else 'fell')
        return out


class Sniffer:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.items = {}
        self.seq = 0
        self.never_expire = False
        self.fade_inactive = False
        self.mute_notched = False
        self.expire_seconds = EXPIRE_SECONDS
        self._filter = None      # None shows everything; otherwise the set of IDs allowed to show
        self.frames_seen = 0

    # --- input ---------------------------------------------------------------------------------
    def feed(self, frames):
        now = self.clock()
        for frame in frames:
            self.frames_seen += 1
            item = self.items.get(frame.can_id)
            if item is None:
                self.items[frame.can_id] = SnifferItem(frame, self.seq, now)
            else:
                item.update(frame, self.seq, now, self.mute_notched)

    def tick(self):
        """Age the list. Returns the IDs that were dropped for being quiet too long."""
        self.seq += 1
        if self.never_expire:
            return []
        now = self.clock()
        gone = [i for i, item in self.items.items() if item.elapsed(now) > self.expire_seconds]
        for can_id in gone:
            del self.items[can_id]
            if self._filter is not None:
                self._filter.discard(can_id)
        return gone

    def tick_notch(self):
        for item in self.items.values():
            item.update_marker()

    def clear(self):
        self.items.clear()
        self._filter = None
        self.frames_seen = 0

    # --- notching ------------------------------------------------------------------------------
    def notch(self):
        """Ignore every bit that changed in the last window, on every visible ID."""
        for item in self._visible_items():
            item.set_notch(True)

    def unnotch(self):
        for item in self._visible_items():
            item.set_notch(False)

    # --- filtering -----------------------------------------------------------------------------
    def show_all(self):
        self._filter = None

    def hide_all(self):
        self._filter = set()

    def set_visible(self, can_id, visible):
        if self._filter is None:
            self._filter = set(self.items)
        (self._filter.add if visible else self._filter.discard)(can_id)

    def is_visible(self, can_id):
        return self._filter is None or can_id in self._filter

    def _visible_items(self):
        return [item for can_id, item in sorted(self.items.items()) if self.is_visible(can_id)]

    # --- output --------------------------------------------------------------------------------
    def ids(self):
        return sorted(self.items)

    def rows(self):
        """One dict per visible ID, in ID order, ready to draw."""
        now = self.clock()
        return [self._row(item, now) for item in self._visible_items()]

    def row_for(self, can_id):
        """The row for one ID whether or not the filter shows it, or None if it is not on the bus."""
        item = self.items.get(can_id)
        return self._row(item, self.clock()) if item is not None else None

    def _row(self, item, now):
        delta = item.delta()
        freq = f'{round(1 / delta)} hz' if delta > 0 else '0 hz'
        cells = []
        for i in range(MAX_BYTES):
            if i >= item.length:
                cells.append(None)
                continue
            cells.append({'text': f'{item.current[i]:02X}', 'change': item.change(i),
                          'fade': item.fade(i) if self.fade_inactive else 0,
                          'notched': item.notch[i], 'bits': item.bits(i)})
        return {'id': item.can_id, 'extended': item.extended,
                'id_text': f'{item.can_id:08X}' if item.extended else f'{item.can_id:03X}',
                'delta': delta, 'freq': freq, 'stale': item.elapsed(now) > STALE_SECONDS, 'bytes': cells}
