"""TCCDutyEngine: default TCC duty-cycle maximum table.

Transcribed by hand from the CPython 3.12 disassembly of the original class
(recovered/6l80e-python-disasm/06341..06372). Status: transcribed, NOT yet
differentially verified (see README.md: the original must not be executed
without approval).

Output: 2D list [5 temp rows][17 line PSI cols] of % duty cycle, clamped to
[90, 98].
"""

from .constants import TCC_DC_LINE_PSI_COLS, TCC_DC_TEMP_ROWS


class TCCDutyEngine:
    @staticmethod
    def max_duty_cycle():
        # max_duty_cycle.dis 6350..6372
        base = 97.0
        rows = []
        for temp in TCC_DC_TEMP_ROWS:
            temp_norm = (temp - 32) / 238
            row_offset = -1.0 * temp_norm
            row = []
            for psi in TCC_DC_LINE_PSI_COLS:
                psi_norm = min(1.0, psi / 60.0)
                pressure_offset = -1.5 * (1.0 - psi_norm)
                mid_dip = 0.0
                if temp >= 151:
                    psi_frac = psi / 96.0
                    if 0.25 < psi_frac < 0.65:
                        mid_dip = -0.5 * temp_norm
                duty = base + row_offset + pressure_offset + mid_dip
                row.append(max(90.0, min(98.0, duty)))
            rows.append(row)
        return rows
