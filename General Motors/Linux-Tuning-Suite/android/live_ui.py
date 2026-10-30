"""The Live screen: the engine and transmission streaming together, with green, yellow and red health.

A StreamRunner reads in the background whenever there is a data source (the demo drive or a connected
adapter), so the Shift tables can show where the car is even while another tab is open. It pauses
while the Scan tab is in front, so the two do not compete for the adapter.
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

from live import STREAM_PIDS, LiveStream
from scan_ui import CARD_HEIGHT, PidCard
from scanner import pids
from table_view import HEX
from ui_kit import (BG, GAP, MUTED, STATUS, TEXT, Card, make_button, panel_label, section_title,
                    stack, style_button)

ROUND_SECONDS = 0.25     # fastest the background reader goes; a real adapter is slower than this
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
        self._stop = threading.Event()
        self._thread = None

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
            self.stream = (LiveStream(source, cfg=cfg, tables=tables, transmission=self.transmission)
                           if source is not None else None)

    def set_transmission(self, on):
        """Turn the TCM reads on or off. Takes effect on the next round."""
        self.transmission = bool(on)
        if self.stream is not None:
            self.stream.transmission = self.transmission

    def refresh_model(self):
        if self.stream is not None:
            self.stream.set_model(*self.model())

    def _loop(self):
        while not self._stop.is_set():
            stream, began = self.stream, time.monotonic()
            if stream is None or self.paused:
                time.sleep(0.2)
                continue
            stream.step()
            time.sleep(BACKOFF_SECONDS if stream.error else max(0.0, ROUND_SECONDS - (time.monotonic() - began)))


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
    def __init__(self, session, runner, on_open_link=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.session = session
        self.runner = runner
        self.on_open_link = on_open_link
        self._event = None
        self.cards = {}
        self.render()

    # --- lifecycle -------------------------------------------------------------------------------

    def activate(self):
        if self._event is None:
            self._event = Clock.schedule_interval(self.refresh, 0.5)

    def deactivate(self):
        if self._event is not None:
            self._event.cancel()
            self._event = None

    def source_changed(self, _status=None):
        self.render()

    # --- layout ----------------------------------------------------------------------------------

    def render(self):
        self.clear_widgets()
        self.cards = {}
        if self.session.active() is None:
            card = Card()
            card.add_widget(section_title('No data source'))
            card.add_widget(panel_label('Connect your scan adapter on the Link tab to stream the engine '
                                        'and transmission computers, or start the demo drive.', color=MUTED))
            card.add_widget(make_button('Start demo', lambda: self.session.set_demo(True), primary=True))
            card.add_widget(make_button('Open Link', lambda: self.on_open_link and self.on_open_link()))
            self.add_widget(stack(card))
            return
        self.status = panel_label('Starting...', color=MUTED, font_size=dp(12))
        self.health_tiles = {}
        health = Card()
        health.add_widget(section_title('Health'))
        for key, label in (('trans_temp', 'Transmission fluid'), ('engine_rpm', 'Engine speed'),
                           ('coolant', 'Coolant'), ('pc_current', 'Line pressure solenoid'),
                           ('gear_follow', 'Gear follows command')):
            tile = HealthTile(label)
            self.health_tiles[key] = tile
            health.add_widget(tile)
        grid = GridLayout(cols=2, spacing=GAP, size_hint_y=None,
                          height=((len(STREAM_PIDS) + 1) // 2) * (CARD_HEIGHT + GAP))
        for pid_id in STREAM_PIDS:
            card = PidCard(pids.get(pid_id))
            self.cards[pid_id] = card
            grid.add_widget(card)
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
        self.add_widget(stack(self.status, self.transmission_button, health, section_title('Readings'), grid,
                              shifts, hint))

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
            card.show((entry['value'], entry['unit']) if entry else None, entry['history'] if entry else [])
        lines = [f'[color=#{HEX[s["level"]]}]{s["text"]}[/color]' for s in snap['shifts'][:6] if s['text']]
        self.shift_log.text = '\n'.join(lines) or 'No shifts yet. Drive, or watch the demo.'
