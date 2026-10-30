"""The menu behind the three bars at the top right: connection, Live, adapter speed, car and about.

Everything here is saved in prefs.json, so it is the same the next time the app opens. The speed settings
send only the adapter set-up commands from obd.timing_commands, through the same read-only guard as everything
else.
"""

import threading

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.modalview import ModalView
from kivy.uix.togglebutton import ToggleButton

import prefs
from link import obd
from pid_editor_ui import PidEditor
from settings_ui import spinner
from ui_kit import MUTED, STATUS, Card, make_button, panel_label, section_title, stack, style_button


def _toggle(text, state, on_change):
    button = ToggleButton(text=text, size_hint_y=None, height=dp(44), state='down' if state else 'normal')
    style_button(button, primary=state)

    def changed(_button, new_state):
        style_button(button, primary=new_state == 'down')
        on_change(new_state == 'down')
    button.bind(state=changed)
    return button


class AppMenu(ModalView):
    def __init__(self, saved, prefs_path, session, runner, link, open_settings, version, profiles, cars_folder,
                 on_pids_saved, **kwargs):
        super().__init__(size_hint=(0.92, 0.9), background_color=(0, 0, 0, 0.6), **kwargs)
        self.saved, self.prefs_path = saved, prefs_path   # the same dict the Link screen keeps
        self.session, self.runner, self.link = session, runner, link
        self.open_settings = open_settings
        self.profiles, self.cars_folder, self.on_pids_saved = profiles, cars_folder, on_pids_saved

        # A scrollable column, so every section can be reached on a short screen.
        self.add_widget(stack(section_title('Settings'), self._connection_card(), self._live_card(),
                              self._speed_card(), self._pids_card(), self._car_card(version)))
        self.refresh()

    def _save(self, **changes):
        self.saved.update(changes)
        prefs.save(self.prefs_path, self.saved)

    # --- sections -----------------------------------------------------------------------------------

    def _connection_card(self):
        card = Card()
        card.add_widget(section_title('Connection'))
        self.connection_status = panel_label('', color=MUTED, font_size=dp(13))
        card.add_widget(self.connection_status)
        self.connect_button = make_button('Connect', self._toggle_connection, primary=True)
        card.add_widget(self.connect_button)
        card.add_widget(_toggle('Connect automatically when the app opens', self.saved['auto_connect'],
                                lambda on: self._save(auto_connect=on)))
        card.add_widget(panel_label('Each screen uses the one connection. Nothing reads the car until you open '
                                    'the screen that needs it.', color=MUTED, font_size=dp(12)))
        return card

    def _live_card(self):
        card = Card()
        card.add_widget(section_title('Live'))
        card.add_widget(_toggle('Also read the transmission (7E2)', self.saved['live_transmission'],
                                self._set_transmission))
        card.add_widget(panel_label('Off: the engine only, so the adapter talks to one module. On: the transmission '
                                    'is read too, which slows each round a little.', color=MUTED, font_size=dp(12)))
        return card

    def _speed_card(self):
        card = Card()
        card.add_widget(section_title('Adapter speed'))
        card.add_widget(_toggle('Adaptive timing (ATAT1)', self.saved['adaptive_timing'],
                                lambda on: self._save(adaptive_timing=on)))
        labels = {0: 'Adapter default', 100: '100 ms', 200: '200 ms', 400: '400 ms'}
        card.add_widget(panel_label('Response timeout', color=MUTED))
        self.timeout_box = spinner([labels[t] for t in prefs.TIMEOUT_CHOICES_MS],
                                   labels[self.saved['timeout_ms']])
        self.timeout_box.bind(text=lambda _box, text: self._save(
            timeout_ms=next(t for t, label in labels.items() if label == text)))
        card.add_widget(self.timeout_box)
        self.apply_button = make_button('Send to the adapter', self._apply_speed, primary=True)
        card.add_widget(self.apply_button)
        self.speed_status = panel_label('Connect first, then send. The settings are also sent on each connection '
                                        'when they are not the defaults.', color=MUTED, font_size=dp(12))
        card.add_widget(self.speed_status)
        return card

    def _pids_card(self):
        card = Card()
        card.add_widget(section_title('Manual PIDs'))
        card.add_widget(panel_label('Type in a sensor the app does not know yet: its id, formula and unit. It is '
                                    'saved to the car profile you choose, and shows on Live and Scan from then on.',
                                    color=MUTED, font_size=dp(12)))
        card.add_widget(make_button('Enter a PID and save to a profile', self._open_pid_editor, primary=True))
        return card

    def _open_pid_editor(self):
        self.dismiss()
        PidEditor(self.profiles, self.cars_folder, self.on_pids_saved).open()

    def _car_card(self, version):
        card = Card()
        card.add_widget(section_title('Car and about'))
        card.add_widget(make_button('Car and transmission', lambda: self._open_settings()))
        card.add_widget(panel_label(f'TunerToolPro {version}. Read only: the app never writes to the car.',
                                    color=MUTED, font_size=dp(12)))
        return card

    # --- actions ----------------------------------------------------------------------------------

    def refresh(self):
        """Show the current connection state on the menu."""
        connected = self.session.elm is not None
        self.connection_status.text = ('Connected to the adapter.' if connected
                                       else 'Not connected to an adapter.')
        self.connection_status.color = STATUS['good'] if connected else MUTED
        self.connect_button.text = 'Disconnect' if connected else 'Connect'

    def _toggle_connection(self):
        self.link.toggle()
        self.refresh()

    def _set_transmission(self, on):
        self._save(live_transmission=on)
        self.runner.set_transmission(on)

    def _open_settings(self):
        self.dismiss()
        self.open_settings()

    def _apply_speed(self):
        elm = self.session.elm
        if elm is None:
            self.speed_status.text = 'Not connected. Connect to the adapter, then send.'
            self.speed_status.color = STATUS['bad']
            return
        self.apply_button.disabled = True
        self.speed_status.text = 'Sending...'

        def work():
            try:
                sent = obd.send_timing(elm, self.saved['adaptive_timing'], self.saved['timeout_ms'])
                text, colour = f'Sent: {", ".join(sent) or "nothing (adapter defaults)"}.', STATUS['good']
            except obd.OBDError as exc:
                text, colour = str(exc), STATUS['bad']
            Clock.schedule_once(lambda dt: self._speed_done(text, colour))

        threading.Thread(target=work, daemon=True).start()

    def _speed_done(self, text, colour):
        self.apply_button.disabled = False
        self.speed_status.text = text
        self.speed_status.color = colour
