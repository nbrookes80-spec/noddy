"""ShiftTimeEngine: desired shift-time tables for 4-speed transmissions.

Transcribed by hand from the CPython 3.12 disassembly of the original class
(recovered/6l80e-python-disasm/06308..06333). Status: transcribed, NOT yet
differentially verified (see README.md: the original must not be executed
without approval).

Output: 2D list [3 shifts][17 torque cols] of seconds.
"""

from .constants import (
    SHIFT_TIME_INTENTS_4SPD,
    SHIFT_TIME_SHIFTS,
    SHIFT_TIME_TORQUE_COLS,
)


class ShiftTimeEngine:
    @staticmethod
    def desired_shift_time_4spd(intent_name):
        # desired_shift_time_4spd.dis 6312..6333
        intent = SHIFT_TIME_INTENTS_4SPD.get(intent_name, SHIFT_TIME_INTENTS_4SPD['Normal'])
        max_torque = float(SHIFT_TIME_TORQUE_COLS[-1])
        rows = []
        for shift in SHIFT_TIME_SHIFTS:
            p = intent[shift]
            t_max = p['max_s']
            t_min = p['min_s']
            curve = p['curve']
            row = []
            for tq in SHIFT_TIME_TORQUE_COLS:
                if t_max == 0 and t_min == 0:
                    row.append(0.0)
                    continue
                t_norm = min(1.0, tq / max_torque)
                sec = t_max - (t_max - t_min) * t_norm ** curve
                row.append(max(t_min, sec))
            rows.append(row)
        return rows
