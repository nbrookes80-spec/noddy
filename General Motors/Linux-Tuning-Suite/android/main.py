"""TunerToolPro for Android: Shift Points (live recalculation) and a read-only scan-adapter link."""

import os
import threading

os.environ.setdefault('KIVY_NO_ARGS', '1')

from kivy.app import App  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.metrics import dp  # noqa: E402
from kivy.uix.boxlayout import BoxLayout  # noqa: E402
from kivy.uix.button import Button  # noqa: E402
from kivy.uix.gridlayout import GridLayout  # noqa: E402
from kivy.uix.label import Label  # noqa: E402
from kivy.uix.scrollview import ScrollView  # noqa: E402
from kivy.uix.spinner import Spinner  # noqa: E402
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem  # noqa: E402
from kivy.uix.textinput import TextInput  # noqa: E402

import shift_live  # noqa: E402
from link import obd  # noqa: E402
from tunertoolpro import core  # noqa: E402

LINK_KINDS = ['Wi-Fi adapter', 'Bluetooth adapter']
LIVE_PIDS = [('010C', 'Engine speed'), ('010D', 'Vehicle speed'), ('0111', 'Throttle'),
             ('0105', 'Coolant')]


def scroll_column(*widgets):
    """Stack widgets in a scrollable column that grows with its content."""
    column = GridLayout(cols=1, size_hint_y=None, spacing=dp(6), padding=dp(8))
    column.bind(minimum_height=column.setter('height'))
    for widget in widgets:
        column.add_widget(widget)
    scroll = ScrollView(do_scroll_x=False)
    scroll.add_widget(column)
    return scroll


def wrapping_label(text='', **kwargs):
    label = Label(text=text, size_hint_y=None, halign='left', valign='top', **kwargs)
    label.bind(width=lambda w, _: setattr(w, 'text_size', (w.width, None)))
    label.bind(texture_size=lambda w, size: setattr(w, 'height', size[1]))
    return label


class ShiftScreen(BoxLayout):
    """Inputs on the left side, tables below. Every change re-runs the whole calculation, so a
    dependent value (for example tire diameter or a ratio) moves the tables at once."""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        values, ratios = shift_live.default_inputs()
        self.inputs = {}
        grid = GridLayout(cols=2, size_hint_y=None, spacing=dp(4), padding=dp(4))
        grid.bind(minimum_height=grid.setter('height'))
        for key, label, *_ in shift_live.FIELDS:
            grid.add_widget(Label(text=label, size_hint_y=None, height=dp(32)))
            box = TextInput(text=values[key], multiline=False, input_filter='float',
                            size_hint_y=None, height=dp(32))
            box.bind(text=self.recalculate)
            self.inputs[key] = box
            grid.add_widget(box)
        grid.add_widget(Label(text='Gear ratios (comma separated)', size_hint_y=None, height=dp(32)))
        self.ratio_box = TextInput(text=ratios, multiline=False, size_hint_y=None, height=dp(32))
        self.ratio_box.bind(text=self.recalculate)
        grid.add_widget(self.ratio_box)
        grid.add_widget(Label(text='Lead mode', size_hint_y=None, height=dp(32)))
        self.lead_box = Spinner(text='rpm', values=('rpm', 'torque'), size_hint_y=None, height=dp(32))
        self.lead_box.bind(text=self.recalculate)
        grid.add_widget(self.lead_box)
        grid.add_widget(Label(text='Stall lock logic', size_hint_y=None, height=dp(32)))
        self.stall_box = Spinner(text='Off', values=('Off', 'On'), size_hint_y=None, height=dp(32))
        self.stall_box.bind(text=self.recalculate)
        grid.add_widget(self.stall_box)

        self.status = wrapping_label(color=(0.9, 0.5, 0.2, 1))
        self.output = wrapping_label(font_size=dp(13))
        self.add_widget(scroll_column(grid, self.status, self.output))
        self.recalculate()

    def recalculate(self, *_):
        values = {key: box.text for key, box in self.inputs.items()}
        tables, error = shift_live.calculate(values, self.ratio_box.text, self.lead_box.text,
                                             self.stall_box.text == 'On')
        if error:
            self.status.text = error
            self.output.text = ''
            return
        self.status.text = ''
        self.output.text = format_tables(tables)


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


class LinkScreen(BoxLayout):
    """Connects to a scan adapter and shows live values. Read only: see link/obd.py."""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.elm = None
        self.busy = False
        self.kind = Spinner(text=LINK_KINDS[0], values=LINK_KINDS, size_hint_y=None, height=dp(40))
        self.address = TextInput(text=f'{obd.DEFAULT_WIFI[0]}:{obd.DEFAULT_WIFI[1]}', multiline=False,
                                 size_hint_y=None, height=dp(40))
        self.connect_button = Button(text='Connect', size_hint_y=None, height=dp(44))
        self.connect_button.bind(on_release=self.toggle)
        self.state = wrapping_label(text='Not connected.')
        self.readings = {pid: wrapping_label(text=f'{name}: --', font_size=dp(18))
                         for pid, name in LIVE_PIDS}
        notice = wrapping_label(text=('Read only: this screen never sends a write or clear command to '
                                      'the car. Bluetooth needs the adapter paired in phone settings '
                                      'first. Wi-Fi is the backup if Bluetooth fails.'),
                                font_size=dp(13))
        self.add_widget(scroll_column(self.kind, self.address, self.connect_button, self.state,
                                      *self.readings.values(), notice))
        self.kind.bind(text=self.on_kind)

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
            message = str(exc) if isinstance(exc, obd.OBDError) else 'Enter the adapter as host:port, e.g. 192.168.0.10:35000'
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
        if getattr(self, '_poll_event', None):
            self._poll_event.cancel()
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


class TunerToolProApp(App):
    title = 'TunerToolPro'

    def build(self):
        self.shift = ShiftScreen()
        self.link = LinkScreen()
        panel = TabbedPanel(tab_width=dp(160))
        for title, content in (('Shift Points', self.shift), ('Link', self.link)):
            item = TabbedPanelItem(text=title)
            item.add_widget(content)
            panel.add_widget(item)
        return panel

    def on_stop(self):
        self.link.disconnect()


if __name__ == '__main__':
    TunerToolProApp().run()
