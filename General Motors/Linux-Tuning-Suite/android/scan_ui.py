"""The Scan screen: a live dashboard, stored codes and the traffic log. Ported from the VE CALAIS Scanner.

It reads from the shared Session, which is either the demo drive or a connected adapter. It only
reads: there is no clear-codes action in this app.
"""

import threading
from collections import deque

from kivy.clock import Clock
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from link import obd
from scanner import pids
from ui_kit import (ACCENT, ALERT, BLUE, BORDER, GAP, MUTED, TEXT, Card, button_row, make_button,
                    panel_label, section_title, stack, style_button)

VIEWS = ('Live', 'Codes', 'Log')
HISTORY = 60
CARD_HEIGHT = dp(132)


def format_value(value, unit):
    """Readable number for a card: whole numbers when large, more digits when small."""
    shown = f'{value:.0f}' if abs(value) >= 100 else (f'{value:.1f}' if abs(value) >= 10 else f'{value:.2f}')
    return shown, unit


class Gauge(Widget):
    """A thin bar showing where a value sits between its low and high limits, or a sparkline."""

    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=dp(34), **kwargs)
        self.fraction = 0.0
        self.series = []
        self.graph = False
        self.bind(pos=self._draw, size=self._draw)

    def update(self, fraction, series, graph):
        self.fraction, self.series, self.graph = fraction, series, graph
        self._draw()

    def _draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*BORDER)
            RoundedRectangle(pos=(self.x, self.center_y - dp(4)), size=(self.width, dp(8)), radius=[dp(4)])
            if self.graph and len(self.series) > 1:
                low, high = min(self.series), max(self.series)
                span = max(high - low, 1e-9)
                step = self.width / (HISTORY - 1)
                points = []
                for i, v in enumerate(self.series):
                    points += [self.x + i * step, self.y + dp(3) + (self.height - dp(6)) * (v - low) / span]
                Color(*BLUE)
                Line(points=points, width=dp(1.6))
            else:
                Color(*ACCENT)
                RoundedRectangle(pos=(self.x, self.center_y - dp(4)),
                                 size=(max(self.width * min(max(self.fraction, 0.0), 1.0), dp(8)), dp(8)),
                                 radius=[dp(4)])


class PidCard(ButtonBehavior, Card):
    """One reading. Tap to switch between the bar and a short history graph."""

    def __init__(self, pid, **kwargs):
        super().__init__(size_hint_y=None, height=CARD_HEIGHT, spacing=dp(2), **kwargs)
        self.pid = pid
        self.graph = False
        flag = '' if pid.verified else '  (unconfirmed)'
        self.name = Label(text=pid.name + flag, color=MUTED if pid.verified else ALERT, font_size=dp(12),
                          halign='left', valign='middle', size_hint_y=None, height=dp(30), shorten=True,
                          shorten_from='right')
        self.name.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
        self.value = Label(text='--', color=TEXT, bold=True, font_size=dp(24), halign='left',
                           valign='middle', size_hint_x=None, width=dp(40))
        self.value.bind(texture_size=lambda w, size: setattr(w, 'width', size[0]))
        self.unit = Label(text='', color=MUTED, font_size=dp(12), halign='left', valign='middle')
        self.unit.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
        reading = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        reading.add_widget(self.value)
        reading.add_widget(self.unit)
        self.gauge = Gauge()
        for widget in (self.name, reading, self.gauge):
            self.add_widget(widget)

    def _fit_height(self, *_):
        pass   # the dashboard grid gives every card the same fixed height

    def on_release(self):
        self.graph = not self.graph

    def show(self, reading, series):
        if reading is None:
            self.value.text, self.value.color = 'no reply', ALERT
            self.unit.text = ''
            self.gauge.update(0.0, [], self.graph)
            return
        number, unit = format_value(*reading)
        self.value.text, self.value.color = number, TEXT
        self.unit.text = unit
        span = max(self.pid.high - self.pid.low, 1e-9)
        self.gauge.update((reading[0] - self.pid.low) / span, list(series), self.graph)


class ScanScreen(BoxLayout):
    def __init__(self, session, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.session = session
        self.pages = pids.monitor_pages()
        self.page = 0
        self.view = 'Live'
        self.history = {}
        self.cards = []
        self.busy = False
        self._event = None
        self.codes_text = 'Tap Read codes to ask the engine computer for stored trouble codes.'
        self.tabs = {}
        bar = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8), padding=(GAP, dp(6), GAP, 0))
        for name in VIEWS:
            button = style_button(Button(text=name))
            button.bind(on_release=lambda _b, n=name: self.set_view(n))
            self.tabs[name] = button
            bar.add_widget(button)
        self.body = BoxLayout()
        self.add_widget(bar)
        self.add_widget(self.body)
        self.set_view('Live')

    # --- lifecycle -------------------------------------------------------------------------------

    def activate(self):
        if self._event is None:
            self._event = Clock.schedule_interval(self.tick, 1.0)
        self.tick(0)

    def deactivate(self):
        if self._event is not None:
            self._event.cancel()
            self._event = None

    def source_changed(self, _status=None):
        self.render()

    # --- views -----------------------------------------------------------------------------------

    def set_view(self, name):
        self.view = name
        for key, button in self.tabs.items():
            style_button(button, primary=(key == name))
        self.render()

    def render(self):
        self.body.clear_widgets()
        self.cards = []
        if self.session.active() is None and self.view != 'Log':
            self.body.add_widget(self._empty_state())
        elif self.view == 'Live':
            self.body.add_widget(self._live_view())
        elif self.view == 'Codes':
            self.body.add_widget(self._codes_view())
        else:
            self.body.add_widget(self._log_view())
        self.tick(0)

    def _empty_state(self):
        card = Card()
        card.add_widget(section_title('No data source'))
        card.add_widget(panel_label('Turn on Demo mode to see simulated readings with no adapter, or '
                                    'connect a scan adapter on the Link tab.', color=MUTED))
        card.add_widget(make_button('Start demo', lambda: self.session.set_demo(True), primary=True))
        return stack(card)

    def _live_view(self):
        page = self.pages[self.page]
        title = panel_label(f'Page {self.page + 1} of {len(self.pages)}', color=MUTED, halign='center')
        controls = button_row(make_button('Previous', lambda: self.turn(-1)),
                              make_button('Next', lambda: self.turn(1)))
        grid = GridLayout(cols=2, spacing=GAP, size_hint_y=None, height=2 * CARD_HEIGHT + GAP)
        for pid in page:
            card = PidCard(pid)
            self.cards.append(card)
            grid.add_widget(card)
        hint = panel_label('Tap a card to switch between the bar and a graph. Readings marked '
                           'unconfirmed have not been checked against a real vehicle.', color=MUTED,
                           font_size=dp(12))
        return stack(title, controls, grid, hint)

    def _codes_view(self):
        self.codes_label = panel_label(self.codes_text)
        card = Card()
        card.add_widget(section_title('Stored trouble codes'))
        card.add_widget(self.codes_label)
        note = panel_label('Read only: this app reads codes but never clears them. Clearing also resets '
                           "the car's readiness monitors, so do it with a dedicated scan tool.",
                           color=MUTED, font_size=dp(12))
        return stack(make_button('Read codes', self.read_codes, primary=True), card, note)

    def _log_view(self):
        source = self.session.active()
        lines = [f'{d}  {t}' for d, t in (source.traffic if source is not None else [])][-30:]
        self.log_label = panel_label('\n'.join(lines) or 'Nothing has been sent yet.', font_size=dp(12),
                                     color=MUTED)
        card = Card()
        card.add_widget(section_title('Traffic'))
        card.add_widget(self.log_label)
        return stack(card)

    def turn(self, step):
        self.page = (self.page + step) % len(self.pages)
        self.render()

    # --- reading ---------------------------------------------------------------------------------

    def tick(self, _dt):
        source = self.session.active()
        if source is None or self.busy:
            return
        if self.view == 'Live' and self.cards:
            ids = [card.pid.pid for card in self.cards]
            self.busy = True
            threading.Thread(target=self._poll, args=(source, ids), daemon=True).start()
        elif self.view == 'Log':
            lines = [f'{d}  {t}' for d, t in source.traffic][-30:]
            self.log_label.text = '\n'.join(lines) or 'Nothing has been sent yet.'

    def _poll(self, source, ids):
        try:
            values, errors = source.poll(ids)
        except obd.OBDError as exc:
            values, errors = {}, {i: str(exc) for i in ids}
        Clock.schedule_once(lambda dt: self._show(values, errors))

    def _show(self, values, _errors):
        self.busy = False
        for card in self.cards:
            reading = values.get(card.pid.pid)
            series = self.history.setdefault(card.pid.pid, deque(maxlen=HISTORY))
            if reading is not None:
                series.append(reading[0])
            card.show(reading, series)

    def read_codes(self):
        source = self.session.active()
        if source is None or self.busy:
            return
        self.busy = True
        self.codes_label.text = 'Reading...'
        threading.Thread(target=self._read_codes, args=(source,), daemon=True).start()

    def _read_codes(self, source):
        try:
            codes = source.read_dtcs()
            text = ('  '.join(codes) if codes else 'No stored codes.')
            if source.label == 'Demo':
                text += '\n\nDemo data: these sample codes are not from a car.'
        except obd.OBDError as exc:
            text = str(exc)

        def done(_dt):
            self.busy = False
            self.codes_text = text
            if self.view == 'Codes':
                self.codes_label.text = text

        Clock.schedule_once(done)
