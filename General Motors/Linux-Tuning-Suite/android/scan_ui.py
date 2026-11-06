"""The Scan screen: a live dashboard, stored codes and the traffic log. Ported from the VE CALAIS Scanner.

It reads from the shared Session, which is either the demo drive or a connected adapter. Clearing the
codes is offered only in builds that allow it (variant.CLEAR_CODES), and always asks first.
"""

import threading
from collections import deque

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

import variant
from tunertoolpro.link import obd
from layout_ui import FullPage
from pid_card import HISTORY, PidCard, equalize, fit_columns, hooks
from tunertoolpro.scanner import dashboard_layout, page_layout, pids, shift_light
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
        self.latest = {}          # the last poll's readings, {pid: (value, unit)}; the shift light takes RPM here
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
        self.latest = {}          # readings from an earlier visit are too old for the shift light
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
        """Full screen: only the sensors of the current page, placed by the page's layout, with the tabs put away."""
        changed = on != self.full
        self.full = on
        for widget in (self.bar, *self.chrome):
            hide(widget, on)
        if changed and self.view == 'Live':
            self.render()           # the page is drawn differently in full screen

    # --- views -----------------------------------------------------------------------------------

    def set_view(self, name):
        self.view = name
        for key, button in self.tabs.items():
            style_button(button, primary=(key == name))
        self.render()

    def sources(self):
        """Every dashboard sensor in the order they are listed before sorting."""
        return dashboard_layout.dashboard_pids()

    def arranged(self):
        """Every dashboard sensor in display order (the pages are cut from this)."""
        return dashboard_layout.arrange(self.sources())

    def _refresh_pages(self):
        """Rebuild the dashboard pages from the active profile, so a car check or a new profile shows at once."""
        self.pages = dashboard_layout.pages(self.arranged()) or [[]]
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

    def layout_target(self):
        """(page index, sensors on it) of the page the layout chooser is for."""
        return self.page, len(self.pages[self.page])

    def open_layout(self):
        if hooks.on_layout is not None:
            hooks.on_layout('scan')

    def _full_view(self):
        """The current page with its cards placed by the page's template (layout_ui.FullPage)."""
        cards = [PidCard(pid) for pid in self.pages[self.page]]
        self.cards.extend(cards)
        self.chrome = []
        return FullPage(cards, self.page, len(self.pages), page_layout.for_page(self.page), self.turn,
                        self.open_layout)

    def _live_view(self):
        if self.full:
            return self._full_view()
        page = self.pages[self.page]
        title = panel_label(f'Page {self.page + 1} of {len(self.pages)}', color=MUTED, halign='center')
        controls = button_row(make_button('Previous', lambda: self.turn(-1)),
                              make_button('Next', lambda: self.turn(1)),
                              make_button('Full screen', lambda: self.on_fullscreen and self.on_fullscreen(True)),
                              make_button('Page layout', self.open_layout))
        grid = BoxLayout(orientation='vertical', spacing=GAP, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for group, members in dashboard_layout.runs(page):
            grid.add_widget(panel_label(dashboard_layout.TITLES[group], color=MUTED, font_size=dp(12)))
            cards = GridLayout(spacing=GAP, size_hint_y=None)
            fit_columns(cards)
            cards.bind(minimum_height=cards.setter('height'))
            for pid in members:
                card = PidCard(pid)
                self.cards.append(card)
                cards.add_widget(card)
            Clock.schedule_once(lambda dt, g=cards: equalize(g), 0)
            grid.add_widget(cards)
        hint = panel_label('Tap a sensor to choose how it is shown. Long press for its menu: edit, move, reorder, '
                           'page layout (used in full screen). '
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
        if not variant.CLEAR_CODES:
            note = panel_label('Read only: this app reads codes but never clears them. Clearing also resets '
                               "the car's readiness monitors, so do it with a dedicated scan tool.",
                               color=MUTED, font_size=dp(12))
            return stack(make_button('Read codes', self.read_codes, primary=True), card, note)
        note = panel_label('Clearing deletes the stored codes and resets the car\'s readiness monitors. Until the '
                           'car has driven through its checks again, an emissions test can fail. Clear only after '
                           'the fault is fixed.', color=MUTED, font_size=dp(12))
        buttons = button_row(make_button('Read codes', self.read_codes, primary=True),
                             make_button('Clear codes', self.ask_clear))
        return stack(buttons, card, note)

    def ask_clear(self):
        """Ask before clearing: a clear is the one thing here that changes the car."""
        if self.session.active() is None or self.busy:
            return
        body = BoxLayout(orientation='vertical', spacing=GAP, padding=GAP)
        popup = Popup(title='Clear the stored codes?', content=body, size_hint=(0.92, None), height=dp(250))
        body.add_widget(panel_label('This deletes every stored code and resets the readiness monitors. Clear only '
                                    'after the fault is fixed.', color=MUTED))
        row = button_row(make_button('Cancel', popup.dismiss),
                         make_button('Clear codes', lambda: (popup.dismiss(), self.clear_codes()), primary=True))
        body.add_widget(row)
        popup.open()

    def clear_codes(self):
        source = self.session.active()
        if source is None or self.busy:
            return
        self.busy = True
        self.codes_label.text = 'Clearing...'
        threading.Thread(target=self._clear_codes, args=(source,), daemon=True).start()

    def _clear_codes(self, source):
        try:
            source.clear_dtcs()
            text = 'Codes cleared. Read codes again to check that none came back.'
            if source.label == 'Demo':
                text += '\n\nDemo data: the sample codes were cleared, not a car.'
        except obd.OBDError as exc:
            text = str(exc)

        def done(_dt):
            self.busy = False
            self.codes_text = text
            if self.view == 'Codes':
                self.codes_label.text = text

        Clock.schedule_once(done)

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

    def rpm_reading(self):
        """(whether this screen reads engine speed, the latest RPM or None), for the shift light over the screens.
        Only the Live view polls, and only the sensors on the page shown."""
        reads = self.view == 'Live' and any(card.pid.pid == shift_light.RPM_PID for card in self.cards)
        reading = self.latest.get(shift_light.RPM_PID) if reads else None
        return reads, None if reading is None else reading[0]

    def _show(self, values, _errors):
        self.busy = False
        self.latest = values
        for card in self.cards:
            reading = values.get(card.pid.pid)
            series = self.history.setdefault(card.pid.pid, deque(maxlen=HISTORY))
            if reading is not None:
                series.append(reading[0])
            idle = ('not in log' if reading is None and self.session.replay is not None
                    and card.pid.pid not in pids.REPLAY else None)    # a log is playing and does not carry it
            card.show(reading, series, idle=idle)

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
