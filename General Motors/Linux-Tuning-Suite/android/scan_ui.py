"""The Scan screen: a live dashboard, stored codes and the traffic log. Ported from the VE CALAIS Scanner.

It reads from the shared Session, which is either the demo drive or a connected adapter. It only
reads: there is no clear-codes action in this app.
"""

import threading
from collections import deque

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from link import obd
from pid_card import HISTORY, PidCard, equalize, fit_columns
from scanner import pids
from ui_kit import GAP, hide, MUTED, Card, button_row, make_button, panel_label, section_title, stack, style_button

VIEWS = ('Live', 'Codes', 'Log')


class ScanScreen(BoxLayout):
    def __init__(self, session, on_fullscreen=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.session = session
        self.on_fullscreen = on_fullscreen
        self.pages = [[]]
        self.page = 0
        self.view = 'Live'
        self.history = {}
        self.cards = []
        self.busy = False
        self.full = False
        self.chrome = []
        self._event = None
        self.codes_text = 'Tap Read codes to ask the engine computer for stored trouble codes.'
        self.tabs = {}
        bar = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8), padding=(GAP, dp(6), GAP, 0))
        for name in VIEWS:
            button = style_button(Button(text=name))
            button.bind(on_release=lambda _b, n=name: self.set_view(n))
            self.tabs[name] = button
            bar.add_widget(button)
        self.bar = bar
        self.body = BoxLayout()
        self.add_widget(bar)
        self.add_widget(self.body)
        self.set_view('Live')

    # --- lifecycle -------------------------------------------------------------------------------

    def activate(self):
        for card in self.cards:
            card.apply_view()
        if self._event is None:
            self._event = Clock.schedule_interval(self.tick, 1.0)
        self.tick(0)

    def deactivate(self):
        if self._event is not None:
            self._event.cancel()
            self._event = None

    def source_changed(self, _status=None):
        self.render()

    def set_full(self, on):
        """Full screen: only the sensors of the current page, with the tabs put away."""
        self.full = on
        for widget in (self.bar, *self.chrome):
            hide(widget, on)

    # --- views -----------------------------------------------------------------------------------

    def set_view(self, name):
        self.view = name
        for key, button in self.tabs.items():
            style_button(button, primary=(key == name))
        self.render()

    def _refresh_pages(self):
        """Rebuild the dashboard pages from the active profile, so a car check or a new profile shows at once."""
        self.pages = pids.monitor_pages() or [[]]
        self.page = min(self.page, len(self.pages) - 1)

    def render(self):
        self._refresh_pages()
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
                              make_button('Next', lambda: self.turn(1)),
                              make_button('Full screen', lambda: self.on_fullscreen and self.on_fullscreen(True)))
        grid = GridLayout(spacing=GAP, size_hint_y=None)
        fit_columns(grid)
        grid.bind(minimum_height=grid.setter('height'))
        for pid in page:
            card = PidCard(pid)
            self.cards.append(card)
            grid.add_widget(card)
        Clock.schedule_once(lambda dt: equalize(grid), 0)
        hint = panel_label('Tap a sensor to choose how it is shown. Long press to edit it or set a red line. '
                           'Triple tap to ask your AI agent about it. Readings marked unconfirmed have not '
                           'been checked against a real vehicle.', color=MUTED, font_size=dp(12))
        self.chrome = [title, hint]
        scroll = stack(title, controls, grid, hint)
        for widget in self.chrome:
            hide(widget, self.full)
        return scroll

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
