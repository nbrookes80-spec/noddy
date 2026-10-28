"""Which car and which automatic transmission the shift tables are for. No Kivy, so it can be tested on a desktop.

GM transmissions come from the tuning data shared with the desktop app. Ford, and the Holden and
Pontiac extras, are gear ratios from published specifications that have not been checked against a car,
so they are marked as unchecked. Check yours against the transmission's tag or a service manual.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from . import core

MAKES = ('GM', 'Holden', 'Pontiac', 'Ford')
LOCK_GEAR_KEYS = ('min_tcc_gear', 'accel_lock_gear', 'wot_lock_gear')
DEFAULT_CHOICE = {'make': 'GM', 'transmission': '', 'profile': ''}


@dataclass(frozen=True)
class Transmission:
    name: str
    ratios: list
    drive: str
    makes: tuple
    verified: bool
    note: str = ''


# Which makes fitted each GM-designed unit that the shared data already knows. Holden and Pontiac (G8)
# sold the same GM units; check the build plate for the one in your car.
_HOLDEN = ('4L60E', '4L65E', '4L80E', '6L45', '6L50', '6L80')
_PONTIAC = ('4L60E', '4L65E', '4L80E', '4T40E', '4T45E', '4T65E', '4T65E-HD', '6L50', '6L80', '6T70', '6T75')

_UNCHECKED = 'Ratios from published specifications, not yet checked against a car.'


def _extra(name, ratios, drive, makes):
    return Transmission(name, ratios, drive, makes, False, _UNCHECKED)


_EXTRAS = [
    _extra('5L40E (2003-2009)', [3.571, 2.2, 1.505, 1.0, 0.803], 'RWD', ('Holden', 'Pontiac')),
    _extra('4R70W (1993-2003)', [2.84, 1.55, 1.0, 0.7], 'RWD', ('Ford',)),
    _extra('4R75E (2002-2011)', [2.84, 1.55, 1.0, 0.7], 'RWD', ('Ford',)),
    _extra('4R100 (1998-2003)', [2.71, 1.54, 1.0, 0.71], 'RWD', ('Ford',)),
    _extra('E4OD (1989-1998)', [2.71, 1.54, 1.0, 0.71], 'RWD', ('Ford',)),
    _extra('A4LD (1985-1995)', [2.4, 1.47, 1.0, 0.75], 'RWD', ('Ford',)),
    _extra('6R60 (2005-2014)', [4.17, 2.34, 1.52, 1.14, 0.87, 0.69], 'RWD', ('Ford',)),
    _extra('6R80 (2009-Current)', [4.17, 2.34, 1.52, 1.14, 0.87, 0.69], 'RWD', ('Ford',)),
    _extra('6F35 (2009-Current)', [4.584, 2.964, 1.912, 1.446, 1.0, 0.746], 'FWD', ('Ford',)),
    _extra('10R80 (2017-Current)', [4.696, 2.985, 2.146, 1.769, 1.52, 1.275, 1.0, 0.854, 0.689, 0.636],
           'RWD', ('Ford',)),
    _extra('ZF 6HP26 (Falcon FG, 2008-2014)', [4.171, 2.34, 1.521, 1.143, 0.867, 0.691], 'RWD', ('Ford',)),
]


def _build():
    from .engines import constants
    everything = []
    for name in core.transmission_names():
        data = constants.TRANS_DB[name]
        code = name.split(' ')[0]
        makes = ['GM']
        if code in _HOLDEN:
            makes.append('Holden')
        if code in _PONTIAC:
            makes.append('Pontiac')
        everything.append(Transmission(name, list(data['ratios']), data['type'], tuple(makes), True))
    return everything + _EXTRAS


ALL = _build()


def transmissions(make):
    """The automatics offered for a make, in the order they are listed."""
    return [t for t in ALL if make in t.makes]


def find(name):
    return next((t for t in ALL if t.name == name), None)


def ratios_text(transmission):
    """'4.027, 2.364, ...' as the gear box on the Shift screen expects."""
    return ', '.join(f'{r:g}' for r in transmission.ratios)


def fit_gears(values, gear_count):
    """A copy of the typed values with the converter-lock gears held within the gears that exist."""
    fitted = dict(values)
    for key in LOCK_GEAR_KEYS:
        try:
            fitted[key] = str(min(int(float(fitted[key])), gear_count))
        except (KeyError, ValueError):
            pass
    return fitted


def load(path):
    """The saved make, transmission and starting profile, or the defaults for anything missing or odd."""
    result = dict(DEFAULT_CHOICE)
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return result
    if not isinstance(data, dict):
        return result
    if data.get('make') in MAKES:
        result['make'] = data['make']
    if find(data.get('transmission')):
        result['transmission'] = data['transmission']
    if data.get('profile') in core.profile_names():
        result['profile'] = data['profile']
    return result


def save(path, choice):
    clean = {key: choice.get(key, DEFAULT_CHOICE[key]) for key in DEFAULT_CHOICE}
    try:
        Path(path).write_text(json.dumps(clean))
    except OSError:
        pass   # nothing here is essential
