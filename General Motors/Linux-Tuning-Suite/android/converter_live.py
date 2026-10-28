"""Converter and differential choices for the Shift screen, working on the screen's text values.

The rules live in tunertoolpro/converter.py. This module only reads and writes the strings the boxes hold,
and keeps a stock-converter base so choosing a type twice does not stack the steps.
"""

from tunertoolpro import converter

FIELDS = ('stall_rpm', 'idle_rpm', 'shift_rpm', 'min_tcc_rpm')
LABELS = [converter.label(k) for k in converter.type_keys()]


def read_base(values):
    """The converter-related numbers in the current boxes. None when one is not a number."""
    try:
        return {k: float(values[k]) for k in FIELDS}
    except (KeyError, ValueError):
        return None


def choose(values, base, label, n_gears):
    """New text values for a converter label. Returns (text changes, stall logic on, notes, advice).

    A stall typed over the base figure counts as the user's own number for this converter.
    """
    key = converter.key_for_label(label)
    now = read_base(values)
    if now is None or base is None:
        return {}, False, ['Fix the highlighted settings first.'], []
    typed = now['stall_rpm']
    stall = typed if key != converter.STOCK and abs(typed - base['stall_rpm']) > 1 else None
    changes, stall_logic, notes = converter.adjust(now, key, stall_rpm=stall, base=base, n_gears=n_gears)
    return ({k: f'{v:.0f}' for k, v in changes.items()}, stall_logic, notes, converter.tcm_advice(key))


def diff_values(axle_text):
    """Preset ratios as text, with the current axle added when it is not in the list."""
    try:
        axle = float(axle_text)
    except ValueError:
        axle = None
    return [f'{r:g}' for r in converter.diff_options(axle)]


def diff_report(ratios_text, old_axle, new_axle, values):
    """Plain-words change report for a new diff ratio. Empty when the inputs are unreadable."""
    try:
        ratios = [float(x) for x in ratios_text.replace(' ', '').split(',') if x]
        return converter.diff_change(ratios, float(old_axle), float(new_axle), float(values['tire_dia']),
                                     float(values['shift_rpm']), float(values.get('chain') or 1.0))
    except (ValueError, KeyError, ZeroDivisionError, IndexError):
        return []


def diff_summary(ratios_text, values):
    """One line on what the current diff does. Empty when the inputs are unreadable."""
    try:
        ratios = [float(x) for x in ratios_text.replace(' ', '').split(',') if x]
        return converter.diff_effect(ratios, float(values['axle']), float(values['tire_dia']),
                                     float(values['shift_rpm']), float(values.get('chain') or 1.0))[1]
    except (ValueError, KeyError, ZeroDivisionError, IndexError):
        return []
