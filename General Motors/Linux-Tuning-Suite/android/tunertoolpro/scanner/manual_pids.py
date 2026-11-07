"""PIDs the user types in by hand: the id, name, unit, formula and module, saved per profile. No Kivy.

Each entry is checked with the same rules as an imported Torque row, so a formula can only use the reply
bytes and arithmetic, and a PID can only be a Mode 01 or Mode 22 read. Entries are kept in one file in the
cars folder, keyed by the profile, so a built-in profile can be given its own PIDs too. Nothing is saved
unless every entry checks out.
"""

import json
from pathlib import Path

from . import torque_csv
from .pids import Pid

FILE_NAME = 'manual_pids.json'
SOURCE = 'Entered by hand'
NOTE = 'Entered by hand. Not confirmed on a real car.'
FIELDS = ('pid', 'name', 'unit', 'equation', 'low', 'high', 'header')


def build(entry):
    """A Pid for one entry. Raises torque_csv.Refused with the reason when the entry is not usable."""
    pid = torque_csv._pid_id(entry.get('pid'))
    decode, count = torque_csv.compile_equation(entry.get('equation'))
    name = str(entry.get('name') or '').strip()[:80] or pid
    unit = str(entry.get('unit') or '').strip()[:12]
    low = torque_csv._number(entry.get('low', 0), 'Min value')
    high = torque_csv._number(entry.get('high', 100), 'Max value')
    if not low < high:
        raise torque_csv.Refused('the minimum must be less than the maximum')
    wanted = str(entry.get('header') or 'Auto').strip().upper()
    if wanted not in ('AUTO',) + torque_csv.KNOWN_MODULES:
        raise torque_csv.Refused(f'the module {wanted!r} is not a known address')
    header = 'Auto' if wanted == 'AUTO' else wanted
    return Pid(pid, name, 'Entered by hand', unit, low, high, NOTE, header,
               torque_csv.KIND_FOR_BYTES[count], decode, SOURCE, False)


def _path(folder):
    return Path(folder) / FILE_NAME


def load(folder):
    """All saved entries as {profile key: [entry, ...]}. A damaged file gives {}, never an error."""
    try:
        data = json.loads(_path(folder).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {key: rows for key, rows in data.items() if isinstance(rows, list)}


def pids_for(folder, profile_key):
    """The Pids the user entered for one profile. Entries that no longer check out are left out."""
    out = []
    for entry in load(folder).get(profile_key, []):
        try:
            out.append(build(entry))
        except (torque_csv.Refused, TypeError, ValueError):
            continue
    return out


def save(folder, profile_key, entries):
    """Check every entry, then save them for the profile. Returns the Pids. Raises torque_csv.Refused on the
    first bad entry and saves nothing."""
    rows = []
    for entry in entries:
        row = {field: entry.get(field) for field in FIELDS}
        build(row)                       # raises if the entry is not usable
        rows.append(row)
    seen = [row['pid'].upper() for row in rows]
    if len(set(seen)) != len(seen):
        raise torque_csv.Refused('the same PID is entered twice')
    everything = load(folder)
    everything[profile_key] = rows
    Path(folder).mkdir(parents=True, exist_ok=True)
    _path(folder).write_text(json.dumps(everything, indent=2), encoding='utf-8')
    return [build(row) for row in rows]
