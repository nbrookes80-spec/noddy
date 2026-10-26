"""Vehicle profile and transmission library. Standard library only (the AI and the checks use it).

Ratios marked with a source were found on the web while building this module. They are not ZF,
GM or Powerglide specification sheets. Check every figure against your own parts list and the
kit maker's data before you rely on it.
"""

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .engines.constants import TRANS_DB
from . import settings

GM_6L80_SOURCE = 'Ratios from the app\'s TRANS_DB (6L80, GM 6-speed). Reverse from vendor listings: ATI, Billy\'s Speed Shop.'
ZF_8HP_SOURCE = ('Forward ratios from RAM forum and Transmission Digest (aftermarket and forum sources, '
                 'not ZF). Reverse and final drive not found.')
POWERGLIDE_SOURCE = 'Ratios from itstillruns.com (1.82 six-cylinder; 1.76 V8 reverse from a single source), and Jalopnik (second gear 1:1).'

# key -> {ratios (1st..top), reverse (or None), type, rated_torque_lbft (or None), note, source}
TRANSMISSIONS = {
    'Stock 6L80 (2006-Current)': {
        'ratios': list(TRANS_DB['6L80 (2006-Current)']['ratios']), 'reverse': 3.06, 'type': 'RWD',
        'rated_torque_lbft': None, 'modified': False,
        'note': 'Stock GM 6-speed. Rated torque not in the app data; enter it from GM or your builder.',
        'source': GM_6L80_SOURCE,
    },
    '6L80 modified (Sonnax zip kit, TransGo shift kit, billet flex plate, Circle D triple-plate converter)': {
        'ratios': list(TRANS_DB['6L80 (2006-Current)']['ratios']), 'reverse': 3.06, 'type': 'RWD',
        'rated_torque_lbft': None, 'modified': True,
        'note': ('Same gear set as the stock 6L80. The kit parts change clutch capacity, shift timing and '
                 'converter stall, so the rated torque and stall must come from the parts makers. The app '
                 'cannot calculate new capacities from these parts.'),
        'source': GM_6L80_SOURCE,
    },
    'ZF 8HP45 / 8HP70 (8-speed)': {
        'ratios': [4.69, 3.13, 2.10, 1.67, 1.29, 1.00, 0.84, 0.67], 'reverse': None, 'type': 'RWD/AWD',
        'rated_torque_lbft': None, 'modified': False,
        'note': ('The 8HP70 shares the 8HP45 gear set. Final drive depends on the axle, and the reverse ratio was '
                 'not found. Enter both from the vehicle.'),
        'source': ZF_8HP_SOURCE,
    },
    '2-Speed Powerglide (six-cylinder ratio)': {
        'ratios': [1.82, 1.00], 'reverse': 1.82, 'type': 'RWD', 'rated_torque_lbft': None, 'modified': False,
        'note': 'Two forward gears: low and direct (1:1). Reverse matches low.',
        'source': POWERGLIDE_SOURCE,
    },
    '2-Speed Powerglide (V8 ratio)': {
        'ratios': [1.76, 1.00], 'reverse': 1.76, 'type': 'RWD', 'rated_torque_lbft': None, 'modified': False,
        'note': 'Two forward gears: low and direct (1:1). The reverse ratio comes from one source; check it.',
        'source': POWERGLIDE_SOURCE,
    },
}


def transmission_keys():
    return list(TRANSMISSIONS)


@dataclass
class VehicleProfile:
    car: str = ''
    engine: str = ''
    transmission: str = 'Stock 6L80 (2006-Current)'
    final_drive: float = 3.08
    tire_dia: float = 26.0
    power_hp: float = 0.0
    torque_lbft: float = 0.0
    weight_lb: float = 0.0
    # ECU limits (from the calibration file or the scan tool). None means not entered.
    ecu_max_torque_lbft: float = None
    redline_rpm: float = None
    notes: str = ''
    sources: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        known = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**known)

    def missing(self):
        """Names of the fields the AI or the user still needs to fill in."""
        needed = {
            'car': self.car, 'engine': self.engine, 'power_hp': self.power_hp,
            'torque_lbft': self.torque_lbft, 'weight_lb': self.weight_lb,
            'ecu_max_torque_lbft': self.ecu_max_torque_lbft, 'redline_rpm': self.redline_rpm,
        }
        return [name for name, value in needed.items() if not value]


def profile_path():
    return settings.user_dir() / 'vehicle.json'


def load_profile():
    try:
        data = json.loads(profile_path().read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return VehicleProfile()
    return VehicleProfile.from_dict(data) if isinstance(data, dict) else VehicleProfile()


def save_profile(profile):
    path = profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    if tmp.is_symlink() or tmp.exists():
        tmp.unlink()
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        json.dump(profile.to_dict(), fh, indent=2)
    os.replace(tmp, path)
    return Path(path)


def transmission(key):
    """Return the library entry for key. Raises KeyError with the valid names if unknown."""
    if key not in TRANSMISSIONS:
        raise KeyError(f'unknown transmission {key!r}; choose one of: {", ".join(TRANSMISSIONS)}')
    return TRANSMISSIONS[key]
