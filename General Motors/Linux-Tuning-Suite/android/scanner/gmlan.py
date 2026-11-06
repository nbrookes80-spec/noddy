"""GMLAN readings decoded from the bus, shown the way a factory scan tool names them.

Only layouts that are confirmed are decoded. The GMLAN README (in the capture folder) names the signals in
each message but not where they sit in the bytes, so the gear comes only from the four 1F5 examples it gives.
The capture has the Park frame; Reverse, Neutral and Drive come from the README examples alone. Any other
payload on 1F5, or any other ID, decodes to nothing. Raw bytes never reach the Live screen: it shows the name.
"""

GEAR_ID = 0x1F5
STALE_SECONDS = 3.0      # a reading older than this is gone: the bus has stopped sending that message
GEAR_FRAMES = {
    bytes.fromhex('0F0F000100000300'): 'Park',
    bytes.fromhex('0F0F000200000300'): 'Reverse',
    bytes.fromhex('0F0F000300000300'): 'Neutral',
    bytes.fromhex('0F0F000400000300'): 'Drive',
}


def decode(can_id, data):
    """The readings in one frame, as {name: value}. Empty when the frame is not a known layout."""
    if can_id == GEAR_ID and bytes(data) in GEAR_FRAMES:
        return {'gear': GEAR_FRAMES[bytes(data)]}
    return {}


def gear_frame(gear):
    """The 1F5 payload for a gear name, as the README gives it. Used by the simulated bus."""
    return next(data for data, name in GEAR_FRAMES.items() if name == gear)


def readings(items):
    """The readings from the latest frame of each ID. items maps CAN ID to the sniffer's SnifferItem."""
    out = {}
    for can_id, item in items.items():
        out.update(decode(can_id, bytes(item.current[:item.length])))
    return out


class Latest:
    """The newest payload seen for each ID, stamped with the local clock when it arrived.

    Frame timestamps from the adapter count from each listening window, so they cannot be compared
    across windows; the arrival time is what a reading's age is measured from.
    """

    def __init__(self):
        self._seen = {}   # CAN ID -> (payload, arrival time)

    def feed(self, frames, now):
        for frame in frames:
            self._seen[frame.can_id] = (bytes(frame.data), now)

    def readings(self, now, max_age=STALE_SECONDS):
        out = {}
        for can_id, (data, arrived) in self._seen.items():
            if now - arrived <= max_age:
                out.update(decode(can_id, data))
        return out
