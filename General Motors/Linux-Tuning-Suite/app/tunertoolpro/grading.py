"""Green, yellow and red for each cell of the shift tables, and for the live readings.

Every verdict is arithmetic on the user's own settings: the engine speed a cell implies, compared
with the shift RPM, idle, stall and converter-lock RPM they entered. The limits are rules of thumb
kept in one place (LIMITS). They flag cells worth a second look; they are not a standard, and a
red cell on a purpose-built tune can be deliberate.

No Kivy here, so the rules can be tested on a desktop.
"""

from dataclasses import dataclass, field

MPH_K = 336.13            # same constant as the desktop CalcEngine
TCC_DISABLED_MPH = 255.0  # the tables use 255 for "the converter never locks in this cell"

GOOD, OK, BAD, OFF = 'good', 'ok', 'bad', 'off'
SEVERITY = {OFF: -1, GOOD: 0, OK: 1, BAD: 2}
TABLES = ('upshift', 'downshift', 'tcc_unlock', 'tcc_lock')


@dataclass(frozen=True)
class Limits:
    over_rev_ok: float = 1.00         # engine speed above this share of the shift RPM: yellow
    over_rev_bad: float = 1.03        # ... above this share: red
    lug_ok: float = 300.0             # rpm after an upshift less than idle + this: yellow
    lug_bad: float = 150.0            # ... less than idle + this: red
    wot_low_ok: float = 0.75          # full-throttle upshift below this share of the shift RPM: yellow
    wot_low_bad: float = 0.60         # ... below this share: red
    step_back_mph: float = 0.05       # a cell may be this much lower than the one before it
    gap_ok_mph: float = 2.0           # downshift less than this far under its upshift: yellow
    gap_bad_mph: float = 0.5          # ... less than this: red (the gearbox would hunt)
    lock_gap_ok_mph: float = 1.0      # unlock less than this far under its lock speed: yellow
    lock_rpm_ok: float = 1.0          # lock below this share of the minimum lock RPM: yellow
    lock_rpm_bad: float = 0.9         # ... below this share: red


LIMITS = Limits()


@dataclass
class Grades:
    levels: dict = field(default_factory=dict)    # table -> grid of good / ok / bad / off
    reasons: dict = field(default_factory=dict)   # table -> grid of text (empty for good cells)
    counts: dict = field(default_factory=dict)    # level -> number of cells
    worst: list = field(default_factory=list)     # red cells first, then yellow, with a sentence each


def _rpm(cfg, mph, gear_index):
    return mph * cfg['axle'] * cfg['chain'] * cfg['ratios'][gear_index] * MPH_K / cfg['tire_dia']


def _worse(current, candidate):
    return candidate if SEVERITY[candidate[0]] > SEVERITY[current[0]] else current


def _check_up(cfg, tables, g, c, lim):
    mph = tables['upshift'][g][c]
    ratios = cfg['ratios']
    before = _rpm(cfg, mph, g)
    after = before * ratios[g + 1] / ratios[g]
    shift_rpm, idle = cfg['shift_rpm'], cfg['idle_rpm']
    verdict = (GOOD, '')
    if before > shift_rpm * lim.over_rev_bad:
        verdict = _worse(verdict, (BAD, f'The engine would be at {before:.0f} rpm before this shift, '
                                        f'well above your {shift_rpm:.0f} rpm shift target.'))
    elif before > shift_rpm * lim.over_rev_ok:
        verdict = _worse(verdict, (OK, f'The engine would be at {before:.0f} rpm before this shift, '
                                       f'just above your {shift_rpm:.0f} rpm shift target.'))
    if after < idle + lim.lug_bad:
        verdict = _worse(verdict, (BAD, f'The engine would fall to {after:.0f} rpm after this shift, '
                                        f'close to the {idle:.0f} rpm idle.'))
    elif after < idle + lim.lug_ok:
        verdict = _worse(verdict, (OK, f'The engine would fall to {after:.0f} rpm after this shift, '
                                       f'low against the {idle:.0f} rpm idle.'))
    if c == len(tables['upshift'][g]) - 1:
        if before < shift_rpm * lim.wot_low_bad:
            verdict = _worse(verdict, (BAD, f'Full-throttle shift at only {before:.0f} rpm, far below '
                                            f'your {shift_rpm:.0f} rpm target.'))
        elif before < shift_rpm * lim.wot_low_ok:
            verdict = _worse(verdict, (OK, f'Full-throttle shift at {before:.0f} rpm, below your '
                                           f'{shift_rpm:.0f} rpm target.'))
    if c > 0 and mph < tables['upshift'][g][c - 1] - lim.step_back_mph:
        verdict = _worse(verdict, (BAD, 'The shift speed falls as the throttle opens.'))
    return verdict


def _check_down(cfg, tables, g, c, lim):
    mph = tables['downshift'][g][c]
    lands = _rpm(cfg, mph, g)
    shift_rpm, down_rpm = cfg['shift_rpm'], cfg['downshift_rpm']
    verdict = (GOOD, '')
    if lands > shift_rpm:
        verdict = _worse(verdict, (BAD, f'The engine would rev to {lands:.0f} rpm after this downshift, '
                                        f'above your {shift_rpm:.0f} rpm shift target.'))
    elif lands > down_rpm:
        verdict = _worse(verdict, (OK, f'The engine would rev to {lands:.0f} rpm after this downshift, '
                                       f'above your {down_rpm:.0f} rpm downshift setting.'))
    gap = tables['upshift'][g][c] - mph
    if gap < lim.gap_bad_mph:
        verdict = _worse(verdict, (BAD, f'Downshift is only {gap:.1f} mph under the upshift, so the '
                                        'gearbox would hunt between gears.'))
    elif gap < lim.gap_ok_mph:
        verdict = _worse(verdict, (OK, f'Downshift is only {gap:.1f} mph under the upshift.'))
    if c > 0 and mph < tables['downshift'][g][c - 1] - lim.step_back_mph:
        verdict = _worse(verdict, (BAD, 'The downshift speed falls as the throttle opens.'))
    return verdict


def _check_lock(cfg, tables, g, c, lim):
    mph = tables['tcc_lock'][g][c]
    if mph >= TCC_DISABLED_MPH:
        return (OFF, '')
    rpm = _rpm(cfg, mph, g)
    minimum = cfg['min_tcc_rpm']
    verdict = (GOOD, '')
    if rpm < minimum * lim.lock_rpm_bad:
        verdict = _worse(verdict, (BAD, f'The converter would lock at {rpm:.0f} rpm, well under your '
                                        f'{minimum:.0f} rpm minimum.'))
    elif rpm < minimum * lim.lock_rpm_ok:
        verdict = _worse(verdict, (OK, f'The converter would lock at {rpm:.0f} rpm, under your '
                                       f'{minimum:.0f} rpm minimum.'))
    if rpm > cfg['shift_rpm']:
        verdict = _worse(verdict, (BAD, f'The converter would lock at {rpm:.0f} rpm, above your '
                                        f'{cfg["shift_rpm"]:.0f} rpm shift target.'))
    return verdict


def _check_unlock(cfg, tables, g, c, lim):
    mph = tables['tcc_unlock'][g][c]
    lock = tables['tcc_lock'][g][c]
    if mph >= TCC_DISABLED_MPH or lock >= TCC_DISABLED_MPH:
        return (OFF, '')
    gap = lock - mph
    if gap <= 0:
        return (BAD, 'The converter would unlock at or above the speed it locks, so it would flutter.')
    if gap < lim.lock_gap_ok_mph:
        return (OK, f'Unlock is only {gap:.1f} mph under lock, so the converter may flutter.')
    return (GOOD, '')


CHECKS = {'upshift': _check_up, 'downshift': _check_down, 'tcc_lock': _check_lock,
          'tcc_unlock': _check_unlock}


def grade_tables(tables, cfg, limits=LIMITS):
    """Grade every cell of the four shift tables against the settings that produced them."""
    result = Grades(counts={GOOD: 0, OK: 0, BAD: 0, OFF: 0})
    problems = []
    for name in TABLES:
        grid, notes = [], []
        for g, row in enumerate(tables[name]):
            levels, texts = [], []
            for c in range(len(row)):
                level, message = CHECKS[name](cfg, tables, g, c, limits)
                levels.append(level)
                texts.append(message)
                result.counts[level] += 1
                if level in (OK, BAD):
                    problems.append({'table': name, 'row': g, 'col': c, 'level': level,
                                     'message': message})
            grid.append(levels)
            notes.append(texts)
        result.levels[name] = grid
        result.reasons[name] = notes
    problems.sort(key=lambda p: -SEVERITY[p['level']])
    result.worst = problems
    return result


# --- live readings --------------------------------------------------------------------------------

@dataclass(frozen=True)
class LiveLimits:
    trans_temp_good: tuple = (60.0, 105.0)    # C. Cold or warm is yellow, hot is red.
    trans_temp_bad: float = 120.0
    coolant_good: tuple = (70.0, 105.0)       # C
    coolant_bad: float = 113.0
    pc_error_good: float = 0.10               # solenoid current off its reference, as a share of it
    pc_error_ok: float = 0.25
    gear_lag_ok_s: float = 1.5                # actual gear not following the command for this long
    gear_lag_bad_s: float = 4.0
    shift_delta_good: float = 8.0             # observed shift speed vs the table, percent
    shift_delta_ok: float = 20.0


LIVE_LIMITS = LiveLimits()


def grade_trans_temp(celsius, lim=LIVE_LIMITS):
    low, high = lim.trans_temp_good
    text = f'{celsius:.0f} C ({celsius * 9 / 5 + 32:.0f} F)'
    if celsius > lim.trans_temp_bad:
        return BAD, text + ', too hot'
    if celsius > high:
        return OK, text + ', running warm'
    if celsius < low:
        return OK, text + ', not up to temperature yet'
    return GOOD, text


def grade_coolant(celsius, lim=LIVE_LIMITS):
    low, high = lim.coolant_good
    text = f'{celsius:.0f} C ({celsius * 9 / 5 + 32:.0f} F)'
    if celsius > lim.coolant_bad:
        return BAD, text + ', too hot'
    if celsius > high:
        return OK, text + ', running warm'
    if celsius < low:
        return OK, text + ', not up to temperature yet'
    return GOOD, text


def grade_engine_rpm(rpm, shift_rpm, lim=LIMITS):
    text = f'{rpm:.0f} rpm'
    if rpm > shift_rpm * lim.over_rev_bad:
        return BAD, text + f', over your {shift_rpm:.0f} rpm shift target'
    if rpm > shift_rpm * lim.over_rev_ok:
        return OK, text + f', just over your {shift_rpm:.0f} rpm shift target'
    return GOOD, text


def grade_pc_current(actual, reference, lim=LIVE_LIMITS):
    if reference is None or reference <= 0:
        return OFF, 'no reference current'
    error = abs(reference - actual) / reference
    text = f'{actual:.2f} against {reference:.2f} wanted ({error * 100:.0f}% off)'
    if error <= lim.pc_error_good:
        return GOOD, text
    return (OK if error <= lim.pc_error_ok else BAD), text


def grade_gear_follow(actual, commanded, seconds, lim=LIVE_LIMITS):
    if actual is None or commanded is None:
        return OFF, 'waiting for gear data'
    if round(actual) == round(commanded):
        return GOOD, f'gear {actual:.0f}, following the command'
    text = f'gear {actual:.0f}, commanded {commanded:.0f} for {seconds:.1f} s'
    if seconds >= lim.gear_lag_bad_s:
        return BAD, text
    if seconds >= lim.gear_lag_ok_s:
        return OK, text
    return GOOD, text


def grade_shift_delta(delta_pct, lim=LIVE_LIMITS):
    size = abs(delta_pct)
    if size <= lim.shift_delta_good:
        return GOOD
    return OK if size <= lim.shift_delta_ok else BAD
