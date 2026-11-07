"""The Link screen: demo mode, and connecting to a scan adapter over Bluetooth or Wi-Fi.

Bluetooth is first and shows the phone's paired adapters as a list, so nothing has to be typed. See
link/obd.py for everything that is ever sent to the car.
"""

import threading

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

from tunertoolpro import prefs
import variant
from tunertoolpro.link import devices, obd
from settings_ui import spinner
from ui_kit import (ACCENT, ALERT, GOOD, MUTED, RAISED, TEXT, Card, button_row, make_button,
                    panel_label, section_title, stack, style_button)
from ui_kit import toggle as _toggle

_NOTICE = {
    False: 'Read only: this app never sends a write or clear command to the car. It reads the engine computer '
           '(ECU) and the transmission computer (TCM).',
    True: 'The app reads the engine computer (ECU) and the transmission computer (TCM). The one write it can '
          'make is clearing stored codes, from the Scan tab, and only after you confirm.',
}


def _text_box(hint, text=''):
    return TextInput(text=text, hint_text=hint, multiline=False, size_hint_y=None, height=dp(44),
                     background_color=RAISED, foreground_color=TEXT, hint_text_color=MUTED,
                     font_size=dp(14), padding=[dp(10), dp(12), dp(10), dp(10)])


class LinkScreen(BoxLayout):
    def __init__(self, session, prefs_path, on_open_live=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.session = session
        self.prefs_path = prefs_path
        self.on_open_live = on_open_live
        self.saved = prefs.load(prefs_path)
        self.kind = self.saved['link_kind']
        self.bt_address = self.saved['bt_address']
        self._connecting = False
        self._retry_step = None      # None, or how many reconnect tries have been made since the adapter dropped
        self._retry_event = None
        self._attempt = 0            # bumped when a reconnect is stopped; a connect started before that is then dropped

        demo_card = Card()
        demo_card.add_widget(section_title('Demo mode'))
        demo_card.add_widget(panel_label('Simulated readings from a repeating six-speed drive. Nothing is '
                                         'sent to any adapter or car, so it works with no hardware.',
                                         color=MUTED, font_size=dp(13)))
        self.demo_button = make_button('Turn on demo', lambda: session.set_demo(not session.demo_on),
                                       primary=True)
        demo_card.add_widget(self.demo_button)

        self.kind_buttons = {}
        kinds = []
        for name in prefs.KINDS:
            button = style_button(Button(text=name))
            button.bind(on_release=lambda _b, n=name: self.set_kind(n))
            self.kind_buttons[name] = button
            kinds.append(button)

        self.panel = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        self.panel.bind(minimum_height=self.panel.setter('height'))
        self.state = panel_label('Not connected.', color=MUTED)
        self.connect_button = style_button(Button(text='Connect'), primary=True)
        self.connect_button.bind(on_release=self.toggle)
        self.auto_button = ToggleButton(text='Connect automatically when the app opens',
                                        state='down' if self.saved['auto_connect'] else 'normal')
        self._style_auto()
        self.auto_button.bind(state=self._auto_changed)

        self.adapter_card = Card()
        self.adapter_card.add_widget(section_title('Scan adapter'))
        self.adapter_card.add_widget(button_row(*kinds))
        self.adapter_card.add_widget(self.panel)
        self.adapter_card.add_widget(self.connect_button)
        self.adapter_card.add_widget(self.auto_button)
        reconnect = _toggle('Reconnect automatically if the adapter drops', self.saved['auto_reconnect'],
                            lambda on: self._save(auto_reconnect=on))
        self.adapter_card.add_widget(reconnect)
        modules = _toggle('Allow reads of other modules (ABS, meter, A/C) for the Toyota-style pack',
                          self.saved['extra_modules'], self._set_extra_modules)
        self.adapter_card.add_widget(modules)
        self.adapter_card.add_widget(panel_label('Protocol', color=MUTED))
        self.names = {code: f'{code}: {name}' if code != '0' else name for code, name in obd.PROTOCOLS.items()}
        self.protocol_box = spinner(list(self.names.values()), self.names[self.saved['adapter_protocol']])
        self.protocol_box.bind(text=lambda _box, text: self._save(
            adapter_protocol=next(code for code, label in self.names.items() if label == text)))
        self.adapter_card.add_widget(self.protocol_box)
        self.adapter_card.add_widget(panel_label('Read at most this many rounds of readings per second',
                                                 color=MUTED))
        self.rate_box = spinner([str(n) for n in range(obd.RATE_MIN, obd.RATE_MAX + 1)],
                                str(self.saved['read_rate']))
        self.rate_box.bind(text=lambda _box, text: self._save(read_rate=int(text)))
        self.adapter_card.add_widget(self.rate_box)
        self.adapter_card.add_widget(self.state)
        self.info_button = make_button('Adapter information', self.show_info)
        self.info_text = panel_label('', font_size=dp(13))

        self.live_button = make_button('Open Live data', lambda: self.on_open_live and self.on_open_live())
        notice = panel_label(_NOTICE[variant.CLEAR_CODES], font_size=dp(12), color=MUTED)
        self.add_widget(stack(demo_card, self.adapter_card, notice))

        self.bt_status = panel_label('', font_size=dp(13))
        self.bt_action = style_button(Button(text='Refresh'), primary=True)
        self.bt_action.bind(on_release=self.bluetooth_action)
        self.device_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(6))
        self.device_list.bind(minimum_height=self.device_list.setter('height'))
        self.pair_button = make_button('Pair a new adapter', devices.open_pairing_settings)
        self.pair_hint = panel_label('Pair it in the phone\'s Bluetooth settings first (the PIN is usually '
                                     '1234 or 0000), then come back and tap Refresh.', font_size=dp(12),
                                     color=MUTED)
        self.manual = _text_box('Or type the adapter address, e.g. 00:1D:A5:68:98:8B')
        self.wifi_box = _text_box('host:port', self.saved['wifi'])
        self.wifi_hint = panel_label('Join the adapter\'s own Wi-Fi network first (often named WiFi_OBDII or '
                                     'similar). The usual address is 192.168.0.10:35000.', font_size=dp(12),
                                     color=MUTED)
        self._bt_state = devices.UNAVAILABLE
        self.set_kind(self.kind)

    # --- layout ----------------------------------------------------------------------------------

    def set_kind(self, kind):
        self.kind = kind
        for name, button in self.kind_buttons.items():
            style_button(button, primary=(name == kind))
        self.panel.clear_widgets()
        if kind == 'Bluetooth':
            for widget in (self.bt_status, self.bt_action, self.device_list, self.pair_button,
                           self.pair_hint, self.manual):
                self.panel.add_widget(widget)
            self.refresh_bluetooth()
        else:
            self.panel.add_widget(self.wifi_box)
            self.panel.add_widget(self.wifi_hint)

    def refresh_bluetooth(self):
        state, message = devices.adapter_state()
        self._bt_state = state
        self.device_list.clear_widgets()
        colour = {devices.READY: GOOD}.get(state, ALERT)
        self.bt_action.text = {devices.NEEDS_PERMISSION: 'Allow Nearby devices',
                               devices.BLUETOOTH_OFF: 'Turn Bluetooth on'}.get(state, 'Refresh paired adapters')
        self.bt_status.color = colour
        if state != devices.READY:
            self.bt_status.text = message
            return
        found = devices.paired_devices()
        if not found:
            self.bt_status.text = 'No paired adapters yet. Pair your scan adapter, then tap Refresh.'
            self.bt_status.color = ACCENT
            return
        self.bt_status.text = f'{len(found)} paired device(s). Tap your scan adapter:'
        if not self.bt_address:
            likely = [d for d in found if d['likely']]
            if len(likely) == 1:
                self.bt_address = likely[0]['address']
        for device in found:
            star = '★ ' if device['likely'] else ''
            button = style_button(Button(text=f'{star}{device["name"]}   {device["address"]}'),
                                  primary=(device['address'] == self.bt_address))
            button.bind(on_release=lambda _b, d=device: self.pick(d))
            self.device_list.add_widget(button)

    def pick(self, device):
        self.bt_address = device['address']
        self.manual.text = ''
        self.refresh_bluetooth()

    def bluetooth_action(self, *_):
        if self._bt_state == devices.NEEDS_PERMISSION:
            devices.request_permissions()
            Clock.schedule_once(lambda dt: self.refresh_bluetooth(), 2.0)
        elif self._bt_state == devices.BLUETOOTH_OFF:
            devices.ask_to_turn_on()
            Clock.schedule_once(lambda dt: self.refresh_bluetooth(), 3.0)
        else:
            self.refresh_bluetooth()

    # --- lifecycle -------------------------------------------------------------------------------

    def activate(self):
        if self.kind == 'Bluetooth' and self.session.elm is None:
            self.refresh_bluetooth()

    def deactivate(self):
        pass

    def source_changed(self, status):
        demo = status == 'DEMO'
        self.demo_button.text = 'Turn off demo' if demo else 'Turn on demo'
        style_button(self.demo_button, primary=not demo)

    # --- connecting ------------------------------------------------------------------------------

    def make_transport(self):
        if self.kind == 'Bluetooth':
            address = devices.normalise_address(self.manual.text) or self.bt_address
            if not address:
                raise ValueError('Pick your adapter from the list, or type its address.')
            return obd.BluetoothTransport(address), address
        host, _, port = self.wifi_box.text.strip().partition(':')
        devices.bind_to_wifi()
        return obd.WifiTransport(host or obd.DEFAULT_WIFI[0], int(port or obd.DEFAULT_WIFI[1])), ''

    def _set_extra_modules(self, on):
        """Save the module-access switch, and apply it to a link that is already open (it is read at each send)."""
        self._save(extra_modules=on)
        if self.session.elm is not None:
            self.session.elm.extra_modules = on

    def _save(self, **choices):
        self.saved.update(choices)
        prefs.save(self.prefs_path, self.saved)

    def _style_auto(self):
        style_button(self.auto_button, primary=self.auto_button.state == 'down')

    def _auto_changed(self, _button, state):
        self._style_auto()
        self.saved['auto_connect'] = state == 'down'
        prefs.save(self.prefs_path, self.saved)

    def auto_connect(self):
        """Called once when the app opens: connect to the last adapter if the user asked for that."""
        if self.saved['auto_connect']:
            self.ensure_connected()

    def ensure_connected(self):
        """Connect to the saved adapter unless a connection is already open or opening. A screen that needs
        the adapter calls this when it is opened, so each one uses the single shared connection."""
        if self.session.elm is not None or self._connecting or self._retry_step is not None:
            return
        try:
            transport, address = self.make_transport()
        except ValueError:
            return   # no adapter saved yet: the user picks one on this screen
        self._connecting = True
        self.session.log.write('LINK', f'connecting (auto) {self.kind} {address}')
        self.connect_button.disabled = True
        self.state.text = 'Connecting to your last adapter...'
        threading.Thread(target=self._connect, args=(transport, address, self._attempt), daemon=True).start()

    def toggle(self, *_):
        if self._retry_step is not None:       # the button reads "Stop reconnecting" while retries are under way
            self.stop_retrying('Stopped reconnecting.')
            return
        if self.session.elm is not None:
            self.disconnect()
            return
        if self._connecting:
            return
        try:
            transport, address = self.make_transport()
        except ValueError as exc:
            hint = 'Enter the adapter as host:port, e.g. 192.168.0.10:35000'
            self.state.text = str(exc) if 'adapter' in str(exc) else hint
            return
        self._connecting = True
        self.session.log.write('LINK', f'connecting {self.kind} {address}')
        self.connect_button.disabled = True
        self.state.text = 'Connecting...'
        threading.Thread(target=self._connect, args=(transport, address, self._attempt), daemon=True).start()

    def _connect(self, transport, address, attempt):
        try:
            elm = obd.Elm327(transport, allow_clear=variant.CLEAR_CODES, extra_modules=self.saved['extra_modules'])
            elm.on_traffic = self.session.log.write   # so the set-up handshake is logged too
            elm.open()
        except obd.OBDError as exc:
            self.session.log.write('ERR', f'connect failed: {type(exc).__name__}: {exc}')
            Clock.schedule_once(lambda dt, m=str(exc): self._failed(m, attempt))
            return
        Clock.schedule_once(lambda dt: self._connected(elm, address, attempt))

    def _connected(self, elm, address, attempt):
        self._connecting = False
        if attempt != self._attempt:          # the user pressed Stop while this try was under way: drop the link
            elm.close()
            self.connect_button.disabled = False
            self.connect_button.text = 'Connect'
            self.state.text = 'Reconnecting was stopped.'
            return
        self._retry_step = None
        self.connect_button.disabled = False
        self.connect_button.text = 'Disconnect'
        self.state.text = 'Connected. The Live tab is now streaming the engine and transmission.'
        prefs.save(self.prefs_path, dict(self.saved, link_kind=self.kind, bt_address=address or self.bt_address,
                                         wifi=self.wifi_box.text.strip() or self.saved['wifi']))
        self.session.attach(elm)
        if self.saved['adaptive_timing'] or self.saved['timeout_ms'] or self.saved['adapter_protocol'] != '0':
            threading.Thread(target=self._send_speed, args=(elm,), daemon=True).start()
        if self.live_button.parent is None:
            self.adapter_card.add_widget(self.live_button)
        if self.info_button.parent is None:
            self.adapter_card.add_widget(self.info_button)
            self.adapter_card.add_widget(self.info_text)

    def _send_speed(self, elm):
        """The saved speed settings, sent once the connection is open. A refusal leaves the adapter's own timing."""
        try:
            with self.session.adapter_job():     # the Live reader stands aside until the settings are sent
                obd.send_timing(elm, self.saved['adaptive_timing'], self.saved['timeout_ms'])
                obd.use_protocol(elm, self.saved['adapter_protocol'])   # the saved protocol, else back to Automatic
        except obd.OBDError:
            pass

    def show_info(self, *_):
        elm = self.session.elm
        if elm is None:
            self.info_text.text = 'Not connected.'
            return
        self.info_button.disabled = True
        self.info_text.text = 'Asking the adapter...'

        def work():
            text = 'Could not read the adapter.'
            try:
                with self.session.adapter_job():     # the Live reader stands aside while the adapter answers
                    info = obd.read_adapter_info(elm)
                text = info_text(info)
            except obd.OBDError as exc:
                text = str(exc)
            finally:
                Clock.schedule_once(lambda dt, t=text: self._info_done(t))   # always, so the button comes back

        threading.Thread(target=work, daemon=True).start()

    def _info_done(self, text):
        self.info_button.disabled = False
        self.info_text.text = text

    def _failed(self, message, attempt):
        self._connecting = False
        self.connect_button.disabled = False
        if attempt != self._attempt:
            return                            # stopped meanwhile: the Stopped text stays
        self.state.text = message
        if self._retry_step is not None:
            self._schedule_retry(f'Still not connected ({message}).')

    def disconnect(self):
        self._cancel_retry()
        self.session.detach()
        devices.release_wifi()
        self.connect_button.text = 'Connect'
        self.state.text = 'Not connected.'
        for widget in (self.live_button, self.info_button, self.info_text):
            if widget.parent is not None:
                self.adapter_card.remove_widget(widget)
        self.info_text.text = ''

    def connection_lost(self, message):
        self.session.log.write('LINK', f'connection lost: {message}')
        self.disconnect()
        self.state.text = f'Connection lost: {message}'
        if self.saved['auto_reconnect']:
            self._retry_step = 0
            self._schedule_retry(f'Connection lost: {message}.')

    # --- reconnecting ----------------------------------------------------------------------------

    def _schedule_retry(self, lead):
        """Wait the next backoff step, then try again; after the last step, stop and say so."""
        schedule = obd.backoff_schedule()
        if self._retry_step >= len(schedule):
            self._retry_step = None
            self.connect_button.text = 'Connect'
            self.state.text = f'{lead} Gave up after {len(schedule)} tries. Tap Connect to try again.'
            self.session.log.write('LINK', 'reconnect gave up')
            return
        delay = schedule[self._retry_step]
        self.connect_button.text = 'Stop reconnecting'
        self.state.text = f'{lead} Trying again in {delay} s (try {self._retry_step + 1} of {len(schedule)}).'
        self._retry_event = Clock.schedule_once(lambda dt: self._retry_now(), delay)

    def _retry_now(self):
        self._retry_event = None
        if self._retry_step is None or self._connecting:
            return
        number = self._retry_step + 1
        self._retry_step += 1       # counts this try; _failed then waits for the next step
        try:
            transport, address = self.make_transport()
        except ValueError as exc:
            self.stop_retrying(str(exc))
            return
        self._connecting = True
        self.session.log.write('LINK', f'reconnecting (try {number}) {self.kind} {address}')
        self.state.text = f'Reconnecting (try {number} of {len(obd.backoff_schedule())})...'
        threading.Thread(target=self._connect, args=(transport, address, self._attempt), daemon=True).start()

    def _cancel_retry(self):
        self._attempt += 1
        self._retry_step = None
        if self._retry_event is not None:
            self._retry_event.cancel()
            self._retry_event = None

    def stop_retrying(self, message):
        self._cancel_retry()
        self.connect_button.text = 'Connect'
        self.state.text = message


def info_text(info):
    """The Adapter information card text from obd.read_adapter_info(), one line per item."""
    lines = [('Adapter', info['firmware']), ('Adapter volts', info['adapter_volts']),
             ('Protocol in use', info['protocol']), ('Car battery', info['car_volts'])]
    return '\n'.join(f'{label}: {value or "no answer"}' for label, value in lines)
