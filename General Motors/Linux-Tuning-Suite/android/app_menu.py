"""The menu behind the three bars at the top right: a list of settings pages that open inside the same popup.

Pages: dashboard layout and themes, PID manager, log data parameters, OBD-II adapter settings and tweaks, the
pre-defined GM and Holden PID lists, the debug log, and the car and about page. The pages that are mostly cards
of choices live in menu_pages.py.

Everything here is saved in prefs.json, so it is the same the next time the app opens. The adapter settings
send only the set-up commands from obd.send_timing, through the same read-only guard as everything else.
"""

import threading

from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

import prefs
from link import obd
from pid_editor_ui import PidEditor
from settings_ui import spinner
import menu_pages
from ui_kit import MUTED, RAISED, TEXT, STATUS, Card, make_button, panel_label, section_title, stack, style_button

PAGES = (
    ('dashboard', 'Dashboard layout and themes', 'Cards across, sensor display, gauge colours, full screen'),
    ('pids', 'PID manager', 'Switch sensors on and off, enter a PID by hand'),
    ('logging', 'Log data parameters', 'Which sensors and how often a data log row is written'),
    ('adapter', 'OBD-II adapter settings and tweaks', 'Connection, timing, timeout, protocol'),
    ('lists', 'GM and Holden PID lists', 'Pre-defined lists, saved to a profile for your car'),
    ('debug', 'Debug log', 'What happened, for finding faults'),
    ('about', 'Car and about', 'Car and transmission, version'),
)


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
                 on_pids_saved, recorder=None, on_fullscreen=None, **kwargs):
        super().__init__(size_hint=(0.92, 0.9), background_color=(0, 0, 0, 0.6), **kwargs)
        self.saved, self.prefs_path = saved, prefs_path   # the same dict the Link screen keeps
        self.session, self.runner, self.link = session, runner, link
        self.open_settings = open_settings
        self.profiles, self.cars_folder, self.on_pids_saved = profiles, cars_folder, on_pids_saved
        self.recorder, self.on_fullscreen, self.version = recorder, on_fullscreen, version

        self.show_hub()

    # --- pages --------------------------------------------------------------------------------------

    def active_profile(self):
        """The car whose PID list is on the dashboard now, or None for the standard list."""
        return next((p for p in self.profiles if p.key == self.saved['scan_profile']), None)

    def show_hub(self):
        """The list of pages, with the connection on top."""
        self._forget_page()
        self._set_page(section_title('Settings'), self._connection_card(), *self._page_buttons())
        self.refresh()

    def open_page(self, key):
        title = next(t for k, t, _d in PAGES if k == key)
        builders = {'dashboard': menu_pages.dashboard_cards, 'pids': menu_pages.pid_manager_cards,
                    'logging': menu_pages.log_cards, 'adapter': self._adapter_cards, 'lists': menu_pages.lists_cards,
                    'debug': lambda _menu: [self._log_card()], 'about': lambda _menu: [self._car_card(self.version)]}
        back = make_button('< Settings', self.show_hub)
        self._forget_page()
        self._set_page(back, section_title(title), *builders[key](self))
        self._show_log_path()
        self._show_recording()
        self.refresh()

    def _forget_page(self):
        """Drop the handles to the widgets of the page being left, before the next page builds its own."""
        for name in ('connection_status', 'connect_button', 'log_button', 'record_button'):
            self.__dict__.pop(name, None)

    def _set_page(self, *widgets):
        """Replace what the popup shows. A scrollable column, so every section can be reached on a short screen."""
        self.clear_widgets()
        self.add_widget(stack(*widgets))

    def _page_buttons(self):
        buttons = []
        for key, title, detail in PAGES:
            small = int(dp(12))     # markup sizes are pixels, not dp
            button = Button(text=f'{title}\n[size={small}][color=bfc9d6]{detail}[/color][/size]', markup=True)
            style_button(button)
            button.height = dp(76)
            button.bind(on_release=lambda _b, key=key: self.open_page(key))
            buttons.append(button)
        return buttons

    def _adapter_cards(self, _menu):
        return [self._connection_card(), self._live_card(), self._speed_card()]

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
        card.add_widget(section_title('Adapter timing and protocol'))
        card.add_widget(_toggle('Adaptive timing (ATAT1)', self.saved['adaptive_timing'],
                                lambda on: self._save(adaptive_timing=on)))
        labels = {0: 'Adapter default', 100: '100 ms', 200: '200 ms', 400: '400 ms'}
        card.add_widget(panel_label('Response timeout', color=MUTED))
        self.timeout_box = spinner([labels[t] for t in prefs.TIMEOUT_CHOICES_MS],
                                   labels[self.saved['timeout_ms']])
        self.timeout_box.bind(text=lambda _box, text: self._save(
            timeout_ms=next(t for t, label in labels.items() if label == text)))
        card.add_widget(self.timeout_box)
        names = {code: f'{code}: {name}' if code != '0' else name for code, name in obd.PROTOCOLS.items()}
        card.add_widget(panel_label('Protocol', color=MUTED))
        self.protocol_box = spinner(list(names.values()), names[self.saved['adapter_protocol']])
        self.protocol_box.bind(text=lambda _box, text: self._save(
            adapter_protocol=next(code for code, label in names.items() if label == text)))
        card.add_widget(self.protocol_box)
        card.add_widget(panel_label('Leave the protocol on Automatic unless the adapter cannot find the car. A '
                                    'Holden VE or VF talks CAN 11-bit at 500 kbaud.', color=MUTED, font_size=dp(12)))
        self.apply_button = make_button('Send to the adapter', self._apply_speed, primary=True)
        card.add_widget(self.apply_button)
        self.speed_status = panel_label('Connect first, then send. The settings are also sent on each connection '
                                        'when they are not the defaults.', color=MUTED, font_size=dp(12))
        card.add_widget(self.speed_status)
        return card

    def _open_pid_editor(self):
        self.dismiss()
        PidEditor(self.profiles, self.cars_folder, self.on_pids_saved).open()

    def _toggle_recording(self):
        if self.recorder is not None:
            self.record_status.text = self.recorder.toggle()
            self.record_status.color = STATUS['good'] if self.recorder.running else MUTED
            self._show_recording()

    def _show_recording(self):
        if not hasattr(self, 'record_button'):
            return
        running = self.recorder is not None and self.recorder.running
        self.record_button.text = 'Stop recording' if running else 'Start recording'

    def _fullscreen(self):
        self.dismiss()
        if self.on_fullscreen is not None:
            self.on_fullscreen(True)

    def _log_card(self):
        card = Card()
        card.add_widget(section_title('Debug log (what happened)'))
        card.add_widget(panel_label('Saves a file of each run: screens opened, what the adapter was sent and '
                                    'answered, errors and crashes. Files are named by date and time in Tuner Tool Info / '
                                    'Debug logs. Bring one back to find out what went wrong.',
                                    color=MUTED, font_size=dp(12)))
        self.log_button = make_button('', self._toggle_log, primary=True)
        card.add_widget(self.log_button)
        self.log_path = panel_label('', color=MUTED, font_size=dp(11))
        card.add_widget(self.log_path)
        self.note_box = TextInput(hint_text='Note for the log, e.g. "engine running, in park"', multiline=False,
                                  size_hint_y=None, height=dp(44), background_color=RAISED,
                                  foreground_color=TEXT, hint_text_color=MUTED)
        card.add_widget(self.note_box)
        card.add_widget(make_button('Add note to the log', self._add_note))
        card.add_widget(make_button('Copy the end of the log', self._copy_log))
        card.add_widget(make_button('Save a copy to Documents now', self._publish_log))
        self.log_status = panel_label('', color=MUTED, font_size=dp(12))
        card.add_widget(self.log_status)
        return card

    def _toggle_log(self):
        """Stop the log, or start a fresh file for the drive about to be tested."""
        if self.session.log.enabled:
            self.session.log.set_enabled(False)
            self._save(debug_log=False)
        else:
            self.session.log.new_file()
            self._save(debug_log=True)
        self._show_log_path()

    def _show_log_path(self):
        if not hasattr(self, 'log_button'):
            return
        log = self.session.log
        self.log_button.text = 'Stop logging' if log.enabled else 'Start logging'
        self.log_path.text = (f'Logging to: {log.path}' if log.path else 'Logging.') if log.enabled else 'Logging is off.'

    def _add_note(self):
        text = self.note_box.text.strip()
        if text:
            self.session.log.write('NOTE', text)
            self.note_box.text = ''
            self.log_status.text = 'Note added.'
        self._show_log_path()

    def _publish_log(self):
        if self.recorder is not None:
            self.recorder.publish_debug()
            self.log_status.text = 'Copying to Documents / Tuner Tool Info / Debug logs...'

    def _copy_log(self):
        text = self.session.log.tail()
        if not text:
            self.log_status.text = 'Nothing logged yet.'
            return
        Clipboard.copy(text)
        self.log_status.text = f'Copied {len(text.splitlines())} lines. Paste them into the chat.'

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
        if not hasattr(self, 'connection_status'):
            return
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
                sent = obd.send_timing(elm, self.saved['adaptive_timing'], self.saved['timeout_ms'],
                                       protocol=self.saved['adapter_protocol'])
                text, colour = f'Sent: {", ".join(sent) or "nothing (adapter defaults)"}.', STATUS['good']
            except obd.OBDError as exc:
                text, colour = str(exc), STATUS['bad']
            Clock.schedule_once(lambda dt: self._speed_done(text, colour))

        threading.Thread(target=work, daemon=True).start()

    def _speed_done(self, text, colour):
        self.apply_button.disabled = False
        self.speed_status.text = text
        self.speed_status.color = colour
