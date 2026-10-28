"""Torque converter types and differential ratios, and how they change the calculated shift settings.

The shift calculation (Blue Cat style) already uses the stall speed, the minimum TCC RPM and gear, and
the accelerator and WOT lock gears. This module chooses sensible values for those inputs from the kind
of converter that is fitted, and lists the TCM-side settings (TCC slip, apply/release, torque
management) that the app cannot calculate but that must change with the converter.

Where a rule comes from is tagged on every note:
  [blog]    VCM Performance, "Basic 6L80e/6L90e tuning guide"
  [video1]  HP Tuners/Blue Cat 6L80 tuning video (youtu.be/4SmhtMQMvRA)
  [video2]  HP Tuners shift-timing "inertia factor" addendum (youtu.be/6VNwM7TRD2E)
  [bct]     Blue Cat Transmission Tool behaviour, from the reverse-engineered Calc_Shifts
  [start]   a starting point chosen here. It is not from a published source, so check it on the car.
"""

from math import pi

STOCK = 'stock'
MILD = 'mild'
HIGH = 'high'
TRIPLE = 'triple'
OTHER = 'other'

# key -> (label, one-line description)
TYPES = {
    STOCK: ('Stock', 'Factory converter, factory lockup clutch.'),
    MILD: ('Mild stall, single plate', 'Slightly looser converter (about 2400 to 2800 stall), single-plate lockup.'),
    HIGH: ('High stall, single plate', 'Looser converter (about 2800 and up), single-plate lockup.'),
    TRIPLE: ('High stall, triple plate', 'Billet or race converter with a triple-plate lockup clutch.'),
    OTHER: ('Other / custom', 'Anything else. Enter the stall and the app treats it by that figure.'),
}

# Stall figures the form accepts (Shift tab limits).
STALL_MIN, STALL_MAX = 1000, 4500
MIN_TCC_LIMITS = (800, 3000)

# What the Blue Cat base tunes change for a high-stall converter, against the same cam with a stock
# converter (docs/research/base-tcm-and-converters.md, A.2/A.3). These are the full steps. The vendor
# changes stall, idle, shift RPM and the minimum lock RPM. It does not change the lock gears, the
# spreads, the lead or the prep/react times, so neither does this module.
FULL_STEP = {'idle_rpm': 100, 'shift_rpm': 200}
MIN_LOCK_STEP = {'few_gears': 100, 'many_gears': 200}   # 4-speed, then 5 gears and up
# Share of the full step for each type. Other/custom is worked out from the stall figure.
SHARE = {STOCK: 0.0, MILD: 0.5, HIGH: 1.0, TRIPLE: 1.0}
FULL_STALL_STEP = 1200   # the vendor's high-stall tunes sit 1000 to 1400 above the stock-converter ones


def type_keys():
    return list(TYPES)


def label(key):
    return TYPES[key][0]


def key_for_label(text):
    for key, (name, _) in TYPES.items():
        if name == text:
            return key
    raise KeyError(text)


def classify(stall_rpm, base_stall):
    """Best guess at the type from the stall figure alone, for a loaded tune with no converter noted."""
    if stall_rpm <= base_stall + 250:
        return STOCK
    if stall_rpm < base_stall + 700:
        return MILD
    return HIGH


def adjust(values, key, stall_rpm=None, base=None, n_gears=6):
    """New calculation inputs for a converter type.

    values: the current form values (stall_rpm, idle_rpm, shift_rpm, min_tcc_rpm).
    key: one of TYPES.
    stall_rpm: the converter's true flash stall, when the user knows it.
    base: the stock-converter values to start from, so choosing a type twice does not stack.
    Returns (changes, stall_lock_logic, notes). changes holds the fields that move.
    """
    if key not in TYPES:
        raise KeyError(key)
    start = dict(base or values)
    fields = ('stall_rpm', 'idle_rpm', 'shift_rpm', 'min_tcc_rpm')
    stall = int(round(stall_rpm)) if stall_rpm else int(start['stall_rpm'])
    stall = max(STALL_MIN, min(STALL_MAX, stall))
    notes = []

    if key == STOCK:
        changes = {k: start[k] for k in fields if k in start}
        if stall_rpm:
            changes['stall_rpm'] = stall
        notes.append('[blog] Stock converter: leave the shift-timing transition times alone. '
                     'They were built for this converter.')
        return changes, False, notes

    if key == OTHER:
        share = max(0.0, min(1.0, (stall - start['stall_rpm']) / FULL_STALL_STEP))
    else:
        share = SHARE[key]
        if not stall_rpm:   # no figure given: use a typical one so the stall slip moves with the type
            stall = max(stall, int(start['stall_rpm'] + FULL_STALL_STEP * share))
            stall = min(STALL_MAX, stall)
    lo, hi = MIN_TCC_LIMITS
    lock_step = MIN_LOCK_STEP['few_gears' if n_gears <= 4 else 'many_gears']
    changes = {
        'stall_rpm': stall,
        'idle_rpm': int(round(start['idle_rpm'] + FULL_STEP['idle_rpm'] * share, -1)),
        'shift_rpm': int(round(start['shift_rpm'] + FULL_STEP['shift_rpm'] * share, -1)),
        'min_tcc_rpm': int(max(lo, min(hi, round(start['min_tcc_rpm'] + lock_step * share, -1)))),
    }
    notes.append(f'[bct] Blue Cat base tunes for high-stall builds: stall +1000 to +1400, idle +50 to +100, '
                 f'shift RPM +100 to +300 and minimum lock RPM +{lock_step} on this gear count. '
                 f'Applied at {int(round(share * 100))}% of that step.')
    notes.append(f'[bct] Stall {stall} rpm sets the converter slip used for the lock speeds, '
                 f'(stall/1000)^1.7 / 100 = {(stall / 1000.0) ** 1.7 / 100.0:.3f}. '
                 'Enter the true flash stall (WOT, output stopped), not the maker\'s rating.')
    notes.append('[bct] The vendor leaves the lock gears, spreads, lead and prep/react unchanged for a '
                 'converter swap, so they are not changed here.')
    notes.append('[bct] Stall logic is switched on: it lowers throttle before locking to avoid a harsh lockup '
                 'when the engine and turbine speeds are far apart.')
    if key == TRIPLE:
        notes.append('[start] No published data separates triple-plate from single-plate calibrations, so the '
                     'calculated numbers match a single-plate high-stall converter. Only the TCM advice differs.')
    return changes, True, notes


def tcm_advice(key):
    """Settings the app cannot calculate but that go with this converter. Returns a list of tagged lines."""
    if key == STOCK:
        return ['[blog] Torque management: leave it on. Rebuilders usually only warrant a unit that has it on.']
    lines = [
        '[blog] Transmission > Torque Converter > General > TCC Desired Slip: set every A/C Off gear to 0, '
        'set Use DoD Slip to Disabled, and set the DoD gears to 0. The factory slip targets assume the '
        'factory converter.',
        '[blog] Torque Converter > Apply/Release: a good start is to max out the 3rd and 4th gear apply '
        'and release. If you change 5th and 6th apply, change the release by the same amount.',
        '[blog] Engine > Torque Management > General: raise Maximum Torque, the Torque Limit table '
        '(all gears) and Trans Input Max so the engine does not cut torque the converter now passes.',
        '[blog] Upshift torque factor of 0.5 to 0.7 gives less torque management and shorter events. '
        'Setting Speed Control Terminate to Immediate puts torque back as soon as the shift ends.',
        '[video2] Turbine transition times (inertia factor tables): on a loose aftermarket converter they '
        'can likely be shortened because the turbine follows the engine more easily. The video author '
        'is not certain, so shorten in small steps and watch for shift flare.',
        '[video1] Log TCC slip, TCC desired slip, trans fluid temperature and shift time, and check the '
        'TCC adapt limits before and after.',
    ]
    if key == TRIPLE:
        lines.append('[start] Ask the converter maker for the lockup clutch torque rating. A multi-plate clutch '
                     'holds more torque, so do not copy single-plate apply pressures without checking slip.')
    return lines


# --- differential ratios -----------------------------------------------------------------------

DIFF_RATIOS = [2.41, 2.56, 2.73, 2.92, 3.08, 3.23, 3.27, 3.42, 3.45, 3.55, 3.73, 3.9, 4.1, 4.3, 4.56, 4.88]


def diff_options(current=None):
    """The preset list, with the current ratio added when it is not already there."""
    options = list(DIFF_RATIOS)
    if current and all(abs(current - r) > 0.004 for r in options):
        options.append(round(float(current), 2))
        options.sort()
    return options


def rpm_at_speed(mph, tire_dia, ratio, axle, chain=1.0):
    """Engine RPM in a gear at a road speed, with no converter slip."""
    return mph * ratio * axle * chain * 63360.0 / (60.0 * pi * tire_dia)


def diff_effect(ratios, axle, tire_dia, shift_rpm, chain=1.0, cruise_kph=100.0):
    """What the diff ratio does. Returns a dict and a list of plain-words lines.

    cruise_rpm: top-gear RPM at cruise_kph. top_mph_first: road speed at the shift RPM in 1st.
    """
    mph_cruise = cruise_kph / 1.609344
    cruise = rpm_at_speed(mph_cruise, tire_dia, ratios[-1], axle, chain)
    first_mph = shift_rpm * 60.0 * pi * tire_dia / (ratios[0] * axle * chain * 63360.0)
    result = {'cruise_rpm': cruise, 'first_gear_top_mph': first_mph, 'cruise_kph': cruise_kph}
    lines = [f'{axle:g} diff: {cruise:.0f} rpm at {cruise_kph:.0f} km/h in top gear, '
             f'{first_mph:.0f} mph ({first_mph * 1.609344:.0f} km/h) in 1st at {shift_rpm:.0f} rpm.']
    if cruise > 2300:
        lines.append('Cruise RPM is high for a highway gear. The converter lock floor and the fuel economy both suffer.')
    elif cruise < 1300:
        lines.append('Cruise RPM is very low. Check the converter will lock without lugging the engine.')
    return result, lines


def diff_change(ratios, old_axle, new_axle, tire_dia, shift_rpm, chain=1.0):
    """Compare two diff ratios. Returns plain-words lines."""
    old, _ = diff_effect(ratios, old_axle, tire_dia, shift_rpm, chain)
    new, _ = diff_effect(ratios, new_axle, tire_dia, shift_rpm, chain)
    delta = new['cruise_rpm'] - old['cruise_rpm']
    return [f'Changing {old_axle:g} to {new_axle:g}: cruise {old["cruise_rpm"]:.0f} to {new["cruise_rpm"]:.0f} rpm '
            f'({delta:+.0f}), 1st gear top speed {old["first_gear_top_mph"]:.0f} to '
            f'{new["first_gear_top_mph"]:.0f} mph. Set the speedometer/VSS calibration for the new ratio.']
