"""One sensor on the Live and Scan screens, and what you can do to it.

  tap          choose how it is drawn: text, digital gauge, graph, histogram or analogue gauge
  long press   the sensor menu: edit it (name, unit, range, zones, colour), choose the display, move it earlier,
               later, to the top or end of its group or onto another page, reset its lowest and highest, ask the agent
  triple tap   ask your AI agent about this sensor

`hooks` is set once by the app. It holds the saved display choices and the actions that need the rest of
the app (editing, asking the agent, changing the order), so a card can be built anywhere without being handed them.
"""

import weakref

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from gauge_ui import GaugeView, height_for
from tunertoolpro.scanner import dashboard_layout, page_layout, pid_view, themes
from ui_kit import ALERT, CAUTION, GAP, MUTED, TEXT, Card, button_row, make_button, panel_label, section_title

HISTORY = 120
LONG_PRESS_SECONDS = 0.6
TAP_WINDOW_SECONDS = 0.4     # taps this close together count as one gesture (triple tap = ask the agent)


class Hooks:
    def __init__(self):
        self.views = None            # pid_view.PidViews
        self.on_edit = None          # callable(pid, done): open the editor for a sensor
        self.on_help = None          # callable(pid): bring the AI agent in on a sensor
        self.arranged = None         # callable(scope): the arranged PID ids of the 'live' or 'scan' screen
        self.on_order = None         # callable(arranged_ids, scope): keep this new order of the 'live' or 'scan' screen, save it, redraw both
        self.on_layout = None        # callable(scope): open the page layout chooser for the 'live' or 'scan' screen
        self.on_changed = lambda: None


hooks = Hooks()

_grids = weakref.WeakSet()
_cards = weakref.WeakSet()
ZONE_TEXT = {'red': ALERT, 'yellow': CAUTION, 'cold': themes.COLD, 'good': themes.GOOD}   # the number's colour in each zone
STATS_HEIGHT = 16     # dp: the line of lowest, highest and average under the number
NAME_HEIGHT = 26      # dp: the sensor's name above the number
_stats_on = True
COLUMN_WIDTH = 170    # dp: a phone turned on its side gets more columns than one held upright


_forced = 0     # sensor cards across, chosen in the menu; 0 fits as many as the screen allows


def _columns():
    if _forced:
        return _forced
    return max(2, int(Window.width / dp(COLUMN_WIDTH)))


def set_columns(count):
    """Use this many cards across on every dashboard (0 = as many as fit), and re-lay-out at once."""
    global _forced
    _forced = count if count in (2, 3, 4) else 0
    _refit()


def set_stats(on):
    """Show the lowest, highest and average under every sensor's number (and mark them on the bar and dial)."""
    global _stats_on
    _stats_on = bool(on)


def reset_stats():
    """Start the lowest, highest and average of every sensor again."""
    for card in list(_cards):
        card.reset_stats()


def _refit(*_):
    for grid in list(_grids):
        grid.cols = _columns()
        Clock.schedule_once(lambda dt, grid=grid: equalize(grid), 0)   # the rows are different once the columns are


Window.bind(size=_refit)


def equalize(grid):
    """Give the cards in each row the height of the tallest in that row, so a row lines up whatever each shows."""
    cards = [child for child in reversed(grid.children) if hasattr(child, 'natural')]
    grid.row_force_default = False
    across = max(1, grid.cols or 1)
    for start in range(0, len(cards), across):
        row = cards[start:start + across]
        tallest = max(card.natural for card in row)
        for card in row:
            card.height = tallest   # a card shorter than its row would sit at the row's edge, out of line


def fit_columns(grid):
    """Keep a grid of sensor cards at as many columns as fit, now and whenever the screen is turned."""
    _grids.add(grid)
    grid.cols = _columns()


def short(value):
    """A number for the min, max and average line: no more digits than the eye can use."""
    return '--' if value is None else (f'{value:.0f}' if abs(value) >= 10 else f'{value:.1f}')


def format_value(value, unit):
    """Readable number for a card: whole numbers when large, more digits when small."""
    shown = f'{value:.0f}' if abs(value) >= 100 else (f'{value:.1f}' if abs(value) >= 10 else f'{value:.2f}')
    return shown, unit


class PidCard(ButtonBehavior, Card):
    def __init__(self, pid, scope='scan', **kwargs):
        super().__init__(size_hint_y=None, spacing=dp(2), **kwargs)
        self.pid = pid
        self.scope = scope           # which screen the card sits on: 'live' (one long list) or 'scan' (pages)
        self.shown = {}
        self._reading = None
        self._idle = None            # text shown instead of "no reply" when this sensor is not being asked for
        self._note = None            # a sensor fault for this reading (replaces the number), or None
        self._series = []
        self._taps = 0
        self._long = self._pending = None
        self._fired = False
        self._cell = False           # True once a full-page layout has given this card a cell to fill (fit_cell)
        self.name = Label(color=MUTED, font_size=dp(12), halign='left', valign='middle', size_hint_y=None,
                          height=dp(NAME_HEIGHT), shorten=True, shorten_from='right')
        self.name.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
        self.value = Label(text='--', color=TEXT, bold=True, halign='left', valign='middle', size_hint_x=None,
                           width=dp(40))
        self.value.bind(texture_size=lambda w, size: setattr(w, 'width', size[0]))
        self.unit = Label(color=MUTED, font_size=dp(12), halign='left', valign='middle', size_hint_x=None,
                          width=dp(48), shorten=True, shorten_from='right')
        self.unit.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
        self.reading = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        self.reading.add_widget(self.value)
        self.reading.add_widget(self.unit)
        self.reading.add_widget(Widget())   # soaks up spare width so the number and unit stay together
        self.stats = pid_view.Stats()
        self.stats_line = Label(color=MUTED, font_size=dp(10.5), halign='left', valign='middle', size_hint_y=None,
                                height=dp(STATS_HEIGHT), shorten=True, shorten_from='right')
        self.stats_line.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
        self.gauge = GaugeView()
        self._spacer = Widget()      # soaks up the spare height of a tall row
        for widget in (self.name, self.reading, self.stats_line, self.gauge, self._spacer):
            self.add_widget(widget)
        self.bind(state=self._state_changed, size=self._adapt)
        _cards.add(self)
        self.apply_view()

    def _fit_height(self, *_):
        pass   # the height is set from the chosen display in apply_view

    # --- how it looks ----------------------------------------------------------------------------

    def apply_view(self):
        """Take the saved choices for this sensor (name, unit, range, zones, colour, display) and redraw."""
        views = hooks.views
        self.shown = views.apply(self.pid) if views is not None else dict(
            {key: None for key in pid_view.ZONE_KEYS}, name=self.pid.name, unit=self.pid.unit, low=self.pid.low,
            high=self.pid.high, mode=pid_view.DEFAULT_MODE, color=None,
            convert=lambda value: value, back=lambda value: value)
        mode = self.shown['mode']
        flag = '' if self.pid.verified else '  (unconfirmed)'
        self.name.text = self.shown['name'] + flag
        self.name.color = MUTED if self.pid.verified else ALERT
        self._number_size = dp(28 if mode in ('digital', 'text') else 22)
        self.value.font_size = self._number_size
        self._reading_height = dp(52 if mode in ('digital', 'text') else 40)
        self.reading.height = self._reading_height
        self.gauge.configure(mode, self.shown['low'], self.shown['high'], self.shown)
        self.stats_line.height = dp(STATS_HEIGHT) if _stats_on else 0
        self.stats_line.opacity = 1 if _stats_on else 0
        # what this display needs: name, number, stats line, picture, and the card's padding and gaps between the 5 children
        self.natural = (2 * GAP + self.name.height + self.reading.height + self.stats_line.height + height_for(mode)
                        + 4 * self.spacing)
        if self._cell:
            self._adapt()
        else:
            self.height = self.natural
        if isinstance(self.parent, GridLayout):
            Clock.schedule_once(lambda dt: equalize(self.parent) if self.parent else None, 0)
        self._show_reading()

    def fit_cell(self):
        """Fill a cell of a full-page layout (layout_ui.PageBoard sets the size) instead of keeping a height of
        its own. The picture takes the spare room, and a small cell drops the parts that do not fit."""
        self._cell = True
        self.size_hint = (None, None)
        self.padding = dp(8)
        self._adapt()

    def _adapt(self, *_):
        """Show as much as the cell allows (page_layout.detail_for decides) and stretch the picture to fill it."""
        if not self._cell or self.height <= 0:
            return
        mode = self.shown['mode']
        stats = dp(STATS_HEIGHT) if _stats_on else 0
        detail = page_layout.detail_for(self.height, dp(NAME_HEIGHT), self._reading_height, stats,
                                        min(height_for(mode), dp(24)), self.padding[1], self.spacing)
        line = detail == 'line'
        self.orientation = 'horizontal' if line else 'vertical'
        self.name.size_hint = (0.5, 1) if line else (1, None)
        self.reading.size_hint = (0.5, 1) if line else (1, None)
        if not line:                          # a side by side card lets the layout size them; put the heights back
            self.name.height, self.reading.height = dp(NAME_HEIGHT), self._reading_height
        show_picture = detail in ('full', 'no_stats')
        self._part(self.stats_line, detail == 'full' and _stats_on, stats)
        self._part(self.gauge, show_picture, None)
        self._part(self._spacer, not (show_picture or line), None)

    @staticmethod
    def _part(widget, shown, height):
        """One part of a card in a cell: a fixed height, or None to take the spare room, or nothing at all."""
        widget.opacity = 1 if shown else 0
        if not shown:
            widget.size_hint, widget.size = (None, None), (0, 0)
        elif height is None:
            widget.size_hint = (1, 1)
        else:
            widget.size_hint, widget.height = (1, None), height

    def reset_stats(self):
        self.stats.reset()
        self._show_reading()

    def show(self, reading, series, idle=None, note=None):
        """`note` is a sensor fault (the reading is outside its sensor's window). It replaces the number, because
        the number is not valid, and is shown in the alert colour."""
        self._note = note
        if note:
            reading = None
        self._reading, self._series, self._idle = reading, list(series)[-HISTORY:], note or idle
        if reading is not None:
            self.stats.add(reading[0])
        self._show_reading()

    def _show_reading(self):
        """Put the latest reading on the card: converted to the user's units, coloured by its band."""
        reading, convert = self._reading, self.shown['convert']
        if reading is None:
            if self._idle:
                self.value.text = self._idle
                self.value.color = ALERT if self._note else MUTED
            else:
                self.value.text, self.value.color = 'no reply', ALERT
            self.value.font_size = dp(16) if self._idle and len(self._idle) > 8 else self._number_size
            self.unit.text = ''
            self.stats_line.text = ''
            self.gauge.update(None, [])
            return
        self.value.font_size = self._number_size
        value = convert(reading[0])
        number, _unit = format_value(value, reading[1])
        self.value.text = number
        self.value.color = ZONE_TEXT.get(pid_view.zone(value, self.shown), pid_view.rgba(self.shown.get('color')) or TEXT)
        self.unit.text = self.shown['unit'] or reading[1]
        low, high, average = (None if x is None else convert(x) for x in (self.stats.low, self.stats.high,
                                                                          self.stats.average))
        self.stats_line.text = (f'{short(low)}\u2013{short(high)}  avg {short(average)}'
                                if _stats_on and self.stats.count > 1 else '')
        marks = (low, high) if _stats_on and self.stats.count > 1 else (None, None)
        self.gauge.update(value, [convert(v) for v in self._series], marks)

    # --- touches ---------------------------------------------------------------------------------

    def on_press(self):
        self._fired = False
        self._cancel(self._long)
        self._long = Clock.schedule_once(self._long_press, LONG_PRESS_SECONDS)

    def _state_changed(self, _card, state):
        if state == 'normal':
            self._cancel(self._long)

    def on_release(self):
        self._cancel(self._long)
        if self._fired:
            self._fired = False
            return
        self._taps += 1
        self._cancel(self._pending)
        self._pending = Clock.schedule_once(self._resolve, TAP_WINDOW_SECONDS)

    @staticmethod
    def _cancel(event):
        if event is not None:
            event.cancel()

    def _long_press(self, _dt):
        self._fired = True
        self._taps = 0
        self._cancel(self._pending)
        self.open_menu()

    def _resolve(self, _dt):
        taps, self._taps = self._taps, 0
        if taps >= 3:
            if hooks.on_help is not None:
                hooks.on_help(self.pid)
        else:
            self.choose_display()

    def _edited(self):
        self.apply_view()
        hooks.on_changed()

    # --- the sensor menu -------------------------------------------------------------------------

    def open_menu(self):
        SensorMenu(self).open()

    def edit(self):
        if hooks.on_edit is not None:
            hooks.on_edit(self.pid, self._edited)

    def ask_agent(self):
        if hooks.on_help is not None:
            hooks.on_help(self.pid)

    # --- choosing the display --------------------------------------------------------------------

    def choose_display(self):
        if hooks.views is None:
            return
        popup = ModalView(size_hint=(0.86, None), height=dp(520), background_color=(0, 0, 0, 0.6))
        box = Card()
        box.add_widget(section_title(self.shown['name']))
        box.add_widget(panel_label('How should this sensor be shown?', color=MUTED, font_size=dp(13)))
        for mode in pid_view.MODES:
            box.add_widget(make_button(pid_view.MODE_NAMES[mode],
                                       lambda m=mode: self._pick(popup, m), primary=mode == self.shown['mode']))
        box.add_widget(make_button('Zones, colour, name and range...', lambda: self._edit_from(popup)))
        box.add_widget(make_button('Reset lowest, highest and average', lambda: self._reset_from(popup)))
        popup.add_widget(box)
        popup.open()

    def _pick(self, popup, mode):
        hooks.views.update(self.pid.pid, mode=mode)
        popup.dismiss()
        self.apply_view()

    def _reset_from(self, popup):
        popup.dismiss()
        self.reset_stats()

    def _edit_from(self, popup):
        popup.dismiss()
        self.edit()


def _greyed(button):
    """A button that cannot be used right now."""
    button.disabled = True
    button.opacity = 0.45
    return button


class SensorMenu(ModalView):
    """The long-press menu of one sensor. Moves are worked out by dashboard_layout.reorder on the arranged ids
    of the screen the card is on, and handed to `hooks.on_order`, which saves them and redraws Live and Scan.

    A move stays inside the sensor's group (TCM, ECU...), because the dashboard always sorts by group first. A
    button that would change nothing is greyed out."""

    def __init__(self, card, **kwargs):
        super().__init__(size_hint=(0.88, 0.92), background_color=(0, 0, 0, 0.6), **kwargs)
        self.card = card
        pid = card.pid
        self.group = dashboard_layout.group_of(pid)
        self.arranged = list(hooks.arranged(card.scope)) if hooks.arranged is not None else []
        self.scan_order = (list(hooks.arranged('scan')) if hooks.arranged is not None else [])
        box = Card()
        box.add_widget(section_title(card.shown['name']))
        box.add_widget(panel_label(self.where(), color=MUTED, font_size=dp(12)))
        box.add_widget(make_button('Settings, zones and colour...', lambda: self._then(card.edit)))
        box.add_widget(make_button('Display: text, digital, graph, histogram, analogue...',
                                   lambda: self._then(card.choose_display)))
        box.add_widget(panel_label(f'Moves within {self.group}', color=MUTED, font_size=dp(12)))
        box.add_widget(button_row(self._move_button('Move earlier', 'earlier'), self._move_button('Move later', 'later')))
        box.add_widget(button_row(self._move_button('Move to top', 'top'), self._move_button('Move to end', 'end')))
        pages = self.reachable_pages()
        more = make_button('Move to page...', self.choose_page)
        box.add_widget(more if pages else _greyed(more))
        layout = make_button('Page layout...', lambda: self._then(lambda: hooks.on_layout(card.scope)))
        box.add_widget(layout if hooks.on_layout is not None else _greyed(layout))
        box.add_widget(make_button('Reset lowest, highest and average', lambda: self._then(card.reset_stats)))
        box.add_widget(make_button('Ask my AI agent', lambda: self._then(card.ask_agent)))
        box.add_widget(make_button('Close', self.dismiss, primary=True))
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        scroll.add_widget(box)
        self.add_widget(scroll)

    def where(self):
        """Where the sensor sits now, in words."""
        size = dashboard_layout.PAGE_SIZE
        pid_id = self.card.pid.pid
        if self.card.scope == 'scan':
            spot = dashboard_layout.position(self.arranged, pid_id, size)
            if spot is not None:
                return f'Page {spot[0] + 1} of {len(dashboard_layout.pages(self.arranged, size))}, place {spot[1] + 1}.'
        elif pid_id in self.arranged:
            return f'Place {self.arranged.index(pid_id) + 1} of {len(self.arranged)} on the Live screen.'
        return ''

    def reachable_pages(self):
        """Pages of the Scan screen this sensor can be moved onto (pages are the Scan screen's)."""
        return dashboard_layout.reachable_pages(self.scan_order, self.card.pid.pid, dashboard_layout.PAGE_SIZE,
                                                group=dashboard_layout.group_of_id)

    def _move_button(self, text, action):
        button = make_button(text, lambda: self.move(action))
        changed = dashboard_layout.reorder(self.arranged, self.card.pid.pid, action) != self.arranged
        return button if changed else _greyed(button)

    def _then(self, action):
        self.dismiss()
        action()

    def move(self, action, value=None, scope=None):
        """Do one move and close. `scope` 'scan' moves on the Scan screen's order whatever screen this card is on."""
        self.dismiss()
        scope = scope or self.card.scope
        order = self.scan_order if scope == 'scan' else self.arranged
        moved = dashboard_layout.reorder(order, self.card.pid.pid, action, value, dashboard_layout.PAGE_SIZE)
        if moved != order and hooks.on_order is not None:
            hooks.on_order(moved, scope)

    def choose_page(self):
        """A second popup: one button per page of the Scan screen. Pages with none of this sensor's group are greyed."""
        self.dismiss()
        reachable = self.reachable_pages()
        size = dashboard_layout.PAGE_SIZE
        popup = ModalView(size_hint=(0.86, 0.8), background_color=(0, 0, 0, 0.6))
        box = Card()
        box.add_widget(section_title('Move to page'))
        box.add_widget(panel_label(f'The sensor goes to the end of the page, among the {self.group} sensors. Pages '
                                   f'with no {self.group} sensor are greyed out.', color=MUTED, font_size=dp(12)))
        for page in range(len(dashboard_layout.pages(self.scan_order, size))):
            def pick(page=page):
                popup.dismiss()
                self.move('page', page, scope='scan')
            button = make_button(f'Page {page + 1}', pick)
            box.add_widget(button if page in reachable else _greyed(button))
        box.add_widget(make_button('Close', popup.dismiss, primary=True))
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        scroll.add_widget(box)
        popup.add_widget(scroll)
        popup.open()
