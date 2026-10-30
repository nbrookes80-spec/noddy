"""Vehicle profiles: which PIDs the app knows for a car, and which it shows first. No Kivy.

A profile is a make, model and years plus the PID lists to load for it. The built-in ones (Holden VE and
VF, Pontiac G8, GM generic, Ford, any car) use the app's own catalogue and the Torque Pro lists in data/.
A user profile is made from a Torque Pro CSV the user imports. Every PID that comes from a file is
unconfirmed until it has been checked on a real car, and nothing is ever sent unless it is a Mode 01 or
Mode 22 read (torque_csv.py enforces that).
"""

import json
import re
from dataclasses import dataclass, replace
from pathlib import Path

from . import car_scan, pids, torque_csv

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
TORQUE_FILES = ('torque_gm_predefined.csv', 'torque_e38_t43_v5.csv')
MODULE_NOTE = 'address is unconfirmed'     # in a PID's description when its module could not be mapped


@dataclass(frozen=True)
class Profile:
    key: str
    name: str
    make: str
    years: str = ''
    transmission: str = ''        # a name from vehicles.py, or ''
    files: tuple = ()             # lists in data/ to load
    mode01_only: bool = False     # a car with no known Mode 22 list: show standard readings only
    notes: str = ''
    user_csv: str = ''            # the text of a CSV the user imported
    builtin: bool = True


def built_in():
    gm_note = ('PIDs come from the Torque Pro GM lists. The GM transmission readings are unconfirmed on a real car '
               'until you check them on yours.')
    return [
        Profile('holden-ve', 'Holden VE Commodore (E38, 6L80)', 'Holden', '2006-2013', '6L80 (2006-Current)',
                TORQUE_FILES, notes=gm_note),
        Profile('holden-vf', 'Holden VF Commodore (E92, 6L80)', 'Holden', '2013-2017', '6L80 (2006-Current)',
                TORQUE_FILES, notes=gm_note),
        Profile('pontiac-g8', 'Pontiac G8 GT / GXP (6L80)', 'Pontiac', '2008-2009', '6L80 (2006-Current)',
                TORQUE_FILES, notes=gm_note),
        Profile('gm-generic', 'GM generic (Mode 01 and GM Mode 22)', 'GM', '', '', TORQUE_FILES, notes=gm_note),
        Profile('ford-generic', 'Ford (standard OBD-II only)', 'Ford', '', '', (), True,
                'Only standard Mode 01 readings until a Ford PID list is added. You can import your own Torque file.'),
        Profile('obd2', 'Any car (standard OBD-II only)', '', '', '', (), True,
                'Standard Mode 01 readings that every OBD-II car answers.'),
    ]


def load_pids(profile):
    """Returns (extra Pids, rejected rows) for a profile: its data lists plus any CSV the user imported."""
    extras, rejected, seen = [], [], set()
    sources = [(name, (DATA_DIR / name).read_text(encoding='utf-8', errors='replace')) for name in profile.files]
    if profile.user_csv:
        sources.append((f'{profile.name} (imported)', profile.user_csv))
    for source, text in sources:
        found, problems = torque_csv.parse(text, source=source)
        for pid in found:
            if pid.pid not in seen:
                seen.add(pid.pid)
                extras.append(pid)
        rejected += [dict(row, source=source) for row in problems if 'already' not in row['reason']]
    return extras, rejected


def monitor_for(profile, extras):
    """The ids shown on the Scan dashboard, in order."""
    if profile.mode01_only:
        return [p for p in pids.DEFAULT_MONITOR if p.startswith('01')] + [p.pid for p in extras if p.mode == '01']
    shown = [p.pid for p in extras if MODULE_NOTE not in p.description]
    return pids.DEFAULT_MONITOR + [p for p in shown if p not in pids.DEFAULT_MONITOR]


def candidates(profile, manual=()):
    """Every PID the PID manager lists for a profile, in dashboard order, before the car check or hiding."""
    extras, _rejected = load_pids(profile)
    by_hand = {p.pid for p in manual}
    extras = list(manual) + [p for p in extras if p.pid not in by_hand]
    return monitor_for(profile, extras)


def activate(profile, scan=None, manual=(), user_hidden=()):
    """Make this profile the catalogue and dashboard list. Returns a summary dict for the screen to show.

    scan is the car's saved scan (car_scan.load_scan). With a complete scan the dashboard only lists the
    readings the car answered, and the summary gives the module address to ask for each of them.
    manual is the PIDs the user entered by hand (manual_pids.pids_for); they replace an imported row with
    the same id. user_hidden is the ids the user turned off in the PID manager: they stay in the catalogue but are
    left off the dashboard.
    """
    extras, rejected = load_pids(profile)
    by_hand = {p.pid for p in manual}
    extras = list(manual) + [p for p in extras if p.pid not in by_hand]
    skipped = pids.use_extras(extras)
    monitor = monitor_for(profile, extras)
    shown, hidden = car_scan.enforce(monitor, scan)
    # A car check only asks for the PIDs that were known when it ran, so a PID typed in afterwards was never
    # asked for. Keep the user's own PIDs on the dashboard rather than hiding them as "no reply".
    keep = {p.pid for p in manual}
    shown = [p for p in monitor if p in shown or p in keep]
    hidden = {p: reason for p, reason in hidden.items() if p not in keep}
    turned_off = {p.upper() for p in user_hidden}
    shown = [p for p in shown if p not in turned_off]
    pids.MONITOR_PIDS[:] = shown
    added = [p for p in extras if p.pid not in skipped]
    return {'profile': profile.name, 'added': len(added), 'already_known': len(skipped), 'rejected': rejected,
            'shown': len(pids.MONITOR_PIDS), 'hidden': hidden, 'turned_off': len(turned_off & set(monitor)), 'headers': car_scan.headers(scan),
            'checked': scan is not None and scan['complete']}


# --- the user's own cars -------------------------------------------------------------------------

def _slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:40] or 'car'


def save_user(directory, name, make, model, year, transmission, csv_text):
    """Check a Torque CSV and save it as a profile. Returns (profile, rejected rows). Nothing is saved when
    the file has no usable PID, so a wrong file cannot replace a good profile."""
    label = ' '.join(part for part in (str(year).strip(), make.strip(), model.strip()) if part) or name.strip()
    probe = Profile(f'user-{_slug(label)}', label, make.strip(), str(year).strip(), transmission,
                    user_csv=csv_text, builtin=False)
    found, rejected = load_pids(probe)
    if not found:
        return None, rejected
    folder = Path(directory)
    folder.mkdir(parents=True, exist_ok=True)
    stem = _slug(label)
    (folder / f'{stem}.csv').write_text(csv_text, encoding='utf-8')
    meta = {'name': label, 'make': probe.make, 'years': probe.years, 'transmission': transmission}
    (folder / f'{stem}.json').write_text(json.dumps(meta))
    return replace(probe, key=f'user-{stem}'), rejected


def list_user(directory):
    """The saved user profiles. A damaged file is skipped, never fatal."""
    out = []
    for meta_path in sorted(Path(directory).glob('*.json')):
        try:
            meta = json.loads(meta_path.read_text())
            text = meta_path.with_suffix('.csv').read_text(encoding='utf-8', errors='replace')
            out.append(Profile(f'user-{meta_path.stem}', str(meta['name'])[:80], str(meta.get('make', ''))[:30],
                               str(meta.get('years', ''))[:12], str(meta.get('transmission', '')),
                               user_csv=text, builtin=False))
        except (OSError, ValueError, KeyError, TypeError):
            continue
    return out


def everything(directory):
    return built_in() + list_user(directory)
