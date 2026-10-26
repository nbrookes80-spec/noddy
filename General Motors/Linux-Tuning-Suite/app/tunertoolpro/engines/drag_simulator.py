"""DragSimulator: Newton-integration vehicle dynamics for a drag run.

Transcribed by hand from the CPython 3.12 disassembly of the original
DragSimulator class (recovered/6l80e-python-disasm/01863..01960). Status:
transcribed, NOT yet differentially verified.

Forces:
  F_drive = engine_tq x ratio x final_drive x eta / r_tire
  F_aero  = 0.5 x rho x Cd*A x v^2
  F_roll  = Crr x W
  a       = (F_drive - F_aero - F_roll) x g / W

Launch: the engine sits at stall_rpm x LAUNCH_FACTOR until vehicle speed
catches up to the rigid-coupling RPM. Shifts interrupt torque for a time
given by _shift_time_for.

Notes on the original: simulate() assigns `last_rpm` and `post_shift_clamp`
but never reads them, so they are not reproduced here.
"""

GRAVITY = 32.174
AIR_DENSITY = 0.00237
DRIVETRAIN_EFF = 0.85
SHIFT_TIME = 0.4
LAUNCH_FACTOR = 0.7

MPH_K = 336.13  # same constant as calc_engine.MPH_K

GEAR_SLIP_PCT = [0.035, 0.018, 0.01, 0.005, 0.003, 0.002, 0.001, 0.001, 0.001, 0.001]


class DragSimulator:
    GRAVITY = GRAVITY
    AIR_DENSITY = AIR_DENSITY
    DRIVETRAIN_EFF = DRIVETRAIN_EFF
    SHIFT_TIME = SHIFT_TIME
    LAUNCH_FACTOR = LAUNCH_FACTOR
    GEAR_SLIP_PCT = GEAR_SLIP_PCT

    def __init__(self, cfg, shift_points_mph=None, cda=9.0, crr=0.012,
                 launch_grip_g=1.1, drivetrain_eff=None):
        # __init__.dis 1883
        self.curve = cfg.get('torque_curve')
        self.ratios = cfg['ratios']
        self.final_drive = cfg['axle'] * cfg['chain']
        self.tire_dia = cfg['tire_dia']
        self.weight = cfg['weight']
        self.stall_rpm = cfg['stall_rpm']
        self.idle_rpm = cfg['idle_rpm']
        global_rpm = cfg['shift_rpm']
        per_gear = cfg.get('per_gear_rpm') or []
        self.shift_rpm_per_gear = [
            per_gear[i] if i < len(per_gear) else global_rpm
            for i in range(len(self.ratios))
        ]
        self.shift_points_mph = shift_points_mph or []
        self.cda = cda
        self.crr = crr
        self.launch_grip_g = launch_grip_g
        if drivetrain_eff is None:
            # Default eta by gear count: <=4 gears 0.82, >=8 gears 0.86, else 0.85.
            n_gears = len(self.ratios)
            if n_gears <= 4:
                self.drivetrain_eff = 0.82
            elif n_gears >= 8:
                self.drivetrain_eff = 0.86
            else:
                self.drivetrain_eff = 0.85
        else:
            self.drivetrain_eff = drivetrain_eff

    def _slip_for_gear(self, gear_idx):
        # _slip_for_gear.dis 1931
        if gear_idx >= len(self.GEAR_SLIP_PCT):
            return self.GEAR_SLIP_PCT[-1]
        return self.GEAR_SLIP_PCT[gear_idx]

    def _shift_time_for(self, gear_idx, torque_load_frac):
        # _shift_time_for.dis 1938
        n = len(self.ratios)
        gear_frac = gear_idx / max(1, n - 1)
        base = 0.55 - 0.2 * gear_frac
        return base * (0.4 + 0.6 * torque_load_frac)

    def mph_to_rpm(self, mph, gear_idx):
        # mph_to_rpm.dis 1954
        return mph * self.final_drive * self.ratios[gear_idx] * MPH_K / self.tire_dia

    def rpm_to_mph(self, rpm, gear_idx):
        # rpm_to_mph.dis 1957
        return rpm * self.tire_dia / (self.final_drive * self.ratios[gear_idx] * MPH_K)

    def simulate(self, max_time=25.0, dt=0.02, max_distance_ft=1320):
        # simulate.dis 1960
        if self.curve is None or self.curve.is_empty:
            return None

        t = 0.0
        v = 0.0
        distance_ft = 0.0
        gear = 0
        shift_timer = 0.0

        trace_t, trace_v, trace_rpm, trace_gear, trace_dist = [], [], [], [], []
        shift_events = []
        results = {
            't_0_30': None, 't_0_60': None, 't_0_100': None, 't_0_120': None,
            't_eighth': None, 'v_eighth': None, 't_quarter': None, 'v_quarter': None,
        }
        max_v = 0.0

        while t < max_time:
            coupled_rpm = self.mph_to_rpm(v, gear)
            stall_couple_mph = self.rpm_to_mph(self.stall_rpm, gear)
            if v < stall_couple_mph and gear == 0:
                launch_rpm = self.stall_rpm * self.LAUNCH_FACTOR
                rpm = launch_rpm + (self.stall_rpm - self.stall_rpm * self.LAUNCH_FACTOR) * (
                    v / max(stall_couple_mph, 1.0))
            else:
                rpm = max(coupled_rpm, self.idle_rpm)

            if shift_timer > 0:
                engine_tq = 0.0
                shift_timer -= dt
            else:
                engine_tq = self.curve.tq_at(rpm)

            r_tire_ft = self.tire_dia / 24.0
            slip_factor = 1.0 - self._slip_for_gear(gear)
            wheel_tq_ftlb = (engine_tq * self.ratios[gear] * self.final_drive
                             * self.drivetrain_eff * slip_factor)
            f_drive = wheel_tq_ftlb / r_tire_ft

            v_fps = v * 1.467
            f_aero = 0.5 * self.AIR_DENSITY * self.cda * v_fps * v_fps
            f_roll = self.crr * self.weight
            f_net = f_drive - f_aero - f_roll

            a_fps2 = f_net * self.GRAVITY / self.weight
            traction_cap_fps2 = self.launch_grip_g * self.GRAVITY
            if a_fps2 > traction_cap_fps2:
                a_fps2 = traction_cap_fps2

            v_fps_new = max(0.0, v_fps + a_fps2 * dt)
            v_new = v_fps_new / 1.467
            distance_ft += 0.5 * (v_fps + v_fps_new) * dt

            if results['t_0_30'] is None and v_new >= 30:
                results['t_0_30'] = t
            if results['t_0_60'] is None and v_new >= 60:
                results['t_0_60'] = t
            if results['t_0_100'] is None and v_new >= 100:
                results['t_0_100'] = t
            if results['t_0_120'] is None and v_new >= 120:
                results['t_0_120'] = t
            if results['t_eighth'] is None and distance_ft >= 660:
                results['t_eighth'] = t
                results['v_eighth'] = v_new
            if results['t_quarter'] is None and distance_ft >= 1320:
                results['t_quarter'] = t
                results['v_quarter'] = v_new

            if shift_timer <= 0 and gear < len(self.ratios) - 1 \
                    and rpm >= self.shift_rpm_per_gear[gear]:
                pre_rpm = rpm
                new_gear = gear + 1
                post_rpm = self.mph_to_rpm(v_new, new_gear)
                shift_events.append({
                    't': t,
                    'shift_name': f'{gear + 1}→{new_gear + 1}',
                    'mph_init': v_new,
                    'rpm_init': pre_rpm,
                    'rpm_post': post_rpm,
                })
                gear = new_gear
                shift_timer = self._shift_time_for(gear - 1, 1.0)

            if not trace_t or t - trace_t[-1] >= 0.05:
                trace_t.append(t)
                trace_v.append(v)
                trace_rpm.append(rpm)
                trace_gear.append(gear + 1)
                trace_dist.append(distance_ft)

            t += dt
            v = v_new
            max_v = max(max_v, v)

            if results['t_quarter'] is not None and t > results['t_quarter'] + 1.0:
                break
            elif v_new < 0.1 and t > 1.0:
                break
            elif distance_ft >= max_distance_ft and v_new < 200:
                break

        results['trace_t'] = trace_t
        results['trace_v'] = trace_v
        results['trace_rpm'] = trace_rpm
        results['trace_gear'] = trace_gear
        results['trace_dist'] = trace_dist
        results['shift_events'] = shift_events
        results['max_v'] = max_v
        return results
