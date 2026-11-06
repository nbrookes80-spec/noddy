"""Read a Torque Pro PID file (CSV) into catalogue entries. No Kivy, no I/O beyond the text it is given.

A Torque file can say more than this app is willing to do, so the reader only accepts what is safe:

  * the id must be a Mode 01 or Mode 22 read; every other service is refused
  * the startDiagnostic and stopDiagnostic columns must be empty, because they carry raw commands
  * the equation is checked against a small whitelist and worked out by this module, never by eval()

Everything read here is marked as not confirmed on a real car.
"""

import csv
import io
import math
import re
from ast import (Add, BinOp, Call, Constant, Div, Expression, LShift, Mult, Name, RShift, Sub, UAdd, UnaryOp,
                 USub, parse as parse_expression)

from .pids import KIND_WIDTH, Pid

MAX_CHARS = 1_000_000
MAX_ROWS = 2000
MAX_EQUATION = 200
MAX_NODES = 80
KNOWN_MODULES = ('7E0', '7E2', '7E3')
KIND_FOR_BYTES = {1: 'byte', 2: 'word', 3: 'bytes3', 4: 'dword'}
LETTERS = 'ABCD'
_ID = re.compile(r'(01[0-9A-F]{2}|22[0-9A-F]{4})')
_TAG = re.compile(r'^\[([^\]]{1,20})\]\s*(.*)$')
_ALLOWED_BINARY = {Add: lambda a, b: a + b, Sub: lambda a, b: a - b, Mult: lambda a, b: a * b,
                   Div: lambda a, b: a / b, LShift: lambda a, b: int(a) << int(b),
                   RShift: lambda a, b: int(a) >> int(b)}


class Refused(ValueError):
    """A row the reader will not accept. The message says why, in plain words."""


def _check(node, state):
    """Walk the tree once: only numbers, A to D, + - * / << >>, a sign and signed() are allowed."""
    state['nodes'] += 1
    if state['nodes'] > MAX_NODES:
        raise Refused('the equation is too long')
    if isinstance(node, Expression):
        return _check(node.body, state)
    if isinstance(node, Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise Refused('the equation may only contain numbers')
        return
    if isinstance(node, Name):
        if node.id not in LETTERS:
            raise Refused(f'the equation uses "{node.id}", but only A to D (the reply bytes) are allowed')
        state['letters'].add(node.id)
        return
    if isinstance(node, UnaryOp) and isinstance(node.op, (USub, UAdd)):
        return _check(node.operand, state)
    if isinstance(node, BinOp) and type(node.op) in _ALLOWED_BINARY:
        if isinstance(node.op, (LShift, RShift)):
            amount = node.right
            if not (isinstance(amount, Constant) and isinstance(amount.value, int)
                    and not isinstance(amount.value, bool) and 0 <= amount.value <= 16):
                raise Refused('a shift must be by a whole number from 0 to 16')
        _check(node.left, state)
        return _check(node.right, state)
    if (isinstance(node, Call) and isinstance(node.func, Name) and node.func.id == 'signed'
            and len(node.args) == 1 and not node.keywords):
        return _check(node.args[0], state)
    raise Refused(f'the equation uses something that is not allowed ({type(node).__name__})')


def _evaluate(node, letters):
    if isinstance(node, Expression):
        return _evaluate(node.body, letters)
    if isinstance(node, Constant):
        return node.value
    if isinstance(node, Name):
        return letters[node.id]
    if isinstance(node, UnaryOp):
        value = _evaluate(node.operand, letters)
        return -value if isinstance(node.op, USub) else value
    if isinstance(node, BinOp):
        return _ALLOWED_BINARY[type(node.op)](_evaluate(node.left, letters), _evaluate(node.right, letters))
    value = _evaluate(node.args[0], letters)       # signed(): a byte as a signed number
    return value - 256 if value > 127 else value


def compile_equation(text):
    """Returns (decode, byte count). decode(raw int) -> float, and raises ZeroDivisionError for a divide by zero."""
    text = (text or '').strip()
    if not text:
        raise Refused('the equation is empty')
    if len(text) > MAX_EQUATION:
        raise Refused('the equation is too long')
    text = re.sub(r'(?<![<>])<(?=\s*\d)', '<<', text)     # Torque exports often write a shift as a single <
    try:
        tree = parse_expression(text, mode='eval')
    except (SyntaxError, ValueError, RecursionError):
        raise Refused('the equation could not be read') from None
    state = {'nodes': 0, 'letters': set()}
    try:
        _check(tree, state)
    except RecursionError:
        raise Refused('the equation is too deeply nested') from None
    if not state['letters']:
        raise Refused('the equation does not use any reply byte (A, B, C or D)')
    count = max(LETTERS.index(letter) for letter in state['letters']) + 1

    def decode(raw):
        letters = {letter: (raw >> (8 * (count - 1 - i))) & 255 for i, letter in enumerate(LETTERS[:count])}
        result = float(_evaluate(tree, letters))
        if not math.isfinite(result):
            raise ZeroDivisionError
        return result
    return decode, count


def _pid_id(text):
    text = (text or '').strip().upper().replace(' ', '')
    text = text[2:] if text.startswith('0X') else text
    if _ID.fullmatch(text):
        return text
    if re.fullmatch(r'[0-9A-F]{2}([0-9A-F]{2})*', text) and text[:2] not in ('01', '22'):
        raise Refused(f'Mode {text[:2]} is not a read the app will send (only Mode 01 and Mode 22)')
    raise Refused('the PID is not a Mode 01 id (4 hex digits) or Mode 22 id (6 hex digits)')


def _number(text, label):
    try:
        value = float(text)
    except (TypeError, ValueError):
        raise Refused(f'{label} is not a number') from None
    if not math.isfinite(value):
        raise Refused(f'{label} is not a number')
    return value


def _entry(fields, source):
    pid = _pid_id(fields.get('modeandpid'))
    if (fields.get('startdiagnostic') or '').strip():
        raise Refused('startDiagnostic is not empty; commands in a PID file are never sent')
    if (fields.get('stopdiagnostic') or '').strip():
        raise Refused('stopDiagnostic is not empty; commands in a PID file are never sent')
    decode, count = compile_equation(fields.get('equation'))
    name = re.sub(r'[^\x20-\x7E°]', '', (fields.get('name') or '').strip())[:80] or pid
    tag = _TAG.match(name)
    category = 'Torque import'
    if tag and tag.group(2):
        category, name = f'Torque import: {tag.group(1)}', tag.group(2)
    low, high = _number(fields.get('minvalue') or '0', 'Min Value'), _number(fields.get('maxvalue') or '100', 'Max Value')
    if not low < high:
        high = low + 1.0
    wanted = (fields.get('header') or '').strip().upper()
    note = ''
    if wanted in ('', 'AUTO', '7DF'):
        header = 'Auto'
    elif wanted in KNOWN_MODULES:
        header = wanted
    else:
        header = 'Auto'
        note = f' The file asks for module "{wanted}", whose address is unconfirmed.'
    unit = re.sub(r'[^\x20-\x7E°]', '', (fields.get('units') or '').strip())[:12]
    return Pid(pid, name, category, unit, low, high, f'Imported from {source}. Not confirmed on a real car.{note}',
               header, KIND_FOR_BYTES[count], decode, source, False)


def parse(text, source='Torque CSV'):
    """Returns (pids, rejected). rejected is a list of {'line', 'name', 'reason'}; good rows are kept either way."""
    if not isinstance(text, str) or not text.strip():
        return [], [{'line': 0, 'name': '', 'reason': 'The file is empty.'}]
    if len(text) > MAX_CHARS:
        return [], [{'line': 0, 'name': '', 'reason': 'The file is too large to be a PID list.'}]
    reader = csv.reader(io.StringIO(text), skipinitialspace=True)
    try:
        header = [cell.replace(' ', '').lower() for cell in next(reader)]
    except (StopIteration, csv.Error):
        return [], [{'line': 0, 'name': '', 'reason': 'The file is empty.'}]
    if 'modeandpid' not in header or 'equation' not in header:
        return [], [{'line': 1, 'name': '', 'reason': 'This is not a Torque PID file (no ModeAndPID and Equation columns).'}]
    found, rejected, seen = [], [], set()
    try:
        for count, cells in enumerate(reader, 1):
            line = reader.line_num
            if count > MAX_ROWS:
                rejected.append({'line': line, 'name': '', 'reason': f'Only the first {MAX_ROWS} rows are read.'})
                break
            if not any(cell.strip() for cell in cells):
                continue
            fields = dict(zip(header, cells))
            try:
                entry = _entry(fields, source)
                if entry.pid in seen:
                    raise Refused('this PID is already in the file; the first one is kept')
            except Refused as why:
                rejected.append({'line': line, 'name': (fields.get('name') or '').strip(), 'reason': str(why)})
                continue
            seen.add(entry.pid)
            found.append(entry)
    except csv.Error as why:
        rejected.append({'line': reader.line_num, 'name': '', 'reason': f'The file could not be read ({why}).'})
    return found, rejected
