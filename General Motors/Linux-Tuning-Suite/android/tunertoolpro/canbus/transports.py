"""Ways to reach an ELM327-compatible adapter from a computer: Wi-Fi (TCP) and a serial port.

A serial port covers USB adapters and Bluetooth ones once bound by the operating system (for example
/dev/rfcomm0 on Linux, a COM port on Windows). Android reaches its Bluetooth adapter through its own
transport in the app; it has the same methods.
"""

import socket
import time

DEFAULT_WIFI = ('192.168.0.10', 35000)


class TransportError(Exception):
    pass


class _Buffered:
    """read_until and read_chunk on top of a subclass's _recv(timeout)."""

    def __init__(self):
        self._buffer = b''

    def _recv(self, timeout):
        raise NotImplementedError

    def read_until(self, prompt=b'>', timeout=5.0):
        deadline = time.monotonic() + timeout
        while prompt not in self._buffer:
            if time.monotonic() > deadline:
                raise TransportError('The adapter stopped answering')
            self._buffer += self._recv(min(0.5, max(0.05, deadline - time.monotonic())))
        reply, _, self._buffer = self._buffer.partition(prompt)
        return reply

    def read_chunk(self, timeout=0.2):
        if self._buffer:
            chunk, self._buffer = self._buffer, b''
            return chunk
        return self._recv(timeout)


class TcpTransport(_Buffered):
    def __init__(self, host=DEFAULT_WIFI[0], port=DEFAULT_WIFI[1], connect_timeout=5.0):
        super().__init__()
        self.host, self.port, self.connect_timeout = host, port, connect_timeout
        self._sock = None

    def open(self):
        try:
            self._sock = socket.create_connection((self.host, self.port), timeout=self.connect_timeout)
        except OSError as exc:
            raise TransportError(f'Could not reach the Wi-Fi adapter at {self.host}:{self.port} ({exc})') from exc

    def write(self, data):
        self._sock.sendall(data)

    def _recv(self, timeout):
        self._sock.settimeout(timeout)
        try:
            chunk = self._sock.recv(1024)
        except socket.timeout:
            return b''
        if not chunk:
            raise TransportError('The adapter closed the connection')
        return chunk

    def close(self):
        if self._sock is not None:
            self._sock.close()
            self._sock = None


class SerialTransport(_Buffered):
    def __init__(self, port, baud=38400):
        super().__init__()
        self.port, self.baud = port, baud
        self._serial = None

    def open(self):
        try:
            import serial
        except ImportError as exc:
            raise TransportError('A serial adapter needs the pyserial package (pip install pyserial)') from exc
        try:
            self._serial = serial.Serial(self.port, self.baud, timeout=0.2, write_timeout=2)
        except (OSError, serial.SerialException) as exc:
            raise TransportError(f'Could not open {self.port}: {exc}') from exc

    def write(self, data):
        self._serial.write(data)
        self._serial.flush()

    def _recv(self, timeout):
        self._serial.timeout = timeout
        return self._serial.read(max(1, self._serial.in_waiting))

    def close(self):
        if self._serial is not None:
            self._serial.close()
            self._serial = None


def serial_ports():
    """Names of the serial ports the system reports, or [] when pyserial is not installed."""
    try:
        from serial.tools import list_ports
    except ImportError:
        return []
    return sorted(p.device for p in list_ports.comports())
