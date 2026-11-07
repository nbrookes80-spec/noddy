"""The shift light over every screen: a slim bar of the ten LEDs, and the one owner of the light's state and chime.

The rules are in scanner/shift_light.py: the LEDs (`frame`), the chime timing (`ChimeTimer`), the bar's size and
place (`bar_height`, `bar_gaps`) and, most of all, who may talk to the adapter (`rpm_source`, `runner_runs`).
The settings are the app's saved choices (`light_*` in prefs.json), the same dict the Live screen's shift light
card edits, read afresh every frame, so the card and the bar can never disagree.

The bar is a row of the app's main column (above the header, or just above the tabs), inside the HUD mirror, so
it is mirrored along with the picture and never covers or swallows a touch meant for the screen: it takes only
the touches on itself. A tap opens the shift light settings; a long press moves it between top and bottom.
"""

import os
import time
import wave

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

from shift_light_ui import LedStrip
from tunertoolpro.scanner import shift_light
from ui_kit import BG, MUTED

LIGHT_TICK = 0.1         # seconds between shift light frames: fast enough for the 0.10 s flash and 0.15 s blink
LONG_PRESS_SECONDS = 0.6
DIM = 0.35               # the LEDs' opacity while the bar has no engine speed on this screen


class ShiftBar(RelativeLayout):
    """The bar: the LED strip, and a short note over it when there is no engine speed to show here."""

    def __init__(self, on_tap=None, on_long=None, **kwargs):
        super().__init__(size_hint_y=None, height=dp(shift_light.bar_height('medium')), **kwargs)
        self.on_tap, self.on_long = on_tap, on_long
        self.left_gap = self.right_gap = self.top_gap = 0
        with self.canvas.before:
            Color(*BG)
            self._back = Rectangle(pos=(0, 0), size=self.size)
        self.strip = LedStrip()
        self.strip.size_hint = (None, None)
        self.note = Label(text='', color=MUTED, font_size=dp(12), halign='center', valign='middle', bold=True)
        self.add_widget(self.strip)
        self.add_widget(self.note)
        self._long = None
        self._touch = None
        self.bind(size=self._place)

    def set_gaps(self, height, left, right, top):
        """The bar's height and the space it leaves free around the LEDs, all in pixels."""
        self.left_gap, self.right_gap, self.top_gap = left, right, top
        self.height = height + top
        self._place()

    def _place(self, *_):
        self._back.size = self.size
        width = max(0, self.width - self.left_gap - self.right_gap)
        height = max(0, self.height - self.top_gap)
        self.strip.pos, self.strip.size = (self.left_gap, 0), (width, height)
        self.note.pos, self.note.size = (self.left_gap, 0), (width, height)
        self.note.text_size = (width, height)

    def show(self, zones, style, theme, note):
        self.strip.show(zones, style, theme)
        self.note.text = note
        self.strip.opacity = DIM if note else 1

    def _on_leds(self, touch):
        """True for a touch on the LEDs themselves, not the gaps left free for the full-screen buttons."""
        if not self.collide_point(*touch.pos):
            return False
        x, y = self.to_local(*touch.pos)
        return self.left_gap <= x <= self.width - self.right_gap and y <= self.height - self.top_gap

    # A RelativeLayout hands its children local coordinates, but the touch it is given is in its parent's.
    def on_touch_down(self, touch):
        if not self._on_leds(touch):
            return False
        touch.grab(self)
        self._touch = touch
        self._long = Clock.schedule_once(self._long_press, LONG_PRESS_SECONDS)
        return True

    def on_touch_move(self, touch):
        return touch.grab_current is self

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return False
        touch.ungrab(self)
        fired = self._long is None
        self._cancel()
        if not fired and self._on_leds(touch) and self.on_tap is not None:
            self.on_tap()
        return True

    def _long_press(self, _dt):
        self._long = None
        if self.on_long is not None:
            self.on_long()

    def _cancel(self):
        if self._long is not None:
            self._long.cancel()
        self._long = None
        self._touch = None


class ShiftOverlay:
    """Owns the shift light for the whole app: the bar, its place, the chime, and whether the Live reader runs.

    The app gives it callables, so it never reaches into the screens itself:
      screen()          the name of the screen in front
      holds_adapter()   True while another part (the sniffer) has the adapter
      scan_rpm()        (Scan reads '010C', its latest RPM or None)
      fullscreen(), mirrored()
    """

    def __init__(self, saved, save, chime_path, runner, column, header, tabs, screen, holds_adapter, scan_rpm,
                 fullscreen=lambda: False, mirrored=lambda: False, reserved=0, below=0, on_open=None):
        self.saved, self.save, self.chime_path, self.runner = saved, save, chime_path, runner
        self.column, self.header, self.tabs = column, header, tabs
        self.screen, self.holds_adapter, self.scan_rpm = screen, holds_adapter, scan_rpm
        self.fullscreen, self.mirrored = fullscreen, mirrored
        self.reserved, self.below = reserved, below    # pixels the full-screen buttons take at the top right
        self.on_open = on_open
        self.timer = shift_light.ChimeTimer()
        self.chimes = 0                 # how many chimes have played, for the smoke test and the debug log
        self._sound, self._sound_failed = None, False
        self.bar = ShiftBar(on_tap=self.open_settings, on_long=self.move)
        self.source = 'none'
        self._event = None
        self._placed = None

    # --- lifecycle -------------------------------------------------------------------------------

    def start(self):
        if self._event is None:
            self._event = Clock.schedule_interval(self.tick, LIGHT_TICK)
        self.tick(0)

    def stop(self):
        if self._event is not None:
            self._event.cancel()
            self._event = None

    # --- the rule --------------------------------------------------------------------------------

    def light_on(self):
        return self.saved.get('light_on') is True

    def apply_runner(self):
        """Let the Live reader run, or make it stand aside, by the rule in shift_light.runner_runs.

        Called on every screen change and every frame, so a sniffer that takes or gives back the adapter is
        followed within LIGHT_TICK. The reader checks `paused` before each round; a round already under way
        finishes inside the adapter's lock before the next owner's first command."""
        self.runner.paused = not shift_light.runner_runs(self.screen(), self.holds_adapter(), self.light_on())

    def reading(self):
        """(source, rpm, note) for this frame."""
        reads_rpm, scan_value = self.scan_rpm()
        screen, holds, on = self.screen(), self.holds_adapter(), self.light_on()
        source = shift_light.rpm_source(screen, holds, on, reads_rpm)
        rpm = None
        if source == 'live':
            stream = self.runner.stream
            latest = stream.latest.get(shift_light.RPM_PID) if stream is not None else None
            rpm = None if latest is None else latest[0]
        elif source == 'scan':
            rpm = scan_value
        return source, rpm, shift_light.rpm_note(screen, holds, on, reads_rpm)

    # --- each frame ------------------------------------------------------------------------------

    def tick(self, _dt=None):
        self.apply_runner()
        self.place()
        if not self.light_on():
            self.timer.due(False, 0)       # the next warning chimes at once
            return
        settings = shift_light.clean({key: self.saved.get(f'light_{key}') for key in shift_light.DEFAULTS})
        self.source, rpm, note = self.reading()
        now = time.monotonic()
        zones, _part, phase = shift_light.frame(rpm, settings, now)
        self.bar.show(zones, settings['style'], settings['theme'], note)
        if self.timer.due(phase != 'off' and settings['chime'], now):
            self._play_chime()

    def place(self):
        """Put the bar where the saved choices say, or take it off the screen while the light is off."""
        settings = shift_light.clean({key: self.saved.get(f'light_{key}') for key in shift_light.DEFAULTS})
        width = self.column.width / dp(1)
        left, right, top = shift_light.bar_gaps(settings['position'], self.fullscreen(), self.mirrored(),
                                                width, self.reserved / dp(1), self.below / dp(1))
        wanted = (self.light_on(), settings['position'], settings['size'], left, right, top)
        if wanted == self._placed:
            return
        self._placed = wanted
        if self.bar.parent is not None:
            self.bar.parent.remove_widget(self.bar)
        if not self.light_on():
            return
        self.bar.set_gaps(dp(shift_light.bar_height(settings['size'])), dp(left), dp(right), dp(top))
        # A vertical BoxLayout draws its children list from the end: the last entry is the top row.
        children = self.column.children
        if settings['position'] == 'top':
            self.column.add_widget(self.bar, index=children.index(self.header) + 1)
        else:
            self.column.add_widget(self.bar, index=children.index(self.tabs) + 1)

    # --- touches ---------------------------------------------------------------------------------

    def open_settings(self):
        if self.on_open is not None:
            self.on_open()

    def move(self):
        """A long press: the bar changes between the top and the bottom, and that is saved."""
        settings = shift_light.clean({key: self.saved.get(f'light_{key}') for key in shift_light.DEFAULTS})
        self.saved['light_position'] = shift_light.other_position(settings['position'])
        if self.save is not None:
            self.save()
        self.place()

    # --- the chime -------------------------------------------------------------------------------

    def _play_chime(self):
        self.chimes += 1
        if self._sound is None and not self._sound_failed:
            self._sound = self._load_sound()
            self._sound_failed = self._sound is None
        if self._sound is not None:
            self._sound.play()

    def _load_sound(self):
        """The chime as a sound the phone can play, or None when it cannot be made or loaded."""
        try:
            if not os.path.exists(self.chime_path):
                shift_light.write_chime(self.chime_path)
            return SoundLoader.load(self.chime_path)
        except (OSError, wave.Error):
            return None
