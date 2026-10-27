"""What a transmission needs besides its gear ratios: shift delays, lead, converter-lock rules and limits.

No Kivy. The values come from two places, and each result says which:

  * Blue Cat Transmission Tool: its Trans_Presets.txt (4L60/65/70, 4L80/85, 6L80/90, 8L90, 10L90) and the
    33 tunes shipped with it (4L60E, 4L70E, 6L80, 8L90). These are the reference.
  * Derived: for a transmission Blue Cat has no data for (Ford, 5L40E, 4T, Allison and so on) the values of the
    Blue Cat class with the same number of gears are used, because the shift logic depends on the gear count.
    These are marked derived and are starting points to check, not measured values.

The torque rating is the one in the shared tuning data, or None when it is not known. It is never guessed.
"""

from dataclasses import dataclass

LEAD_MODE = 'torque'      # every shipped Blue Cat tune uses torque-based lead

# Blue Cat classes: delays (prep, react) per shift, lead, VSS teeth, min TCC rpm, min / accel / WOT lock gear.
_CLASSES = {
    '4L60/65': dict(prep=[0, 0, 0], react=[0.35, 0.4, 0.35], lead=1.0, vss=40, tcc=(1250, 3, 4, 2),
                    source='Blue Cat preset 4L60/65/70 and its 4L60E tunes'),
    '4L70': dict(prep=[0, 0, 0], react=[0, 0, 0], lead=1.0, vss=40, tcc=(1250, 3, 4, 2),
                 source='Blue Cat 4L70E shipped tunes (no delays)'),
    '4L80/85': dict(prep=[0, 0, 0], react=[0.45, 0.45, 0.4], lead=1.0, vss=40, tcc=(1250, 3, 4, 2),
                    source='Blue Cat preset 4L80/85'),
    '6L80/90': dict(prep=[0.45, 0.45, 0.5, 0.45, 0.45], react=[0.15] * 5, lead=2.5, vss=36, tcc=(1250, 3, 3, 3),
                    source='Blue Cat preset 6L80/90 and its 6L80 tunes'),
    '8L90': dict(prep=[0.45, 0.35, 0.4, 0.4, 0.4, 0.4, 0.4], react=[0.15] + [0.1] * 6, lead=2.5, vss=68,
                 tcc=(1250, 3, 3, 3), source='Blue Cat preset 8L90 and its 8L90 tunes'),
    '10L90': dict(prep=[0.45] + [0.4] * 8, react=[0.15] + [0.1] * 8, lead=2.5, vss=68, tcc=(1250, 3, 3, 3),
                  source='Blue Cat preset 10L90'),
}
_BY_CODE = {'4L60E': '4L60/65', '4L65E': '4L60/65', '4L70E': '4L70', '4L80E': '4L80/85', '4L85E': '4L80/85',
            '6L80': '6L80/90', '6L90': '6L80/90', '8L90': '8L90', '10L90': '10L90'}
# Gear count -> the Blue Cat class used when there is no data for the transmission itself.
_BY_GEARS = {4: '4L60/65', 5: '6L80/90', 6: '6L80/90', 7: '8L90', 8: '8L90', 9: '10L90', 10: '10L90'}


@dataclass(frozen=True)
class TransData:
    delays: list
    lead_mode: str
    lead_value: float
    vss: int
    min_tcc_rpm: int
    min_tcc_gear: int
    accel_lock_gear: int
    wot_lock_gear: int
    derived: bool
    source: str
    torque_rating: object = None      # lb-ft, or None when not known


def _torque(name):
    from tunertoolpro.engines import constants
    entry = constants.TRANS_DB.get(name)
    return entry['torque'] if entry else None


def for_transmission(transmission):
    gears = len(transmission.ratios)
    code = transmission.name.split(' ')[0]
    key = _BY_CODE.get(code)
    derived = key is None
    if derived:
        key = _BY_GEARS.get(gears, '6L80/90')
    spec = _CLASSES[key]
    shifts = gears - 1
    prep = (spec['prep'] + [spec['prep'][-1]] * shifts)[:shifts]
    react = (spec['react'] + [spec['react'][-1]] * shifts)[:shifts]
    tcc, min_gear, accel_gear, wot_gear = spec['tcc']
    source = spec['source']
    if derived:
        source = f'Derived from the {gears}-gear Blue Cat class ({key}); check against your transmission'
    return TransData(list(zip(prep, react)), LEAD_MODE, spec['lead'], spec['vss'], tcc,
                     min(min_gear, gears), min(accel_gear, gears), min(wot_gear, gears), derived, source,
                     _torque(transmission.name))


def apply(values, data):
    """A copy of the typed values with this transmission's lock and lead settings. The car's own values
    (tyres, axle, weight, power, engine speeds) are left alone."""
    out = dict(values)
    out.update(min_tcc_rpm=str(data.min_tcc_rpm), min_tcc_gear=str(data.min_tcc_gear),
               accel_lock_gear=str(data.accel_lock_gear), wot_lock_gear=str(data.wot_lock_gear),
               lead_value=f'{data.lead_value:g}')
    return out


def summary(data):
    """Plain words for the Settings screen."""
    delays = ', '.join(f'{p:g}/{r:g}' for p, r in data.delays)
    rating = f'{data.torque_rating} lb-ft rated. ' if data.torque_rating else 'Torque rating not known. '
    return (f'Shift delays prep/react (s): {delays}.\nLead {data.lead_value:g} ({data.lead_mode}), converter lock from '
            f'{data.min_tcc_rpm} rpm, minimum / accelerator / WOT lock gear {data.min_tcc_gear}/'
            f'{data.accel_lock_gear}/{data.wot_lock_gear}. {rating}\nSource: {data.source}.')
