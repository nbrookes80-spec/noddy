"""The shift light card on the Live screen: the ten LEDs, and the settings that sit under them.

The rules are in scanner/shift_light.py. This file draws the frame it is given, saves the settings through the
app's saved choices, and plays the chime from a WAV file written beside the app's data the first time it is needed.
The LEDs stay on the screen in full screen mode, because that is where a driver looks; the settings do not.
"""

import os
import wave

from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from scanner import shift_light
from ui_kit import MUTED, PANEL, RADIUS, TEXT, Card, button_row, hide, make_button, panel_label, section_title, toggle

ROWS = (('start', 'Start RPM'), ('shift', 'Shift RPM'), ('margin', 'Warning before shift'))


class LedStrip(Widget):
    """The ten LEDs in one row. The bar, centre and outside styles draw dots; the strip draws one solid bar."""

    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=dp(44), **kwargs)
        self._zones = [None] * shift_light.LEDS
        self._style = 'bar'
        self._theme = 'classic'
        self.bind(pos=self._draw, size=self._draw)

    def show(self, zones, style, theme):
        self._zones, self._style, self._theme = zones, style, theme
        self._draw()

    def _draw(self, *_):
        colours = shift_light.THEMES[self._theme]
        cell = self.width / shift_light.LEDS
        self.canvas.clear()
        with self.canvas:
            Color(*PANEL)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[RADIUS])
            for position, zone in enumerate(self._zones):
                Color(*(colours[zone] if zone else shift_light.OFF))
                x = self.x + position * cell
                if self._style == 'strip':
                    Rectangle(pos=(x, self.y + dp(8)), size=(cell, self.height - dp(16)))
                else:
                    dot = min(cell, self.height) * 0.78
                    Ellipse(pos=(x + (cell - dot) / 2, self.y + (self.height - dot) / 2), size=(dot, dot))


class ShiftLight(Card):
    """The shift light card: the switch, the chime, the LEDs and the settings for them."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.saved, self.save, self.chime_path = {}, None, None
        self._loading = False       # True while the switches are being set from the saved choices
        self._sound, self._sound_failed = None, False
        self.timer = shift_light.ChimeTimer()
        self.switch = toggle('Shift light', False, self._switched)
        self.chime_switch = toggle('Chime', True, self._chimed)
        self.strip = LedStrip()
        self.settings = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        self.settings.bind(minimum_height=self.settings.setter('height'))
        self.style_button = make_button('', self._next_style)
        self.theme_button = make_button('', self._next_theme)
        self.values = {}
        self.settings.add_widget(button_row(self.style_button, self.theme_button))
        for key, label in ROWS:
            self.settings.add_widget(self._stepper(key, label))
        self.settings.add_widget(panel_label('The LEDs fill from the start RPM to the shift RPM. Inside the warning '
                                             'window they blink, and at the shift point they all flash. The chime '
                                             'sounds through the warning.', font_size=dp(12), color=MUTED))
        self.add_widget(section_title('Shift light'))
        self.add_widget(button_row(self.switch, self.chime_switch))
        self.add_widget(self.strip)
        self.add_widget(self.settings)

    # --- settings --------------------------------------------------------------------------------

    def attach(self, saved, save, chime_path):
        """Use the app's saved choices. `save()` writes them to prefs.json after each change."""
        self.saved, self.save, self.chime_path = saved, save, chime_path
        self._show()

    def _settings(self):
        return shift_light.clean({key: self.saved.get(f'light_{key}') for key in shift_light.DEFAULTS})

    def _store(self, **changes):
        settings = self._settings()
        settings.update(changes)
        for key, value in shift_light.clean(settings).items():
            self.saved[f'light_{key}'] = value
        if self.save is not None:
            self.save()
        self._show()

    def _show(self):
        settings = self._settings()
        self._loading = True
        self.switch.state = 'down' if self.saved.get('light_on') is True else 'normal'
        self.chime_switch.state = 'down' if settings['chime'] else 'normal'
        self._loading = False
        self.style_button.text = f'Style: {shift_light.STYLE_NAMES[settings["style"]]}'
        self.theme_button.text = f'Colours: {shift_light.THEMES[settings["theme"]]["name"]}'
        for key, _label in ROWS:
            self.values[key].text = f'{settings[key]} rpm'
        hide(self.strip, self.saved.get('light_on') is not True)

    def _stepper(self, key, label):
        name = Label(text=label, color=MUTED, font_size=dp(13), halign='left', valign='middle', size_hint_x=0.46)
        name.bind(size=lambda widget, _: setattr(widget, 'text_size', widget.size))
        value = Label(text='', color=TEXT, font_size=dp(15), size_hint_x=0.3)
        self.values[key] = value
        minus = make_button('-', lambda: self._store(**{key: self._settings()[key] - shift_light.STEP}))
        minus.size_hint_x = 0.12
        plus = make_button('+', lambda: self._store(**{key: self._settings()[key] + shift_light.STEP}))
        plus.size_hint_x = 0.12
        row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        for widget in (name, minus, value, plus):
            row.add_widget(widget)
        return row

    def _switched(self, on):
        if self._loading:
            return
        self.saved['light_on'] = on
        if self.save is not None:
            self.save()
        self._show()

    def _chimed(self, on):
        if not self._loading:
            self._store(chime=on)

    def _next_style(self):
        styles = list(shift_light.STYLES)
        current = self._settings()['style']
        self._store(style=styles[(styles.index(current) + 1) % len(styles)])

    def _next_theme(self):
        themes = list(shift_light.THEMES)
        current = self._settings()['theme']
        self._store(theme=themes[(themes.index(current) + 1) % len(themes)])

    # --- running ---------------------------------------------------------------------------------

    def update(self, rpm, now):
        """Draw the LEDs for this RPM and play the chime if one is due. Called about ten times a second."""
        if self.saved.get('light_on') is not True:
            return
        settings = self._settings()
        zones, _part, phase = shift_light.frame(rpm, settings, now)
        self.strip.show(zones, settings['style'], settings['theme'])
        if self.timer.due(phase != 'off' and settings['chime'], now):
            self._play_chime()

    def _play_chime(self):
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
