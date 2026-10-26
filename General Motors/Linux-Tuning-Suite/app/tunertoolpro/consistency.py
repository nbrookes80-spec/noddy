"""Checks that the calibration inputs agree with each other and with the ECU limits.

Each rule is plain arithmetic on values the user entered. A finding is advice to check, not a
verdict on the vehicle. Levels: 'error' (inputs contradict each other), 'warn' (likely wrong or
risky), 'info' (a missing value or a note).
"""

from dataclasses import dataclass


@dataclass
class Finding:
    level: str
    field: str
    message: str
    suggestion: object = None  # a value to try, or None

    def as_dict(self):
        return {'level': self.level, 'field': self.field, 'message': self.message,
                'suggestion': self.suggestion}


def check(profile, cfg, transmission_entry=None):
    """profile: VehicleProfile. cfg: Shift Points inputs (dict). transmission_entry: library entry or None."""
    found = []
    redline = profile.redline_rpm
    shift = cfg.get('shift_rpm')
    stall = cfg.get('stall_rpm')
    idle = cfg.get('idle_rpm')
    min_tcc = cfg.get('min_tcc_rpm')
    ratios = cfg.get('ratios') or []

    if redline is None:
        found.append(Finding('info', 'redline_rpm', 'Redline is not entered, so shift RPM cannot be checked against it.'))
    elif shift is not None and shift > redline:
        found.append(Finding('error', 'shift_rpm',
                             f'WOT shift RPM {shift:.0f} is above the redline {redline:.0f}. The engine would be asked to shift past its limit.',
                             suggestion=redline - 300))
    if redline is not None and stall is not None and stall > redline:
        found.append(Finding('error', 'stall_rpm', f'Converter stall {stall:.0f} is above the redline {redline:.0f}.'))
    if idle is not None and stall is not None and stall < idle + 300:
        found.append(Finding('warn', 'stall_rpm',
                             f'Converter stall {stall:.0f} is very close to idle {idle:.0f}. Check the stall figure from the converter data.'))
    if min_tcc is not None and idle is not None and min_tcc < idle:
        found.append(Finding('warn', 'min_tcc_rpm', f'Minimum TCC RPM {min_tcc:.0f} is below idle {idle:.0f}. The converter would lock at idle.',
                             suggestion=idle))
    if min_tcc is not None and shift is not None and min_tcc > shift:
        found.append(Finding('error', 'min_tcc_rpm', f'Minimum TCC RPM {min_tcc:.0f} is above the WOT shift RPM {shift:.0f}.'))

    if any(b >= a for a, b in zip(ratios, ratios[1:])):
        found.append(Finding('error', 'ratios', 'Gear ratios must fall from first to top gear. Check the order.'))

    ecu_torque = profile.ecu_max_torque_lbft
    rated = transmission_entry.get('rated_torque_lbft') if transmission_entry else None
    if ecu_torque is None:
        found.append(Finding('info', 'ecu_max_torque_lbft',
                             'ECU torque limit is not entered. Enter it from the calibration so torque and transmission limits can be compared.'))
    if ecu_torque is not None and rated is not None and ecu_torque > rated:
        found.append(Finding('warn', 'ecu_max_torque_lbft',
                             f'ECU torque limit {ecu_torque:.0f} lb-ft is above the transmission rating {rated:.0f} lb-ft. '
                             'Either the limit or the rating is wrong, or the transmission is not built for this torque.',
                             suggestion=rated))
    if rated is None and transmission_entry is not None:
        found.append(Finding('info', 'rated_torque',
                             'The transmission rated torque is not known for this build, so torque limits cannot be checked against it.'))
    if profile.power_hp and profile.torque_lbft and ecu_torque is not None and profile.torque_lbft > ecu_torque * 1.05:
        found.append(Finding('warn', 'ecu_max_torque_lbft',
                             f'Engine torque {profile.torque_lbft:.0f} lb-ft is more than 5% above the ECU limit {ecu_torque:.0f}. '
                             'The ECU will cut torque; the shift and converter settings were not built for that cut.'))
    if transmission_entry is not None and transmission_entry.get('modified'):
        found.append(Finding('info', 'transmission',
                             'Modified transmission: the kit changes clutch capacity and converter stall. '
                             'Check the rated torque and stall figures with the parts makers before you set limits.'))
    return found
