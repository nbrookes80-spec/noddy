"""GUI-free application logic: builds engine configs and tables from user choices.

Everything here is pure Python so it can be unit tested without a display.
"""

from .engines import constants as C
from .engines.boost_curve import BoostCurve
from .engines.calc_engine import CalcEngine
from .engines.drag_simulator import DragSimulator
from .engines.logimporter import LogImporter
from .engines.pressure_engine import PressureEngine
from .engines.shift_time_engine import ShiftTimeEngine
from .engines.tcc_duty_engine import TCCDutyEngine
from .engines.torque_curve import TorqueCurve

# Per-gear (up, down) delays used when the user has not set a table. This is the
# fallback the original DelayDialog.get_delays uses on a parse error.
DEFAULT_DELAY = (0.5, 0.15)

# Fallback throttle-body values when the profile names none (Custom preset).
DEFAULT_TB = (1.0, 0.0, 5.0, 5.0)  # factor, offset, up firmness, down firmness

CUSTOM_INTENT = '(Custom — keep current overrides)'


def profile_names():
    return list(C.STARTER_PROFILES)


def transmission_names():
    return list(C.TRANS_DB)


def intent_names():
    return [name for name in C.INTENT_PRESETS if name != CUSTOM_INTENT]


def throttle_names():
    return [name for name in C.TB_PRESETS if name != 'Custom']


def tps_axis():
    """TPS percentages for the columns of the upshift, downshift and TCC tables."""
    return [col * C.TPS_STEP for col in range(C.TPS_COLS)]


def apply_intent(cfg, intent_name):
    """Apply a driving intent to a config in place.

    INTENT_PRESETS keys end in _delta (add to the base value) or _abs (replace it).
    Values are then clamped to the original's ranges (_INTENT_CLAMPS).
    """
    preset = C.INTENT_PRESETS.get(intent_name)
    if not preset:
        return cfg
    for key, value in preset.items():
        if key.endswith('_delta'):
            field = key[:-len('_delta')]
            cfg[field] = cfg[field] + value
        elif key.endswith('_abs'):
            cfg[key[:-len('_abs')]] = value
    for field, (lo, hi) in C._INTENT_CLAMPS.items():
        if field in cfg:
            cfg[field] = max(lo, min(hi, cfg[field]))
    return cfg


def shift_cfg_from_profile(profile_name, intent_name=None):
    """CalcEngine config from a starter profile, with an optional driving intent applied."""
    p = C.STARTER_PROFILES[profile_name]
    ratios = list(C.TRANS_DB[p['trans_name']]['ratios'])
    tb = C.TB_PRESETS.get(p.get('tps_preset'))
    factor, offset, up, down = tb if tb else DEFAULT_TB
    cfg = {
        'ratios': ratios,
        'tire_dia': p['tire_dia'],
        'axle': p['axle'],
        'chain': p['chain'],
        'idle_rpm': p['idle_rpm'],
        'stall_rpm': p['stall_rpm'],
        'shift_rpm': p['shift_rpm'],
        'downshift_rpm': p['downshift_rpm'],
        'weight': p['weight'],
        'rwhp': p['rwhp'],
        'tps_offset': offset,
        'tps_factor': factor,
        'up_firmness': up,
        'down_firmness': down,
        'spread_up': p['spread_up'],
        'spread_lock': p['spread_lock'],
        'spread_lock_up': p['spread_lock_up'],
        'spread_unlock_dn': p['spread_unlock_dn'],
        'lead_mode': p['lead_mode'],
        'lead_value': p['lead_value'],
        'down_time': p['down_time'],
        'delays': [DEFAULT_DELAY] * len(ratios),
        'min_tcc_rpm': p['min_tcc_rpm'],
        'min_tcc_gear': p['min_tcc_gear'],
        'accel_lock_gear': p['accel_lock_gear'],
        'wot_lock_gear': p['wot_lock_gear'],
        'stall_lock_logic': False,
    }
    if intent_name and intent_name != CUSTOM_INTENT:
        apply_intent(cfg, intent_name)
    return cfg


def calc_shift_tables(cfg):
    """Run CalcEngine and return its dict of tables."""
    return CalcEngine.calculate(cfg)


# Shift Points engines. The BC Trans engine runs the Calc_Shifts port on a loaded .BTC tune.
ENGINE_CALC = 'TunerToolPro (CalcEngine)'
ENGINE_BC = 'BC Trans (Calc_Shifts)'


def bc_shift_tables(tune):
    """Run the BC Trans Calc_Shifts port on a BtcTune.

    Returns the same keys as calc_shift_tables, so the tables and TPS x Gear export work
    for both engines. Also returns logic_error and iterations for the status line.
    """
    from .bct.calc_shifts import calc_shifts
    result = calc_shifts(tune)
    return {
        'upshift': result.upshift,
        'downshift': result.downshift,
        'tcc_unlock': result.tcc_unlock,
        'tcc_lock': result.tcc_lock,
        'n_gears': result.gears,
        'logic_error': result.logic_error,
        'iterations': result.iterations,
    }


def tps_gear_text(tables):
    """Tab-separated TPS x Gear matrices for pasting into VCM Editor or TunerPro.

    Each block has a title line, a header line of TPS percentages, then one row
    per shift or gear.
    """
    axis = tps_axis()
    header = '\t'.join(f'{v:g}' for v in axis)
    shift_labels = [f'{g + 1}-{g + 2}' for g in range(len(tables['upshift']))]
    gear_labels = [f'Gear {g + 1}' for g in range(tables['n_gears'])]
    blocks = [
        ('Upshift MPH', shift_labels, tables['upshift']),
        ('Downshift MPH', shift_labels, tables['downshift']),
        ('TCC unlock MPH', gear_labels, tables['tcc_unlock']),
        ('TCC lock MPH', gear_labels, tables['tcc_lock']),
    ]
    out = []
    for title, labels, rows in blocks:
        out.append(title)
        out.append('TPS %\t' + header)
        for label, row in zip(labels, rows):
            out.append(label + '\t' + '\t'.join(f'{v:.2f}' for v in row))
        out.append('')
    return '\n'.join(out)


def pressure_table(kind, intent, max_torque=640.0, max_psi=296.0, era=None):
    """Return (row_labels, col_labels, data, unit) for a pressure or timing table.

    era is only used by the TCC apply ramp (one of C.TCC_RAMP_ERAS).
    """
    temps = [f'{t} °F' for t in C.PRESSURE_TEMP_ROWS]
    torque = [f'{t:g} lb-ft' for t in PressureEngine.torque_cols(max_torque)]
    if kind == 'Base shift pressure 4-speed':
        data = PressureEngine.base_shift_pressure_4spd(intent)
        cols = [f'{t:g} lb-ft' for t in C.PRESSURE_4SPD_TORQUE_COLS]
        return list(C.PRESSURE_4SPD_SHIFTS), cols, data, 'psi'
    if kind == 'TCC apply ramp':
        cfg = C.TCC_RAMP_ERAS[era or '2015+']
        data = PressureEngine.tcc_apply_pressure_ramp(intent, era or '2015+', max_torque)
        if cfg['row_axis'] == 'torque':
            rows = [f'{t:g} torque' for t in cfg['torque_rows']]
        else:
            rows = [f'{r:g} RPM' for r in cfg['rpm_rows']]
        cols = [f'{s:g} slip' for s in cfg['slip_cols']]
        return rows, cols, data, 'psi'
    if kind == 'Base shift pressure':
        data = PressureEngine.base_shift_pressure(intent, max_torque, '1-2', max_psi)
        return temps, torque, data, 'psi'
    if kind == 'TCC apply pressure':
        data = PressureEngine.tcc_apply_pressure(intent, max_torque, max_psi)
        return temps, torque, data, 'psi'
    if kind == 'Coast pressure':
        data = PressureEngine.coast_pressure(intent, max_torque, max_psi)
        return temps, torque, data, 'psi'
    if kind == 'Shift time 4-speed':
        data = ShiftTimeEngine.desired_shift_time_4spd(intent)
        cols = [f'{t:g} lb-ft' for t in C.SHIFT_TIME_TORQUE_COLS]
        return list(C.SHIFT_TIME_SHIFTS), cols, data, 'seconds'
    if kind == 'TCC duty maximum':
        data = TCCDutyEngine.max_duty_cycle()
        rows = [f'{t} °F' for t in C.TCC_DC_TEMP_ROWS]
        cols = [f'{p:g} psi' for p in C.TCC_DC_LINE_PSI_COLS]
        return rows, cols, data, '%'
    raise ValueError(f'unknown table kind: {kind}')


PRESSURE_KINDS = ['Base shift pressure', 'Base shift pressure 4-speed', 'TCC apply pressure',
                  'TCC apply ramp', 'Coast pressure', 'Shift time 4-speed', 'TCC duty maximum']
def drag_cfg(shift_cfg, curve):
    """DragSimulator config: a shift config plus a torque curve."""
    cfg = dict(shift_cfg)
    cfg['torque_curve'] = curve
    return cfg


def run_drag(shift_cfg, curve, boost=None, shift_points_mph=None):
    """Run a launch-to-quarter-mile simulation and return its results dict (or None)."""
    if boost is not None:
        curve = TorqueCurve(curve.points, boost_curve=boost)
    sim = DragSimulator(drag_cfg(shift_cfg, curve), shift_points_mph=shift_points_mph)
    return sim.simulate()


def load_dyno(path):
    """Load a dyno CSV (rpm, hp, tq) into a TorqueCurve.

    The engine parser drops any row with a blank or non-numeric cell. If nothing is
    left, the error says so, because the usual cause is a blank torque column.
    """
    curve = TorqueCurve.from_csv(path)
    if curve.is_empty:
        raise ValueError('no usable rows. Every row needs numbers in rpm, hp and tq. '
                         'Enter 0 for torque to have it calculated from horsepower.')
    return curve


def dyno_summary(curve):
    """Peak numbers and the RPM range of a curve, as a list of (label, value)."""
    if curve.is_empty:
        return [('Points', 0)]
    lo, hi = curve.rpm_range
    return [
        ('Points', len(curve.points)),
        ('RPM range', f'{lo:.0f} – {hi:.0f}'),
        ('Peak HP', f'{curve.peak_hp:.1f} at {curve.peak_hp_rpm:.0f} RPM'),
        ('Peak torque', f'{curve.peak_tq:.1f} at {curve.peak_tq_rpm:.0f} RPM'),
    ]


def make_boost(spool_rpm, peak_psi, peak_rpm, redline_psi, torque_per_psi):
    if peak_psi <= 0:
        return None
    return BoostCurve(spool_rpm=spool_rpm, peak_psi=peak_psi, peak_rpm=peak_rpm,
                      redline_psi=redline_psi, torque_per_psi_pct=torque_per_psi)


def analyze_log(path, cfg=None, progress_cb=None, target_hz=None):
    """Load a datalog CSV and run LogImporter.analyze. Returns (importer, result)."""
    imp = LogImporter.from_csv(path, progress_cb=progress_cb, target_hz=target_hz)
    return imp, imp.analyze(cfg)
