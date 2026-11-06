"""How the dashboard sensors are grouped, ordered and paged on the Live and Scan screens. No Kivy, no I/O.

Every sensor sits in one group: TCM (transmission computer), ECU (engine computer), Fuel, Air or Boost. Within
a group the user's own order is kept. A full-screen page holds 4, 5 or 6 sensors. The chosen order and page size
are set once at start-up and whenever the user changes them, the same way the column count is.
"""

from . import pids as _pids

GROUPS = ('TCM', 'ECU', 'Fuel', 'Air', 'Boost', 'Imported')   # Imported: signals from a CAN log being played back
TITLES = {'TCM': 'TCM - transmission', 'ECU': 'ECU - engine', 'Fuel': 'Fuel', 'Air': 'Air', 'Boost': 'Boost',
          'Imported': 'Imported from a CAN log'}
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
    if pid.category == 'Imported':
        return 'Imported'
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
    """The dashboard's sensors from the catalogue, in the order the profile lists them. Signals from a CAN log
    being played back come last."""
    listed = [_pids.get(p) for p in _pids.MONITOR_PIDS if _pids.get(p) is not None]
    return listed + list(_pids.REPLAY.values())


def clean_order(raw):
    """A saved order from a settings file: only valid, de-duplicated PID ids, in the order given."""
    if not isinstance(raw, list):
        return []
    kept = []
    for item in raw:
        if isinstance(item, str) and _pids.valid_id(item.upper()) and item.upper() not in kept:
            kept.append(item.upper())
    return kept[:200]


# --- Moving a sensor (the long-press menu) -----------------------------------------------------------------
#
# These work on the *arranged* list of PID ids, which is what `arrange` returns for a screen. Each returns a
# new list holding exactly the ids it was given, never fewer, never twice, and leaves the argument alone. An id
# that is not in the list changes nothing. The caller saves the result as the user's order (see `merged_order`).
#
# `group` is an optional function id -> group name. `arrange` sorts by group first, so a move across a group
# boundary would be undone the next time the list is drawn. With `group` given, a sensor only trades places with
# sensors of its own group: the other groups keep their slots and the sensor's group keeps its slots as a block.

def _slots(order, pid_id, group):
    """The indexes the moving sensor may use: all of them, or only those held by its own group."""
    if group is None:
        return list(range(len(order)))
    wanted = group(pid_id)
    return [i for i, item in enumerate(order) if group(item) == wanted]


def _place(order, slots, members):
    """`order` with the sensors in `slots` replaced, in slot order, by `members`."""
    out = list(order)
    for index, item in zip(slots, members):
        out[index] = item
    return out


def move(order, pid_id, step, group=None):
    """Move a sensor `step` places (negative = earlier, positive = later), stopping at the ends of the list, or
    of its group when `group` is given."""
    if pid_id not in order or not step:
        return list(order)
    slots = _slots(order, pid_id, group)
    members = [order[i] for i in slots]
    here = members.index(pid_id)
    there = max(0, min(len(members) - 1, here + step))
    members.insert(there, members.pop(here))
    return _place(order, slots, members)


def move_to_edge(order, pid_id, edge, group=None):
    """Move a sensor to the first place ('top') or last place ('end') of the list, or of its group."""
    if edge not in ('top', 'end'):
        raise ValueError(f'edge must be "top" or "end", not {edge!r}')
    if pid_id not in order:
        return list(order)
    slots = _slots(order, pid_id, group)
    members = [order[i] for i in slots]
    members.remove(pid_id)
    members.insert(0 if edge == 'top' else len(members), pid_id)
    return _place(order, slots, members)


def _page_size(size):
    return PAGE_SIZE if size is None else (size if size in PAGE_SIZES else DEFAULT_PAGE_SIZE)


def position(order, pid_id, size=None):
    """(page index, place on that page), both counting from 0, of a sensor in the arranged list, or None if it
    is not there. `size` is 4, 5 or 6 and defaults to the configured page size."""
    if pid_id not in order:
        return None
    return divmod(order.index(pid_id), _page_size(size))


def _page_target(order, pid_id, page_index, size, group):
    """The index the sensor ends up at when moved to this page, or None if that page cannot take it."""
    if pid_id not in order or isinstance(page_index, bool) or not isinstance(page_index, int):
        return None
    size = _page_size(size)
    first, last = page_index * size, min((page_index + 1) * size, len(order))   # the page covers [first, last)
    if page_index < 0 or first >= len(order):
        return None
    slots = _slots(order, pid_id, group)
    # a group's sensors are one run of the arranged list; the slots it can use on this page are where the two meet
    usable = [i for i in slots if first <= i < last]
    return usable[-1] if usable else None


def move_to_page(order, pid_id, page_index, size=None, group=None):
    """Move a sensor to the end of page `page_index` (from 0) when the screen is cut into pages of `size`.

    Pages are cut after `arrange` has sorted by group, so a page can hold several groups. With `group` given
    (the app always passes it) the sensor takes the LAST slot, on that page, that belongs to its own group, and
    the sensors of that group between its old and new slot shift up by one. If the page holds no slot of the
    sensor's group, or does not exist, nothing changes and the list comes back equal to the one given (use
    `reachable_pages` to know beforehand). Without `group` the whole list is one group, so the sensor goes to
    the very last place on the page.
    """
    target = _page_target(order, pid_id, page_index, size, group)
    if target is None:
        return list(order)
    slots = _slots(order, pid_id, group)
    members = [order[i] for i in slots]
    members.remove(pid_id)
    members.insert(slots.index(target), pid_id)
    return _place(order, slots, members)


def reachable_pages(order, pid_id, size=None, group=None):
    """The page indexes `move_to_page` can put this sensor on (all pages when `group` is None)."""
    count = len(pages(order, size))
    return [p for p in range(count) if _page_target(order, pid_id, p, size, group) is not None]


def _arranged_ids(source, order):
    """What `arrange` would give for these ids (in the order the screen lists them) and this saved order."""
    rank = {pid: i for i, pid in enumerate(order)}
    keyed = [(GROUPS.index(group_of_id(pid)), rank.get(pid, len(rank)), i, pid) for i, pid in enumerate(source)]
    return [pid for *_, pid in sorted(keyed, key=lambda item: item[:3])]


def merged_order(saved, arranged, source=None):
    """The order to save after a sensor was moved on one screen, changing as little as possible.

    `arranged` is that screen's new arranged ids and `source` the same ids in the order the screen lists them
    before `arrange` (the catalogue order that breaks ties; default: `arranged`). The Live screen and the Scan
    pages show different sensors but share one saved order, so listing every sensor of the moved screen would
    reshuffle sensors the user never touched on the other one. Instead, for each group on its own, this lists only
    the first k sensors of the group for the smallest k that makes `arrange` give exactly `arranged` (the sensors
    after them already fall in the right order by themselves). Ids saved before follow, in their saved order. So a
    group nobody moved in is not listed at all, and sensors left unlisted keep their own order on both screens.
    Where the two screens disagree on how two shared sensors stand by default, the moved screen's order wins for
    the ones listed."""
    arranged = list(arranged)
    source = arranged if source is None else list(source)
    heads = []
    for group in GROUPS:
        want = [i for i in arranged if group_of_id(i) == group]
        if not want:
            continue
        mine = [i for i in source if group_of_id(i) == group]
        for k in range(len(want) + 1):
            taken = set(want[:k])
            trial = want[:k] + [item for item in saved if item not in taken]
            if _arranged_ids(mine, trial) == want:
                heads += want[:k]
                break
        else:                       # `arranged` is not a sorting of `source`: list the whole group as given
            heads += want
    listed = set(heads)
    return heads + [item for item in saved if item not in listed]


def group_of_id(pid_id):
    """The group of a sensor given by its id ('ECU' for an id the catalogue does not know)."""
    found = _pids.get(pid_id)
    return group_of(found) if found is not None else 'ECU'


ACTIONS = ('earlier', 'later', 'top', 'end', 'page')


def reorder(arranged, pid_id, action, value=None, size=None):
    """What a menu entry does to the arranged ids of a screen, always within the sensor's own group:
    'earlier' / 'later' (one place), 'top' / 'end' (of its group), 'page' (`value` = page index from 0, see
    `move_to_page`). Returns the new arranged ids, equal to the old ones when the move is not possible."""
    if action == 'earlier':
        return move(arranged, pid_id, -1, group=group_of_id)
    if action == 'later':
        return move(arranged, pid_id, 1, group=group_of_id)
    if action in ('top', 'end'):
        return move_to_edge(arranged, pid_id, action, group=group_of_id)
    if action == 'page':
        return move_to_page(arranged, pid_id, value, size, group=group_of_id)
    raise ValueError(f'unknown move {action!r}')
