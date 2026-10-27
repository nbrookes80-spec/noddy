"""TunerToolPro for Android: Shift Points, Dyno, an OBD-II scanner and a read-only adapter link."""

import os
import threading

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
import shift_live  # noqa: E402
from link import obd  # noqa: E402
from scan_ui import ScanScreen, format_value  # noqa: E402
from scanner.session import Session  # noqa: E402
from tunertoolpro import core  # noqa: E402
from ui_kit import (ACCENT, ALERT, BG, BLUE, BORDER, GAP, MUTED, RAISED, TEXT, Card,  # noqa: E402
                    HeaderBar, button_row, icon, make_button, panel_label, section_title, stack,
                    style_button)

MONO = os.path.join(kivy_data_dir, 'fonts', 'RobotoMono-Regular.ttf')
LINK_KINDS = ['Wi-Fi adapter', 'Bluetooth adapter']
LIVE_PIDS = [('010C', 'Engine speed'), ('010D', 'Vehicle speed'), ('0111', 'Throttle'),
             ('0105', 'Coolant')]

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
                  halign='left', valign='top')
    label.bind(texture_size=lambda w, size: setattr(w, 'size', size))
    scroll = ScrollView(do_scroll_y=False, size_hint_y=None, bar_width=dp(3))
    scroll.add_widget(label)
    label.bind(height=lambda _w, h: setattr(scroll, 'height', h + dp(8)))
    return scroll


class ShiftScreen(BoxLayout):
    """Each input has a slider and a typed box that stay in step. Any change recalculates the
    shift tables and asks the Dyno screen to run again."""

    def __init__(self, on_change, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.on_change = on_change
        self._syncing = False
        values, ratios = shift_live.default_inputs()
        self.inputs, self.sliders, self.ranges, self.decimals = {}, {}, {}, {}
        fields = {f[0]: f for f in shift_live.FIELDS}
        widgets = []
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
        widgets += [self.status, section_title('Shift tables (MPH)'), self.tables]
        self.add_widget(stack(*widgets))
        self.recalculate()

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
        if error:
            self.status.text = error
        else:
            self.status.text = ''
            for title, text in table_blocks(tables):
                card = Card()
                card.add_widget(panel_label(title, color=ACCENT, bold=True))
                card.add_widget(mono_scroller(text))
                self.tables.add_widget(card)
        self.on_change()


def table_blocks(tables):
    """The four shift tables as (title, text) pairs, one block per table."""
    blocks = []
    tps = [f'{v:g}%' for v in core.tps_axis()]
    gear_labels = [f'Gear {g + 1}' for g in range(tables['n_gears'])]
    shift_labels = [f'{g + 1}-{g + 2}' for g in range(len(tables['upshift']))]
    sections = [('Upshift MPH', shift_labels, tables['upshift']),
                ('Downshift MPH', shift_labels, tables['downshift']),
                ('TCC unlock MPH', gear_labels, tables['tcc_unlock']),
                ('TCC lock MPH', gear_labels, tables['tcc_lock'])]
    for title, labels, rows in sections:
        lines = ['        ' + ' '.join(f'{t:>7}' for t in tps)]
        for label, row in zip(labels, rows):
            lines.append(f'{label:>8}' + ' '.join(f'{x:7.1f}' for x in row))
        blocks.append((title, '\n'.join(lines)))
    return blocks


def format_tables(tables):
    """Plain-text version of the four shift tables, one block per table."""
    return '\n\n'.join(f'{title}\n{text}' for title, text in table_blocks(tables))


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


class LinkScreen(BoxLayout):
    """Demo mode, and a connection to a scan adapter with live values. Read only: see link/obd.py."""

    def __init__(self, session, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.session = session
        self.busy = False
        self._poll_event = None
        self._connecting = False

        demo_card = Card()
        demo_card.add_widget(section_title('Demo mode'))
        demo_card.add_widget(panel_label('Simulated readings from a repeating drive. Nothing is sent to '
                                         'any adapter or car, so it works with no hardware.',
                                         color=MUTED, font_size=dp(13)))
        self.demo_button = make_button('Turn on demo', lambda: session.set_demo(not session.demo_on),
                                       primary=True)
        demo_card.add_widget(self.demo_button)

        adapter_card = Card()
        adapter_card.add_widget(section_title('Scan adapter'))
        self.kind = Spinner(text=LINK_KINDS[0], values=LINK_KINDS)
        style_button(self.kind)
        self.address = TextInput(text=f'{obd.DEFAULT_WIFI[0]}:{obd.DEFAULT_WIFI[1]}', multiline=False,
                                 size_hint_y=None, height=dp(44), background_color=RAISED,
                                 foreground_color=TEXT, font_size=dp(14),
                                 padding=[dp(10), dp(12), dp(10), dp(10)])
        self.connect_button = style_button(Button(text='Connect'), primary=True)
        self.connect_button.bind(on_release=self.toggle)
        self.state = panel_label(text='Not connected.', color=MUTED)
        self.kind.bind(text=self.on_kind)
        for widget in (self.kind, self.address, self.connect_button, self.state):
            adapter_card.add_widget(widget)

        values_card = Card()
        values_card.add_widget(section_title('Live values'))
        self.readings = {pid: panel_label(text=f'{name}: --', font_size=dp(20), color=TEXT)
                         for pid, name in LIVE_PIDS}
        for label in self.readings.values():
            values_card.add_widget(label)
        notice = panel_label(text=('Read only: this app never sends a write or clear command to the car. '
                                   'Bluetooth needs the adapter paired in phone settings first. Wi-Fi is '
                                   'the backup if Bluetooth fails.'), font_size=dp(12), color=MUTED)
        self.add_widget(stack(demo_card, adapter_card, values_card, notice))

    # --- screen lifecycle ------------------------------------------------------------------------

    def activate(self):
        if self._poll_event is None:
            self._poll_event = Clock.schedule_interval(self.refresh, 1.0)

    def deactivate(self):
        if self._poll_event is not None:
            self._poll_event.cancel()
            self._poll_event = None

    def source_changed(self, status):
        demo = status == 'DEMO'
        self.demo_button.text = 'Turn off demo' if demo else 'Turn on demo'
        style_button(self.demo_button, primary=not demo)
        if status == 'OFFLINE':
            for pid, name in LIVE_PIDS:
                self.readings[pid].text = f'{name}: --'

    # --- adapter connection ----------------------------------------------------------------------

    def on_kind(self, _spinner, text):
        if text == 'Bluetooth adapter':
            self.address.text = ''
            self.address.hint_text = 'Adapter address, e.g. 00:1D:A5:00:00:00'
        else:
            self.address.text = f'{obd.DEFAULT_WIFI[0]}:{obd.DEFAULT_WIFI[1]}'

    def make_transport(self):
        if self.kind.text == 'Bluetooth adapter':
            return obd.BluetoothTransport(self.address.text.strip())
        host, _, port = self.address.text.strip().partition(':')
        return obd.WifiTransport(host or obd.DEFAULT_WIFI[0], int(port or obd.DEFAULT_WIFI[1]))

    def toggle(self, *_):
        if self.session.elm is None:
            if self._connecting:
                return
            self._connecting = True
            self.connect_button.disabled = True
            self.state.text = 'Connecting...'
            threading.Thread(target=self._connect, daemon=True).start()
        else:
            self.disconnect()

    def _connect(self):
        try:
            elm = obd.Elm327(self.make_transport())
            elm.open()
        except (obd.OBDError, ValueError) as exc:
            message = (str(exc) if isinstance(exc, obd.OBDError)
                       else 'Enter the adapter as host:port, e.g. 192.168.0.10:35000')
            Clock.schedule_once(lambda dt: self._failed(message))
            return
        Clock.schedule_once(lambda dt: self._connected(elm))

    def _connected(self, elm):
        self._connecting = False
        self.connect_button.disabled = False
        self.connect_button.text = 'Disconnect'
        self.state.text = 'Connected. Reading live values every second.'
        self.session.attach(elm)

    def _failed(self, message):
        self._connecting = False
        self.connect_button.disabled = False
        self.state.text = message

    def disconnect(self):
        self.session.detach()
        self.connect_button.text = 'Connect'
        self.state.text = 'Not connected.'

    # --- reading ---------------------------------------------------------------------------------

    def refresh(self, _dt):
        source = self.session.active()
        if self.busy or source is None:
            return
        self.busy = True
        threading.Thread(target=self._poll, args=(source,), daemon=True).start()

    def _poll(self, source):
        try:
            values, errors = source.poll([pid for pid, _ in LIVE_PIDS])
        except obd.OBDError as exc:
            Clock.schedule_once(lambda dt: self._lost(str(exc)))
            return
        Clock.schedule_once(lambda dt: self._show(values, errors))

    def _show(self, values, errors):
        self.busy = False
        for pid, name in LIVE_PIDS:
            if pid in values:
                number, unit = format_value(*values[pid])
                self.readings[pid].text = f'{name}: {number} {unit}'
            else:
                self.readings[pid].text = f'{name}: {errors.get(pid, "no reply")}'

    def _lost(self, message):
        self.busy = False
        self.disconnect()
        self.state.text = f'Connection lost: {message}'


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
        self.header = HeaderBar()
        self.shift = ShiftScreen(on_change=self.request_dyno_refresh)
        self.dyno = DynoScreen(self.shift)
        self.scan = ScanScreen(self.session)
        self.link = LinkScreen(self.session)
        screens = (('shift', 'Shift', 'Shift points', self.shift),
                   ('dyno', 'Dyno', 'Dyno and launch simulation', self.dyno),
                   ('scan', 'Scan', 'OBD-II scanner', self.scan),
                   ('link', 'Link', 'Data source and adapter', self.link))
        self.titles = {name: subtitle for name, _t, subtitle, _c in screens}
        self.navs = {}
        for name, _title, _subtitle, content in screens:
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
        self.session.listeners += [self.header.set_source, self.scan.source_changed,
                                   self.link.source_changed]
        self.show('shift')
        return root

    def show(self, name):
        self.manager.current = name
        self.header.set_screen(self.titles[name])
        self.header.set_source(self.session.status)
        for key, nav in self.navs.items():
            nav.set_active(key == name)
        (self.scan.activate if name == 'scan' else self.scan.deactivate)()
        (self.link.activate if name == 'link' else self.link.deactivate)()

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

    def on_stop(self):
        self.session.detach()


if __name__ == '__main__':
    TunerToolProApp().run()
