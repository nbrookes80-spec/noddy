"""Full-page templates: how the sensors of one full-screen page are placed. No Kivy, no I/O.

A full-screen page on the Live and Scan screens holds 4, 5 or 6 sensors (see dashboard_layout.pages). A template
says where each one goes, as fractions of the page: `slots` gives one `(x, y, w, h)` per sensor, in sensor order,
with `(0, 0)` the top-left corner. The cells tile the page: no overlap and no gap.

The chosen template is saved as a default for every page (`dash_template`) plus an optional choice for single pages
(`dash_page_templates`, page index as a string -> template id), the same way the page size is, and is set once at
start-up and whenever the user changes it (`configure`).
"""

import math

DEFAULT = 'grid'
MAX_PAGE_CHOICES = 100          # saved per-page choices kept: a damaged file cannot grow without limit
MAX_PAGE_INDEX = 999
HERO_SHARE = 0.6                # width of the large sensor in the 'hero' layout
SQUARE_ASPECT = 1.0             # the page shape assumed when the caller does not say

# id -> name and the sensor counts the template can lay out. The grid is the fallback, so it takes any number.
TEMPLATES = {
    'grid': {'name': 'Grid', 'min': 1, 'max': 12},
    'columns2': {'name': 'Two columns', 'min': 2, 'max': 12},
    'hero': {'name': 'One large, rest beside', 'min': 2, 'max': 8},
    'hero_top': {'name': 'One wide, rest below', 'min': 2, 'max': 7},
    'rows': {'name': 'Rows', 'min': 1, 'max': 8},
    'dials': {'name': 'Big dials', 'min': 1, 'max': 9},
}

CHOSEN = DEFAULT                # the default for every page, as configured
PER_PAGE = {}                   # page index (as a string) -> template id for pages with their own choice


def supports(template_id, count):
    """True when the template can lay out this many sensors."""
    spec = TEMPLATES.get(template_id) if isinstance(template_id, str) else None
    return spec is not None and spec['min'] <= count <= spec['max']


def _span(start, i, n, total):
    """Start and size of slice i of n equal slices of the stretch [start, start + total], from shared edges so the
    slices meet exactly."""
    lo = start + total * (i / n)
    hi = start + total * ((i + 1) / n)
    return lo, hi - lo


def _table(sizes, x=0.0, y=0.0, w=1.0, h=1.0):
    """Rows of cells filling the box: `sizes` is how many cells each row holds. Cells in a row share its width."""
    out = []
    for row, count in enumerate(sizes):
        top, height = _span(y, row, len(sizes), h)
        for col in range(count):
            left, width = _span(x, col, count, w)
            out.append((left, top, width, height))
    return out


def _fill(count, cols):
    """Row sizes that hold `count` cells, `cols` to a row, the last row taking what is left."""
    rows = -(-count // cols)
    return [cols] * (rows - 1) + [count - cols * (rows - 1)]


def _grid(count, aspect):
    if count == 1:
        cols = 1
    elif count in (2, 4) or aspect < 1.2:
        cols = 2
    else:
        cols = 3
    return _table(_fill(count, cols))


def _columns2(count, _aspect):
    left = -(-count // 2)
    return _table([1] * left, 0, 0, 0.5, 1) + _table([1] * (count - left), 0.5, 0, 0.5, 1)


def _hero(count, _aspect):
    return [(0.0, 0.0, HERO_SHARE, 1.0)] + _table([1] * (count - 1), HERO_SHARE, 0, 1 - HERO_SHARE, 1)


def _hero_top(count, _aspect):
    rest = count - 1
    sizes = _fill(rest, min(rest, 3))
    top = 0.5 if rest == 1 else (0.45 if len(sizes) == 1 else 0.4)
    return [(0.0, 0.0, 1.0, top)] + _table(sizes, 0, top, 1, 1 - top)


def _rows(count, _aspect):
    return _table([1] * count)


def _dials(count, aspect):
    """The number of columns that makes the cells closest to square on a page of this shape."""
    def off_square(cols):
        return abs(math.log(aspect * (-(-count // cols)) / cols))
    cols = min(range(1, count + 1), key=lambda c: (off_square(c), c))
    return _table(_fill(count, cols))


_BUILDERS = {'grid': _grid, 'columns2': _columns2, 'hero': _hero, 'hero_top': _hero_top, 'rows': _rows,
             'dials': _dials}


def slots(template_id, count, aspect=None):
    """One `(x, y, w, h)` cell per sensor, as fractions of the page, in sensor order. An unknown template or a
    count it does not support gives the grid. `aspect` (page width over height) only changes the templates that
    depend on the page's shape (grid, dials)."""
    if count < 1:
        return []
    aspect = aspect if isinstance(aspect, (int, float)) and aspect > 0 else SQUARE_ASPECT
    build = _BUILDERS[template_id] if supports(template_id, count) else _grid
    return build(count, aspect)


def to_pixels(rects, x, y, width, height, gap=0):
    """Fractional cells placed in a box whose bottom-left corner is `(x, y)` (y counts up, as in Kivy). Each cell is
    drawn inset by half the gap, so neighbours end up a gap apart; a gap never takes more than a quarter of a
    cell's width or height. Returns `(x, y, w, h)` per cell."""
    out = []
    for rx, ry, rw, rh in rects:
        left, cell_w, cell_h = x + rx * width, rw * width, rh * height
        bottom = y + height - (ry + rh) * height
        inset_x, inset_y = min(gap / 2, cell_w / 4), min(gap / 2, cell_h / 4)
        out.append((left + inset_x, bottom + inset_y, cell_w - 2 * inset_x, cell_h - 2 * inset_y))
    return out


# --- What a card can show in its cell ------------------------------------------------------------------------

DETAILS = ('line', 'no_gauge', 'no_stats', 'full')     # from least to most


def detail_for(height, name, reading, stats, gauge, pad, spacing):
    """How much a sensor card can show in a cell `height` tall. All sizes are in one unit (dp or pixels):
    `name` and `reading` are the heights of the name and the number, `stats` of the lowest/highest line, `gauge`
    the least useful height for the picture, `pad` the card's padding and `spacing` the gap between its parts.

    'full'      name, number, lowest/highest line and picture
    'no_stats'  without the lowest/highest line
    'no_gauge'  name and number, one above the other
    'line'      name and number side by side, when even those do not fit one above the other
    """
    base = 2 * pad + name + reading + spacing
    if height < base:
        return 'line'
    if height < base + gauge + spacing:
        return 'no_gauge'
    if height < base + gauge + stats + 2 * spacing:
        return 'no_stats'
    return 'full'


# --- Saved choices -----------------------------------------------------------------------------------------

def clean_choice(raw):
    """A saved template id, or the grid when it is missing or not one we know."""
    return raw if isinstance(raw, str) and raw in TEMPLATES else DEFAULT


def _page_key(raw):
    """A page index as the plain digits string used in the saved file, or None."""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        index = raw
    elif isinstance(raw, str) and raw.isascii() and raw.isdigit():
        index = int(raw)
    else:
        return None
    return str(index) if 0 <= index <= MAX_PAGE_INDEX else None


def clean_per_page(raw):
    """The saved per-page choices: only page numbers with a template we know, at most MAX_PAGE_CHOICES of them."""
    if not isinstance(raw, dict):
        return {}
    out = {}
    for key, value in raw.items():
        page = _page_key(key)
        if page is not None and isinstance(value, str) and value in TEMPLATES and len(out) < MAX_PAGE_CHOICES:
            out[page] = value
    return out


def template_for_page(default_id, per_page, page_index):
    """The template for one page: its own choice if it has one, else the default."""
    if isinstance(per_page, dict):
        own = per_page.get(str(page_index))
        if isinstance(own, str) and own in TEMPLATES:
            return own
    return clean_choice(default_id)


def apply_to_page(default_id, per_page, page_index, template_id):
    """The choices after giving one page its own template: `(default, per_page)`, both new."""
    pages = clean_per_page(per_page)
    key = _page_key(page_index)
    if key is not None:
        pages[key] = clean_choice(template_id)
    return clean_choice(default_id), pages


def apply_to_all(template_id):
    """The choices after setting one template for every page, dropping any page's own choice."""
    return clean_choice(template_id), {}


def configure(default_id, per_page):
    """Use these choices from now on, like dashboard_layout.configure. Anything not valid falls back."""
    global CHOSEN
    CHOSEN = clean_choice(default_id)
    PER_PAGE.clear()
    PER_PAGE.update(clean_per_page(per_page))


def for_page(page_index):
    """The configured template for a page."""
    return template_for_page(CHOSEN, PER_PAGE, page_index)
