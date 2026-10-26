"""Shift-speed math as implemented by BC_Trans (Calc_Shifts).

The original uses the literal 3.14 for pi. The port keeps that constant so the
numbers match the original output exactly. CalcEngine uses the exact value of
pi through its MPH_K constant, so the two differ by about 0.05%.
"""

BCT_PI = 3.14


def speed_mph(rpm, ratio, final_drive, tire_dia):
    """Vehicle speed in MPH at an engine RPM in a given gear."""
    return rpm / (ratio * final_drive) * (tire_dia * BCT_PI) * 60.0 / 12.0 / 5280.0


def rpm_for_speed(mph, ratio, final_drive, tire_dia):
    """Inverse of speed_mph."""
    return mph * ratio * final_drive * 12.0 * 5280.0 / (tire_dia * BCT_PI * 60.0)


def stall_slip(stall_rpm):
    """Torque-converter slip fraction at stall, (stall/1000)^1.7 / 100."""
    return (stall_rpm / 1000.0) ** 1.7 / 100.0


def gear_speed_table(tune, rpm_values):
    """Rows of MPH per gear for each RPM in rpm_values, from a BtcTune."""
    final_drive = tune.getfloat('Gear')
    tire = tune.getfloat('Tire')
    ratios = tune.ratios()
    if None in ratios or final_drive is None or tire is None:
        raise ValueError('tune is missing ratio, final drive or tire data')
    return [[speed_mph(rpm, r, final_drive, tire) for r in ratios] for rpm in rpm_values]
