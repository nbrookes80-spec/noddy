"""PressureEngine: shift, TCC apply, coast and garage pressure tables.

Transcribed by hand from the CPython 3.12 disassembly of the original
PressureEngine class (recovered/6l80e-python-disasm/058xx..0628x). Every
function names the disassembly file it was read from. Status: transcribed,
NOT yet differentially verified (the original module must not be executed
without approval; see README.md).

Constants come from constants.py, which holds exact copies of the original
module-level data.
"""

from constants import (
    BRAKE_SHIFT_4SPD_MAX_PSI,
    BRAKE_SHIFT_4SPD_SHIFTS,
    BRAKE_SHIFT_4SPD_TORQUE_COLS,
    BRAKE_SHIFT_INTENTS_4SPD,
    COAST_PRESSURE_INTENTS,
    COLD_PRELOAD_FACTOR,
    FORCE_MOTOR_MAX_MA,
    FORCE_MOTOR_MIN_MA,
    FORCE_MOTOR_PSI_COLS,
    FORCE_MOTOR_TEMP_ROWS,
    GARAGE_SHIFT_INTENTS,
    GARAGE_SHIFT_TEMP_MULT,
    MAX_COAST_PRESSURE_PSI,
    MAX_GARAGE_SHIFT_PSI,
    MAX_PRESSURE_PSI,
    MAX_TCC_APPLY_PSI,
    PRESSURE_4SPD_MAX_PSI,
    PRESSURE_4SPD_SHIFTS,
    PRESSURE_4SPD_TORQUE_COLS,
    PRESSURE_INTENTS,
    PRESSURE_INTENTS_4SPD,
    PRESSURE_TEMP_ROWS,
    PRESSURE_TORQUE_PCT,
    SHIFT_PRESSURE_MULT,
    TCC_APPLY_INTENTS,
    TCC_RAMP_ERAS,
)


def _psi_table(intent, max_torque, cap, shift_mult=1.0):
    """2-D table: PRESSURE_TEMP_ROWS x torque_cols(max_torque).

    Shared by base_shift_pressure, tcc_apply_pressure and coast_pressure.
    (base.dis 5826-5868; tcc and coast use the same loop body with
    shift_mult = 1.0, which is exact in floating point.)
    """
    base = intent['base_psi'] * shift_mult
    peak = intent['max_psi'] * shift_mult
    cold_preload = intent['cold_preload'] * shift_mult
    hot_scale = intent['hot_scale']
    curve = intent['torque_curve']
    cols = PressureEngine.torque_cols(max_torque)
    rows = []
    for temp in PRESSURE_TEMP_ROWS:
        cold_factor = COLD_PRELOAD_FACTOR.get(temp, 0.0)
        hot_dev = max(0.0, min(1.0, (temp - 68) / 189)) * 0.18
        hot_mult = 1.0 + hot_dev * hot_scale
        row = []
        for tq in cols:
            t_norm = min(1.0, tq / max(1.0, float(max_torque)))
            torque_psi = base + (peak - base) * t_norm ** curve
            cold_add = cold_preload * cold_factor * (1.0 - 0.82 * t_norm)
            psi = (torque_psi + cold_add) * hot_mult
            row.append(min(psi, cap))
        rows.append(row)
    return rows


def _tcc_ramp_07_14(torque_rows, slip_cols, intent_mult, cap):
    """Ramp table for the 2007-2010 and 2011-2014 eras (_tcc_ramp_07_14.dis 5955)."""
    out = []
    for tq in torque_rows:
        tq_norm = max(0.0, min(1.0, tq / 368.8))
        r = []
        for slip in slip_cols:
            if slip <= -25:
                if tq < 0:
                    val = 17.0 * (1.0 + (slip + 25) * 0.04) * intent_mult
                else:
                    if tq < 5:
                        spike_30 = cap
                        spike_25 = cap * 0.25
                    elif tq < 100:
                        spike_30 = cap
                        spike_25 = cap * 0.6
                    else:
                        spike_30 = 60.0 + tq_norm * 8.0
                        spike_25 = 65.0
                    if slip <= -30:
                        val = spike_30
                    else:
                        f = (slip + 30) / 5.0
                        val = spike_30 + f * (spike_25 - spike_30)
                    val *= intent_mult
                r.append(round(min(val, cap), 2))
            elif slip <= -20:
                if tq < 0:
                    val = 14.0
                elif tq < 100:
                    val = 17.0 + tq_norm * 19.0
                else:
                    val = 18.5
                r.append(round(val * intent_mult, 2))
            elif slip <= -15:
                if tq < 0:
                    val = 1.9
                elif tq < 100:
                    val = 2.5 + tq_norm * 1.0
                else:
                    val = 3.5 + tq_norm * 0.5
                band_pos = (slip + 20) / 5.0
                val = val * (1.0 - 0.2 * band_pos)
                r.append(round(val * intent_mult, 2))
            elif slip <= -2:
                val = 0.4 + (slip + 15) / 13.0 * 1.6
                val = max(0.2, 2.0 - val)
                r.append(round(val * intent_mult, 2))
            elif slip <= 0:
                val = 0.15 + (slip + 2) * 0.05
                r.append(round(val * intent_mult, 2))
            elif slip <= 30:
                pos = slip / 30.0
                val = 0.15 + pos * 1.6
                r.append(round(val * intent_mult * (0.9 + 0.3 * tq_norm), 2))
            else:
                slip_norm = (slip - 30) / 220.0
                val = 2.0 + slip_norm * (10.0 + 35.0 * tq_norm)
                r.append(round(min(val * intent_mult, cap), 2))
        out.append(r)
    return out


def _tcc_ramp_15_plus(rpm_rows, slip_cols, intent_mult, cap):
    """Ramp table for the 2015+ era, indexed by RPM (_tcc_ramp_15_plus.dis 6046)."""
    out = []
    for rpm in rpm_rows:
        rpm_norm = max(0.0, min(1.0, (rpm - 800) / 5200))
        r = []
        for slip in slip_cols:
            if slip < 0:
                neg = abs(slip) / 40.0
                val = (1.5 + 5.0 * rpm_norm) * (1.0 + 6.5 * neg) * intent_mult
                val *= neg ** 0.7
                r.append(round(min(val, cap), 2))
            elif slip == 0:
                val = 0.0 + rpm_norm * 2.0 * intent_mult
                r.append(round(val, 2))
            else:
                pos = slip / 400.0
                val = (0.3 + 5.0 * rpm_norm) * pos ** 0.55 * (1.0 + 4.0 * pos)
                val *= intent_mult
                r.append(round(min(val, cap), 2))
        out.append(r)
    return out


def _tcc_ramp_shudder_fix(rows, slip_cols, cap, row_axis, intent_max_psi):
    """'Shudder Fix' ramp (_tcc_ramp_shudder_fix.dis 6071)."""
    plateau = 65.0 if intent_max_psi <= 148 else 65.0 + (intent_max_psi - 148) / 47.0 * 45.0
    plateau = min(plateau, cap * 0.85)
    max_at_corner = min(intent_max_psi * 0.95, cap)
    if row_axis == 'rpm':
        plateau = 30.0 if intent_max_psi <= 148 else 30.0 + (intent_max_psi - 148) * 0.6
        max_at_corner = min(intent_max_psi * 0.5, cap)
    out = []
    for row in rows:
        if row_axis == 'torque':
            row_norm = max(0.0, min(1.0, row / 368.8))
        else:
            row_norm = max(0.0, min(1.0, (row - 800) / 5200.0))
        r = []
        for slip in slip_cols:
            if slip < 0:
                neg = abs(slip) / 40.0
                relief = (0.04 + 10.0 * neg ** 1.5) * (0.5 + 0.5 * row_norm)
                r.append(round(relief, 2))
            elif slip <= 60:
                r.append(round(plateau, 2))
            else:
                slip_norm = (slip - 60) / max(1, slip_cols[-1] - 60)
                ramp = plateau + (max_at_corner - plateau) * row_norm * slip_norm ** 1.05
                r.append(round(min(ramp, cap), 2))
        out.append(r)
    return out


class PressureEngine:
    """Pressure tables for the 6L80E. All methods are static, as in the original."""

    @staticmethod
    def torque_cols(max_torque):
        # torque_cols.dis 5821
        return [int(round(max_torque * p)) for p in PRESSURE_TORQUE_PCT]

    @staticmethod
    def base_shift_pressure(intent_name, max_torque, shift_name, max_pressure_psi):
        # base_shift_pressure.dis 5826
        intent = PRESSURE_INTENTS.get(intent_name, PRESSURE_INTENTS['Daily'])
        shift_mult = SHIFT_PRESSURE_MULT.get(shift_name, 1.0)
        cap = max_pressure_psi if max_pressure_psi is not None else MAX_PRESSURE_PSI
        return _psi_table(intent, max_torque, cap, shift_mult)

    @staticmethod
    def tcc_apply_pressure(intent_name, max_torque, max_pressure_psi):
        # tcc_apply_pressure.dis 5874
        intent = TCC_APPLY_INTENTS.get(intent_name, TCC_APPLY_INTENTS['Daily'])
        cap = max_pressure_psi if max_pressure_psi is not None else MAX_TCC_APPLY_PSI
        return _psi_table(intent, max_torque, cap)

    @staticmethod
    def coast_pressure(intent_name, max_torque, max_pressure_psi):
        # coast_pressure.dis 6135
        intent = COAST_PRESSURE_INTENTS.get(intent_name, COAST_PRESSURE_INTENTS['Daily'])
        cap = max_pressure_psi if max_pressure_psi is not None else MAX_COAST_PRESSURE_PSI
        return _psi_table(intent, max_torque, cap)

    @staticmethod
    def tcc_apply_pressure_ramp(intent_name, era, max_torque):
        # tcc_apply_pressure_ramp.dis 5918
        # max_torque is accepted for signature compatibility; the disassembly
        # does not read it.
        if era not in TCC_RAMP_ERAS:
            era = '2015+'
        cfg = TCC_RAMP_ERAS[era]
        slip_cols = cfg['slip_cols']
        cap = cfg.get('max_psi', MAX_TCC_APPLY_PSI)
        intent = TCC_APPLY_INTENTS.get(intent_name, TCC_APPLY_INTENTS['Daily'])
        intent_mult = intent['max_psi'] / 110.0
        if intent_name == 'Shudder Fix':
            rows = cfg.get('torque_rows') or cfg['rpm_rows']
            return _tcc_ramp_shudder_fix(rows, slip_cols, cap, cfg['row_axis'], intent['max_psi'])
        if era == '2015+':
            return _tcc_ramp_15_plus(cfg['rpm_rows'], slip_cols, intent_mult, cap)
        return _tcc_ramp_07_14(cfg['torque_rows'], slip_cols, intent_mult, cap)

    @staticmethod
    def garage_shift_pressure(intent_name):
        # garage_shift_pressure.dis 6179 (no rounding in the original)
        intent = GARAGE_SHIFT_INTENTS.get(intent_name, GARAGE_SHIFT_INTENTS['Daily'])
        out = {}
        for direction in ('PD', 'PR', 'ND', 'NR'):
            base_psi = intent[direction]
            out[direction] = [
                min(base_psi * GARAGE_SHIFT_TEMP_MULT.get(temp, 1.0), MAX_GARAGE_SHIFT_PSI)
                for temp in PRESSURE_TEMP_ROWS
            ]
        return out

    @staticmethod
    def base_shift_pressure_4spd(intent_name):
        # base_shift_pressure_4spd.dis 6206
        intent = PRESSURE_INTENTS_4SPD.get(intent_name, PRESSURE_INTENTS_4SPD['Normal'])
        max_torque = float(PRESSURE_4SPD_TORQUE_COLS[-1])
        rows = []
        for shift in PRESSURE_4SPD_SHIFTS:
            p = intent[shift]
            base = p['base']
            peak = p['max_psi']
            curve = p['curve']
            thresh = p['threshold']
            row = []
            for tq in PRESSURE_4SPD_TORQUE_COLS:
                if tq <= thresh:
                    row.append(base)
                    continue
                t_norm = (tq - thresh) / max(1.0, max_torque - thresh)
                t_norm = min(1.0, t_norm)
                psi = base + (peak - base) * t_norm ** curve
                row.append(min(psi, PRESSURE_4SPD_MAX_PSI))
            rows.append(row)
        return rows

    @staticmethod
    def brake_shift_pressure_4spd(intent_name):
        # brake_shift_pressure_4spd.dis 6242
        intent = BRAKE_SHIFT_INTENTS_4SPD.get(intent_name, BRAKE_SHIFT_INTENTS_4SPD['Normal'])
        cap = BRAKE_SHIFT_4SPD_MAX_PSI
        range_top = BRAKE_SHIFT_4SPD_TORQUE_COLS[-1]
        out = []
        for shift in BRAKE_SHIFT_4SPD_SHIFTS:
            p = intent[shift]
            base_high = p['base_high']
            valley = p['valley_psi']
            center = p['valley_center']
            high_end = p['high_end_psi']
            row = []
            for tq in BRAKE_SHIFT_4SPD_TORQUE_COLS:
                if tq <= 60:
                    val = base_high
                elif tq < center:
                    f = (tq - 60) / max(1.0, center - 60)
                    val = base_high + (valley - base_high) * f
                elif tq < center + 100:
                    val = valley
                else:
                    f = (tq - (center + 100)) / max(1.0, range_top - (center + 100))
                    val = valley + (high_end - valley) * f
                row.append(round(min(val, cap), 0))
            out.append(row)
        return out

    @staticmethod
    def force_motor_current():
        # force_motor_current.dis 6284 (rows: FORCE_MOTOR_TEMP_ROWS x FORCE_MOTOR_PSI_COLS)
        out = []
        psi_full = FORCE_MOTOR_PSI_COLS[-1]
        for temp in FORCE_MOTOR_TEMP_ROWS:
            temp_norm = (temp + 40) / 346
            row = []
            for psi in FORCE_MOTOR_PSI_COLS:
                psi_norm = psi / psi_full
                base_ma = FORCE_MOTOR_MAX_MA - (FORCE_MOTOR_MAX_MA - FORCE_MOTOR_MIN_MA) * psi_norm
                mid_factor = 4.0 * psi_norm * (1.0 - psi_norm)
                temp_adjust = (1.0 - temp_norm) * 30 - temp_norm * 50
                ma = base_ma + temp_adjust * mid_factor
                ma = max(FORCE_MOTOR_MIN_MA, min(FORCE_MOTOR_MAX_MA, ma))
                row.append(round(ma, 0))
            out.append(row)
        return out
