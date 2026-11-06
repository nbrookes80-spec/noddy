"""A fake ELM327 adapter for tests: a localhost TCP server that answers like an adapter with spaces and line
feeds off. The apps' test suites use it too, so every one of them tests against the same adapter. Not used at runtime."""

import socket
import threading


class FakeElm327:
    """A localhost TCP server that answers like an ELM327 with spaces and line feeds off."""

    REPLIES = {
        'ATZ': 'ELM327 v1.5',
        'ATE0': 'OK', 'ATL0': 'OK', 'ATH0': 'OK', 'ATS0': 'OK', 'ATSP0': 'OK',
        '0100': 'SEARCHING...\r4100BE3FA813',
        '010C': 'SEARCHING...\r410C1AF8',   # 0x1AF8 / 4 = 1726 rpm
        '010D': '410D3C',                   # 60 km/h
        '0105': '410578',                   # 120 - 40 = 80 C
        '0111': '411180',                   # 128 * 100 / 255 = 50.2 %
        '010F': 'NO DATA',
        'ATSH7DF': 'OK', 'ATSH7E0': 'OK', 'ATSH7E2': 'OK',
        '221940': '62194078',               # transmission fluid temperature: 120 - 40 = 80 C
        '03': '4303010420',                 # stored codes P0301 and P0420
    }

    def __init__(self):
        self.received = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('127.0.0.1', 0))
        self.server.listen(1)
        self.port = self.server.getsockname()[1]
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()

    def _serve(self):
        conn, _ = self.server.accept()
        conn.settimeout(5)
        buffer = b''
        with conn:
            while True:
                chunk = conn.recv(256)
                if not chunk:
                    return
                buffer += chunk
                while b'\r' in buffer:
                    line, _, buffer = buffer.partition(b'\r')
                    command = line.decode('ascii').strip()
                    self.received.append(command)
                    reply = self.REPLIES.get(command, '?')
                    conn.sendall((reply + '\r\r>').encode('ascii'))

    def close(self):
        self.server.close()
