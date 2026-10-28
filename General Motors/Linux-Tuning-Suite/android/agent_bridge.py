"""A small web service inside the app, so the user's own AI agent can watch and advise.

The agent can read the settings, the shift tables with their green/yellow/red grades, and the live
engine and transmission stream. It can leave a note to show on the Agent screen, and it can propose
a change to a setting. A proposal only waits in a list: the user approves or rejects it in the app,
and only approval changes a setting. The bridge has no way to send anything to the adapter or the
car, and it is off until the user starts it.

Every request needs the token shown in the app. Standard library only, no Kivy, so it can be
tested on a desktop.
"""

import hmac
import json
import math
import secrets
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

DEFAULT_PORT = 8765
MAX_BODY = 8192
MAX_PENDING = 20
MAX_NOTES = 30
NOTE_LEVELS = ('info', 'warn', 'alert')


class AgentBridge:
    def __init__(self, get_state, bounds, host='0.0.0.0', port=DEFAULT_PORT, token=None):
        self.get_state = get_state
        self.bounds = dict(bounds)
        self.host, self.port = host, port
        self.token = token or secrets.token_urlsafe(18)
        self._lock = threading.Lock()
        self._proposals = []
        self._notes = deque(maxlen=MAX_NOTES)
        self._next_id = 1
        self._server = None
        self._thread = None

    # --- lifecycle -------------------------------------------------------------------------------

    def start(self):
        bridge = self

        class Handler(_Handler):
            owner = bridge

        self._server = ThreadingHTTPServer((self.host, self.port), Handler)
        self._server.daemon_threads = True
        self.port = self._server.server_address[1]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def stop(self):
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None

    @property
    def running(self):
        return self._server is not None

    # --- what the app sees -----------------------------------------------------------------------

    def pending(self):
        with self._lock:
            return [dict(p) for p in self._proposals if p['status'] == 'pending']

    def resolve(self, proposal_id, approved):
        """Mark a waiting proposal approved or rejected. Returns it, or None if it is not waiting."""
        with self._lock:
            for proposal in self._proposals:
                if proposal['id'] == proposal_id and proposal['status'] == 'pending':
                    proposal['status'] = 'approved' if approved else 'rejected'
                    return dict(proposal)
        return None

    def notes(self):
        with self._lock:
            return list(reversed(self._notes))

    # --- what the agent does ---------------------------------------------------------------------

    def propose(self, field, value, reason):
        """Returns (proposal or None, error text)."""
        if field not in self.bounds:
            return None, f'"{field}" is not a setting an agent may change. See /v1/help for the list.'
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            return None, f'"{field}" needs a number.'
        low, high = self.bounds[field]
        if not low <= value <= high:
            return None, f'{value:g} is outside the allowed range {low:g} to {high:g} for {field}.'
        with self._lock:
            if sum(p['status'] == 'pending' for p in self._proposals) >= MAX_PENDING:
                return 'full', 'Too many proposals are waiting for the user. Wait for them to be answered.'
            proposal = {'id': self._next_id, 'field': field, 'value': float(value),
                        'reason': str(reason or '')[:500], 'status': 'pending', 'time': time.time()}
            self._next_id += 1
            self._proposals.append(proposal)
            del self._proposals[:-100]
            return dict(proposal), ''

    def add_note(self, text, level):
        text = str(text or '').strip()[:1000]
        if not text:
            return None
        note = {'text': text, 'level': level if level in NOTE_LEVELS else 'info', 'time': time.time()}
        with self._lock:
            self._notes.append(note)
        return note

    def help(self):
        return {
            'about': 'TunerToolPro agent bridge. Read the tune and the live ECU and TCM stream, then '
                     'advise. Nothing you send can reach the car.',
            'auth': 'Send the token as "Authorization: Bearer <token>", or as ?token=<token>.',
            'endpoints': {
                'GET /v1/state': 'Settings, data source (LIVE, DEMO or OFFLINE), grade summary, live data.',
                'GET /v1/tables': 'The four shift tables with a green/yellow/red level and a reason for each cell.',
                'GET /v1/live': 'Latest engine and transmission readings, their history, health tiles and '
                                'the last shifts compared with the table.',
                'GET /v1/proposals': 'Proposals and whether the user approved or rejected them.',
                'GET /v1/notes': 'Notes already left for the user.',
                'POST /v1/propose': 'JSON {field, value, reason}. Waits for the user to approve it in the app. '
                                    'Nothing changes until they do.',
                'POST /v1/note': 'JSON {text, level: info|warn|alert}. Shown on the Agent screen.',
            },
            'rules': ['read-only for the car: there is no command endpoint',
                      'a proposal is not applied until the user approves it',
                      'proposals outside a setting\'s range are refused'],
            'levels': {'good': 'green', 'ok': 'yellow, worth a look', 'bad': 'red, likely a problem',
                       'off': 'not graded'},
            'settings': {name: {'min': low, 'max': high} for name, (low, high) in self.bounds.items()},
        }


class _Handler(BaseHTTPRequestHandler):
    owner = None
    server_version = 'TunerToolProBridge'

    def log_message(self, *_):
        pass

    # --- plumbing --------------------------------------------------------------------------------

    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def _authorised(self, query):
        supplied = self.headers.get('Authorization', '')
        supplied = supplied[7:] if supplied.startswith('Bearer ') else query.get('token', [''])[0]
        return hmac.compare_digest(supplied.encode(), self.owner.token.encode())

    def _body(self):
        """Parsed JSON body, or None after an error response has been sent."""
        length = int(self.headers.get('Content-Length') or 0)
        if length > MAX_BODY:
            self.rfile.read(min(length, 65536))
            self._send(413, {'error': f'Request too large. The limit is {MAX_BODY} bytes.'})
            return None
        try:
            body = json.loads(self.rfile.read(length) or b'{}')
        except ValueError:
            self._send(400, {'error': 'The body must be JSON.'})
            return None
        if not isinstance(body, dict):
            self._send(400, {'error': 'The body must be a JSON object.'})
            return None
        return body

    def _route(self, method):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        if not self._authorised(query):
            self._send(401, {'error': 'Missing or wrong token. Copy it from the Agent screen in the app.'})
            return
        bridge = self.owner
        if method == 'GET':
            if url.path == '/v1/help':
                return self._send(200, bridge.help())
            if url.path in ('/v1/state', '/v1/tables', '/v1/live'):
                state = bridge.get_state()
                if url.path == '/v1/tables':
                    return self._send(200, state.get('tables', {}))
                if url.path == '/v1/live':
                    return self._send(200, state.get('live', {}))
                return self._send(200, {k: v for k, v in state.items() if k != 'tables'})
            if url.path == '/v1/proposals':
                with bridge._lock:
                    return self._send(200, {'proposals': [dict(p) for p in bridge._proposals]})
            if url.path == '/v1/notes':
                return self._send(200, {'notes': bridge.notes()})
        if method == 'POST' and url.path in ('/v1/propose', '/v1/note'):
            body = self._body()
            if body is None:
                return
            if url.path == '/v1/propose':
                proposal, error = bridge.propose(body.get('field'), body.get('value'), body.get('reason'))
                if proposal == 'full':
                    return self._send(429, {'error': error})
                if proposal is None:
                    return self._send(422, {'error': error})
                return self._send(201, proposal)
            note = bridge.add_note(body.get('text'), body.get('level'))
            if note is None:
                return self._send(422, {'error': 'A note needs some text.'})
            return self._send(201, note)
        self._send(404, {'error': 'No such endpoint. GET /v1/help lists them.'})

    def do_GET(self):
        self._route('GET')

    def do_POST(self):
        self._route('POST')

    def _refuse(self):
        self._send(405, {'error': 'Only GET and POST are used.'})

    do_PUT = do_DELETE = do_PATCH = _refuse


def local_ip():
    """This phone's address on the network it is joined to, or 127.0.0.1 if there is none."""
    import socket
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(('10.255.255.255', 1))   # no packet is sent; this only picks the outgoing interface
        return probe.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        probe.close()


def build_agent_prompt(url, token, help_info):
    """Text to paste into an AI agent's chat so it knows how to reach the app and what it may do."""
    settings = ', '.join(f'{name} ({low:g} to {high:g})' for name, (low, high) in
                         ((n, (v['min'], v['max'])) for n, v in help_info['settings'].items()))
    return (
        'You are helping me tune a GM 6L80E automatic transmission with the TunerToolPro app on my phone.\n'
        f'The app serves JSON at {url} while I have the agent bridge switched on.\n'
        f'Send "Authorization: Bearer {token}" with every request (or add ?token={token} to the address).\n\n'
        'Read:\n'
        '  GET /v1/help       what you can do\n'
        '  GET /v1/state      my settings, data source, grade summary and live data\n'
        '  GET /v1/tables     the four shift tables, each cell graded good (green), ok (yellow) or bad (red) '
        'with a reason\n'
        '  GET /v1/live       live engine and transmission readings, health tiles, recent shifts vs the table\n'
        'Act:\n'
        '  POST /v1/note      {"text": "...", "level": "info|warn|alert"} shows a note on my screen\n'
        '  POST /v1/propose   {"field": "...", "value": 0, "reason": "..."} suggests a change. Nothing '
        'changes until I approve it in the app.\n\n'
        f'Settings you may propose changes to: {settings}.\n'
        'You cannot send anything to the car. Watch the live data, point out problems in plain words, and '
        'propose small changes with a reason. Never say a change is applied until /v1/proposals shows it '
        'as approved.'
    )
