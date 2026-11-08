"""OBD-II link to an ELM327-compatible scan adapter, over Wi-Fi (TCP) or Bluetooth (RFCOMM).

Only commands that pass is_allowed() are ever sent: adapter set-up, Mode 01 and Mode 22 reads of PIDs
in the scanner catalogue, the Mode 03 stored-code read, a header switch to one of four known module
addresses (four more, with Mode 21 reads of catalogued ids, only with extra_modules=True), and the Mode 04 code clear only when the app builds the link with allow_clear=True. Nothing here
writes anything else to the controller: no Mode 08 tests, no Mode 09 writes, no ECU programming, no
free-form Mode 22 sweeps. Any other command raises UnsafeCommand before anything is sent.

Wi-Fi is the fallback path: many adapters open a hotspot at 192.168.0.10 port 35000. Bluetooth
Classic (SPP) needs the adapter paired in Android settings first. The Bluetooth path can only run
on Android, and it has not been tested with a real adapter yet.
"""

import math
import re
import socket
import threading
import time

from tunertoolpro.scanner import pids as catalog
from tunertoolpro.scanner import sensor_window

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
CLEAR_DTC = '04'          # only sent when the link was built with allow_clear=True; is_allowed() checks it at send time
CLEAR_REPLY = '44'        # the car's answer to a clear: 44 is 40 (a Mode 04 request) plus 04
HEADER_COMMANDS = {f'ATSH{h}' for h in catalog.KNOWN_HEADERS}
ALLOWED |= HEADER_COMMANDS
# Four more module addresses (ABS, meter, A/C and one more), only for a link built with extra_modules=True.
EXTRA_HEADERS = catalog.EXTRA_HEADERS
EXTRA_HEADER_COMMANDS = {f'ATSH{h}' for h in EXTRA_HEADERS}
MODULE_OFF = 'module access is off'

# Adapter information: ATI is the adapter's firmware name, ATRV the volts at the adapter's own supply pin, ATDP the
# protocol it settled on. All three only ask the adapter about itself; no request reaches the car. Exact matches only.
INFO_COMMANDS = ('ATI', 'ATRV', 'ATDP')
ALLOWED |= set(INFO_COMMANDS)


# Adapter timing, for speed settings: ATAT0/1/2 is adaptive timing, ATST sets the response timeout in units of
# 4 ms. Both only change how long the adapter waits for a car, so they are allowed on their own.
TIMING_COMMAND = re.compile(r'ATAT[012]|ATST[0-9A-F]{2}')

# The protocol the adapter talks to the car in. ATSP picks how the adapter speaks on the bus, so it is allowed on
# its own: it adds no request. The choices are the CAN protocols a GM car answers on (0 lets the adapter choose).
PROTOCOLS = {'0': 'Automatic', '6': 'CAN 11-bit, 500 kbaud (Holden VE/VF, most GM since 2008)',
             '7': 'CAN 29-bit, 500 kbaud', '8': 'CAN 11-bit, 250 kbaud', '9': 'CAN 29-bit, 250 kbaud'}


def timing_commands(adaptive, timeout_ms):
    """The adapter set-up for the speed settings: ATAT1 (adaptive timing) or ATAT0 (off), then ATST when a
    timeout is chosen. ATST counts 4 ms steps, so 200 ms is 50 steps, sent as ATST32."""
    commands = [f'ATAT{1 if adaptive else 0}']
    if timeout_ms:
        steps = min(255, max(1, round(timeout_ms / 4)))
        commands.append(f'ATST{steps:02X}')
    return commands


def send_timing(elm, adaptive, timeout_ms, protocol=None):
    """Send the speed settings to a connected adapter, one command at a time. Returns the commands sent.
    protocol is a key of PROTOCOLS to select too, or None to leave the adapter's protocol alone."""
    sent = timing_commands(adaptive, timeout_ms)
    if protocol in PROTOCOLS:
        sent.append(f'ATSP{protocol}')
    for command in sent:
        with elm._lock:
            elm.command(command)
    return sent


PROBE = '0100'    # asks which Mode 01 readings the car supports; a protocol that gets no answer to it is no use


def protocol_plan(saved):
    """The commands for a saved protocol choice: try it, check the car answers, else go back to Automatic.

    Returns ['ATSP<n>', '0100', 'ATSP0'] for a CAN protocol, where the last command is sent only when the car did
    not answer the probe (use_protocol does that), and ['ATSP0'] for Automatic or anything not in PROTOCOLS."""
    if saved not in PROTOCOLS or saved == '0':
        return ['ATSP0']
    return [f'ATSP{saved}', PROBE, 'ATSP0']


def use_protocol(elm, saved):
    """Send protocol_plan(saved) to a connected adapter. The fallback to Automatic is sent only when the probe gets
    an error word (or no data) back. Returns the commands actually sent."""
    plan = protocol_plan(saved)
    sent = []
    with elm._lock:
        reply = ''
        for command in plan[:2]:
            reply = elm.command(command)
            sent.append(command)
        if len(plan) == 3 and any(word in reply.upper() for word in ERROR_WORDS):
            elm.command(plan[2])
            sent.append(plan[2])
    return sent


def read_adapter_info(elm):
    """What the adapter says about itself: {'firmware', 'adapter_volts', 'protocol', 'car_volts'}, text, '' when a
    command got no usable answer. car_volts is the car's battery from Mode 01 PID 0142, read through the
    scanner catalogue (0142 is catalogued) and left empty if the car does not answer. Besides ATI, ATRV and ATDP it
    sends only that one catalogued read."""
    info = {'firmware': '', 'adapter_volts': '', 'protocol': '', 'car_volts': ''}
    with elm._lock:
        for key, command in (('firmware', 'ATI'), ('adapter_volts', 'ATRV'), ('protocol', 'ATDP')):
            text = ' '.join(elm.command(command).replace('SEARCHING...', '').split())
            if text and not any(word in text.upper() for word in ERROR_WORDS):
                info[key] = text[6:] if key == 'protocol' and text.upper().startswith('AUTO, ') else text
        if '0142' in catalog.CATALOG:
            try:
                value, unit = elm.read('0142')
                info['car_volts'] = f'{value:.1f} {unit}'
            except OBDError:
                pass
    return info


# Reconnecting after the adapter drops: wait this many seconds before each try, then give up.
BACKOFF_SECONDS = (1, 2, 4, 8, 16)


def backoff_schedule():
    """Seconds to wait before each reconnect try, in order. After the last one the app stops and says so."""
    return BACKOFF_SECONDS


# How often the Live reader may start a round of readings, per second.
RATE_MIN, RATE_MAX, DEFAULT_RATE = 1, 10, 4


def clean_rate(rate):
    """A whole number from RATE_MIN to RATE_MAX (rounded and clamped), or DEFAULT_RATE if it is not a number."""
    if isinstance(rate, bool) or not isinstance(rate, (int, float)) or not math.isfinite(rate):
        return DEFAULT_RATE
    return min(RATE_MAX, max(RATE_MIN, round(rate)))


def round_delay(rate):
    """The shortest time in seconds between the starts of two rounds for "at most `rate` rounds per second"."""
    return 1.0 / clean_rate(rate)


def module_note(pid, extra_modules):
    """"module access is off" for a Mode 21 reading when the link may not read other modules, else None."""
    return MODULE_OFF if pid.mode == '21' and not extra_modules else None


def _module_read(command):
    """True for a Mode 21 request for a catalogued id on one of the four module addresses."""
    found = catalog.CATALOG.get(command)
    return found is not None and found.mode == '21' and found.header in EXTRA_HEADERS


def is_allowed(command, allow_clear=False, extra_modules=False):
    """True for a read-only command: set-up, a header switch, Mode 03, adapter timing, or a catalogued Mode 01/22 PID.

    The Mode 04 code clear passes only when allow_clear is True, which an app sets for a build that offers it.
    The four module addresses (7B0, 7C0, 7C4, 7E1) and catalogued Mode 21 reads pass only when extra_modules is True."""
    command = command.replace(' ', '').upper()
    if command.startswith('21') or command in EXTRA_HEADER_COMMANDS:
        return extra_modules and (command in EXTRA_HEADER_COMMANDS or _module_read(command))
    return (command in ALLOWED or command in catalog.CATALOG or bool(TIMING_COMMAND.fullmatch(command))
            or command in {f'ATSP{code}' for code in PROTOCOLS}
            or (command == CLEAR_DTC and allow_clear))

ERROR_WORDS = ('NO DATA', 'ERROR', 'UNABLE', 'STOPPED', 'BUS INIT', '?', 'CAN ERROR')
MISS_LIMIT = 3     # a reading with this many failures in a row is skipped...
RETRY_EVERY = 8    # ...and tried again on every eighth later request


class OBDError(Exception):
    """The adapter did not answer, or answered with an error or unexpected text."""


class ModuleAccessOff(OBDError):
    """A Mode 21 module reading was skipped because the link may not read other modules."""


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

    def read_chunk(self, timeout=0.2):
        """Whatever the adapter has sent (b'' if nothing arrived within timeout). Used by the CAN sniffer."""
        if self._buffer:
            chunk, self._buffer = self._buffer, b''
            return chunk
        self._sock.settimeout(timeout)
        try:
            chunk = self._sock.recv(1024)
        except socket.timeout:
            return b''
        finally:
            self._sock.settimeout(self.timeout)
        if not chunk:
            raise AdapterLost('The adapter closed the connection')
        return chunk

    def close(self):
        if self._sock is not None:
            self._sock.close()
            self._sock = None


class SerialTransport:
    """A USB or RS-232 cable to the adapter. Desktop only: needs pyserial, which the phone does not have."""

    def __init__(self, port, baud=38400, timeout=5.0):
        self.port, self.baud, self.timeout = port, baud, timeout
        self._serial = None
        self._buffer = b''

    def open(self):
        try:
            import serial
        except ImportError as exc:
            raise OBDError('A cable needs the pyserial package (pip install pyserial)') from exc
        try:
            self._serial = serial.Serial(self.port, self.baud, timeout=0.2, write_timeout=2)
        except (OSError, serial.SerialException) as exc:
            raise OBDError(f'Could not open the cable port {self.port} ({exc})') from exc

    def write(self, data):
        self._serial.write(data)
        self._serial.flush()

    def read_until(self, prompt=b'>'):
        """Read until the adapter's prompt character arrives. Returns the text before it."""
        last = time.monotonic()
        while prompt not in self._buffer:
            chunk = self._serial.read(max(1, self._serial.in_waiting))
            if chunk:
                self._buffer += chunk
                last = time.monotonic()
            elif time.monotonic() - last > self.timeout:
                raise AdapterLost('The adapter stopped answering')
        reply, _, self._buffer = self._buffer.partition(prompt)
        return reply

    def read_chunk(self, timeout=0.2):
        """Whatever the adapter has sent (b'' if nothing arrived within timeout). Used by the CAN sniffer."""
        if self._buffer:
            chunk, self._buffer = self._buffer, b''
            return chunk
        self._serial.timeout = timeout
        return self._serial.read(max(1, self._serial.in_waiting))

    def close(self):
        if self._serial is not None:
            self._serial.close()
            self._serial = None


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

    def _stream(self):
        """The input stream, taken once per read. close() can run on another thread and set self._in to None;
        a read that finds it gone is an adapter that has been lost, not a bug."""
        stream = self._in
        if stream is None:
            raise AdapterLost('The adapter connection is closed')
        return stream

    def read_until(self, prompt=b'>', timeout=5.0):
        """Bytes up to the prompt. An adapter that goes quiet raises AdapterLost instead of waiting forever,
        which used to freeze every screen until the app was restarted."""
        import time
        stream = self._stream()
        out = bytearray()
        deadline = time.monotonic() + timeout
        try:
            while True:
                if stream.available() == 0:
                    if time.monotonic() >= deadline:
                        raise AdapterLost('The adapter stopped answering')
                    time.sleep(0.005)
                    continue
                value = stream.read()
                if value < 0:
                    raise AdapterLost('The adapter closed the connection')
                if value == prompt[0]:
                    return bytes(out)
                out.append(value & 0xFF)
        except AdapterLost:
            raise
        except Exception as exc:   # a closed Java socket surfaces through pyjnius as a generic exception
            raise AdapterLost(f'The adapter connection failed: {exc}') from exc

    def read_chunk(self, timeout=0.2):
        """Whatever bytes are waiting (b'' if none arrive within timeout). Used by the CAN sniffer."""
        import time
        stream = self._stream()
        deadline = time.monotonic() + timeout
        try:
            while stream.available() == 0:
                if time.monotonic() >= deadline:
                    return b''
                time.sleep(0.01)
            out = bytearray()
            while stream.available() > 0 and len(out) < 1024:
                value = stream.read()
                if value < 0:
                    raise AdapterLost('The adapter closed the connection')
                out.append(value & 0xFF)
            return bytes(out)
        except AdapterLost:
            raise
        except Exception as exc:
            raise AdapterLost(f'The adapter connection failed: {exc}') from exc

    def close(self):
        if self._socket is not None:
            self._socket.close()
        self._socket = self._in = self._out = None


class Elm327:
    """Sends allowlisted commands and decodes the replies. Use one instance per connection."""

    label = 'Live'

    def __init__(self, transport, allow_clear=False, extra_modules=False):
        self.transport = transport
        self.allow_clear = allow_clear   # True lets the Mode 04 code clear through; read-only when False
        self.extra_modules = extra_modules   # True lets catalogued Mode 21 reads on 7B0/7C0/7C4/7E1 through
        self.traffic = []   # (direction, text) of what this link sent and got back, newest last
        self.on_traffic = None   # optional callback(kind, text) for a debug log: TX, RX, REFUSED or ERR
        self.on_values = None    # optional callback({pid: (value, unit)}) for the data log, after each poll
        self._header = catalog.DEFAULT_HEADER
        self._header_memory = {}   # PID -> the module address that answered for it
        self._misses = {}          # PID -> failures in a row
        self.notes = {}            # PID -> note for a reading that arrived but is outside its sensor's window
        self._lock = threading.RLock()   # one conversation with the adapter at a time

    def open(self):
        self.transport.open()
        self._header = catalog.DEFAULT_HEADER
        for command in SETUP_COMMANDS:
            self.command(command)

    def close(self):
        self.transport.close()

    def command(self, command):
        if not is_allowed(command, self.allow_clear, self.extra_modules):
            self._tell('REFUSED', command)
            raise UnsafeCommand(f'{command!r} is not a read-only command, so it was not sent')
        command = command.replace(' ', '').upper()
        self.traffic.append(('TX', command))
        self._tell('TX', command)
        try:
            self.transport.write((command + '\r').encode('ascii'))
            raw = self.transport.read_until(b'>')
        except Exception as exc:   # also a closed or broken socket, so the log shows why a reading stopped
            self._tell('ERR', f'{type(exc).__name__}: {exc}')
            if isinstance(exc, (OBDError, UnsafeCommand)):
                raise
            raise AdapterLost(f'The adapter connection failed: {exc}') from exc
        reply = raw.decode('ascii', 'replace').replace('\r', '\n').strip()
        self.traffic.append(('RX', reply.replace('\n', ' ')))
        self._tell('RX', reply.replace('\n', ' '))
        del self.traffic[:-200]
        return reply

    def _tell(self, kind, text):
        """Pass a line to the debug log, if one is listening. A broken log must never stop a reading."""
        if self.on_traffic is not None:
            try:
                self.on_traffic(kind, text)
            except Exception:
                pass

    def header_for(self, pid):
        """The module address that last answered for a catalogue reading, or None if none has yet."""
        return self._header_memory.get(pid)

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
        # Each module answers on its own line, so decode each line by itself and drop codes seen twice.
        codes = []
        for line in text.replace('SEARCHING', '').splitlines():
            hex_text = re.sub(r'[^0-9A-F]', '', line)
            data = hex_text[2:] if hex_text.startswith('43') else hex_text
            codes.extend(code for code in catalog.decode_dtcs(data) if code not in codes)
        return codes

    def clear_dtcs(self):
        """Clear the stored trouble codes (Mode 04). Also resets the readiness monitors, so the UI asks first."""
        with self._lock:
            return self._clear_dtcs()

    def _clear_dtcs(self):
        """Raise OBDError unless the module answers 44. A reply of NO DATA or an error word is not a clear."""
        self.set_header('Auto')
        text = self.command(CLEAR_DTC).upper()
        lines = [re.sub(r'[^0-9A-F]', '', line) for line in text.splitlines()]
        if any(word in text for word in ERROR_WORDS) or not any(line.startswith(CLEAR_REPLY) for line in lines):
            raise OBDError(f'Clearing codes failed: the adapter replied "{text.strip() or "nothing"}"')

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
            result = self._poll(pids, headers or {})
        if self.on_values is not None and result[0]:
            try:
                self.on_values(result[0])
            except Exception:   # a broken data log must never stop a reading
                pass
        return result

    def _poll(self, pids, headers):
        values, errors, retry = {}, {}, []
        for pid in pids:
            info = catalog.CATALOG.get(pid)   # the built-in list only: an imported CAN signal is never read
            if info is None:     # not a built-in read (for example an imported CAN signal): nothing is sent
                errors[pid] = f'{pid!r} is not on the read list'
                continue
            first = headers.get(pid)
            fallback = bool(first and info and first != info.header and pid not in self._header_memory)
            try:
                values[pid] = self.read(pid, header=first, final=not fallback)
                self._take_note(pid, errors)
            except AdapterLost:
                raise
            except ModuleAccessOff as exc:
                errors[pid] = str(exc)
            except UnsafeCommand as exc:     # the list changed under us: report it, never let it stop the poll
                errors[pid] = str(exc)
            except OBDError as exc:
                if fallback:
                    retry.append(pid)
                else:
                    errors[pid] = str(exc)
        for pid in sorted(retry, key=lambda p: catalog.CATALOG[p].header):
            try:
                values[pid] = self.read(pid)
                self._take_note(pid, errors)
            except AdapterLost:
                raise
            except OBDError as exc:
                errors[pid] = str(exc)
        return values, errors

    def _read_catalog(self, pid_id, header=None, final=True):
        pid = catalog.CATALOG.get(pid_id)
        if pid is None:
            raise UnsafeCommand(f'{pid_id!r} is not on the read list')
        if module_note(pid, self.extra_modules):
            raise ModuleAccessOff(f'{pid.name}: {MODULE_OFF}')
        misses = self._misses.get(pid_id, 0)
        if misses >= MISS_LIMIT and misses % RETRY_EVERY:
            self._misses[pid_id] = misses + 1
            raise OBDError(f'{pid.name}: no reply, skipped until it answers')
        candidates = [self._header_memory.get(pid_id), header]
        if final:
            candidates.append(pid.header)
            if pid.mode == '22':
                candidates.append(catalog.DEFAULT_HEADER)   # some transmissions only answer the broadcast address
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

    def _take_note(self, pid, errors):
        """A reading that arrived with a note keeps its value; the note is passed on beside it, in the errors."""
        note = self.notes.pop(pid, None)
        if note:
            errors[pid] = note

    def _read_from(self, pid, header):
        self.set_header(header)
        self.notes.pop(pid.pid, None)
        text = self.command(pid.command).upper()
        if any(word in text for word in ERROR_WORDS):
            raise OBDError(f'{pid.name}: the adapter replied "{text.splitlines()[-1].strip()}"')
        hex_text = re.sub(r'[^0-9A-F]', '', text.replace('SEARCHING', ''))
        at = hex_text.find(pid.echo)
        if at < 0:
            raise OBDError(f'{pid.name}: unexpected reply "{text}"')
        data = hex_text[at + len(pid.echo):]
        value = pid.parse(data)
        if value is None:
            raise OBDError(f'{pid.name}: reply too short "{text}"')
        note = sensor_window.fault(pid.pid, data)
        if note:
            self.notes[pid.pid] = note
        return value, pid.unit
