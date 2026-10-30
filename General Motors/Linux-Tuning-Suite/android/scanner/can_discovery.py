"""Turn a CAN capture into a plain-text report of what the car is sending. No Kivy, no hardware.

A capture gives three things:
- Module readings: standard OBD-II replies from a module (Mode 01, and Mode 22 for GM). Each one is decoded
  with the app's catalogue, so the report shows the reading, its unit and the module address it came from.
- Broadcast traffic: every other ID. Each is listed with how often it arrives and which of its bytes change.
  That is how an unknown reading is found before anything says what it is.
- Catalogue readings the capture did not show, so you know which ones still need a request to check.

A passive capture only shows what the car already sends. Mode 22 replies appear only when something asks for
them, so a capture with no scan tool attached may show none.
"""

from collections import defaultdict

from scanner import pids

REPLY_IDS = range(0x7E8, 0x7F0)            # module replies; the request for reply 7E8 is 7E0
MODULE_NAMES = {0x7E0: 'Engine (ECM)', 0x7E2: 'Transmission (TCM)'}
BYTES = 8


def module_of(reply_id):
    """The request address a reply comes from (7E8 -> 7E0), and its name when known."""
    request = reply_id - 8
    return request, MODULE_NAMES.get(request, 'Module')


def _single_frame(data):
    """The payload of a single-frame ISO-TP reply, or None for anything else."""
    if not data or data[0] >> 4 != 0 or data[0] & 0x0F == 0:
        return None
    length = data[0] & 0x0F
    if length > len(data) - 1:
        return None
    return data[1:1 + length]


def decode_reply(frame):
    """(reading id, value, unit, name) for a standard reply frame, or None when it is not one.

    value is None when the reading is known but the reply is too short to decode."""
    if frame.can_id not in REPLY_IDS or frame.extended:
        return None
    payload = _single_frame(frame.data)
    if payload is None or len(payload) < 2:
        return None
    if payload[0] == 0x41:
        reading = f'01{payload[1]:02X}'
        body = payload[2:]
    elif payload[0] == 0x62 and len(payload) >= 3:
        reading = f'22{payload[1]:02X}{payload[2]:02X}'
        body = payload[3:]
    else:
        return None
    info = pids.get(reading)
    if info is None:
        return reading, None, '', 'not in the catalogue'
    value = info.parse(''.join(f'{b:02X}' for b in body))
    return reading, value, info.unit, info.name


class Stream:
    """Everything one non-reply ID did in the capture."""

    def __init__(self, can_id):
        self.can_id = can_id
        self.count = 0
        self.first = None
        self.last = None
        self.length = 0
        self.seen = [set() for _ in range(BYTES)]
        self.last_data = b''

    def add(self, frame):
        self.count += 1
        self.first = frame.timestamp if self.first is None else self.first
        self.last = frame.timestamp
        self.length = max(self.length, len(frame.data))
        self.last_data = frame.data
        for index, value in enumerate(frame.data[:BYTES]):
            self.seen[index].add(value)

    @property
    def rate(self):
        span = (self.last or 0) - (self.first or 0)
        return (self.count - 1) / span if self.count > 1 and span > 0 else None

    @property
    def changing(self):
        return [i for i in range(self.length) if len(self.seen[i]) > 1]


def _split(frames):
    """(replies, broadcast streams), where replies is a list of decoded replies with their frame times."""
    replies, streams = [], {}
    for frame in frames:
        decoded = decode_reply(frame)
        if decoded is not None:
            replies.append((frame, decoded))
            continue
        streams.setdefault(frame.can_id, Stream(frame.can_id)).add(frame)
    return replies, streams


def _hex(data):
    return ' '.join(f'{b:02X}' for b in data)


def _frames(count):
    return 'frame' if count == 1 else 'frames'


def _rate_text(rate):
    return f'{rate:.1f}' if rate is not None else '-'


def report(frames):
    """A plain-text report of a capture. frames is a list of Frame with timestamps in seconds."""
    if not frames:
        return 'The capture has no CAN frames. Check the adapter link, the CAN protocol, and that the ignition is on.'
    replies, streams = _split(frames)
    span = max(f.timestamp for f in frames) - min(f.timestamp for f in frames)
    lines = [
        'CAN capture report',
        f'{len(frames)} {_frames(len(frames))} over {span:.1f} s ({len(frames) / span:.1f} per second)'
        if span > 0 else f'{len(frames)} {_frames(len(frames))}',
        f'{len(replies)} standard module replies, {len(streams)} other CAN IDs',
        '',
    ]

    # Module readings, grouped by the module that sent them.
    readings = defaultdict(lambda: defaultdict(list))
    for frame, (reading, value, unit, name) in replies:
        module, _ = module_of(frame.can_id)
        readings[module][(reading, name, unit)].append(value)
    lines.append('Module readings (standard replies)')
    if not readings:
        lines.append('  None. No scan tool was asking, or the car did not answer. Mode 22 needs a request.')
    for module in sorted(readings):
        lines.append(f'  Module {module:03X} {MODULE_NAMES.get(module, "")}'.rstrip())
        for (reading, name, unit), values in sorted(readings[module].items()):
            known = [v for v in values if v is not None]
            if known:
                text = (f'{min(known):g} to {max(known):g} {unit}'.rstrip() if min(known) != max(known)
                        else f'{known[-1]:g} {unit}'.rstrip())
            else:
                text = 'could not decode'
            lines.append(f'    {reading}  {name:<28} {text}  ({len(values)} replies)')
    lines.append('')

    # Broadcast traffic: what the car sends without being asked.
    lines.append('Broadcast traffic (not standard replies)')
    lines.append('  ID     count   rate/s  bytes  changing bytes   last data')
    for can_id in sorted(streams):
        stream = streams[can_id]
        changing = ','.join(str(i) for i in stream.changing) or 'none'
        lines.append(f'  {can_id:03X}  {stream.count:>6}  {_rate_text(stream.rate):>6}  {stream.length:>5}  '
                     f'{changing:<15}  {_hex(stream.last_data)}')
    if not streams:
        lines.append('  None.')
    lines.append('')

    # Catalogue readings the default dashboard expects, but this capture did not show.
    seen = {reading for _, (reading, *_rest) in replies}
    missing = [p for p in pids.DEFAULT_MONITOR if p not in seen]
    lines.append('Dashboard readings not in this capture')
    for pid in missing:
        info = pids.get(pid)
        lines.append(f'  {pid}  {info.name if info else ""}')
    if not missing:
        lines.append('  None.')
    lines.append('')
    lines.append('Changing bytes in a broadcast ID are candidates for a reading. Match them against a known')
    lines.append('value (for example the coolant gauge) before trusting them.')
    return '\n'.join(lines)


CSV_HEADER = ['section', 'module', 'id', 'name', 'count', 'rate_hz', 'value_min', 'value_max', 'unit',
              'changing_bytes', 'last_data']


def csv_rows(frames):
    """The report as spreadsheet rows (header first): one row per module reading, then one per broadcast ID."""
    replies, streams = _split(frames)
    grouped = defaultdict(list)
    for frame, (reading, value, unit, name) in replies:
        module, _ = module_of(frame.can_id)
        grouped[(module, reading, name, unit)].append(value)
    rows = [CSV_HEADER]
    for (module, reading, name, unit), values in sorted(grouped.items()):
        known = [v for v in values if v is not None]
        rows.append(['module reading', f'{module:03X}', reading, name, len(values), '',
                     min(known) if known else '', max(known) if known else '', unit, '', ''])
    for can_id in sorted(streams):
        stream = streams[can_id]
        rate = '' if stream.rate is None else round(stream.rate, 1)
        rows.append(['broadcast', '', f'{can_id:03X}', '', stream.count, rate, '', '', '',
                     ' '.join(str(i) for i in stream.changing), _hex(stream.last_data)])
    return rows
