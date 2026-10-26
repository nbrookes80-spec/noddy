"""Map a Bluecat .BTC tune onto the inputs of the Shift Points tab (CalcEngine).

This is an input translation only. CalcEngine is the Python app's shift algorithm.
BC Trans runs a different one (Main_Form.cs Calc_Shifts), so the tables the Shift
Points tab produces from a tune are not BC Trans output.

Each mapping below names the BTC key, and the BC Trans control it is written from
(Main_Form.cs, the BTC writer around lines 6278-6557). The meanings follow how
Calc_Shifts reads those controls.
"""

from .tune import BtcTune

# (CalcEngine key, BTC key, how it is read)
_SCALARS = [
    ('tire_dia', 'Tire', 'float'),            # Tire.Value
    ('axle', 'Gear', 'float'),                # Gear is labelled "Final" (final drive)
    ('idle_rpm', 'Idle', 'int'),              # Idle.Value
    ('stall_rpm', 'Stall', 'int'),            # Stall.Value
    ('downshift_rpm', 'DownRPM', 'int'),      # DRPM.Value
    ('weight', 'Weight', 'int'),              # Lead_Form.Weight
    ('rwhp', 'RWHP', 'int'),                  # Lead_Form.RWHP
    ('down_time', 'DownTime', 'float'),       # Lead_Form.Down_Time
    ('lead_value', 'Lead', 'float'),          # Lead_Form.Lead
    ('tps_offset', 'Offset', 'float'),        # Offset.Value
    ('tps_factor', 'Factor', 'float'),        # Factor.Value
    ('up_firmness', 'UpFactor', 'float'),     # UpF.Value
    ('down_firmness', 'DownFactor', 'float'), # DownF.Value
    ('spread_up', 'ShiftSpread', 'float'),          # Shift_Spread
    ('spread_lock', 'LockSpread', 'float'),         # Lock_Spread
    ('spread_lock_up', 'ShiftLockSpread', 'float'), # Lock_Shift_Spread
    ('spread_unlock_dn', 'UnlockShiftSpread', 'float'),  # Unlock_Shift_Spread
    ('min_tcc_rpm', 'TCC_MinRpm', 'int'),     # TCC_Form.MinTCCrpm (scalar floor)
    ('min_tcc_gear', 'MinLockGear', 'int'),   # MinLck.Value
    ('accel_lock_gear', 'AccelLockGear', 'int'),  # AclLck.Value
    ('wot_lock_gear', 'WOTLockGear', 'int'),  # WotLck.Value
]


def required_keys(gear_count):
    """Every BTC key the mapping reads, for a tune with gear_count gears."""
    keys = ['Gears', 'Lead', 'AdvancedLead', 'StallLogic']
    keys += [k for _, k, _ in _SCALARS]
    keys += [f'Ratio{i}' for i in range(1, gear_count + 1)]
    keys += [f'RPM{i}' for i in range(1, gear_count + 1)]
    keys += [f'Prep{i}' for i in range(1, gear_count)]
    keys += [f'React{i}' for i in range(1, gear_count)]
    return list(dict.fromkeys(keys))


def shift_cfg_from_btc(tune):
    """Return a CalcEngine cfg dict built from a BtcTune.

    Raises ValueError naming every missing key. The tune is not changed.
    """
    gear_count = tune.gear_count()
    if gear_count < 2:
        raise ValueError(f'BTC tune has {gear_count} gear(s); at least two are needed')
    missing = [k for k in required_keys(gear_count) if tune.get(k) is None]
    if missing:
        raise ValueError('BTC tune is missing: ' + ', '.join(missing))

    n = gear_count
    cfg = {}
    for cfg_key, btc_key, kind in _SCALARS:
        raw = tune.getfloat(btc_key)
        cfg[cfg_key] = int(round(raw)) if kind == 'int' else raw
    cfg['ratios'] = [tune.getfloat(f'Ratio{i}') for i in range(1, n + 1)]
    cfg['chain'] = 1.0                          # BC Trans has no separate chain ratio
    cfg['shift_rpm'] = int(round(tune.getfloat(f'RPM{n}')))
    cfg['per_gear_rpm'] = [tune.getfloat(f'RPM{i}') for i in range(1, n + 1)]
    # AdvancedLead is written as "0" when BC Trans's RPM lead radio is selected.
    cfg['lead_mode'] = 'rpm' if tune.getint('AdvancedLead') == 0 else 'torque'
    cfg['stall_lock_logic'] = tune.getint('StallLogic') == 1
    # Delay pair per shift: (Prep, React). BC Trans reads Prep + React on the upshift and
    # adds DownTime on the downshift. CalcEngine uses the same sums. BC Trans has no
    # delay for the top gear; CalcEngine falls back to the last pair for that gear.
    cfg['delays'] = [(tune.getfloat(f'Prep{i}'), tune.getfloat(f'React{i}'))
                     for i in range(1, n)]
    return cfg


def load_btc_shift_cfg(path):
    """Read a .BTC file and return its CalcEngine cfg."""
    return shift_cfg_from_btc(BtcTune.load(path))
