"""TunerToolPro for Android: Shift Points, Dyno and a read-only scan-adapter link."""

import os
import threading

os.environ.setdefault('KIVY_NO_ARGS', '1')

from kivy.app import App  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402
from kivy.graphics import Color, Line, Rectangle  # noqa: E402
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
from tunertoolpro import core  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(HERE, 'icons')

# A dark instrument look: amber for the main values, blue for the second trace.
BG = (0.067, 0.086, 0.110, 1)
PANEL = (0.110, 0.137, 0.169, 1)
TEXT = (1.0, 1.0, 1.0, 1)
MUTED = (0.74, 0.79, 0.84, 1)
ACCENT = (0.96, 0.65, 0.14, 1)
BLUE = (0.47, 0.78, 1.0, 1)
ALERT = (1.0, 0.45, 0.40, 1)

LINK_KINDS = ['Wi-Fi adapter', 'Bluetooth adapter']
LIVE_PIDS = [('010C', 'Engine speed'), ('010D', 'Vehicle speed'), ('0111', 'Throttle'),
             ('0105', 'Coolant')]


def icon(name):
    return os.path.join(ICON_DIR, f'{name}.png')


def style_button(button, primary=False):
    button.background_normal = ''
    button.background_color = ACCENT if primary else PANEL
    button.color = BG if primary else TEXT
    button.size_hint_y = None
    button.height = dp(48)
    button.font_size = dp(14)
    button.halign = 'center'
    button.valign = 'middle'
    button.bind(size=lambda w, _: setattr(w, 'text_size', (w.width - dp(12), None)))
    return button


def panel_label(text='', **kwargs):
    kwargs.setdefault('color', TEXT)
    kwargs.setdefault('halign', 'left')
    kwargs.setdefault('font_size', dp(14))
    label = Label(text=text, size_hint_y=None, valign='top', **kwargs)
    label.bind(width=lambda w, _: setattr(w, 'text_size', (w.width, None)))
    label.bind(texture_size=lambda w, size: setattr(w, 'height', size[1]))
    return label


def section_title(text):
    label = Label(text=text, color=ACCENT, size_hint_y=None, height=dp(34), halign='left',
                  bold=True, font_size=dp(17))
    label.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, None)))
    return label


def scroll_column(*widgets):
    """Stack widgets in a scrollable column that grows with its content."""
    column = GridLayout(cols=1, size_hint_y=None, spacing=dp(8), padding=dp(12))
    column.bind(minimum_height=column.setter('height'))
    for widget in widgets:
        column.add_widget(widget)
    scroll = ScrollView(do_scroll_x=False)
    scroll.add_widget(column)
    return scroll


def snap(value, lo, hi, step):
    """Round a slider position to the field's step, and keep it inside the field's range."""
    stepped = lo + round((value - lo) / step) * step
    return min(max(stepped, lo), hi)


class ShiftScreen(BoxLayout):
    """Each input has a slider and a typed box that stay in step. Any change recalculates the
    shift tables and asks the Dyno screen to run again."""

    def __init__(self, on_change, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.on_change = on_change
        self._syncing = False
        values, ratios = shift_live.default_inputs()
        self.inputs, self.sliders, self.ranges, self.decimals = {}, {}, {}, {}
        column = GridLayout(cols=1, size_hint_y=None, spacing=dp(6), padding=dp(12))
        column.bind(minimum_height=column.setter('height'))
        column.add_widget(section_title('Vehicle and shift settings'))
        for key, label, lo, hi, step, decimals in shift_live.FIELDS:
            column.add_widget(self._field_row(key, label, lo, hi, step, decimals, values[key]))
        column.add_widget(section_title('Gears'))
        self.ratio_box = TextInput(text=ratios, multiline=False, size_hint_y=None, height=dp(44),
                                   background_color=PANEL, foreground_color=TEXT)
        self.ratio_box.bind(text=lambda *_: self.recalculate())
        column.add_widget(panel_label('Gear ratios, comma separated', color=MUTED))
        column.add_widget(self.ratio_box)
        self.lead_box = Spinner(text='rpm', values=('rpm', 'torque'), size_hint_y=None, height=dp(44))
        self.lead_box.bind(text=lambda *_: self.recalculate())
        self.stall_box = Spinner(text='Off', values=('Off', 'On'), size_hint_y=None, height=dp(44))
        self.stall_box.bind(text=lambda *_: self.recalculate())
        column.add_widget(panel_label('Lead mode', color=MUTED))
        column.add_widget(self.lead_box)
        column.add_widget(panel_label('Stall lock logic', color=MUTED))
        column.add_widget(self.stall_box)
        column.add_widget(section_title('Shift tables (MPH)'))
        self.status = panel_label(color=ALERT)
        self.output = panel_label(font_size=dp(13))
        column.add_widget(self.status)
        column.add_widget(self.output)
        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(column)
        self.add_widget(scroll)
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
                        background_color=PANEL, foreground_color=TEXT, font_size=dp(15),
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
        if error:
            self.status.text = error
            self.output.text = ''
        else:
            self.status.text = ''
            self.output.text = format_tables(tables)
        self.on_change()


def format_tables(tables):
    """Plain-text version of the four shift tables, one block per table."""
    blocks = []
    tps = [f'{v:g}%' for v in core.tps_axis()]
    gear_labels = [f'Gear {g + 1}' for g in range(tables['n_gears'])]
    shift_labels = [f'{g + 1}-{g + 2}' for g in range(len(tables['upshift']))]
    sections = [('Upshift MPH', shift_labels, tables['upshift']),
                ('Downshift MPH', shift_labels, tables['downshift']),
                ('TCC unlock MPH', gear_labels, tables['tcc_unlock']),
                ('TCC lock MPH', gear_labels, tables['tcc_lock'])]
    for title, labels, rows in sections:
        lines = [title, '  ' + ' '.join(f'{t:>7}' for t in tps)]
        for label, row in zip(labels, rows):
            lines.append(f'{label:>8}' + ' '.join(f'{x:7.1f}' for x in row))
        blocks.append('\n'.join(lines))
    return '\n\n'.join(blocks)


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
            Color(*PANEL)
            Rectangle(pos=self.pos, size=self.size)
            if len(self.rpms) < 2:
                return
            left, bottom = self.x + dp(40), self.y + dp(24)
            width, height = self.width - dp(52), self.height - dp(40)
            lo, hi = self.rpms[0], self.rpms[-1]
            top = max(max(self.hp), max(self.tq), 1.0) * 1.08

            def point(rpm, value):
                x = left + width * (rpm - lo) / max(hi - lo, 1e-9)
                y = bottom + height * value / top
                return x, y

            Color(0.2, 0.25, 0.3, 1)
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


class DynoScreen(BoxLayout):
    """Simulated or loaded dyno curve, with a launch simulation from the Shift Points settings."""

    def __init__(self, shift_screen, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.shift_screen = shift_screen
        self.curve = None
        self.source = 'Simulated from the Shift Points settings'
        self.chart = DynoChart(size_hint_y=None, height=dp(260))
        self.source_label = panel_label(self.source, color=MUTED)
        self.summary = GridLayout(cols=2, size_hint_y=None, spacing=dp(4))
        self.summary.bind(minimum_height=self.summary.setter('height'))
        self.results = GridLayout(cols=2, size_hint_y=None, spacing=dp(4))
        self.results.bind(minimum_height=self.results.setter('height'))
        self.status = panel_label(color=ALERT)
        load = style_button(Button(text='Load CSV'), primary=True)
        load.bind(on_release=lambda *_: self.choose_csv())
        reset = style_button(Button(text='Simulated'))
        reset.bind(on_release=lambda *_: self.use_simulated())
        buttons = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        buttons.add_widget(load)
        buttons.add_widget(reset)
        self.add_widget(scroll_column(
            buttons,
            self.source_label,
            self.chart,
            section_title('Curve'),
            self.summary,
            section_title('Launch simulation'),
            self.results,
            self.status,
        ))
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
        row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        row.add_widget(cancel)
        row.add_widget(open_button)
        body.add_widget(row)
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
            self.status.text = error
        else:
            self.status.text = ''
            self._fill(self.results, dyno_live.result_rows(result))

    @staticmethod
    def _fill(grid, rows):
        grid.clear_widgets()
        for label, value in rows:
            grid.add_widget(panel_label(label, color=MUTED, font_size=dp(14)))
            grid.add_widget(panel_label(str(value), color=TEXT, font_size=dp(15), halign='right'))


class LinkScreen(BoxLayout):
    """Connects to a scan adapter and shows live values. Read only: see link/obd.py."""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.elm = None
        self.busy = False
        self._poll_event = None
        self.kind = Spinner(text=LINK_KINDS[0], values=LINK_KINDS, size_hint_y=None, height=dp(44))
        self.address = TextInput(text=f'{obd.DEFAULT_WIFI[0]}:{obd.DEFAULT_WIFI[1]}', multiline=False,
                                 size_hint_y=None, height=dp(44), background_color=PANEL,
                                 foreground_color=TEXT)
        self.connect_button = style_button(Button(text='Connect'), primary=True)
        self.connect_button.bind(on_release=self.toggle)
        self.state = panel_label(text='Not connected.', color=MUTED)
        self.readings = {pid: panel_label(text=f'{name}: --', font_size=dp(20), color=TEXT)
                         for pid, name in LIVE_PIDS}
        notice = panel_label(text=('Read only: this screen never sends a write or clear command to '
                                   'the car. Bluetooth needs the adapter paired in phone settings '
                                   'first. Wi-Fi is the backup if Bluetooth fails.'),
                             font_size=dp(13), color=MUTED)
        self.kind.bind(text=self.on_kind)
        self.add_widget(scroll_column(
            section_title('Scan adapter'), self.kind, self.address, self.connect_button, self.state,
            section_title('Live values'), *self.readings.values(), notice))

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
        if self.elm is None:
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
        self.elm = elm
        Clock.schedule_once(lambda dt: self._connected())

    def _connected(self):
        self.connect_button.disabled = False
        self.connect_button.text = 'Disconnect'
        self.state.text = 'Connected. Reading live values every second.'
        self._poll_event = Clock.schedule_interval(self.refresh, 1.0)

    def _failed(self, message):
        self.connect_button.disabled = False
        self.state.text = message

    def disconnect(self):
        if self._poll_event is not None:
            self._poll_event.cancel()
            self._poll_event = None
        if self.elm is not None:
            self.elm.close()
        self.elm = None
        self.connect_button.text = 'Connect'
        self.state.text = 'Not connected.'

    def refresh(self, _dt):
        if self.busy or self.elm is None:
            return
        self.busy = True
        threading.Thread(target=self._poll, daemon=True).start()

    def _poll(self):
        try:
            values, errors = self.elm.poll([pid for pid, _ in LIVE_PIDS])
        except obd.OBDError as exc:
            Clock.schedule_once(lambda dt: self._lost(str(exc)))
            return
        Clock.schedule_once(lambda dt: self._show(values, errors))

    def _show(self, values, errors):
        self.busy = False
        for pid, name in LIVE_PIDS:
            if pid in values:
                value, unit = values[pid]
                self.readings[pid].text = f'{name}: {value:.0f} {unit}'
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
        self.add_widget(Image(source=icon(name), size_hint_y=0.7, allow_stretch=True))
        self.label = Label(text=title, size_hint_y=0.3, color=MUTED, font_size=dp(12))
        self.add_widget(self.label)

    def on_press(self):
        self.on_press_screen(self.screen_name)

    def set_active(self, active):
        self.label.color = ACCENT if active else MUTED


class TunerToolProApp(App):
    title = 'TunerToolPro'

    def build(self):
        Window.clearcolor = BG
        self._refresh_event = None  # must exist before the Shift screen runs its first recalculation
        self.manager = ScreenManager()
        self.shift = ShiftScreen(on_change=self.request_dyno_refresh)
        self.dyno = DynoScreen(self.shift)
        self.link = LinkScreen()
        screens = (('shift', 'Shift', self.shift), ('dyno', 'Dyno', self.dyno),
                   ('link', 'Link', self.link))
        self.navs = {}
        for name, _title, content in screens:
            screen = Screen(name=name)
            screen.add_widget(content)
            self.manager.add_widget(screen)
        root = BoxLayout(orientation='vertical')
        root.add_widget(self.manager)
        bar = BoxLayout(size_hint_y=None, height=dp(64), spacing=dp(2))
        for name, title, _content in screens:
            nav = NavButton(name, title, self.show)
            self.navs[name] = nav
            bar.add_widget(nav)
        root.add_widget(bar)
        self.show('shift')
        return root

    def show(self, name):
        self.manager.current = name
        for key, nav in self.navs.items():
            nav.set_active(key == name)

    def request_dyno_refresh(self):
        """Run the dyno again shortly after the last change, so a drag on a slider stays smooth."""
        if self._refresh_event is not None:
            self._refresh_event.cancel()
        self._refresh_event = Clock.schedule_once(lambda dt: self.dyno.refresh(), 0.15)

    def on_stop(self):
        self.link.disconnect()


if __name__ == '__main__':
    TunerToolProApp().run()
