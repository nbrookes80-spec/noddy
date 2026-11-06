"""Unit choices for the dashboard: show temperatures in C or F, pressures in kPa, psi or bar, speeds in km/h or mph.
No Kivy.

This only changes how a reading is shown on a card. Nothing sent to the car or decoded from a reply changes, and a
recording keeps each sensor's own unit, so a log means the same whatever the screen was set to. A sensor whose unit
is not one of these (RPM, %, volts...) is left exactly as it is.
"""

from collections import namedtuple

# Each group converts through one base unit: unit -> (to base, from base).
_GROUPS = {
    'temperature': {'°C': (lambda v: v, lambda v: v),
                    '°F': (lambda v: (v - 32) / 1.8, lambda v: v * 1.8 + 32)},
    'pressure': {'kPa': (lambda v: v, lambda v: v),
                 'psi': (lambda v: v * 6.894757, lambda v: v / 6.894757),
                 'bar': (lambda v: v * 100.0, lambda v: v / 100.0),
                 'Pa': (lambda v: v / 1000.0, lambda v: v * 1000.0)},
    'speed': {'km/h': (lambda v: v, lambda v: v),
              'mph': (lambda v: v * 1.609344, lambda v: v / 1.609344)},
    'distance': {'km': (lambda v: v, lambda v: v),
                 'mi': (lambda v: v * 1.609344, lambda v: v / 1.609344)},
}

CHOICES = {'temperature': ('°C', '°F'), 'pressure': ('kPa', 'psi', 'bar'), 'speed': ('km/h', 'mph')}
DEFAULTS = {'temperature': '°C', 'pressure': 'kPa', 'speed': 'km/h'}
# The pressure choice offers the group's base unit (kPa); Pa is only ever a sensor's own unit, never a choice.

Conversion = namedtuple('Conversion', 'unit forward back')   # forward: sensor's unit -> shown unit; back: the reverse


def identity(value):
    return value


def clean(choices):
    """The saved choices, keeping only ones that are offered."""
    out = dict(DEFAULTS)
    if isinstance(choices, dict):
        for group, allowed in CHOICES.items():
            if choices.get(group) in allowed:
                out[group] = choices[group]
    return out


def group_of(unit):
    return next((group for group, units in _GROUPS.items() if unit in units), None)


def conversion(unit, choices):
    """How to show a sensor measured in `unit`, given the user's choices. Anything unrecognised is shown as it is."""
    group = group_of(unit)
    if group is None:
        return Conversion(unit, identity, identity)
    wanted = clean(choices)
    if group == 'distance':
        wanted_unit = 'mi' if wanted['speed'] == 'mph' else 'km'    # distance follows the speed choice
    else:
        wanted_unit = wanted[group]
    if wanted_unit == unit:
        return Conversion(unit, identity, identity)
    to_base, _ = _GROUPS[group][unit]
    _, from_base = _GROUPS[group][wanted_unit]
    back_to_base, back_from = _GROUPS[group][wanted_unit][0], _GROUPS[group][unit][1]
    return Conversion(wanted_unit, lambda v: from_base(to_base(v)), lambda v: back_from(back_to_base(v)))
