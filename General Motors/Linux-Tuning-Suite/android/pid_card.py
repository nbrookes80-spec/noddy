"""One sensor on the Live and Scan screens, and what you can do to it.

  tap          choose how it is drawn: text, digital gauge, graph, histogram or analogue gauge
  long press   edit it: name, unit, range, red line (and the equation and module of a PID you entered)
  triple tap   ask your AI agent about this sensor

`hooks` is set once by the app. It holds the saved display choices and the two actions that need the rest of
the app (editing and asking the agent), so a card can be built anywhere without being handed them.
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
from kivy.uix.widget import Widget

from gauge_ui import GaugeView, height_for
from scanner import pid_view
from ui_kit import ALERT, MUTED, TEXT, Card, make_button, panel_label, section_title

HISTORY = 120
LONG_PRESS_SECONDS = 0.6
TAP_WINDOW_SECONDS = 0.4     # taps this close together count as one gesture (triple tap = ask the agent)


class Hooks:
    def __init__(self):
        self.views = None            # pid_view.PidViews
        self.on_edit = None          # callable(pid, done): open the editor for a sensor
        self.on_help = None          # callable(pid): bring the AI agent in on a sensor
        self.on_changed = lambda: None


hooks = Hooks()

_grids = weakref.WeakSet()
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


def format_value(value, unit):
    """Readable number for a card: whole numbers when large, more digits when small."""
    shown = f'{value:.0f}' if abs(value) >= 100 else (f'{value:.1f}' if abs(value) >= 10 else f'{value:.2f}')
    return shown, unit


class PidCard(ButtonBehavior, Card):
    def __init__(self, pid, **kwargs):
        super().__init__(size_hint_y=None, spacing=dp(2), **kwargs)
        self.pid = pid
        self.shown = {}
        self._reading = None
        self._series = []
        self._taps = 0
        self._long = self._pending = None
        self._fired = False
        self.name = Label(color=MUTED, font_size=dp(12), halign='left', valign='middle', size_hint_y=None,
                          height=dp(26), shorten=True, shorten_from='right')
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
        self.gauge = GaugeView()
        for widget in (self.name, self.reading, self.gauge):
            self.add_widget(widget)
        self.bind(state=self._state_changed)
        self.apply_view()

    def _fit_height(self, *_):
        pass   # the height is set from the chosen display in apply_view

    # --- how it looks ----------------------------------------------------------------------------

    def apply_view(self):
        """Take the saved choices for this sensor (name, unit, range, red line, display) and redraw."""
        views = hooks.views
        self.shown = views.apply(self.pid) if views is not None else {
            'name': self.pid.name, 'unit': self.pid.unit, 'low': self.pid.low, 'high': self.pid.high,
            'redline': None, 'mode': pid_view.DEFAULT_MODE}
        mode = self.shown['mode']
        flag = '' if self.pid.verified else '  (unconfirmed)'
        self.name.text = self.shown['name'] + flag
        self.name.color = MUTED if self.pid.verified else ALERT
        self.value.font_size = dp(28 if mode in ('digital', 'text') else 22)
        self.reading.height = dp(52 if mode in ('digital', 'text') else 40)
        self.gauge.configure(mode, self.shown['low'], self.shown['high'], self.shown['redline'])
        self.natural = dp(26 + 2 * 12) + self.reading.height + height_for(mode)   # what this display needs
        self.height = self.natural
        if isinstance(self.parent, GridLayout):
            Clock.schedule_once(lambda dt: equalize(self.parent) if self.parent else None, 0)
        self.show(self._reading, self._series)

    def show(self, reading, series):
        self._reading, self._series = reading, list(series)[-HISTORY:]
        if reading is None:
            self.value.text, self.value.color = 'no reply', ALERT
            self.unit.text = ''
            self.gauge.update(None, [])
            return
        number, _unit = format_value(*reading)
        redline = self.shown.get('redline')
        self.value.text = number
        self.value.color = ALERT if redline is not None and reading[0] >= redline else TEXT
        self.unit.text = self.shown['unit'] or reading[1]
        self.gauge.update(reading[0], self._series)

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
        if hooks.on_edit is not None:
            hooks.on_edit(self.pid, self._edited)

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

    # --- choosing the display --------------------------------------------------------------------

    def choose_display(self):
        if hooks.views is None:
            return
        popup = ModalView(size_hint=(0.86, None), height=dp(470), background_color=(0, 0, 0, 0.6))
        box = Card()
        box.add_widget(section_title(self.shown['name']))
        box.add_widget(panel_label('How should this sensor be shown?', color=MUTED, font_size=dp(13)))
        for mode in pid_view.MODES:
            box.add_widget(make_button(pid_view.MODE_NAMES[mode],
                                       lambda m=mode: self._pick(popup, m), primary=mode == self.shown['mode']))
        box.add_widget(make_button('Red line, name and range...', lambda: self._edit_from(popup)))
        popup.add_widget(box)
        popup.open()

    def _pick(self, popup, mode):
        hooks.views.update(self.pid.pid, mode=mode)
        popup.dismiss()
        self.apply_view()

    def _edit_from(self, popup):
        popup.dismiss()
        if hooks.on_edit is not None:
            hooks.on_edit(self.pid, self._edited)
