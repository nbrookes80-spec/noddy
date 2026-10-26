"""Read-only OBD-II link to an ELM327-compatible scan adapter, over Wi-Fi (TCP) or Bluetooth (RFCOMM).

Only the commands in ALLOWED are ever sent. They set up the adapter and read live Mode 01 values
(the same data a scan tool shows). Nothing here writes to the controller: no Mode 04 clears, no
Mode 08 tests, no Mode 09 writes, no ECU programming. An unlisted command raises UnsafeCommand
before anything is sent.

Wi-Fi is the fallback path: many adapters open a hotspot at 192.168.0.10 port 35000. Bluetooth
Classic (SPP) needs the adapter paired in Android settings first. The Bluetooth path can only run
on Android, and it has not been tested with a real adapter yet.
"""

import re
import socket

SPP_UUID = '00001101-0000-1000-8000-00805F9B34FB'
DEFAULT_WIFI = ('192.168.0.10', 35000)

# Adapter set-up commands: reset, echo off, no line feeds, no headers, no spaces, auto protocol.
SETUP_COMMANDS = ('ATZ', 'ATE0', 'ATL0', 'ATH0', 'ATS0', 'ATSP0')
ALLOWED = set(SETUP_COMMANDS) | {'0100'}

# PID -> (name, unit, bytes, decode(A, B)). Mode 01 only.
PIDS = {
    '0105': ('Coolant temperature', 'C', 1, lambda a, b: a - 40),
    '010C': ('Engine speed', 'rpm', 2, lambda a, b: (256 * a + b) / 4),
    '010D': ('Vehicle speed', 'km/h', 1, lambda a, b: a),
    '010F': ('Intake air temperature', 'C', 1, lambda a, b: a - 40),
    '0111': ('Throttle position', '%', 1, lambda a, b: a * 100 / 255),
}
ALLOWED |= set(PIDS)

ERROR_WORDS = ('NO DATA', 'ERROR', 'UNABLE', 'STOPPED', 'BUS INIT', '?', 'CAN ERROR')


class OBDError(Exception):
    """The adapter did not answer, or answered with an error or unexpected text."""


class UnsafeCommand(Exception):
    """A command outside the read-only allowlist was refused before it was sent."""


class WifiTransport:
    def __init__(self, host=DEFAULT_WIFI[0], port=DEFAULT_WIFI[1], timeout=5.0):
        self.host, self.port, self.timeout = host, port, timeout
        self._sock = None
        self._buffer = b''

    def open(self):
        try:
            self._sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        except OSError as exc:
            raise OBDError(f'Could not reach the Wi-Fi adapter at {self.host}:{self.port} ({exc})') from exc

    def write(self, data):
        self._sock.sendall(data)

    def read_until(self, prompt=b'>'):
        """Read until the adapter's prompt character arrives. Returns the text before it."""
        while prompt not in self._buffer:
            try:
                chunk = self._sock.recv(256)
            except socket.timeout as exc:
                raise OBDError('The adapter stopped answering') from exc
            if not chunk:
                raise OBDError('The adapter closed the connection')
            self._buffer += chunk
        reply, _, self._buffer = self._buffer.partition(prompt)
        return reply

    def close(self):
        if self._sock is not None:
            self._sock.close()
            self._sock = None


class BluetoothTransport:
    """Bluetooth Classic SPP through Android's API (pyjnius). Android only."""

    def __init__(self, address):
        self.address = address
        self._in = None
        self._out = None
        self._socket = None

    def open(self):
        try:
            from jnius import autoclass  # only available inside the Android app
        except ImportError as exc:
            raise OBDError('Bluetooth needs the Android app. It cannot run on this computer.') from exc
        try:
            adapter = autoclass('android.bluetooth.BluetoothAdapter').getDefaultAdapter()
            if adapter is None or not adapter.isEnabled():
                raise OBDError('Turn Bluetooth on in the phone settings first.')
            device = adapter.getRemoteDevice(self.address)
            uuid = autoclass('java.util.UUID').fromString(SPP_UUID)
            self._socket = device.createRfcommSocketToServiceRecord(uuid)
            adapter.cancelDiscovery()
            self._socket.connect()
            self._in = self._socket.getInputStream()
            self._out = self._socket.getOutputStream()
        except OBDError:
            raise
        except Exception as exc:  # Java exceptions surface through pyjnius
            raise OBDError(f'Could not connect over Bluetooth to {self.address}: {exc}') from exc

    def write(self, data):
        self._out.write([b - 256 if b > 127 else b for b in data])
        self._out.flush()

    def read_until(self, prompt=b'>'):
        out = bytearray()
        while True:
            value = self._in.read()
            if value < 0:
                raise OBDError('The adapter closed the connection')
            if value == prompt[0]:
                return bytes(out)
            out.append(value & 0xFF)

    def close(self):
        if self._socket is not None:
            self._socket.close()
        self._socket = self._in = self._out = None


class Elm327:
    """Sends allowlisted commands and decodes the replies. Use one instance per connection."""

    def __init__(self, transport):
        self.transport = transport

    def open(self):
        self.transport.open()
        for command in SETUP_COMMANDS:
            self.command(command)

    def close(self):
        self.transport.close()

    def command(self, command):
        if command not in ALLOWED:
            raise UnsafeCommand(f'{command!r} is not a read-only command, so it was not sent')
        self.transport.write((command + '\r').encode('ascii'))
        raw = self.transport.read_until(b'>')
        return raw.decode('ascii', 'replace').replace('\r', '\n').strip()

    def read(self, pid):
        """Return (value, unit) for one Mode 01 PID, or raise OBDError."""
        if pid not in PIDS:
            raise UnsafeCommand(f'{pid!r} is not on the read list')
        name, unit, width, decode = PIDS[pid]
        text = self.command(pid).upper()
        if any(word in text for word in ERROR_WORDS):
            raise OBDError(f'{name}: the adapter replied "{text.splitlines()[-1].strip()}"')
        hex_text = re.sub(r'[^0-9A-F]', '', text.replace('SEARCHING', ''))
        header = '41' + pid[2:]
        at = hex_text.find(header)
        if at < 0:
            raise OBDError(f'{name}: unexpected reply "{text}"')
        data = hex_text[at + len(header):]
        if len(data) < 2 * width:
            raise OBDError(f'{name}: reply too short "{text}"')
        a = int(data[0:2], 16)
        b = int(data[2:4], 16) if width == 2 else 0
        return decode(a, b), unit

    def poll(self, pids):
        """Read several PIDs. Returns {pid: (value, unit)} for those that answered, and {pid: error text}."""
        values, errors = {}, {}
        for pid in pids:
            try:
                values[pid] = self.read(pid)
            except OBDError as exc:
                errors[pid] = str(exc)
        return values, errors
