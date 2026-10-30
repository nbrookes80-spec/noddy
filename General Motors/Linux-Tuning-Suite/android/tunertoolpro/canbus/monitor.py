"""Listen to a CAN bus through an ELM327-compatible adapter. Receive only: nothing is ever transmitted.

The adapter's ATMA command ("monitor all") makes it print every frame it hears and send nothing, so it
cannot disturb the bus. Only the commands that is_allowed() accepts are ever written to the adapter:
set-up (reset, echo, headers, protocol), an optional receive filter, and ATMA itself. Anything else
raises UnsafeCommand before it is sent. That is a narrower list than the OBD link's, and it contains
no request to any module.

A transport is anything with open(), write(bytes), read_until(b'>') -> bytes, read_chunk(timeout) ->
bytes (b'' when nothing arrived) and close(). The TCP and serial ones are in transports.py; the
Android app wraps its Bluetooth socket the same way.

An ELM327 is slow next to a busy bus. It copes with a few hundred frames a second, and reports
BUFFER FULL when it falls behind, which the monitor counts in overruns. A receive filter (rx_filter)
makes it much quieter.
"""

import re
import time

from .frames import Frame, parse_elm_line

PROTOCOLS = {
    '6': 'CAN 500 kbit/s, 11-bit IDs (most cars, GM HS-CAN)',
    '7': 'CAN 500 kbit/s, 29-bit IDs',
    '8': 'CAN 250 kbit/s, 11-bit IDs',
    '9': 'CAN 250 kbit/s, 29-bit IDs',
    'A': 'J1939, 250 kbit/s, 29-bit IDs',
    '0': 'Automatic',
}
DEFAULT_PROTOCOL = '6'

# Echo off, line feeds off, headers on, spaces on, raw frames (no OBD formatting), then the protocol.
SETUP_COMMANDS = ('ATE0', 'ATL0', 'ATH1', 'ATS1', 'ATCAF0')
RESTORE_COMMANDS = ('ATAR', 'ATH0', 'ATS0', 'ATCAF1', 'ATSP0')   # back to what the OBD link expects
_ALLOWED_FIXED = {'ATZ', 'ATMA', 'ATAR', *SETUP_COMMANDS, *RESTORE_COMMANDS}
_ALLOWED_PATTERN = re.compile(r'^(ATSP[0-9A-C]|ATCRA[0-9A-F]{3}|ATCRA[0-9A-F]{8})$')

BAD_LINES = ('BUFFER FULL', 'CAN ERROR', 'DATA ERROR', 'STOPPED', 'UNABLE', 'ERROR', '?')


class MonitorError(Exception):
    """The adapter did not answer, or refused a set-up command."""


class UnsafeCommand(Exception):
    """A command outside the receive-only allowlist was refused before it was sent."""


def is_allowed(command):
    command = command.replace(' ', '').upper()
    return command in _ALLOWED_FIXED or bool(_ALLOWED_PATTERN.match(command))


def monitor_commands(protocol=DEFAULT_PROTOCOL, rx_filter=None):
    """The exact commands sent to start listening, in order. rx_filter is a hex ID such as '7E8'."""
    commands = list(SETUP_COMMANDS) + [f'ATSP{protocol}']
    if rx_filter:
        commands.append(f'ATCRA{rx_filter.upper()}')
    return commands


class ElmMonitor:
    def __init__(self, transport, clock=time.monotonic):
        self.transport = transport
        self.clock = clock
        self.running = False
        self.overruns = 0
        self.traffic = []        # (direction, text) of the set-up conversation, newest last
        self._partial = ''
        self._started_at = 0.0
        self._last_chunk = 0.0     # seconds since start when the previous chunk arrived

    def command(self, command):
        if not is_allowed(command):
            raise UnsafeCommand(f'{command!r} is not a receive-only command, so it was not sent')
        command = command.replace(' ', '').upper()
        self.traffic.append(('TX', command))
        try:
            self.transport.write((command + '\r').encode('ascii'))
            raw = self.transport.read_until(b'>')
        except Exception as exc:
            raise MonitorError(f'The adapter stopped answering during {command}: {exc}') from exc
        reply = raw.decode('ascii', 'replace').replace('\r', '\n').strip()
        self.traffic.append(('RX', reply.replace('\n', ' ')))
        del self.traffic[:-100]
        return reply

    def start(self, protocol=DEFAULT_PROTOCOL, rx_filter=None):
        """Configure the adapter and begin monitoring. Returns once frames can be read with poll()."""
        if protocol not in PROTOCOLS:
            raise MonitorError(f'Unknown CAN protocol {protocol!r}')
        if rx_filter and not re.fullmatch(r'[0-9A-Fa-f]{3}|[0-9A-Fa-f]{8}', rx_filter):
            raise MonitorError('The receive filter must be one CAN ID in hex, such as 7E8')
        for command in monitor_commands(protocol, rx_filter):
            reply = self.command(command)
            if any(word in reply.upper() for word in ('?', 'ERROR', 'UNABLE')):
                raise MonitorError(f'The adapter refused {command}: {reply.splitlines()[-1]}')
        self.transport.write(b'ATMA\r')
        self.traffic.append(('TX', 'ATMA'))
        self.running = True
        self.overruns = 0
        self._partial = ''
        self._started_at = self.clock()
        self._last_chunk = 0.0

    def poll(self, timeout=0.2):
        """Frames heard since the last call (possibly none). Call it in a loop while running."""
        if not self.running:
            return []
        try:
            chunk = self.transport.read_chunk(timeout)
        except Exception as exc:
            self.running = False
            raise MonitorError(f'The adapter stopped sending: {exc}') from exc
        if not chunk:
            return []
        return self.parse(chunk.decode('ascii', 'replace'))

    def parse(self, text):
        """Frames in a block of monitor text. The adapter sends no timestamps, so the frames of one
        block are spread evenly over the time since the previous block; that keeps per-ID spacing,
        and so Delta and Frequency, close to the truth even when several frames arrive at once."""
        now = self.clock() - self._started_at
        text = self._partial + text.replace('\r', '\n')
        *lines, self._partial = text.split('\n')
        parsed = []
        for line in lines:
            line = line.strip().rstrip('>').strip()
            if not line:
                continue
            frame = parse_elm_line(line, 0.0)
            if frame is not None:
                parsed.append(frame)
            elif 'BUFFER FULL' in line.upper():
                self.overruns += 1
        span = max(0.0, now - self._last_chunk)
        frames = [Frame(f.can_id, f.data, f.extended, self._last_chunk + span * (i + 1) / len(parsed))
                  for i, f in enumerate(parsed)]
        self._last_chunk = now
        return frames

    def restore(self):
        """Put the adapter back as the OBD link expects it (headers and spaces off, auto protocol)."""
        for command in RESTORE_COMMANDS:
            self.command(command)

    def stop(self):
        """Leave monitor mode and hand the adapter back. Safe to call twice."""
        if not self.running:
            return
        self.running = False
        try:
            self.transport.write(b'\r')   # any character interrupts ATMA
            self.transport.read_until(b'>')
            self.restore()
        except Exception as exc:
            raise MonitorError(f'Could not hand the adapter back cleanly: {exc}') from exc
