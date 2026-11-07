"""The owner's 2011 Holden VE Calais Turbo ("CALAIS TURBO"): its 16 logger PIDs and its vehicle settings. No Kivy.

The 16 PIDs are rows of data/torque_gm_predefined.csv that the logger did not have: the air-conditioning high side
pressure, EGR duty and voltage, H2O sensor, ignition 1 voltage, injector PWM for both banks, the misfire history
for all eight cylinders, and oil pressure. They are saved as a user car (scanner/profiles.py), so they show on
Scan and are written to a data log like any other sensor. (The Live grid is the fixed engine and
transmission stream; it does not show a saved car's extra sensors.)

The Shift tab's vehicle is a "CALAIS TURBO (6L80E)" starter profile: the app's 6L80 starter profile with the 3.9
differential ratio the owner gave. The other values in it (tyre, weight, RPM limits, converter lock) are the 6L80
starter profile's own, not measured on the Calais, and can be changed on the Shift tab.
"""

import copy

from . import predefined, profiles
from tunertoolpro import vehicles
from tunertoolpro.engines import constants

CAR_NAME = 'CALAIS TURBO'
CAR_KEY = 'user-2011-holden-calais-turbo'       # profiles.save_user keys a car by its slugged label
CAR_TRANSMISSION = '6L80 (2006-Current)'        # the name the built-in Holden profiles use
FINAL_DRIVE = 3.9
PROFILE_NAME = 'CALAIS TURBO (6L80E)'     # the Shift tab's starter profile
BASE_PROFILE = 'LS3 Camaro SS (6L80)'          # the app's own 6L80 starter profile it is copied from

# The Torque names of the 16 PIDs, from data/torque_gm_predefined.csv.
NAMES = frozenset({
    '[GM]AirCon High Side Pressure',
    '[GM]EGR Duty Cycle',
    '[GM]EGR V',
    '[GM]H2OS Sensor',
    '[GM]Ignition 1 Voltage',
    '[GM]Injector PWM Bank 1',
    '[GM]Injector PWM Bank 2',
    '[GM]Misfire Cyl.1 History',
    '[GM]Misfire Cyl.2 History',
    '[GM]Misfire Cyl.3 History',
    '[GM]Misfire Cyl.4 History',
    '[GM]Misfire Cyl.5 History',
    '[GM]Misfire Cyl.6 History',
    '[GM]Misfire Cyl.7 History',
    '[GM]Misfire Cyl.8 History',
    '[GM]Oil Pressure <2005',
})

PIDS_LIST = predefined.PredefinedList(
    'calais-turbo', 'Holden VE Calais Turbo: the 16 logger PIDs',
    'The 16 GM readings the logger was missing: AC high side pressure, EGR duty and voltage, H2O sensor, '
    'ignition 1 voltage, injector PWM, misfire history for all eight cylinders, oil pressure.',
    'torque_gm_predefined.csv', lambda name: name in NAMES)


def ensure_car(cars_dir):
    """Save the CALAIS TURBO car if it is not there yet. Returns the new profile, or None when it already exists."""
    if any(p.key == CAR_KEY for p in profiles.list_user(cars_dir)):
        return None
    profile, _rejected = predefined.save_to_profile(cars_dir, PIDS_LIST, CAR_NAME, 'Holden', CAR_NAME, '2011',
                                                    CAR_TRANSMISSION)
    return profile


def register_profile():
    """Add the CALAIS TURBO starter profile to the app's list, so the Shift tab can load it. Safe to call again.
    Must run before the Shift settings screen reads the saved choice, which is checked against this list."""
    if PROFILE_NAME not in constants.STARTER_PROFILES:
        constants.STARTER_PROFILES[PROFILE_NAME] = dict(copy.deepcopy(constants.STARTER_PROFILES[BASE_PROFILE]),
                                                        axle=FINAL_DRIVE)


def ensure_vehicle(choice_path):
    """Make CALAIS TURBO the Shift tab's vehicle (Holden, 6L80, 3.9 axle), unless the owner has already chosen a
    vehicle or a transmission there. Returns True when it was set. choice_path is the app's vehicle choice file."""
    register_profile()
    choice = vehicles.load(choice_path)
    if choice['profile'] or choice['transmission']:
        return False
    vehicles.save(choice_path, {'make': 'Holden', 'transmission': CAR_TRANSMISSION, 'profile': PROFILE_NAME})
    return True
