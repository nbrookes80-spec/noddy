"""Port of BC_Trans Calc_Shifts (Main_Form.cs 5213-5920) and Update_Slope (5113-5212).

The inputs come from a .BTC tune, and the grid layout is described in
recovered/bct-csharp/CALC_SHIFTS_NOTES.md. The result is what BC Trans puts in its
grids, so the tables should match BC Trans output. Verification against BC Trans
itself is still pending (see the notes).

Grids use BC Trans's 1-based coordinates, with header row 0 (TPS axis) and header
column 0. Every store is rounded to float32, as BC stores its grids.
"""

import math
import struct

from .shiftmath import BCT_PI
from .tune import BtcTune

NX = 17                      # TPS columns
DIS_LOW_HIGH = (254, 255)    # disabled markers (Dis_Low, Dis_High) when Gears <= 4
DIS_LOW_HIGH_LARGE = (317, 318)
SLOPE_BLEND = (0.0, 0.1, 0.1, 0.1, 0.1, 0.125, 0.15, 0.225, 0.35, 0.5,
               0.675, 0.825, 0.925, 0.95, 1.0, 1.0, 1.0)  # Update_Slope array
STALL_BASE = (0.0, 0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.6,
              0.65, 0.7, 0.75, 0.8, 0.9, 1.0, 1.0)         # Main_Form ctor


def f32(value):
    """Round to the nearest 32-bit float, as BC Trans stores its grid values."""
    return struct.unpack('f', struct.pack('f', float(value)))[0]


def mph(rpm, ratio, final_drive, tire):
    """Calc_Shifts speed conversion (uses the literal 3.14 for pi)."""
    return rpm / (ratio * final_drive) * (tire * BCT_PI) * 60.0 / 12.0 / 5280.0


class Grid:
    """A BCGridControl table. Coordinates are 1-based; row 0 and column 0 are headers."""

    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self._d = {}

    def get(self, x, y):
        return self._d.get((x, y), 0.0)

    def set(self, x, y, value):
        self._d[(x, y)] = f32(value)


class ShiftTables:
    """Results of calc_shifts. Rows are gears (or shifts); columns are the 17 TPS points."""

    def __init__(self, gears, upshift, downshift, unlock, lock, speed, slope, rpm,
                 min_speed, iterations, logic_error, last_pass_log=()):
        self.gears = gears
        self.upshift = upshift          # gears - 1 rows
        self.downshift = downshift      # gears - 1 rows
        self.tcc_unlock = unlock        # gears rows
        self.tcc_lock = lock            # gears rows
        self.speed = speed              # gears rows of 4 columns
        self.slope = slope              # 3 rows of 17 columns
        self.rpm = rpm                  # shift RPM after Calc_Shifts clamps it
        self.min_speed = min_speed
        self.iterations = iterations
        self.logic_error = logic_error
        self.last_pass_log = list(last_pass_log)  # (rule, running count) pairs for the last pass


def _rows(grid, rows, cols=NX):
    return [[grid.get(x, y) for x in range(1, cols + 1)] for y in range(1, rows + 1)]


def _slope_grid(factor, offset, up, down):
    """Update_Slope: the 3 x 17 slope table from the four slope inputs."""
    slope = Grid(NX, 3)
    tps = [6.25 * (c - 1) for c in range(1, NX + 1)]  # the TPS header row

    def x_of(c):
        v = tps[c - 1] - offset
        v = min(max(v, 0.0), 100.0)
        return v / 100.0

    slope.set(1, 1, 0.0)
    for c in range(2, NX + 1):
        slope.set(c, 1, min(max(f32(math.pow(f32(x_of(c)), factor)), 0.0), 1.0))
    slope.set(NX, 1, 1.0)

    slope.set(1, 2, 0.0)
    for c in range(2, NX + 1):
        x = x_of(c)
        y = f32(1.0 - math.pow(f32(1.0 - x), factor + up / 10.0))
        base = slope.get(c, 1)
        y = f32(base + (y - base) * SLOPE_BLEND[c - 1])
        slope.set(c, 2, min(max(y, 0.0), 1.0))
    slope.set(NX, 2, 1.0)

    slope.set(1, 3, 0.0)
    for c in range(2, NX + 1):
        x = x_of(c)
        y = f32(math.pow(x, factor + 0.1 + (10.0 - down) / 5.0))
        slope.set(c, 3, min(max(y, 0.0), 1.0))
    slope.set(NX, 3, 1.0)
    return slope


def _stall_min(tune_vals, slope):
    """StallMin[l] for l = 1..17. Index 0 stays null, as in the original array."""
    stall_min = {}
    for l in range(1, NX + 1):
        n = STALL_BASE[l - 1] + slope.get(l, 1)
        if n > 0.66:
            n = 0.66
        v = f32(n * tune_vals['stall_rpm'] + tune_vals['idle_rpm'])
        if v > tune_vals['stall_rpm']:
            v = f32(tune_vals['stall_rpm'])
        stall_min[l] = v
    return stall_min


def calc_shifts(tune):
    """Run the Calc_Shifts port on a BtcTune. Returns a ShiftTables."""
    v = _read_inputs(tune)
    gears = v['gears']
    if gears < 2:
        raise ValueError('BTC tune has fewer than two gears')
    final = v['final_drive']
    tire = v['tire']
    ratios = v['ratios']

    # Input clamp on RPM (5218-5232): <= 0 becomes 5000, then < 1500 becomes 1500.
    rpm = []
    for r in v['rpm']:
        if r <= 0:
            r = 5000.0
        if r < 1500:
            r = 1500.0
        rpm.append(r)

    stall_slip = f32((v['stall_rpm'] / 1000.0) ** 1.7 / 100.0)

    min_speed = {n: f32(mph(v['idle_rpm'] + 400.0, ratios[n], final, tire))
                 for n in range(1, gears + 1)}

    min_tcc = v['min_tcc']  # Grid(17, 2G) of MinTCC cells
    min_tcc_speed = {}
    for j in range(1, gears + 1):
        for k in range(1, NX + 1):
            min_tcc_speed[(k, j)] = f32(mph(min_tcc.get(k, 2 * j - 1), ratios[j], final, tire))

    slope = _slope_grid(v['factor'], v['offset'], v['up_firmness'], v['down_firmness'])
    stall_min = _stall_min({'stall_rpm': v['stall_rpm'], 'idle_rpm': v['idle_rpm']}, slope)

    # Speed grid: columns 1-4, rows 1..G.
    speed = Grid(4, gears)
    for m in range(1, gears + 1):
        r = rpm[m - 1]
        s1 = mph(r, ratios[m], final, tire)
        speed.set(1, m, s1)
        s2 = f32(speed.get(1, m) * (1.0 - stall_slip))
        speed.set(2, m, s2)
        locked_wot = v['max_speed_locked'] and m >= v['wot_lock_gear']
        base = speed.get(1, m) if locked_wot else speed.get(2, m)
        if v['advanced_lead'] == 0:
            _rpm_lead_speeds(speed, m, base, ratios[m], final, tire, v)
        else:
            _torque_lead_speeds(speed, m, base, ratios[m], final, tire, v)

    upshift = Grid(NX, gears - 1)
    downshift = Grid(NX, gears - 1)
    s_up = v['shift_spread']
    for n in range(1, gears):
        for c in range(1, NX + 1):
            slope_u = (v['override'].get(c, 2 * n - 1) if v['override_on']
                       else slope.get(c, 2))
            upshift.set(c, n, min_speed[n] + s_up
                        + ((speed.get(1, n) - min_speed[n]) - s_up) * slope_u)
    for n in range(1, gears):
        for c in range(1, NX + 1):
            slope_d = (v['override'].get(c, 2 * n) if v['override_on']
                       else slope.get(c, 3))
            downshift.set(c, n, min_speed[n] + (speed.get(4, n) - min_speed[n]) * slope_d)

    unlock = Grid(NX, gears)
    lock = Grid(NX, gears)
    for g in range(2, gears + 1):
        for c in range(1, NX + 1):
            unlock.set(c, g, downshift.get(c, g - 1) + v['unlock_shift_spread'])
    for g in range(1, gears + 1):
        for c in range(1, NX + 1):
            if g == 1:
                unlock.set(c, g, 0.0)
            if unlock.get(c, g) < min_tcc_speed[(c, g)]:
                unlock.set(c, g, min_tcc_speed[(c, g)])
    for g in range(1, gears + 1):
        for c in range(1, NX + 1):
            lock.set(c, g, unlock.get(c, g) + v['lock_spread'])

    if v['stall_logic']:
        for g in range(1, gears + 1):
            for c in range(1, NX + 1):
                n = stall_min.get(c - 1, 0.0)  # StallMin[c - 1]; the original's off-by-one
                if n > rpm[g - 1] * 0.66:
                    n = f32(rpm[g - 1] * 0.66)
                n = f32(mph(n, ratios[g], final, tire))
                if n > lock.get(c, g):
                    lock.set(c, g, n)

    iterations, logic_error, last_log = _iterate(v, gears, speed, upshift, downshift, unlock, lock)

    # Lock = Unlock where MinTCC(c, 2g) == 2.
    for g in range(1, gears + 1):
        for c in range(1, NX + 1):
            if min_tcc.get(c, 2 * g) == 2.0:
                lock.set(c, g, unlock.get(c, g))

    _wot_lock(v, gears, rpm, speed, upshift, lock, unlock)

    # Monotone passes: each cell is at most the cell to its right.
    for grid in (lock, unlock):
        for g in range(1, gears + 1):
            for c in range(NX, 1, -1):
                if grid.get(c - 1, g) > grid.get(c, g):
                    grid.set(c - 1, g, grid.get(c, g))

    dis_lo, dis_hi = DIS_LOW_HIGH if gears <= 4 else DIS_LOW_HIGH_LARGE
    for g in range(1, gears + 1):
        for c in range(1, NX - 2):                 # columns 1..14
            if g < v['min_lock_gear']:
                lock.set(c, g, dis_hi)
                unlock.set(c, g, dis_lo)
        for c in range(NX - 2, NX + 1):            # columns 15..17
            if g < v['wot_lock_gear']:
                lock.set(c, g, dis_hi)
                unlock.set(c, g, dis_lo)

    _extras(v, gears, upshift, downshift, lock, unlock, speed, dis_hi)

    for grid, rows in ((upshift, gears - 1), (downshift, gears - 1), (lock, gears), (unlock, gears)):
        for y in range(1, rows + 1):
            for c in range(1, NX + 1):
                if grid.get(c, y) < 0:
                    grid.set(c, y, 0.0)

    return ShiftTables(
        gears=gears,
        upshift=_rows(upshift, gears - 1),
        downshift=_rows(downshift, gears - 1),
        unlock=_rows(unlock, gears),
        lock=_rows(lock, gears),
        speed=[[speed.get(x, y) for x in range(1, 5)] for y in range(1, gears + 1)],
        slope=_rows(slope, 3),
        rpm=rpm,
        min_speed=[min_speed[n] for n in range(1, gears + 1)],
        iterations=iterations,
        logic_error=logic_error,
        last_pass_log=last_log,
    )


def _rpm_lead_speeds(speed, m, base, ratio, final, tire, v):
    lead = v['lead_value'] / 8.0
    s2 = speed.get(2, m)
    s3 = f32(base * (1.0 - 0.01 * ratio * final * lead) - (ratio + 1.0) * final * lead)
    if s3 < s2 * 0.2:
        s3 = f32(s2 * 0.2)
    speed.set(3, m, s3)
    s4 = f32(s3 * 0.98 - 2.0 - ratio * final * (1.0 + v['lead_value'] / 10.0) * 0.5)
    speed.set(4, m, s4)
    cap = f32(mph(v['downshift_rpm'], ratio, final, tire))
    if speed.get(4, m) > cap:
        speed.set(4, m, cap)
    if speed.get(4, m) < s3 * 0.2:
        speed.set(4, m, f32(s3 * 0.2))


def _torque_lead_speeds(speed, m, base, ratio, final, tire, v):
    accel = f32(v['rwhp'] * 0.75 * 375.0 / base / v['weight'] * 21.93685)
    row = min(m, len(v['delays']))           # Delay row; the top gear uses the last pair
    prep, react = v['delays'][row - 1]
    s3 = f32(base - accel * (prep + react))
    s4 = f32(base - accel * (v['down_time'] + prep + react))
    speed.set(3, m, s3)
    speed.set(4, m, s4)
    cap = f32(mph(v['downshift_rpm'], ratio, final, tire))
    if speed.get(4, m) > cap:
        speed.set(4, m, cap)
    if speed.get(4, m) > s3 - v['shift_spread']:
        speed.set(4, m, f32(s3 - v['shift_spread']))
    if speed.get(4, m) < s3 * 0.2:
        speed.set(4, m, f32(s3 * 0.2))


def _iterate(v, gears, speed, up, dn, unlock, lock):
    """The do-while pass loop (5388-5606).

    Returns (passes run, logic-error count of the last pass, per-rule changes of the last pass).
    """
    acl = v['accel_lock_gear']
    passes = 0
    last = 0
    log = []
    for pass_no in range(1, 33):
        passes = pass_no
        num = 0
        log = []
        log.append(('InitLock', num))
        if v['init_lock']:
            for g in range(1, gears + 1):
                if g != acl:
                    continue
                for c in range(1, NX - 2):
                    if g < up.grid_y and g == 1:
                        val = f32(lock.get(c, 1) + v['lock_shift_spread'])
                        if up.get(c, 1) < val:
                            up.set(c, 1, val)
                            num += 1
                    elif g <= up.grid_y:
                        val = f32((up.get(c, g - 1) + up.get(c, g)) / 2.0)
                        if lock.get(c, g) < val:
                            lock.set(c, g, val)
                            num += 1
                        val = f32(up.get(c, g - 1) + v['lock_shift_spread'])
                        if lock.get(c, g) < val:
                            lock.set(c, g, val)
                            num += 1
                        val = f32(lock.get(c, g) + v['lock_shift_spread'])
                        if up.get(c, g) < val:
                            up.set(c, g, val)
                            num += 1
                    else:
                        val = f32(up.get(c, g - 1) + v['lock_shift_spread'])
                        if lock.get(c, g) < val:
                            lock.set(c, g, val)
                            num += 1
        log.append(('PreLock', num))
        if v['pre_lock']:
            for g in range(up.grid_y, 0, -1):
                for c in range(1, NX - 2):
                    if g < acl:
                        val = f32(up.get(c, g) + 2.5)
                        if lock.get(c, g) < val:
                            lock.set(c, g, val)
                            num += 10
        log.append(('PostLock', num))
        if v['post_lock']:
            for g in range(1, gears + 1):
                for c in range(1, NX - 2):
                    if g > acl:
                        val = f32(lock.get(c, g) + 1.0)
                        if up.get(c, g - 1) < val:
                            up.set(c, g - 1, val)
                            num += 100
        log.append(('Unlock->D', num))
        for g in range(unlock.grid_y, 0, -1):
            for c in range(1, NX - 2):
                if g > acl:
                    val = f32(unlock.get(c, g) + v['unlock_shift_spread'])
                    if v['min_tcc_flag'](c, g) != 1.0 and dn.get(c, g - 1) < val:
                        dn.set(c, g - 1, val)
                        num += 1000
        log.append(('ULckStay', num))
        if v['unlock_stay']:
            for g in range(unlock.grid_y, 1, -1):
                for c in range(1, NX - 2):
                    if unlock.get(c, g) > dn.get(c, g - 1) and lock.get(c, g - 1) < dn.get(c, g - 1):
                        lock.set(c, g - 1, f32(dn.get(c, g - 1) + v['unlock_shift_spread']))
                        num += 10000000
        log.append(('LockUnlock', num))
        if v['lock_unlock']:
            for g in range(lock.grid_y, 0, -1):
                for c in range(1, NX - 2):
                    val = f32(unlock.get(c, g) + v['lock_spread'])
                    if lock.get(c, g) < val:
                        lock.set(c, g, val)
                        num += 10000
        log.append(('UpDown', num))
        if v['up_down']:
            for g in range(up.grid_y, 0, -1):
                for c in range(1, NX + 1):
                    val = f32(dn.get(c, g) + v['shift_spread'])
                    if up.get(c, g) < val:
                        up.set(c, g, val)
                        num += 100000
        log.append(('ShiftMax', num))
        if v['shift_max']:
            for g in range(1, up.grid_y + 1):
                for c in range(1, NX + 1):
                    if up.get(c, g) > speed.get(3, g):
                        up.set(c, g, speed.get(3, g))
                        num += 1000000
            for g in range(1, dn.grid_y + 1):
                for c in range(1, NX + 1):
                    if dn.get(c, g) > speed.get(4, g):
                        dn.set(c, g, speed.get(4, g))
                        num += 1000000
        log.append(('end', num))
        last = num
        if num == 0:
            break
    # BC Trans reports "Data in Logic Error" from the count of the last pass only.
    return passes, last, log


def _wot_lock(v, gears, rpm, speed, up, lock, unlock):
    wot_gear = v['wot_lock_gear']
    wot_rpm = v['wot_lock_rpm']
    stay = v['wot_stay_locked']
    if v['auto_wot']:
        wot_rpm = 1000.0
        stay = False
    for g in range(wot_gear, gears + 1):
        if not v['max_speed_locked']:
            base = speed.get(2, g)
        else:
            base = speed.get(2, g) if g < wot_gear else speed.get(1, g)
        accel = f32(v['rwhp'] * 0.75 * 375.0 / base / v['weight'] * 21.93685)
        for c in range(NX - 2, NX + 1):
            if v['auto_wot']:
                if wot_rpm == 1000.0:
                    wot_rpm = math.floor(rpm[g - 1] * 0.8 / 50.0) * 50.0
                if g > wot_gear and lock.get(c, g) - up.get(NX, g - 1) < 15.0:
                    stay = True
            lock.set(c, g, speed.get(1, g) * (wot_rpm / rpm[g - 1]) - accel * v['tcc_delay'])
            if g > wot_gear and stay:
                lock.set(c, g, up.get(NX, g - 1) - 1.0)
            unlock.set(c, g, lock.get(c, g) * 0.95 - 1.0)
    return wot_rpm, stay


def _extras(v, gears, up, dn, lock, unlock, speed, dis_hi):
    """Option steps after the WOT lock passes (5830-5920 region)."""
    trans = v['trans']
    wot_gear = v['wot_lock_gear']
    if v['wot_tcc_prep'] and wot_gear <= up.grid_y + 1 and wot_gear > 1 and trans >= 3:
        a = wot_gear - 1
        for c in (NX, NX - 1, NX - 2):
            lock.set(c, a, up.get(NX, a) + 2.0)
            unlock.set(c, a, up.get(NX, a) + 1.0)
    if not v['allow_4l60_wot4th'] and trans == 1:
        for c in range(NX, NX - 5, -1):
            up.set(c, 3, dis_hi)
    if v['no_2ct_6l'] and trans >= 3:
        for c in (1, 2, 3):
            dn.set(c, 2, dn.get(c, 1))
    if v['dyno_mode']:
        for g in range(1, dn.grid_y + 1):
            for c in range(2, NX + 1):
                dn.set(c, g, dn.get(1, g))
        for g in range(1, lock.grid_y + 1):
            for c in range(2, NX + 1):
                lock.set(c, g, lock.get(1, g))
                unlock.set(c, g, unlock.get(1, g))
    if v['rrm']:
        for g in range(1, up.grid_y + 1):
            for c in range(1, NX):
                up.set(c, g, up.get(NX, g))
        for g in range(1, dn.grid_y + 1):
            for c in range(1, NX):
                dn.set(c, g, dn.get(NX, g))
        for g in range(1, lock.grid_y + 1):
            for c in range(2, NX + 1):
                lock.set(c, g, lock.get(1, g))
                unlock.set(c, g, unlock.get(1, g))
    if v['sgs']:
        for c in range(1, NX + 1):
            up.set(c, 1, 0.0)
            dn.set(c, 1, 0.0)


def _read_inputs(tune):
    """Read the BTC keys the Calc_Shifts port needs. Missing keys raise ValueError."""
    gears = tune.getint('Gears')
    if gears is None:
        raise ValueError('BTC tune is missing: Gears')
    needed = ['Gear', 'Tire', 'Idle', 'DownRPM', 'Stall', 'Weight', 'RWHP', 'DownTime',
              'TCC_Delay', 'Factor', 'Offset', 'UpFactor', 'DownFactor', 'ShiftSpread',
              'LockSpread', 'ShiftLockSpread', 'UnlockShiftSpread', 'MinLockGear',
              'AccelLockGear', 'WOTLockGear', 'WOTLockRPM', 'Lead', 'AdvancedLead',
              'StallLogic', 'Trans']
    needed += [f'Ratio{i}' for i in range(1, gears + 1)]
    needed += [f'RPM{i}' for i in range(1, gears + 1)]
    needed += [f'Prep{i}' for i in range(1, gears)] + [f'React{i}' for i in range(1, gears)]
    missing = [k for k in needed if tune.get(k) is None]
    if missing:
        raise ValueError('BTC tune is missing: ' + ', '.join(missing))

    def flag(key, default=False):
        raw = tune.get(key)
        return default if raw is None else tune.getint(key) == 1

    min_tcc = Grid(NX, 2 * gears)
    for g in range(1, gears + 1):
        for k in range(1, NX + 1):
            suffix = '' if g == 1 else f'-{g}'
            min_tcc.set(k, 2 * g - 1, tune.getfloat(f'MinTCCRPM{k}{suffix}', 0.0))
            min_tcc.set(k, 2 * g, tune.getfloat(f'TCC_UlckBeforeDown{k}{suffix}', 0.0))

    override = Grid(NX, 2 * (gears - 1))
    override_on = flag('SlopeOverride')
    if override_on:
        for row in range(1, 2 * (gears - 1) + 1):
            for c in range(1, NX + 1):
                override.set(c, row, tune.getfloat(f'SlopeOverride{c}-{row}', 0.0))

    delays = [(tune.getfloat(f'Prep{i}'), tune.getfloat(f'React{i}')) for i in range(1, gears)]
    # BC Trans's TCC_UlckBeforeDown and MinTCC cells are integers in the file.
    return {
        'gears': gears,
        'ratios': [None] + [tune.getfloat(f'Ratio{i}') for i in range(1, gears + 1)],
        'rpm': [tune.getfloat(f'RPM{i}') for i in range(1, gears + 1)],
        'final_drive': tune.getfloat('Gear'),
        'tire': tune.getfloat('Tire'),
        'idle_rpm': tune.getfloat('Idle'),
        'downshift_rpm': tune.getfloat('DownRPM'),
        'stall_rpm': tune.getfloat('Stall'),
        'weight': tune.getfloat('Weight'),
        'rwhp': tune.getfloat('RWHP'),
        'down_time': tune.getfloat('DownTime'),
        'tcc_delay': tune.getfloat('TCC_Delay'),
        'lead_value': tune.getfloat('Lead'),
        'advanced_lead': tune.getint('AdvancedLead'),
        'delays': delays,
        'factor': tune.getfloat('Factor'),
        'offset': tune.getfloat('Offset'),
        'up_firmness': tune.getfloat('UpFactor'),
        'down_firmness': tune.getfloat('DownFactor'),
        'shift_spread': tune.getfloat('ShiftSpread'),
        'lock_spread': tune.getfloat('LockSpread'),
        'lock_shift_spread': tune.getfloat('ShiftLockSpread'),
        'unlock_shift_spread': tune.getfloat('UnlockShiftSpread'),
        'min_lock_gear': tune.getint('MinLockGear'),
        'accel_lock_gear': tune.getint('AccelLockGear'),
        'wot_lock_gear': tune.getint('WOTLockGear'),
        'wot_lock_rpm': tune.getfloat('WOTLockRPM'),
        'wot_stay_locked': flag('WOTStayLocked'),
        'auto_wot': flag('AUTOWOT'),
        'stall_logic': flag('StallLogic'),
        'init_lock': flag('AccelGearLock'),
        'pre_lock': flag('PreAccelGearLock'),
        'post_lock': flag('PostAccelGearLock'),
        'unlock_stay': flag('UnlockStay'),
        'lock_unlock': flag('Lock>Unlock'),
        'up_down': flag('Up>Down'),
        'shift_max': flag('Shift<Max'),
        'max_speed_locked': flag('UseLockedSpeed'),
        'wot_tcc_prep': flag('WOTTCCPrep', True),
        'allow_4l60_wot4th': flag('Allow4L60WOT4th'),
        'no_2ct_6l': flag('No6L_CT2nd'),
        'dyno_mode': flag('DynoMode'),
        'rrm': flag('RollRaceMode'),
        'sgs': flag('SecondGearStart'),
        'trans': tune.getint('Trans'),
        'override_on': override_on,
        'override': override,
        'min_tcc': min_tcc,
        'min_tcc_flag': lambda c, g: min_tcc.get(c, 2 * g),
    }


def calc_shifts_from_file(path):
    """Read a .BTC file and run calc_shifts."""
    return calc_shifts(BtcTune.load(path))
