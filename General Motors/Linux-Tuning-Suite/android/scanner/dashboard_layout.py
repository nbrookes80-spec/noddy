"""How the dashboard sensors are grouped, ordered and paged on the Live and Scan screens. No Kivy, no I/O.

Every sensor sits in one group: TCM (transmission computer), ECU (engine computer), Fuel, Air or Boost. Within
a group the user's own order is kept. A full-screen page holds 4, 5 or 6 sensors. The chosen order and page size
are set once at start-up and whenever the user changes them, the same way the column count is.
"""

from . import pids as _pids

GROUPS = ('TCM', 'ECU', 'Fuel', 'Air', 'Boost')
TITLES = {'TCM': 'TCM - transmission', 'ECU': 'ECU - engine', 'Fuel': 'Fuel', 'Air': 'Air', 'Boost': 'Boost'}
PAGE_SIZES = (4, 5, 6)
DEFAULT_PAGE_SIZE = 4
BOOST = {'010B', '01BB'}                                              # MAP sensor, relative boost pressure
AIR = {'010F', '0110', '0111', '0133', '0145', '0146', '0147', '0149', '014A', '014C'}   # intake air, MAF, throttle, baro, ambient

ORDER = []                    # the user's sensor order, by PID id; sensors not listed keep their own order
PAGE_SIZE = DEFAULT_PAGE_SIZE


def configure(order, size):
    """Use this order and page size from now on. An unknown size falls back to the default."""
    global PAGE_SIZE
    ORDER[:] = [p.upper() for p in order]
    PAGE_SIZE = size if size in PAGE_SIZES else DEFAULT_PAGE_SIZE


def group_of(pid):
    """The group a sensor belongs to. Transmission sensors answer on 7E2; the rest is set by PID or category."""
    if pid.header == '7E2' or pid.category.startswith('Transmission'):
        return 'TCM'
    if pid.pid in BOOST:
        return 'Boost'
    if pid.pid in AIR:
        return 'Air'
    if pid.category == 'Fuel':
        return 'Fuel'
    return 'ECU'


def arrange(pid_list, order=None):
    """The sensors in display order: by group, then in the user's order inside each group. A sensor the order
    does not mention goes after the ones it does, in the order it came."""
    rank = {pid: i for i, pid in enumerate(ORDER if order is None else order)}
    keyed = [(GROUPS.index(group_of(p)), rank.get(p.pid, len(rank)), i, p) for i, p in enumerate(pid_list)]
    return [p for *_, p in sorted(keyed, key=lambda item: item[:3])]


def runs(pid_list):
    """The sensors split into runs of one group each, in the order given, so each run gets its heading."""
    out = []
    for pid in pid_list:
        group = group_of(pid)
        if out and out[-1][0] == group:
            out[-1][1].append(pid)
        else:
            out.append((group, [pid]))
    return out


def pages(pid_list, size=None):
    """The arranged sensors cut into pages of `size` (4, 5 or 6). Never an empty page."""
    size = PAGE_SIZE if size is None else (size if size in PAGE_SIZES else DEFAULT_PAGE_SIZE)
    return [pid_list[i:i + size] for i in range(0, len(pid_list), size)]


def dashboard_pids():
    """The dashboard's sensors from the catalogue, in the order the profile lists them."""
    return [_pids.get(p) for p in _pids.MONITOR_PIDS if _pids.get(p) is not None]


def clean_order(raw):
    """A saved order from a settings file: only valid, de-duplicated PID ids, in the order given."""
    if not isinstance(raw, list):
        return []
    kept = []
    for item in raw:
        if isinstance(item, str) and _pids.valid_id(item.upper()) and item.upper() not in kept:
            kept.append(item.upper())
    return kept[:200]
