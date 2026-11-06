"""The pre-defined GM and Holden PID lists, and saving one to a car profile. No Kivy.

Each list is a slice of one of the Torque Pro files in data/ (the GM list and the E38 + T43 list for the
Holden VE/VF and Pontiac G8). A list is saved by writing its rows as a user profile (scanner/profiles.py),
which is the car's make, model, year and transmission plus the PIDs to load. Rows go through the same Torque
checks as an imported file, so only Mode 01 and Mode 22 reads can ever be saved.
"""

import csv
import io
from dataclasses import dataclass
from typing import Callable

from . import profiles


def _has(*words):
    return lambda name: any(word in name.lower() for word in words)


def _not(test):
    return lambda name: not test(name)


TRANSMISSION = _has('shift', 'tcc', 'gear', 'transmission', 'trans ', 'solenoid', 'torque converter', 't43')
ENGINE_ONLY = lambda name: not (TRANSMISSION(name) or _has('misfire', 'abs ', 'wheel')(name))


@dataclass(frozen=True)
class PredefinedList:
    key: str
    title: str
    summary: str
    file: str
    keep: Callable[[str], bool]


LISTS = (
    PredefinedList('holden-e38-t43', 'Holden VE/VF and G8: engine and 6L80 tuning set',
                   'The E38 engine and T43 (6L80) readings used for transmission tuning: shift times and errors, '
                   'TCC slip, gear, shaft speeds, solenoid current, fluid temperature, knock.',
                   'torque_e38_t43_v5.csv', lambda name: True),
    PredefinedList('holden-t43', 'Holden / G8: 6L80 transmission only', 'Just the T43 (6L80) readings.',
                   'torque_e38_t43_v5.csv', _has('t43')),
    PredefinedList('holden-e38', 'Holden / G8: E38 engine only', 'Just the E38 engine readings.',
                   'torque_e38_t43_v5.csv', _has('e38')),
    PredefinedList('gm-transmission', 'GM: transmission', 'Shift times and errors, current gear, TCC slip, '
                   'shaft speeds, solenoid current, fluid temperature, efficiency.',
                   'torque_gm_predefined.csv', TRANSMISSION),
    PredefinedList('gm-engine', 'GM: engine', 'Knock, spark, oil, injectors, idle, EGR, air-fuel, voltage.',
                   'torque_gm_predefined.csv', ENGINE_ONLY),
    PredefinedList('gm-misfire', 'GM: misfire counters', 'Current and history misfire count for every cylinder.',
                   'torque_gm_predefined.csv', _has('misfire')),
    PredefinedList('gm-abs', 'GM: ABS wheel speeds', 'The four wheel speeds from the ABS module.',
                   'torque_gm_predefined.csv', _has('abs ')),
    PredefinedList('gm-all', 'GM: everything', 'Every GM reading in the Torque Pro list.',
                   'torque_gm_predefined.csv', lambda name: True),
)


def by_key(key):
    return next((item for item in LISTS if item.key == key), None)


def _rows(item):
    text = (profiles.DATA_DIR / item.file).read_text(encoding='utf-8-sig', errors='replace')
    reader = csv.reader(io.StringIO(text), skipinitialspace=True)
    header = next(reader)
    name_at = [cell.replace(' ', '').lower() for cell in header].index('name')
    return header, [row for row in reader if len(row) > name_at and item.keep(row[name_at])]


def _id_column(header):
    return [cell.replace(' ', '').lower() for cell in header].index('modeandpid')


def csv_text(item):
    """The list as Torque CSV text: the file's own header, then only this list's rows."""
    header, rows = _rows(item)
    out = io.StringIO()
    writer = csv.writer(out, quoting=csv.QUOTE_ALL, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(rows)
    return out.getvalue()


def count(item):
    """How many different PIDs the list loads. A file can list one PID twice (two ways of reading the same
    value); the app keeps the first, so that is what is counted."""
    header, rows = _rows(item)
    at = _id_column(header)
    return len({row[at].strip().lower() for row in rows if len(row) > at})


def save_to_profile(directory, item, name, make, model, year, transmission):
    """Save the list as the user's profile for a car. Returns (profile, rejected rows); profile is None when
    nothing was usable. The car needs a name, a make or a model so the profile can be told apart later."""
    if not (name or make or model).strip():
        return None, [{'line': 0, 'name': '', 'reason': 'Give the car a name, make or model first.'}]
    return profiles.save_user(directory, name, make, model, year, transmission, csv_text(item))
