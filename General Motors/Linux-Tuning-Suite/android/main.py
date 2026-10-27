"""TunerToolPro for Android: Shift Points, Dyno, an OBD-II scanner and a read-only adapter link."""

import os

os.environ.setdefault('KIVY_NO_ARGS', '1')

from kivy import kivy_data_dir  # noqa: E402
from kivy.app import App  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402
from kivy.graphics import Color, Line  # noqa: E402
from kivy.metrics import dp  # noqa: E402
from kivy.properties import ListProperty  # noqa: E402
from kivy.uix.behaviors import ButtonBehavior  # noqa: E402
from kivy.uix.boxlayout import BoxLayout  # noqa: E402
from kivy.uix.floatlayout import FloatLayout  # noqa: E402
from kivy.uix.button import Button  # noqa: E402
from kivy.uix.filechooser import FileChooserListView  # noqa: E402
from kivy.uix.gridlayout import GridLayout  # noqa: E402
from kivy.uix.image import Image  # noqa: E402
from kivy.uix.label import Label  # noqa: E402
from kivy.uix.popup import Popup  # noqa: E402
from kivy.uix.screenmanager import Screen, ScreenManager  # noqa: E402
from kivy.uix.scrollview import ScrollView  # noqa: E402
from kivy.uix.slider import Slider  # noqa: E402
from kivy.uix.spinner import Spinner  # noqa: E402
from kivy.uix.textinput import TextInput  # noqa: E402
from kivy.uix.widget import Widget  # noqa: E402

import dyno_live  # noqa: E402
import grading  # noqa: E402
import shift_live  # noqa: E402
import vehicles  # noqa: E402
from agent_ui import AgentScreen  # noqa: E402
from link_ui import LinkScreen  # noqa: E402
from splash_ui import SplashOverlay  # noqa: E402
from live_ui import LiveScreen, StreamRunner  # noqa: E402
from scan_ui import ScanScreen  # noqa: E402
from settings_ui import SettingsScreen  # noqa: E402
from scanner.session import Session  # noqa: E402
from table_view import HEX, table_blocks  # noqa: E402
from tunertoolpro import core  # noqa: E402
from ui_kit import (ACCENT, ALERT, BG, BLUE, BORDER, GAP, MUTED, RAISED, TEXT, Card,  # noqa: E402
                    HeaderBar, button_row, icon, make_button, panel_label, section_title, stack,
                    style_button)

MONO = os.path.join(kivy_data_dir, 'fonts', 'RobotoMono-Regular.ttf')
APP_VERSION = '0.2.2'

# How the 23 shift settings are grouped into cards.
GROUPS = [
    ('Vehicle', ['tire_dia', 'axle', 'chain', 'weight', 'rwhp']),
    ('Engine and converter', ['idle_rpm', 'stall_rpm', 'shift_rpm', 'downshift_rpm']),
    ('Converter lock', ['min_tcc_rpm', 'min_tcc_gear', 'accel_lock_gear', 'wot_lock_gear']),
    ('Throttle', ['tps_offset', 'tps_factor']),
    ('Shift feel', ['up_firmness', 'down_firmness', 'spread_up', 'spread_lock', 'spread_lock_up',
                    'spread_unlock_dn', 'lead_value', 'down_time']),
]


def snap(value, lo, hi, step):
    """Round a slider position to the field's step, and keep it inside the field's range."""
    stepped = lo + round((value - lo) / step) * step
    return min(max(stepped, lo), hi)


def mono_scroller(text):
    """Monospace text that scrolls sideways, so wide tables keep their columns on a narrow screen."""
    label = Label(text=text, font_name=MONO, font_size=dp(11), color=TEXT, size_hint=(None, None),
                  halign='left', valign='top', markup=True)
    label.bind(texture_size=lambda w, size: setattr(w, 'size', size))
    scroll = ScrollView(do_scroll_y=False, size_hint_y=None, bar_width=dp(3))
    scroll.add_widget(label)
    label.bind(height=lambda _w, h: setattr(scroll, 'height', h + dp(8)))
    return scroll


class ShiftScreen(BoxLayout):
    """Each input has a slider and a typed box that stay in step. Any change recalculates the
    shift tables and asks the Dyno screen to run again."""

    def __init__(self, on_change, on_settings=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.on_change = on_change
        self._syncing = False
        values, ratios = shift_live.default_inputs()
        self.inputs, self.sliders, self.ranges, self.decimals = {}, {}, {}, {}
        fields = {f[0]: f for f in shift_live.FIELDS}
        widgets = []
        if on_settings:
            choose = Card()
            choose.add_widget(section_title('Car and transmission'))
            self.car_label = panel_label('', color=MUTED, font_size=dp(13))
            choose.add_widget(self.car_label)
            choose.add_widget(make_button('Change car or transmission', on_settings, primary=True))
            widgets.append(choose)
        for title, keys in GROUPS:
            card = Card()
            card.add_widget(section_title(title))
            for key in keys:
                _key, label, lo, hi, step, decimals = fields[key]
                card.add_widget(self._field_row(key, label, lo, hi, step, decimals, values[key]))
            widgets.append(card)

        gears = Card()
        gears.add_widget(section_title('Gears'))
        self.ratio_box = TextInput(text=ratios, multiline=False, size_hint_y=None, height=dp(44),
                                   background_color=RAISED, foreground_color=TEXT, font_size=dp(14),
                                   padding=[dp(10), dp(12), dp(10), dp(10)])
        self.ratio_box.bind(text=lambda *_: self.recalculate())
        gears.add_widget(panel_label('Gear ratios, comma separated', color=MUTED))
        gears.add_widget(self.ratio_box)
        self.lead_box = Spinner(text='rpm', values=('rpm', 'torque'), size_hint_y=None, height=dp(44))
        self.lead_box.bind(text=lambda *_: self.recalculate())
        self.stall_box = Spinner(text='Off', values=('Off', 'On'), size_hint_y=None, height=dp(44))
        self.stall_box.bind(text=lambda *_: self.recalculate())
        for spinner in (self.lead_box, self.stall_box):
            style_button(spinner)
        gears.add_widget(panel_label('Lead mode', color=MUTED))
        gears.add_widget(self.lead_box)
        gears.add_widget(panel_label('Stall lock logic', color=MUTED))
        gears.add_widget(self.stall_box)
        widgets.append(gears)

        self.status = panel_label(color=ALERT)
        self.tables = BoxLayout(orientation='vertical', size_hint_y=None, spacing=GAP)
        self.tables.bind(minimum_height=self.tables.setter('height'))
        self.last = None          # (cfg, tables, grades) of the latest valid calculation
        self.cursor = None        # where the car is on the tables while live data streams
        self.table_labels = {}
        widgets += [self.status, section_title('Shift tables (MPH)'), self.tables]
        self.add_widget(stack(*widgets))
        self.recalculate()

    # --- car and transmission, chosen on the Settings screen -------------------------------------

    def _set_all(self, values, ratios):
        """Put new values in every box and slider, then recalculate once."""
        self._syncing = True
        for key, text in values.items():
            if key in self.inputs:
                self.inputs[key].text = text
                lo, hi, _ = self.ranges[key]
                self.sliders[key].value = min(max(float(text), lo), hi)
        self.ratio_box.text = ratios
        self._syncing = False
        self.recalculate()

    def apply_profile(self, name):
        values, ratios = shift_live.default_inputs(name)
        self._set_all(values, ratios)

    def apply_transmission(self, transmission):
        values = vehicles.fit_gears({key: box.text for key, box in self.inputs.items()},
                                    len(transmission.ratios))
        self._set_all(values, vehicles.ratios_text(transmission))

    def _field_row(self, key, label, lo, hi, step, decimals, text):
        self.ranges[key] = (lo, hi, step)
        self.decimals[key] = decimals
        row = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(84), spacing=dp(2))
        top = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))
        name = Label(text=label, color=TEXT, size_hint_x=0.62, halign='left', valign='middle',
                     font_size=dp(14))
        name.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
        box = TextInput(text=text, multiline=False, input_filter='float', size_hint_x=0.38,
                        background_color=RAISED, foreground_color=TEXT, font_size=dp(15),
                        halign='right', padding=[dp(8), dp(9), dp(8), dp(9)])
        box.bind(text=lambda b, t, k=key: self._text_changed(k, t))
        top.add_widget(name)
        top.add_widget(box)
        slider = Slider(min=lo, max=hi, value=min(max(float(text), lo), hi),
                        cursor_size=(dp(22), dp(22)), padding=dp(12), size_hint_y=None, height=dp(36))
        slider.bind(value=lambda s, v, k=key: self._slider_moved(k, v))
        row.add_widget(top)
        row.add_widget(slider)
        self.inputs[key] = box
        self.sliders[key] = slider
        return row

    def _slider_moved(self, key, value):
        if self._syncing:
            return
        lo, hi, step = self.ranges[key]
        number = snap(value, lo, hi, step)
        self._syncing = True
        self.inputs[key].text = f'{number:.{self.decimals[key]}f}'
        self._syncing = False
        self.recalculate()

    def _text_changed(self, key, text):
        if self._syncing:
            return
        try:
            number = float(text)
        except ValueError:
            number = None
        if number is not None:
            lo, hi, _ = self.ranges[key]
            self._syncing = True
            self.sliders[key].value = min(max(number, lo), hi)
            self._syncing = False
        self.recalculate()

    def current(self):
        """(values, ratios, lead mode, stall lock) as the calculation expects them."""
        values = {key: box.text for key, box in self.inputs.items()}
        return values, self.ratio_box.text, self.lead_box.text, self.stall_box.text == 'On'

    def recalculate(self):
        values, ratios, lead, stall = self.current()
        tables, error = shift_live.calculate(values, ratios, lead, stall)
        self.tables.clear_widgets()
        self.table_labels = {}
        if error:
            self.status.text = error
            self.last = None
        else:
            self.status.text = ''
            cfg = shift_live.build_cfg(values, ratios, lead, stall)
            grades = grading.grade_tables(tables, cfg)
            self.last = (cfg, tables, grades)
            self.tables.add_widget(self._summary_card(grades))
            for title, text in table_blocks(tables, grades.levels, self.cursor):
                card = Card()
                card.add_widget(panel_label(title, color=ACCENT, bold=True))
                scroller = mono_scroller(text)
                self.table_labels[title] = scroller.children[0]
                card.add_widget(scroller)
                self.tables.add_widget(card)
        self.on_change()

    def _summary_card(self, grades):
        """How the settings grade: counts, the legend, and the few worst cells in words."""
        counts = grades.counts
        card = Card()
        card.add_widget(section_title('How your settings grade'))
        card.add_widget(panel_label(
            f'[color=#{HEX["good"]}]{counts["good"]} green[/color]   '
            f'[color=#{HEX["ok"]}]{counts["ok"]} yellow[/color]   '
            f'[color=#{HEX["bad"]}]{counts["bad"]} red[/color]', markup=True, font_size=dp(16)))
        problems = [f'[color=#{HEX[p["level"]]}]{self._cell_name(p)}: {p["message"]}[/color]'
                    for p in grades.worst[:3]]
        card.add_widget(panel_label('\n\n'.join(problems) if problems else 'Every cell is in range.',
                                    markup=True, color=MUTED, font_size=dp(13)))
        card.add_widget(panel_label('Green is good, yellow (~) is satisfactory and worth a look, red (!) is '
                                    'likely a problem. * marks where the car is now while live data '
                                    'streams. These are rules of thumb from your own settings.',
                                    color=MUTED, font_size=dp(12)))
        return card

    @staticmethod
    def _cell_name(problem):
        axis = core.tps_axis()[problem['col']]
        titles = {'upshift': 'Upshift', 'downshift': 'Downshift', 'tcc_lock': 'TCC lock',
                  'tcc_unlock': 'TCC unlock'}
        row = problem['row'] + 1
        label = f'{row}-{row + 1}' if problem['table'] in ('upshift', 'downshift') else f'gear {row}'
        return f'{titles[problem["table"]]} {label} at {axis:g}% throttle'

    # --- hooks for the other screens -------------------------------------------------------------

    def model(self):
        """(cfg, tables) of the latest calculation, or (None, None) while an input is invalid."""
        return (self.last[0], self.last[1]) if self.last else (None, None)

    def grading(self):
        return self.last[2] if self.last else None

    def settings(self):
        """The numeric settings as the agent bridge reports them."""
        out = {}
        for key, box in self.inputs.items():
            try:
                out[key] = float(box.text)
            except ValueError:
                out[key] = None
        return out

    def set_value(self, key, number):
        """Approved change from the agent: update the typed box, which moves the slider and recalculates."""
        lo, hi, _step = self.ranges[key]
        self.inputs[key].text = f'{min(max(number, lo), hi):.{self.decimals[key]}f}'

    def set_cursor(self, cursor):
        """Mark where the car is on the tables. Only the table text changes, so this is cheap."""
        if cursor == self.cursor:
            return
        self.cursor = cursor
        if self.last:
            _cfg, tables, grades = self.last
            for title, text in table_blocks(tables, grades.levels, cursor):
                if title in self.table_labels:
                    self.table_labels[title].text = text


class DynoChart(Widget):
    """Horsepower (amber) and torque (blue) against RPM, drawn on the canvas."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rpms, self.hp, self.tq = [], [], []
        self.bind(pos=self._redraw, size=self._redraw)

    def set_data(self, rpms, hp, tq):
        self.rpms, self.hp, self.tq = rpms, hp, tq
        self._redraw()

    def _redraw(self, *_):
        self.canvas.clear()
        with self.canvas:
            if len(self.rpms) < 2:
                return
            left, bottom = self.x + dp(8), self.y + dp(8)
            width, height = self.width - dp(16), self.height - dp(16)
            lo, hi = self.rpms[0], self.rpms[-1]
            top = max(max(self.hp), max(self.tq), 1.0) * 1.08

            def point(rpm, value):
                x = left + width * (rpm - lo) / max(hi - lo, 1e-9)
                y = bottom + height * value / top
                return x, y

            Color(*BORDER)
            for i in range(1, 4):
                y = bottom + height * i / 4
                Line(points=[left, y, left + width, y], width=dp(1))
            Color(*MUTED)
            Line(points=[left, bottom + height, left, bottom, left + width, bottom], width=dp(1.2))
            for values, colour in ((self.hp, ACCENT), (self.tq, BLUE)):
                Color(*colour)
                flat = []
                for rpm, value in zip(self.rpms, values):
                    flat.extend(point(rpm, value))
                Line(points=flat, width=dp(2.2))


class StatTile(Card):
    """A big number with a small caption: used for 0-60 and the quarter mile."""

    def __init__(self, caption, **kwargs):
        super().__init__(spacing=dp(2), **kwargs)
        self.caption = Label(text=caption, color=MUTED, font_size=dp(12), size_hint_y=None, height=dp(18),
                             halign='left')
        self.caption.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, None)))
        self.number = Label(text='--', color=ACCENT, bold=True, font_size=dp(24), size_hint_y=None,
                            height=dp(40), halign='left', valign='middle', shorten=True)
        self.number.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
        self.add_widget(self.caption)
        self.add_widget(self.number)


class DynoScreen(BoxLayout):
    """Simulated or loaded dyno curve, with a launch simulation from the Shift Points settings."""

    def __init__(self, shift_screen, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.shift_screen = shift_screen
        self.curve = None
        self.source = 'Simulated from the Shift Points settings'
        self.source_label = panel_label(self.source, color=MUTED, font_size=dp(12))
        self.chart = DynoChart(size_hint_y=None, height=dp(240))
        self.chart_card = Card()
        self.chart_card.add_widget(self.chart)
        legend = panel_label('Horsepower (amber), torque (blue)', color=MUTED, font_size=dp(12))
        self.chart_card.add_widget(legend)
        self.summary = GridLayout(cols=2, size_hint_y=None, spacing=dp(4))
        self.summary.bind(minimum_height=self.summary.setter('height'))
        self.results = GridLayout(cols=2, size_hint_y=None, spacing=dp(4))
        self.results.bind(minimum_height=self.results.setter('height'))
        self.status = panel_label(color=ALERT)
        self.tile_060 = StatTile('0-60 mph')
        self.tile_quarter = StatTile('1/4 mile')
        tiles = GridLayout(cols=2, spacing=GAP, size_hint_y=None, height=dp(92))
        tiles.add_widget(self.tile_060)
        tiles.add_widget(self.tile_quarter)
        curve_card = Card()
        curve_card.add_widget(section_title('Curve'))
        curve_card.add_widget(self.summary)
        launch_card = Card()
        launch_card.add_widget(section_title('Launch simulation'))
        launch_card.add_widget(self.results)
        self.add_widget(stack(
            button_row(make_button('Load CSV', self.choose_csv, primary=True),
                       make_button('Simulated', self.use_simulated)),
            self.source_label, tiles, self.chart_card, curve_card, launch_card, self.status))
        self.refresh()

    def use_simulated(self):
        self.curve = None
        self.source = 'Simulated from the Shift Points settings'
        self.refresh()

    def choose_csv(self):
        try:
            from plyer import filechooser
        except ImportError:
            filechooser = None
        if filechooser is not None:
            try:
                filechooser.open_file(on_selection=self._native_picked, filters=['*.csv'],
                                      multiple=False)
                return
            except Exception:  # the platform chooser is missing or refused; use the built-in one
                pass
        self._open_picker()

    def _native_picked(self, selection):
        if selection:
            path = selection[0]
            Clock.schedule_once(lambda dt: self.load_path(path))

    def _open_picker(self):
        chooser = FileChooserListView(path=os.path.expanduser('~'), filters=['*.csv'])
        body = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(8))
        body.add_widget(chooser)
        cancel = style_button(Button(text='Cancel'))
        open_button = style_button(Button(text='Open'), primary=True)
        body.add_widget(button_row(cancel, open_button))
        popup = Popup(title='Choose a dyno CSV (rpm, hp, tq)', content=body, size_hint=(0.95, 0.9))
        cancel.bind(on_release=lambda *_: popup.dismiss())

        def open_selected(*_):
            popup.dismiss()
            if chooser.selection:
                self.load_path(chooser.selection[0])

        open_button.bind(on_release=open_selected)
        popup.open()

    def load_path(self, path):
        if not os.path.isfile(path):
            self.status.text = ('Could not open that file. Copy the CSV into Downloads, '
                                'then choose it again.')
            return
        try:
            self.curve = dyno_live.load_curve(path)
        except (OSError, ValueError) as exc:
            self.status.text = f'Could not read the dyno file: {exc}'
            return
        self.source = f'Loaded: {os.path.basename(path)}'
        self.refresh()

    def refresh(self):
        """Draw the curve and run the launch from the current Shift Points values."""
        values, ratios, lead, stall = self.shift_screen.current()
        try:
            if self.curve is None:
                curve = dyno_live.simulated_curve(float(values['rwhp']), float(values['shift_rpm']),
                                                  float(values['idle_rpm']))
            else:
                curve = self.curve
        except ValueError:
            self.status.text = 'Fix the highlighted shift setting first.'
            return
        self.source_label.text = self.source
        rpms, hp, tq = dyno_live.chart_series(curve)
        self.chart.set_data(rpms, hp, tq)
        self._fill(self.summary, dyno_live.summary_rows(curve))
        result, error = dyno_live.run(values, ratios, curve, lead, stall)
        if result is None:
            self._fill(self.results, [])
            self.tile_060.number.text = self.tile_quarter.number.text = '--'
            self.status.text = error
        else:
            self.status.text = ''
            self._fill(self.results, dyno_live.result_rows(result))
            rows = dict(dyno_live.result_rows(result))
            self.tile_060.number.text = rows['0-60 mph (s)'] + ' s'
            self.tile_quarter.number.text = rows['1/4 mile (s)'] + ' s'

    @staticmethod
    def _fill(grid, rows):
        grid.clear_widgets()
        for label, value in rows:
            grid.add_widget(panel_label(label, color=MUTED, font_size=dp(14)))
            grid.add_widget(panel_label(str(value), color=TEXT, font_size=dp(15), halign='right'))


class NavButton(ButtonBehavior, BoxLayout):
    """An icon above a label. The label is amber when its screen is showing."""

    colour = ListProperty(MUTED)

    def __init__(self, name, title, on_press_screen, **kwargs):
        super().__init__(orientation='vertical', padding=(0, dp(4)), **kwargs)
        self.screen_name = name
        self.on_press_screen = on_press_screen
        self.add_widget(Image(source=icon(name), size_hint_y=0.7, fit_mode='contain'))
        self.label = Label(text=title, size_hint_y=0.3, color=MUTED, font_size=dp(12))
        self.add_widget(self.label)

    def on_press(self):
        self.on_press_screen(self.screen_name)

    def set_active(self, active):
        self.label.color = ACCENT if active else MUTED


class NavBar(BoxLayout):
    """The bottom bar, with a 1 dp rule along its top edge."""

    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=dp(64), spacing=dp(2), **kwargs)
        with self.canvas.after:
            Color(*BORDER)
            self._rule = Line(points=[0, 0, 0, 0], width=dp(1))
        self.bind(x=self._place, y=self._place, width=self._place, height=self._place)

    def _place(self, *_):
        self._rule.points = [self.x, self.y + self.height, self.x + self.width, self.y + self.height]


class TunerToolProApp(App):
    title = 'TunerToolPro'

    def build(self):
        Window.clearcolor = BG
        Window.softinput_mode = 'below_target'   # keep a text box visible above the keyboard
        Window.bind(on_keyboard=self.on_back)
        self._refresh_event = None  # must exist before the Shift screen runs its first recalculation
        self.session = Session()
        self.manager = ScreenManager()
        self.header = HeaderBar(on_settings=lambda: self.show('settings'))
        self.shift = ShiftScreen(on_change=self.request_dyno_refresh, on_settings=lambda: self.show('settings'))
        self.dyno = DynoScreen(self.shift)
        self.runner = StreamRunner(self.session, self.shift.model)
        self.live = LiveScreen(self.session, self.runner, on_open_link=lambda: self.show('link'))
        self.scan = ScanScreen(self.session)
        prefs_path = os.path.join(self.user_data_dir, 'prefs.json')
        self.link = LinkScreen(self.session, prefs_path, on_open_live=lambda: self.show('live'))
        fields = {f[0]: f for f in shift_live.FIELDS}
        self.agent = AgentScreen(self.agent_state, {k: (f[2], f[3]) for k, f in fields.items()},
                                 {k: f[1] for k, f in fields.items()},
                                 lambda key: self.shift.inputs[key].text, self.shift.set_value)
        self.settings = SettingsScreen(self.shift, os.path.join(self.user_data_dir, 'vehicle.json'),
                                       APP_VERSION)
        self.settings.restore()
        self.settings.on_changed = self.show_car
        self.show_car()
        screens = (('shift', 'Shift', 'Shift points', self.shift),
                   ('dyno', 'Dyno', 'Dyno and launch simulation', self.dyno),
                   ('live', 'Live', 'Live engine and transmission', self.live),
                   ('scan', 'Scan', 'OBD-II scanner', self.scan),
                   ('link', 'Link', 'Bluetooth, Wi-Fi and demo', self.link),
                   ('agent', 'Agent', 'Connect your AI agent', self.agent))
        self.titles = {name: subtitle for name, _t, subtitle, _c in screens}
        self.titles['settings'] = 'Settings'
        self.navs = {}
        for name, _title, _subtitle, content in (*screens, ('settings', '', '', self.settings)):
            screen = Screen(name=name)
            screen.add_widget(content)
            self.manager.add_widget(screen)
        root = BoxLayout(orientation='vertical')
        root.add_widget(self.header)
        root.add_widget(self.manager)
        bar = NavBar()
        for name, title, _subtitle, _content in screens:
            nav = NavButton(name, title, self.show)
            self.navs[name] = nav
            bar.add_widget(nav)
        root.add_widget(bar)
        self.session.listeners += [self.header.set_source, self.runner.source_changed,
                                   self.live.source_changed, self.scan.source_changed,
                                   self.link.source_changed]
        self.runner.start()
        Clock.schedule_interval(self.update_cursor, 1.0)
        Clock.schedule_interval(self.check_connection, 2.0)
        self.show('shift')
        self.frame = FloatLayout()
        self.frame.add_widget(root)
        self.frame.add_widget(SplashOverlay())
        return self.frame

    def show_car(self):
        self.shift.car_label.text = (f'{self.settings.summary()}\n{self.shift.ratio_box.text}')

    def show(self, name):
        self.manager.current = name
        self.header.set_screen(self.titles[name])
        self.header.set_source(self.session.status)
        for key, nav in self.navs.items():
            nav.set_active(key == name)
        self.runner.paused = name == 'scan'      # the Scan tab reads the adapter itself
        for key in ('live', 'scan', 'link', 'agent'):
            screen = getattr(self, key)
            (screen.activate if name == key else screen.deactivate)()
        if name == 'shift':
            self.update_cursor(0)

    def on_back(self, _window, key, *_args):
        """Android Back: return to Shift first, then leave the app."""
        if key == 27 and self.manager.current != 'shift':
            self.show('shift')
            return True
        return False

    def request_dyno_refresh(self):
        """Run the dyno again shortly after the last change, so a drag on a slider stays smooth."""
        if self._refresh_event is not None:
            self._refresh_event.cancel()
        self._refresh_event = Clock.schedule_once(lambda dt: self.dyno.refresh(), 0.15)

    def update_cursor(self, _dt):
        """Mark the car's place on the Shift tables, while that screen is showing."""
        if self.manager.current != 'shift':
            return
        stream = self.runner.stream
        self.shift.set_cursor(stream.cursor() if stream is not None else None)

    def check_connection(self, _dt):
        """If a connected adapter stops answering, say so on the Link tab and drop the connection."""
        stream = self.runner.stream
        if self.session.elm is not None and stream is not None and stream.error and not self.session.demo_on:
            self.link.connection_lost(stream.error)

    def agent_state(self):
        """Everything the agent bridge shares: settings, grades, tables and live data. Read only."""
        cfg, tables = self.shift.model()
        grades = self.shift.grading()
        stream = self.runner.stream
        state = {'app': 'TunerToolPro', 'version': APP_VERSION, 'source': self.session.status,
                 'transmission': self.settings.summary(), 'settings': self.shift.settings(), 'ratios': self.shift.ratio_box.text,
                 'live': stream.snapshot() if stream is not None else {},
                 'grades': None, 'tables': {}}
        if grades is not None:
            state['grades'] = {'counts': grades.counts, 'worst': grades.worst[:20]}
            axis = core.tps_axis()
            state['tables'] = {'tps_axis': axis, 'cursor': stream.cursor() if stream else None}
            for name in grading.TABLES:
                state['tables'][name] = {'mph': tables[name], 'levels': grades.levels[name],
                                         'reasons': grades.reasons[name]}
        return state

    def on_stop(self):
        self.runner.stop()
        self.agent.shutdown()
        self.session.detach()


if __name__ == '__main__':
    TunerToolProApp().run()
