"""Shift Points calculation for the Android app. No Kivy here, so it can be tested on a desktop.

Every change to an input re-runs the calculation, so a change to one value shows its effect on the
shift tables straight away. The calculation is the same code the desktop app uses.
"""

from tunertoolpro import core

# key, label, min, max, step, decimals. Same ranges as the desktop Shift Points tab.
FIELDS = [
    ('tire_dia', 'Tire diameter (in)', 20.0, 40.0, 0.1, 2),
    ('axle', 'Axle ratio', 1.5, 6.0, 0.01, 2),
    ('chain', 'Transfer / chain ratio', 0.5, 3.0, 0.01, 2),
    ('weight', 'Weight (lb)', 1500, 8000, 10, 0),
    ('rwhp', 'Rear-wheel HP', 50, 2000, 5, 0),
    ('idle_rpm', 'Idle RPM', 400, 1200, 10, 0),
    ('stall_rpm', 'Stall RPM', 1000, 4500, 10, 0),
    ('shift_rpm', 'Shift RPM (WOT)', 3000, 9000, 50, 0),
    ('downshift_rpm', 'Downshift RPM', 1000, 9900, 50, 0),
    ('min_tcc_rpm', 'Minimum TCC RPM', 800, 3000, 10, 0),
    ('min_tcc_gear', 'Minimum TCC gear', 1, 10, 1, 0),
    ('accel_lock_gear', 'Accelerator-lock gear', 1, 10, 1, 0),
    ('wot_lock_gear', 'WOT-lock gear', 1, 10, 1, 0),
    ('tps_offset', 'TPS offset (%)', -20, 50, 1, 1),
    ('tps_factor', 'TPS factor', 0.5, 4.0, 0.05, 2),
    ('up_firmness', 'Upshift firmness', 0.0, 10.0, 0.5, 1),
    ('down_firmness', 'Downshift firmness', 0.0, 10.0, 0.5, 1),
    ('spread_up', 'Upshift spread (mph)', 0.5, 15.0, 0.5, 2),
    ('spread_lock', 'Lock spread (mph)', 0.5, 10.0, 0.5, 2),
    ('spread_lock_up', 'Lock-up spread (mph)', 0.5, 10.0, 0.5, 2),
    ('spread_unlock_dn', 'Unlock spread (mph)', 0.5, 10.0, 0.5, 2),
    ('lead_value', 'Lead value', 0.0, 8.0, 0.25, 2),
    ('down_time', 'Downshift time (s)', 0.0, 2.0, 0.05, 2),
]
INTEGER_FIELDS = {'idle_rpm', 'stall_rpm', 'shift_rpm', 'downshift_rpm', 'min_tcc_rpm', 'weight',
                  'rwhp', 'min_tcc_gear', 'accel_lock_gear', 'wot_lock_gear'}


def parse_value(key, text):
    """Return the number typed for a field, or raise ValueError with a message the user can act on."""
    _, label, lo, hi, _, _ = next(f for f in FIELDS if f[0] == key)
    try:
        number = float(text)
    except (TypeError, ValueError):
        raise ValueError(f'{label}: enter a number') from None
    if not lo <= number <= hi:
        raise ValueError(f'{label}: must be between {lo:g} and {hi:g}')
    return int(round(number)) if key in INTEGER_FIELDS else number


def default_inputs(profile_name=None):
    """The starting values, taken from a built-in vehicle profile: ({key: text}, ratios_text)."""
    name = profile_name or core.profile_names()[0]
    cfg = core.shift_cfg_from_profile(name)
    values = {key: str(cfg[key]) for key, *_ in FIELDS}
    ratios = ', '.join(f'{r:g}' for r in cfg['ratios'])
    return values, ratios


def build_cfg(values, ratios_text, lead_mode='rpm', stall_lock=False):
    """Turn the typed values into the settings core.calc_shift_tables expects.

    values: {key: text}. ratios_text: '3.06, 1.63, 1.00, 0.70'.
    """
    cfg = {}
    for key, *_ in FIELDS:
        cfg[key] = parse_value(key, values[key])
    ratios = [float(x) for x in ratios_text.replace(' ', '').split(',') if x]
    if len(ratios) < 2:
        raise ValueError('enter at least two gear ratios, separated by commas')
    cfg['ratios'] = ratios
    cfg['lead_mode'] = lead_mode
    cfg['lead_value'] = float(cfg['lead_value'])
    cfg['delays'] = [core.DEFAULT_DELAY] * len(ratios)
    cfg['stall_lock_logic'] = bool(stall_lock)
    return cfg


def calculate(values, ratios_text, lead_mode='rpm', stall_lock=False):
    """Run the shift calculation. Returns (tables, error). error is '' when the tables are valid."""
    try:
        cfg = build_cfg(values, ratios_text, lead_mode, stall_lock)
        return core.calc_shift_tables(cfg), ''
    except (ValueError, ZeroDivisionError, KeyError) as exc:
        return None, str(exc)


def upshift_rows(tables):
    """The upshift table as text rows: a header, then one row per shift, cells at each throttle point."""
    tps = [f'{v:g}%' for v in core.tps_axis()]
    rows = [['Shift'] + tps]
    for g, row in enumerate(tables['upshift']):
        rows.append([f'{g + 1}-{g + 2}'] + [f'{x:.1f}' for x in row])
    return rows
