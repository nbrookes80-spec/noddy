"""Readings that the sensor could not have produced, so the number on the screen is not to be trusted.

A sensor such as the Proflow PFEFI-MAP2 2.7 bar MAP outputs 0.5 V to 4.5 V (owner's sensor, GM reference doc section 2).
The ECU digitises that on an 8-bit scale, so the byte A stands for A * 5 / 255 volts. A byte outside the window means
the wire is open, shorted, or the supply is wrong, not that the boost is that high. The value is still returned, and
the caller shows the note in place of the reading.

Scope: PID 010B only, and only for the 2.7 bar scaling in pid_table. On a stock OS, PID 0B is plain kPa and a byte
above 229 is a real pressure, so this note is only meaningful with the custom-OS scaling that PID 010B assumes.
"""

VOLTS_FULL_SCALE = 5.0
MAP_LOW_VOLTS = 0.5
MAP_HIGH_VOLTS = 4.5


def volts(raw_byte):
    """The voltage the ECU's 8-bit count stands for (0 to 5 V)."""
    return raw_byte * VOLTS_FULL_SCALE / 255.0


def map_27_bar_note(data_hex):
    """The note for a 010B reply's data, or None when its voltage is inside the sensor's 0.5-4.5 V window."""
    if len(data_hex) < 2:
        return None
    v = volts(int(data_hex[:2], 16))
    if v > MAP_HIGH_VOLTS:
        return (f'MAP sensor reads {v:.2f} V, above its 4.5 V limit. Open or shorted to 5 V, or a supply '
                f'fault. The pressure is not valid.')
    if v < MAP_LOW_VOLTS:
        return (f'MAP sensor reads {v:.2f} V, below its 0.5 V limit. Open or shorted to ground. '
                f'The pressure is not valid.')
    return None


WINDOWS = {'010B': map_27_bar_note}


def fault(pid_id, data_hex):
    """A note when the reading is outside its sensor's window, else None. Only PIDs listed in WINDOWS are checked."""
    check = WINDOWS.get(pid_id)
    return check(data_hex) if check else None
