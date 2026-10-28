"""Read-only OBD-II link to an ELM327-compatible scan adapter, over Wi-Fi (TCP) or Bluetooth (RFCOMM).

Only commands that pass is_allowed() are ever sent: adapter set-up, Mode 01 and Mode 22 reads of PIDs
in the scanner catalogue, the Mode 03 stored-code read, and a header switch to one of four known
module addresses. Nothing here writes to the controller: no Mode 04 clears, no Mode 08 tests, no
Mode 09 writes, no ECU programming, no free-form Mode 22 sweeps. Any other command raises
UnsafeCommand before anything is sent.

Wi-Fi is the fallback path: many adapters open a hotspot at 192.168.0.10 port 35000. Bluetooth
Classic (SPP) needs the adapter paired in Android settings first. The Bluetooth path can only run
on Android, and it has not been tested with a real adapter yet.
"""

import re
import socket
import threading

from scanner import pids as catalog

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
READ_DTC = '03'
ALLOWED.add(READ_DTC)
HEADER_COMMANDS = {f'ATSH{h}' for h in catalog.KNOWN_HEADERS}
ALLOWED |= HEADER_COMMANDS


def is_allowed(command):
    """True for a read-only command: set-up, a header switch, Mode 03, or a catalogued Mode 01/22 PID."""
    command = command.replace(' ', '').upper()
    return command in ALLOWED or command in catalog.CATALOG

ERROR_WORDS = ('NO DATA', 'ERROR', 'UNABLE', 'STOPPED', 'BUS INIT', '?', 'CAN ERROR')
MISS_LIMIT = 3     # a reading with this many failures in a row is skipped...
RETRY_EVERY = 8    # ...and tried again on every eighth later request


class OBDError(Exception):
    """The adapter did not answer, or answered with an error or unexpected text."""


class AdapterLost(OBDError):
    """The adapter stopped answering or closed the link, as opposed to the car not having an answer."""


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
                raise AdapterLost('The adapter stopped answering') from exc
            if not chunk:
                raise AdapterLost('The adapter closed the connection')
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
            self._ensure_permissions(autoclass)
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

    @staticmethod
    def _ensure_permissions(autoclass):
        """Android 12 and newer ask for Nearby devices at run time. Ask, then have the user retry."""
        if autoclass('android.os.Build$VERSION').SDK_INT < 31:
            return
        try:
            from android.permissions import check_permission, request_permissions
        except ImportError:
            return
        needed = [p for p in ('android.permission.BLUETOOTH_CONNECT', 'android.permission.BLUETOOTH_SCAN')
                  if not check_permission(p)]
        if needed:
            request_permissions(needed)
            raise OBDError('Allow Nearby devices when Android asks, then tap Connect again.')

    def write(self, data):
        self._out.write([b - 256 if b > 127 else b for b in data])
        self._out.flush()

    def read_until(self, prompt=b'>'):
        out = bytearray()
        while True:
            value = self._in.read()
            if value < 0:
                raise AdapterLost('The adapter closed the connection')
            if value == prompt[0]:
                return bytes(out)
            out.append(value & 0xFF)

    def close(self):
        if self._socket is not None:
            self._socket.close()
        self._socket = self._in = self._out = None


class Elm327:
    """Sends allowlisted commands and decodes the replies. Use one instance per connection."""

    label = 'Live'

    def __init__(self, transport):
        self.transport = transport
        self.traffic = []   # (direction, text) of what this link sent and got back, newest last
        self._header = catalog.DEFAULT_HEADER
        self._header_memory = {}   # PID -> the module address that answered for it
        self._misses = {}          # PID -> failures in a row
        self._lock = threading.RLock()   # one conversation with the adapter at a time

    def open(self):
        self.transport.open()
        self._header = catalog.DEFAULT_HEADER
        for command in SETUP_COMMANDS:
            self.command(command)

    def close(self):
        self.transport.close()

    def command(self, command):
        if not is_allowed(command):
            raise UnsafeCommand(f'{command!r} is not a read-only command, so it was not sent')
        command = command.replace(' ', '').upper()
        self.traffic.append(('TX', command))
        self.transport.write((command + '\r').encode('ascii'))
        raw = self.transport.read_until(b'>')
        reply = raw.decode('ascii', 'replace').replace('\r', '\n').strip()
        self.traffic.append(('RX', reply.replace('\n', ' ')))
        del self.traffic[:-200]
        return reply

    def set_header(self, header):
        """Point requests at a module (7E0 engine, 7E2 transmission) or back at the broadcast address."""
        target = catalog.DEFAULT_HEADER if header == 'Auto' else header
        if target != self._header:
            self.command(f'ATSH{target}')
            self._header = target

    def read_dtcs(self):
        with self._lock:
            return self._read_dtcs()

    def _read_dtcs(self):
        """Stored trouble codes (Mode 03), e.g. ['P0301']. An empty list means none are stored."""
        self.set_header('Auto')
        text = self.command(READ_DTC).upper()
        if any(word in text for word in ('UNABLE', 'ERROR', 'STOPPED', '?')):
            raise OBDError(f'Reading codes failed: the adapter replied "{text.splitlines()[-1].strip()}"')
        if 'NO DATA' in text:
            return []
        hex_text = re.sub(r'[^0-9A-F]', '', text.replace('SEARCHING', ''))
        return catalog.decode_dtcs(hex_text[2:] if hex_text.startswith('43') else hex_text)

    def read(self, pid, header=None, final=True):
        with self._lock:
            return self._read(pid, header, final)

    def _read(self, pid, header, final):
        """Return (value, unit) for one PID, or raise OBDError. Catalogue PIDs cover Mode 01 and Mode 22."""
        if pid not in PIDS:
            return self._read_catalog(pid, header, final)
        name, unit, width, decode = PIDS[pid]
        self.set_header('Auto')
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

    def poll(self, pids, headers=None):
        """Read several PIDs. Returns {pid: (value, unit)} for those that answered, and {pid: error text}.

        headers maps a PID to the module address to try first (for example the transmission at 7E2).
        Readings that get no answer there are tried again together on their catalogue address, so the
        adapter does not flip between modules for every miss. A lost adapter raises AdapterLost.
        """
        with self._lock:
            return self._poll(pids, headers or {})

    def _poll(self, pids, headers):
        values, errors, retry = {}, {}, []
        for pid in pids:
            info = catalog.get(pid)
            first = headers.get(pid)
            fallback = bool(first and info and first != info.header and pid not in self._header_memory)
            try:
                values[pid] = self.read(pid, header=first, final=not fallback)
            except AdapterLost:
                raise
            except OBDError as exc:
                if fallback:
                    retry.append(pid)
                else:
                    errors[pid] = str(exc)
        for pid in sorted(retry, key=lambda p: catalog.get(p).header):
            try:
                values[pid] = self.read(pid)
            except AdapterLost:
                raise
            except OBDError as exc:
                errors[pid] = str(exc)
        return values, errors

    def _read_catalog(self, pid_id, header=None, final=True):
        pid = catalog.get(pid_id)
        if pid is None:
            raise UnsafeCommand(f'{pid_id!r} is not on the read list')
        misses = self._misses.get(pid_id, 0)
        if misses >= MISS_LIMIT and misses % RETRY_EVERY:
            self._misses[pid_id] = misses + 1
            raise OBDError(f'{pid.name}: no reply, skipped until it answers')
        candidates = [self._header_memory.get(pid_id), header]
        if final:
            candidates.append(pid.header)
        candidates = [h for h in candidates if h]
        last = None
        for candidate in dict.fromkeys(candidates):
            try:
                value = self._read_from(pid, candidate)
            except AdapterLost:
                raise
            except OBDError as exc:
                last = exc
                continue
            self._header_memory[pid_id] = candidate
            self._misses.pop(pid_id, None)
            return value
        if final:
            self._misses[pid_id] = misses + 1
        raise last

    def _read_from(self, pid, header):
        self.set_header(header)
        text = self.command(pid.command).upper()
        if any(word in text for word in ERROR_WORDS):
            raise OBDError(f'{pid.name}: the adapter replied "{text.splitlines()[-1].strip()}"')
        hex_text = re.sub(r'[^0-9A-F]', '', text.replace('SEARCHING', ''))
        at = hex_text.find(pid.echo)
        if at < 0:
            raise OBDError(f'{pid.name}: unexpected reply "{text}"')
        value = pid.parse(hex_text[at + len(pid.echo):])
        if value is None:
            raise OBDError(f'{pid.name}: reply too short "{text}"')
        return value, pid.unit
