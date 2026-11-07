"""The shift light card on the Live screen (its settings) and the LED strip the app-wide bar draws.

The rules are in scanner/shift_light.py. The LEDs themselves, and the chime, belong to the bar over every screen
(shift_overlay.py), which reads the same saved choices this card writes; this card only edits them.
"""

from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from tunertoolpro.scanner import shift_light
from ui_kit import MUTED, PANEL, RADIUS, TEXT, Card, button_row, make_button, panel_label, section_title, toggle

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
    """The shift light card: the switch, the chime and the settings. The LEDs are on the bar over every screen."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.saved, self.save, self.chime_path = {}, None, None
        self.on_change = None       # called after any change, so the bar over the screens follows at once
        self._loading = False       # True while the switches are being set from the saved choices
        self.switch = toggle('Shift light', False, self._switched)
        self.chime_switch = toggle('Chime', True, self._chimed)
        self.settings = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        self.settings.bind(minimum_height=self.settings.setter('height'))
        self.style_button = make_button('', self._next_style)
        self.theme_button = make_button('', self._next_theme)
        self.values = {}
        self.position_button = make_button('', self._next_position)
        self.size_button = make_button('', self._next_size)
        self.settings.add_widget(button_row(self.style_button, self.theme_button))
        self.settings.add_widget(button_row(self.position_button, self.size_button))
        for key, label in ROWS:
            self.settings.add_widget(self._stepper(key, label))
        self.settings.add_widget(panel_label('The LEDs fill from the start RPM to the shift RPM. Inside the warning '
                                             'window they blink, and at the shift point they all flash. The chime '
                                             'sounds through the warning. The bar shows over every screen: tap '
                                             'it to come here, hold it to move it to the top or bottom.',
                                             font_size=dp(12), color=MUTED))
        self.add_widget(section_title('Shift light'))
        self.add_widget(button_row(self.switch, self.chime_switch))
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
        self.position_button.text = f'Bar: {settings["position"].capitalize()}'
        self.size_button.text = f'Size: {shift_light.SIZE_NAMES[settings["size"]]}'
        for key, _label in ROWS:
            self.values[key].text = f'{settings[key]} rpm'
        if self.on_change is not None:
            self.on_change()

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

    def _next_position(self):
        self._store(position=shift_light.other_position(self._settings()['position']))

    def _next_size(self):
        sizes = list(shift_light.SIZES)
        self._store(size=sizes[(sizes.index(self._settings()['size']) + 1) % len(sizes)])

    def refresh(self):
        """Show the saved choices again, after the bar changed one (a long press moves it)."""
        self._show()
