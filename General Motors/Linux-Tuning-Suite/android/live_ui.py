"""The Live screen: the engine and transmission streaming together, with green, yellow and red health.

A StreamRunner reads in the background whenever there is a data source (the demo drive or a connected
adapter). Whether it may read is decided in one place, shift_light.runner_runs (applied by shift_overlay.py): on
the Live screen, and on the other screens while the shift light is on, but never on Scan (which polls the adapter
itself) or while the sniffer has the adapter, so two parts never talk to the adapter at once.
"""

import threading
import time

from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton

from tunertoolpro.link import obd
from tunertoolpro.live import HEALTH, STREAM_PIDS, TCM_PIDS, LiveStream
from layout_ui import FullPage
from pid_card import PidCard, equalize, fit_columns, hooks
from tunertoolpro.scanner import dashboard_layout, page_layout, pids
from tunertoolpro.scanner.bus_listen import bus_reader
from shift_light_ui import ShiftLight
from table_view import HEX
from ui_kit import (BG, hide, GAP, MUTED, STATUS, TEXT, Card, button_row, make_button, panel_label, section_title,
                    stack, style_button)

EXTRA_CHUNK = 4          # other sensors read per round while recording
BACKOFF_SECONDS = 1.0    # wait this long after a failed round before trying again


class StreamRunner:
    """Owns the LiveStream and the thread that keeps it reading."""

    def __init__(self, session, model):
        self.session = session
        self.model = model            # callable returning (cfg, tables), either may be None
        self.stream = None
        self.paused = False
        self.transmission = False     # reading the TCM too is a second conversation with the car, so it is opt-in
        self._source = None
        self.rate = None              # callable returning the saved most-rounds-per-second (obd.round_delay clamps it)
        self.extras = None            # callable returning more sensors to read while a data log is recording
        self._cursor = 0
        self._stop = threading.Event()
        self._thread = None
        self._idle = threading.Event()   # set while no round is under way
        self._idle.set()
        session.wait_reader = self.wait_idle   # a one-off adapter job (Session.adapter_job) waits for our round

    def start(self):
        if self._thread is None:
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._stop.set()

    def source_changed(self, _status=None):
        """Called when demo is switched on or off or an adapter connects. Starts a fresh stream."""
        source = self.session.active()
        if source is not self._source:
            self._source = source
            cfg, tables = self.model()
            self.stream = (LiveStream(source, cfg=cfg, tables=tables, transmission=self.transmission,
                                      bus=bus_reader(source))
                           if source is not None else None)

    def set_transmission(self, on):
        """Turn the TCM reads on or off. Takes effect on the next round."""
        self.transmission = bool(on)
        if self.stream is not None:
            self.stream.transmission = self.transmission

    def refresh_model(self):
        if self.stream is not None:
            self.stream.set_model(*self.model())

    def _read_extras(self):
        """While recording, also read the other dashboard sensors a few at a time, so the data log holds
        every sensor without slowing the Live readings much."""
        wanted = self.extras() if self.extras else []
        source = self.session.active()
        if not wanted or source is None:
            return
        count = min(EXTRA_CHUNK, len(wanted))
        chunk = [wanted[(self._cursor + i) % len(wanted)] for i in range(count)]
        self._cursor = (self._cursor + count) % len(wanted)
        try:
            source.poll(chunk)
        except Exception as exc:   # a lost adapter is caught by the next Live round
            self.session.log.write('ERR', f'data log extras: {type(exc).__name__}: {exc}')

    def wait_idle(self, timeout):
        """Wait until no round is under way, so a part taking the adapter (the sniffer) starts after the reader's
        last command, not in the middle of its round. Set `paused` first. True if idle within `timeout` seconds."""
        return self._idle.wait(timeout)

    def _loop(self):
        while not self._stop.is_set():
            self._idle.clear()             # before `paused` is read, so wait_idle cannot miss a round starting
            stream, began = self.stream, time.monotonic()
            if stream is None or self.paused or self.session.adapter_busy:   # adapter_busy: a one-off job has it
                self._idle.set()
                time.sleep(0.2)
                continue
            try:
                stream.step()
            except Exception as exc:   # one bad round must not end the reader for good
                stream.error = f'{type(exc).__name__}: {exc}'
                self.session.log.write('ERR', f'live reader: {stream.error}')
            if not stream.error:
                self._read_extras()
            self._idle.set()
            wait = obd.round_delay(self.rate() if self.rate else None) - (time.monotonic() - began)
            time.sleep(BACKOFF_SECONDS if stream.error else max(0.0, wait))


class HealthTile(Card):
    """One health check: what it is, and what it reads, in the colour of its grade."""

    def __init__(self, label, **kwargs):
        super().__init__(size_hint_y=None, height=dp(66), spacing=dp(2), padding=(GAP, dp(8)), **kwargs)
        self.title = Label(text=label, color=MUTED, font_size=dp(12), halign='left', valign='middle',
                           size_hint_y=None, height=dp(18))
        self.title.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
        self.reading = Label(text='no reading yet', color=STATUS['off'], font_size=dp(15), halign='left',
                             valign='middle', shorten=True, shorten_from='right')
        self.reading.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
        self.add_widget(self.title)
        self.add_widget(self.reading)

    def _fit_height(self, *_):
        pass

    def set(self, level, text):
        self.reading.text = text
        self.reading.color = STATUS[level] if level != 'off' else MUTED
        self.set_border(STATUS[level])


class LiveScreen(BoxLayout):
    def __init__(self, session, runner, on_open_link=None, on_fullscreen=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.session = session
        self.runner = runner
        self.on_open_link = on_open_link
        self.on_fullscreen = on_fullscreen
        self._event = None
        self.cards = {}
        self.chrome = []
        self.full = False
        self.full_page = 0          # the page shown in full screen (the Live list is cut into pages like Scan's)
        self.light = ShiftLight()   # the shift light settings, kept across renders; the LEDs are on the app-wide bar
        self.render()

    # --- lifecycle -------------------------------------------------------------------------------

    def activate(self):
        for card in self.cards.values():
            card.apply_view()       # pick up a display or red line changed on another screen
        if self._event is None:
            self._event = Clock.schedule_interval(self.refresh, 0.5)

    def deactivate(self):
        if self._event is not None:
            self._event.cancel()
            self._event = None

    def source_changed(self, _status=None):
        self.render()

    def show_light_settings(self):
        """Bring the shift light settings into view (a tap on the bar over the screens comes here)."""
        scroller = getattr(self, 'scroller', None)
        if scroller is not None and self.light.parent is not None:
            Clock.schedule_once(lambda dt: scroller.scroll_to(self.light, padding=dp(8)), 0.1)

    def set_full(self, on):
        """Full screen: show only the sensors, one page at a time, placed by the page's layout, with the status,
        health and shift panels put away."""
        changed = on != self.full
        self.full = on
        for widget in self.chrome:
            hide(widget, on)
        if changed:
            self.render()           # the sensors are drawn differently in full screen

    # --- layout ----------------------------------------------------------------------------------

    def sources(self):
        """The sensors shown here, in the order they are listed before sorting."""
        return [pids.get(p) for p in STREAM_PIDS + list(pids.REPLAY)]

    def arranged(self):
        """The sensors shown here, in display order: by group, then the user's order."""
        return dashboard_layout.arrange(self.sources())

    def full_pages(self):
        """The shown sensors cut into full-screen pages."""
        return dashboard_layout.pages(self.arranged()) or [[]]

    def layout_target(self):
        """(page index, sensors on it) of the full-screen page the layout chooser is for."""
        pages = self.full_pages()
        self.full_page = min(self.full_page, len(pages) - 1)
        return self.full_page, len(pages[self.full_page])

    def open_layout(self):
        if hooks.on_layout is not None:
            hooks.on_layout('live')

    def turn(self, step):
        self.full_page = (self.full_page + step) % len(self.full_pages())
        self.render()

    def _full_view(self):
        """The current page, its cards placed by the page's template (layout_ui.FullPage). The shift light is the
        app-wide bar over it."""
        page, _count = self.layout_target()
        pages = self.full_pages()
        cards = []
        for pid in pages[page]:
            card = PidCard(pid, scope='live')
            self.cards[pid.pid] = card
            cards.append(card)
        return FullPage(cards, page, len(pages), page_layout.for_page(page), self.turn, self.open_layout)

    def render(self):
        if self.light.parent is not None:      # the light outlives the layout it sits in, so take it out first
            self.light.parent.remove_widget(self.light)
        self.clear_widgets()
        self.cards = {}
        if self.session.active() is None:
            card = Card()
            card.add_widget(section_title('No data source'))
            card.add_widget(panel_label('Connect your scan adapter on the Link tab to stream the engine '
                                        'and transmission computers, or start the demo drive.', color=MUTED))
            card.add_widget(make_button('Start demo', lambda: self.session.set_demo(True), primary=True))
            card.add_widget(make_button('Open Link', lambda: self.on_open_link and self.on_open_link()))
            self.scroller = stack(card, self.light)    # the light's settings are reachable with no data source too
            self.add_widget(self.scroller)
            return
        self.status = panel_label('Starting...', color=MUTED, font_size=dp(12))
        self.health_tiles = {}
        health = Card()
        health.add_widget(section_title('Health'))
        for key, label in HEALTH:
            tile = HealthTile(label)
            self.health_tiles[key] = tile
            health.add_widget(tile)
        self.shift_log = panel_label('No shifts yet.', markup=True, color=TEXT, font_size=dp(13))
        shifts = Card()
        shifts.add_widget(section_title('Shifts against your table'))
        shifts.add_widget(self.shift_log)
        hint = panel_label('Green: within 8% of the table. Yellow: within 20%. Red: further out. The '
                           'average of the speeds either side of a shift is used.', font_size=dp(12),
                           color=MUTED)
        self.transmission_button = ToggleButton(text='Also read the transmission (7E2)', size_hint_y=None,
                                                height=dp(44), state='down' if self.runner.transmission else 'normal')
        self._style_transmission()
        self.transmission_button.bind(state=self._transmission_changed)
        readings_title = section_title('Readings')
        full_button = make_button('Full screen: live data only', lambda: self.on_fullscreen and self.on_fullscreen(True))
        layout_button = make_button('Page layout', self.open_layout)
        full_row = button_row(full_button, layout_button)
        self.chrome = [self.light.settings, self.status, self.transmission_button, full_row, health,
                       readings_title, shifts, hint]
        if self.full:
            self.scroller = None
            self.add_widget(self._full_view())      # the panels above are kept, unseen, for refresh to write to
        else:
            self.scroller = stack(self.light, self.status, self.transmission_button, full_row, health,
                                  readings_title, self._grid(), shifts, hint)
            self.add_widget(self.scroller)
        self.set_full(self.full)

    def _grid(self):
        """The sensors in groups, as a list that scrolls (not full screen)."""
        grid = BoxLayout(orientation='vertical', spacing=GAP, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for group, members in dashboard_layout.runs(self.arranged()):
            grid.add_widget(panel_label(dashboard_layout.TITLES[group], color=MUTED, font_size=dp(12)))
            cards = GridLayout(spacing=GAP, size_hint_y=None)
            fit_columns(cards)
            cards.bind(minimum_height=cards.setter('height'))
            for pid in members:
                card = PidCard(pid, scope='live')
                self.cards[pid.pid] = card
                cards.add_widget(card)
            Clock.schedule_once(lambda dt, g=cards: equalize(g), 0)
            grid.add_widget(cards)
        return grid

    def _style_transmission(self):
        style_button(self.transmission_button, primary=self.transmission_button.state == 'down')

    def _transmission_changed(self, _button, state):
        self._style_transmission()
        self.runner.set_transmission(state == 'down')
        self.status.text = ''

    # --- updating --------------------------------------------------------------------------------

    def refresh(self, _dt):
        stream = self.runner.stream
        if stream is None or not self.cards:
            return
        self.runner.refresh_model()
        snap = stream.snapshot()
        rate = snap['rate_hz']
        label = getattr(self.session.active(), 'label', 'Live')
        if snap['error']:
            self.status.text = f'Adapter not answering: {snap["error"]}'
            self.status.color = STATUS['bad']
        else:
            what = 'engine (ECU) and transmission (TCM)' if self.runner.transmission else 'engine (ECU) only'
            self.status.text = f'{label}: {what} streaming, {rate:.1f} rounds per second'
            self.status.color = MUTED
        for tile in snap['health']:
            self.health_tiles[tile['key']].set(tile['level'], tile['text'])
        for pid_id, card in self.cards.items():
            entry = snap['values'].get(pid_id)
            idle = None
            if pid_id in TCM_PIDS and not self.runner.transmission:
                idle = 'transmission off'
            elif self.session.replay is not None and pid_id not in pids.REPLAY:
                idle = 'not in log'   # a CAN log is playing and it does not carry this reading
            elif entry is None:
                idle = obd.module_note(card.pid, getattr(self.session.active(), 'extra_modules', False))
            card.show((entry['value'], entry['unit']) if entry else None, entry['history'] if entry else [],
                      idle=idle, note=entry.get('note') if entry else None)
        lines = [f'[color=#{HEX[s["level"]]}]{s["text"]}[/color]' for s in snap['shifts'][:6] if s['text']]
        self.shift_log.text = '\n'.join(lines) or 'No shifts yet. Drive, or watch the demo.'
