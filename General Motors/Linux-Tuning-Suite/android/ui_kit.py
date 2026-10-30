"""Shared look for every screen: colours, one corner radius, one gap, cards, chips, buttons.

Keeping these in one place is what keeps the border width, spacing and scale the same on every screen.
"""

import os

from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import SpinnerOption
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(HERE, 'icons')

# A dark instrument look: amber for the main values, blue for the second trace.
BG = (0.067, 0.086, 0.110, 1)
PANEL = (0.110, 0.137, 0.169, 1)
RAISED = (0.145, 0.176, 0.212, 1)
BORDER = (0.20, 0.25, 0.31, 1)
TEXT = (1.0, 1.0, 1.0, 1)
MUTED = (0.74, 0.79, 0.84, 1)
ACCENT = (0.96, 0.65, 0.14, 1)
BLUE = (0.47, 0.78, 1.0, 1)
ALERT = (1.0, 0.45, 0.40, 1)
GOOD = (0.40, 0.80, 0.55, 1)
CAUTION = (1.0, 0.85, 0.25, 1)

# Green, yellow and red for grades. The same colours as the table text in table_view.py.
STATUS = {'good': GOOD, 'ok': CAUTION, 'bad': ALERT, 'off': (0.42, 0.46, 0.52, 1)}

RADIUS = dp(12)
GAP = dp(12)
BORDER_WIDTH = dp(1)
BODY = dp(14)


def icon(name):
    return os.path.join(ICON_DIR, f'{name}.png')


class WrapOption(SpinnerOption):
    """A dropdown row that wraps long text instead of clipping it at the edges."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = RAISED
        self.color = TEXT
        self.font_size = dp(15)
        self.halign = 'center'
        self.valign = 'middle'
        self.size_hint_y = None
        self.height = dp(56)
        self.bind(width=lambda w, _: setattr(w, 'text_size', (w.width - dp(16), None)))


def style_button(button, primary=False):
    button.background_normal = ''
    button.background_down = ''
    button.background_color = ACCENT if primary else RAISED
    button.color = BG if primary else TEXT
    button.size_hint_y = None
    button.height = dp(48)
    button.font_size = BODY
    button.halign = 'center'
    button.valign = 'middle'
    button.bind(size=lambda w, _: setattr(w, 'text_size', (w.width - dp(12), None)))
    return button


def panel_label(text='', **kwargs):
    kwargs.setdefault('color', TEXT)
    kwargs.setdefault('halign', 'left')
    kwargs.setdefault('font_size', BODY)
    label = Label(text=text, size_hint_y=None, valign='top', **kwargs)
    label.bind(width=lambda w, _: setattr(w, 'text_size', (w.width, None)))
    label.bind(texture_size=lambda w, size: setattr(w, 'height', size[1]))
    return label


def section_title(text):
    label = Label(text=text, color=ACCENT, size_hint_y=None, height=dp(30), halign='left',
                  valign='middle', bold=True, font_size=dp(16))
    label.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
    return label


class Card(BoxLayout):
    """A rounded panel with a 1 dp border. Grows to fit what is inside it."""

    def __init__(self, fill=PANEL, border=BORDER, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('padding', GAP)
        kwargs.setdefault('spacing', dp(8))
        kwargs.setdefault('size_hint_y', None)
        super().__init__(**kwargs)
        self._fill = fill
        self._border = border
        self.bind(minimum_height=self._fit_height, pos=self._draw, size=self._draw)

    def _fit_height(self, _widget, value):
        if self.size_hint_y is None:
            self.height = value

    def set_border(self, colour):
        """Change the outline colour (for example to a grade colour). Width and corners stay the same."""
        self._border = colour
        self._draw()

    def _draw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self._fill)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[RADIUS])
            Color(*self._border)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, RADIUS), width=BORDER_WIDTH)


class Chip(Label):
    """A small rounded status label, for example DEMO, LIVE or OFFLINE."""

    def __init__(self, text='', colour=MUTED, **kwargs):
        super().__init__(text=text, bold=True, font_size=dp(11), color=BG, size_hint=(1, None),
                         height=dp(24), **kwargs)
        self._colour = colour
        self.bind(pos=self._draw, size=self._draw)

    def set_state(self, text, colour):
        self.text, self._colour = text, colour
        self._draw()

    def _draw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self._colour)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height / 2])


class MenuButton(ButtonBehavior, Widget):
    """Three bars that open the menu. Drawn, so it does not depend on a font having a symbol."""

    def __init__(self, on_press_cb, **kwargs):
        super().__init__(size_hint_x=None, width=dp(48), **kwargs)   # a full-size thumb target, whatever the screen width
        self._cb = on_press_cb
        with self.canvas:
            Color(*TEXT)
            self._bars = [Line(points=[0, 0, 0, 0], width=dp(1.6)) for _ in range(3)]
        self.bind(pos=self._place, size=self._place)

    def _place(self, *_):
        left, right = self.x + dp(6), self.right - dp(6)
        for i, bar in enumerate(self._bars):
            y = self.center_y + (1 - i) * dp(7)
            bar.points = [left, y, right, y]

    def on_release(self):
        self._cb()


class HeaderBar(BoxLayout):
    """The title strip at the top of every screen: app name, screen name, and the data-source chip."""

    def __init__(self, on_menu=None, on_rec=None, **kwargs):
        super().__init__(size_hint_y=None, height=dp(64), padding=(dp(10), dp(8)), spacing=dp(4), **kwargs)
        titles = BoxLayout(orientation='vertical', size_hint_x=0.39)
        self.app_name = Label(text='TunerToolPro', bold=True, font_size=dp(16), color=TEXT, halign='left',
                              valign='bottom', shorten=True, shorten_from='right')
        self.screen_name = Label(text='', font_size=dp(11), color=MUTED, halign='left', valign='top',
                                 shorten=True, shorten_from='right')
        for label in (self.app_name, self.screen_name):
            label.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
            titles.add_widget(label)
        self.chip = Chip('OFFLINE')
        holder = BoxLayout(size_hint_x=0.23, padding=(0, dp(13)))
        holder.add_widget(self.chip)
        self.add_widget(titles)
        self.add_widget(holder)
        self.rec = None
        if on_rec is not None:
            slot = BoxLayout(size_hint_x=0.22, padding=(0, dp(11)))
            self.rec = RecButton(on_rec)
            slot.add_widget(self.rec)
            self.add_widget(slot)
        if on_menu is not None:
            self.add_widget(MenuButton(on_menu))
        self.canvas.after.clear()
        with self.canvas.after:
            Color(*BORDER)
            self._rule = Line(points=[0, 0, 0, 0], width=BORDER_WIDTH)
        # The car sits faintly behind the title, so it fits whatever the screen width.
        logo = CoreImage(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo_car.png'))
        self._car_ratio = logo.width / logo.height
        with self.canvas.before:
            Color(1, 1, 1, 0.42)
            self._car = Rectangle(texture=logo.texture, pos=self.pos, size=(0, 0))
        self.bind(x=self._place_car, y=self._place_car, width=self._place_car, height=self._place_car)
        self.bind(x=self._place_rule, y=self._place_rule, width=self._place_rule, height=self._place_rule)

    def _place_car(self, *_):
        width = min(self.width - 2 * GAP, (self.height - dp(10)) * self._car_ratio)
        height = width / self._car_ratio
        self._car.size = (width, height)
        self._car.pos = (self.x + GAP, self.y + (self.height - height) / 2)

    def _place_rule(self, *_):
        self._rule.points = [self.x, self.y, self.x + self.width, self.y]

    def set_screen(self, title):
        self.screen_name.text = title

    def set_recording(self, text):
        if self.rec is not None:
            self.rec.set_recording(text)

    def set_source(self, status):
        colour = {'DEMO': ACCENT, 'LIVE': GOOD}.get(status, MUTED)
        self.chip.set_state(status, colour)


def stack(*widgets, spacing=GAP, padding=GAP):
    """Widgets in a scrollable column that grows with its content."""
    column = GridLayout(cols=1, size_hint_y=None, spacing=spacing, padding=padding)
    column.bind(minimum_height=column.setter('height'))
    for widget in widgets:
        column.add_widget(widget)
    scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
    scroll.add_widget(column)
    return scroll


class RecButton(ButtonBehavior, Label):
    """The record button in the header: grey REC when idle, a red dot and the running time while recording."""

    def __init__(self, on_press_cb, **kwargs):
        super().__init__(text='REC', bold=True, font_size=dp(12), color=TEXT, size_hint=(1, None),
                         height=dp(30), **kwargs)
        self._cb = on_press_cb
        self._colour = RAISED
        self.bind(pos=self._draw, size=self._draw)

    def set_recording(self, text):
        """text is the running time while recording, or None when idle."""
        self.text = 'REC' if text is None else f'REC {text}'
        self._colour = RAISED if text is None else (0.35, 0.12, 0.12, 1)
        self._draw()

    def _draw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self._colour)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height / 2])
            Color(*BORDER)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, self.height / 2), width=BORDER_WIDTH)

    def on_release(self):
        self._cb()


def hide(widget, hidden):
    """Take a widget out of sight and out of the layout (height 0), or put it back as it was."""
    if hidden and not hasattr(widget, '_shown_as'):
        widget._shown_as = (widget.size_hint_y, widget.height, widget.opacity, widget.disabled)
        widget.size_hint_y, widget.height, widget.opacity, widget.disabled = None, 0, 0, True
    elif not hidden and hasattr(widget, '_shown_as'):
        widget.size_hint_y, widget.height, widget.opacity, widget.disabled = widget._shown_as
        del widget._shown_as


def toggle(text, state, on_change):
    """An on/off button that lights up while on. `on_change` is called with True or False."""
    button = ToggleButton(text=text, size_hint_y=None, height=dp(44), state='down' if state else 'normal')
    style_button(button, primary=state)

    def changed(_button, new_state):
        style_button(button, primary=new_state == 'down')
        button.height = dp(44)
        on_change(new_state == 'down')
    button.bind(state=changed)
    return button


def button_row(*buttons, height=dp(48)):
    row = BoxLayout(size_hint_y=None, height=height, spacing=dp(8))
    for button in buttons:
        row.add_widget(button)
    return row


def make_button(text, on_release, primary=False):
    button = style_button(Button(text=text), primary=primary)
    button.bind(on_release=lambda *_: on_release())
    return button
