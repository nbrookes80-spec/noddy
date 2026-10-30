"""The Sniff screen: watch which CAN IDs are active and which bytes and bits change.

Receive only. On the adapter that is connected on the Link tab it listens with the ELM327 "monitor
all" command and sends nothing to the car (see tunertoolpro/canbus/monitor.py). It can also play a
log file or a simulated bus, so it can be learned with no adapter. The ID tracking is a port of the
Sniffer in SavvyCAN; see docs/THIRD_PARTY.md. The row text comes from sniffer_view.py.
"""

import os
import threading

from kivy import kivy_data_dir
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

import sniffer_view
from link.obd import OBDError
from scanner import car_check, profiles
from tunertoolpro.canbus import MonitorError, PROTOCOLS, SnifferSession, read_log
from ui_kit import (ACCENT, ALERT, GOOD, MUTED, RAISED, TEXT, Card, WrapOption, button_row, make_button,
                    panel_label, section_title, stack, style_button)

MONO = os.path.join(kivy_data_dir, 'fonts', 'RobotoMono-Regular.ttf')
POLL_SECONDS = 0.05
CHECK_SECONDS = 60     # how long 'Check this car' records the bus
CHECK_LINES = 30       # lines of the result shown on screen; the full report is in the saved files
REFRESH_SECONDS = 0.2
SOURCES = ('Simulated', 'Adapter', 'Log file')
LABELS = {'Simulated': 'Demo'}      # the button text, where it has to be shorter than the source's name


MONO_WIDTH = 0.62      # width of a RobotoMono character as a fraction of its font size


def _mono_label(chars, **kwargs):
    """A monospace label whose font shrinks until `chars` characters fit on one line, so rows never wrap."""
    label = Label(font_name=MONO, font_size=dp(11), color=TEXT, size_hint_y=None, halign='left', valign='top',
                  markup=True, **kwargs)

    def fit(widget, width):
        widget.text_size = (width, None)
        if width > 0:
            widget.font_size = max(dp(6), min(dp(11), width / (chars * MONO_WIDTH)))

    label.bind(width=fit)
    label.bind(texture_size=lambda w, size: setattr(w, 'height', size[1]))
    return label


def _text_box(hint, text=''):
    return TextInput(text=text, hint_text=hint, multiline=False, size_hint_y=None, height=dp(44),
                     background_color=RAISED, foreground_color=TEXT, hint_text_color=MUTED,
                     font_size=dp(14), padding=[dp(10), dp(12), dp(10), dp(10)])


class SnifferScreen(BoxLayout):
    def __init__(self, session, runner, folder, on_open_link=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app_session = session          # the connected adapter, if any (Link tab)
        self.runner = runner                # the Live reader, which must stand aside while we listen
        self.folder = folder                # where captures are saved
        self.data_dir = os.path.dirname(folder)   # the app's data folder: cars/ and car_scans/ live here
        self.car_profiles = {}
        self._checking = False
        self.on_open_link = on_open_link
        self.sniff = SnifferSession()
        self.kind = 'Simulated'
        self.log_frames = None
        self.log_name = ''
        self.active = False
        self._starting = False
        self._events = []

        source = Card()
        source.add_widget(section_title('CAN sniffer'))
        source.add_widget(panel_label(
            'Shows only the CAN IDs that are updating. A byte that went up is green (+), one that went down '
            'is red (-). Hold still and press Notch a few times to mute the bits that always change, then '
            'move the thing you are hunting for (steering, a pedal, a switch) and watch which ID lights up. '
            'Receive only: nothing is sent to the car.', color=MUTED, font_size=dp(13)))
        self.source_buttons = {}
        buttons = []
        for name in SOURCES:
            button = style_button(Button(text=LABELS.get(name, name)))
            button.font_size = dp(12)
            button.bind(on_release=lambda _b, n=name: self.set_kind(n))
            self.source_buttons[name] = button
            buttons.append(button)
        source.add_widget(button_row(*buttons))
        self.source_note = panel_label('', color=MUTED, font_size=dp(13))
        source.add_widget(self.source_note)
        self.bus_box = Spinner(text=self._bus_label('6'), values=[self._bus_label(k) for k in PROTOCOLS],
                               size_hint_y=None, height=dp(48), option_cls=WrapOption)
        self.filter_box = _text_box('Hear only this ID, hex (optional)')
        self.log_button = make_button('Choose a log file', self.choose_log)
        self.extra = BoxLayout(orientation='vertical', size_hint_y=None, height=0, spacing=dp(8))   # per-source controls
        self.extra.bind(minimum_height=self.extra.setter('height'))
        source.add_widget(self.extra)
        self.start_button = style_button(Button(text='Start', size_hint_y=None, height=dp(52)), primary=True)
        self.start_button.bind(on_release=lambda *_: self.toggle())
        source.add_widget(self.start_button)
        self.state = panel_label('Stopped.', color=MUTED)
        source.add_widget(self.state)

        controls = Card()
        controls.add_widget(section_title('Notching'))
        self.notch_button = make_button('Notch', lambda: self.sniff.sniffer.notch(), primary=True)
        self.unnotch_button = make_button('Unnotch', lambda: self.sniff.sniffer.unnotch())
        self.clear_button = make_button('Clear', self.clear)
        for button in (self.notch_button, self.unnotch_button, self.clear_button):
            button.font_size = dp(12)
        controls.add_widget(button_row(self.notch_button, self.unnotch_button, self.clear_button))
        self.options = {}
        for key, text in (('never_expire', 'Keep IDs'), ('mute_notched', 'Mute notched'),
                          ('fade_inactive', 'Fade quiet')):
            toggle = ToggleButton(text=text)
            style_button(toggle)
            toggle.height = dp(44)
            toggle.font_size = dp(12)
            toggle.bind(state=lambda b, state, k=key: setattr(self.sniff.sniffer, k, state == 'down'))
            self.options[key] = toggle
        controls.add_widget(button_row(*self.options.values(), height=dp(44)))
        self.only_box = _text_box('Only these IDs, hex')
        self.only_box.bind(on_text_validate=lambda *_: self.apply_filter(), focus=self._leave_filter)
        controls.add_widget(self.only_box)
        self.bits_box = _text_box('Show the bits of one ID, hex')
        controls.add_widget(self.bits_box)

        frames = Card()
        frames.add_widget(section_title('Frames'))
        self.table = _mono_label(sniffer_view.LINE_CHARS, text='Press Start.')
        frames.add_widget(self.table)
        self.bits_card = Card()
        self.bits_card.add_widget(section_title('Bits'))
        self.bits = _mono_label(30, text='')
        self.bits_card.add_widget(self.bits)
        saving = Card()
        saving.add_widget(section_title('Save'))
        saving.add_widget(make_button('Save the captured frames', self.save))
        self.save_note = panel_label('', color=MUTED, font_size=dp(13))
        saving.add_widget(self.save_note)

        self.scroller = stack(self._check_card(), source, controls, frames, self.bits_card, saving)
        self.add_widget(self.scroller)
        self.set_kind('Simulated')

    def _check_card(self):
        card = Card()
        card.add_widget(section_title('Check this car'))
        card.add_widget(panel_label(
            f'Scans which readings the car answers, then records {CHECK_SECONDS} seconds of the bus and decodes '
            'it. Saves the raw capture, a readable report and a CSV. Ignition on. Connect the adapter on the '
            'Link tab first, and stop the sniffer.', color=MUTED, font_size=dp(13)))
        self.car_profiles = {p.name: p for p in profiles.everything(os.path.join(self.data_dir, 'cars'))}
        names = list(self.car_profiles)
        self.car_box = Spinner(text=names[0], values=names, size_hint_y=None, height=dp(48),
                               option_cls=WrapOption, shorten=True, shorten_from='right')
        self.car_box.bind(width=lambda box, width: setattr(box, 'text_size', (width - dp(32), None)))
        card.add_widget(self.car_box)
        card.add_widget(make_button('Check this car', self.check_car, primary=True))
        self.check_output = panel_label('Nothing checked yet.', font_size=dp(13))
        card.add_widget(self.check_output)
        return card

    def _check_message(self, text, error=False):
        self.check_output.text = text
        self.check_output.color = ALERT if error else TEXT

    def check_car(self):
        if self._checking:
            return
        if self.app_session.elm is None:
            self._check_message('Connect the adapter on the Link tab first.', error=True)
            return
        if self.sniff.running:
            self._check_message('Stop the sniffer first: it is using the adapter.', error=True)
            return
        profile = self.car_profiles[self.car_box.text]
        self._checking = True
        self.runner.paused = True            # the Live reader must not touch the adapter during the check
        self._check_message(f'Scanning {profile.name}...')
        threading.Thread(target=self._check_work, args=(self.app_session.elm, profile), daemon=True).start()

    def _check_work(self, elm, profile):
        def scan_progress(index, total, pid):
            Clock.schedule_once(lambda dt: self._check_message(f'Reading {index + 1} of {total}: {pid}'))

        def capture_progress(elapsed, total):
            Clock.schedule_once(lambda dt: self._check_message(f'Recording the bus: {total - elapsed:.0f} s left'))

        result, error = None, None
        try:
            result = car_check.check(elm, profile, self.data_dir, CHECK_SECONDS, scan_progress, capture_progress)
        except (OBDError, MonitorError, OSError) as exc:
            error = str(exc)
        Clock.schedule_once(lambda dt: self._check_done(result, error))

    def _check_done(self, result, error):
        self._checking = False
        self.runner.paused = self.sniff.holds_adapter()
        if error:
            self._check_message(f'The check stopped: {error}', error=True)
            return
        note = f' {result["capture_error"]}' if result['capture_error'] else ''
        body = result['scan_text'].splitlines() + [''] + result['report'].splitlines()
        shown = body[:CHECK_LINES]
        if len(body) > CHECK_LINES:
            shown.append(f'... {len(body) - CHECK_LINES} more lines in the saved report.')
        lines = [f'Recorded {result["frames"]} frames.{note}', ''] + shown + [
                 '', 'Saved to:', result['raw'], result['report_path'], result['csv']]
        self._check_message('\n'.join(lines))
        self._check_message('\n'.join(lines))

    @staticmethod
    def _bus_label(key):
        return f'{key}: {PROTOCOLS[key]}'

    # --- screen lifecycle ------------------------------------------------------------------------
    def activate(self):
        self.active = True
        if not self._events:
            Clock.schedule_once(lambda dt: setattr(self.scroller, 'scroll_y', 1), 0.1)   # open at the top
            self._events = [Clock.schedule_interval(self._poll, POLL_SECONDS),
                            Clock.schedule_interval(self._refresh, REFRESH_SECONDS),
                            Clock.schedule_interval(lambda dt: self.sniff.sniffer.tick_notch(), REFRESH_SECONDS)]
        self._draw()

    def deactivate(self):
        self.active = False

    def source_changed(self, _status=None):
        """The adapter was connected or dropped on the Link tab."""
        if self.sniff.listening_to_adapter and self.app_session.elm is None:
            self.stop()
        self._explain_source()

    def holds_adapter(self):
        return self.sniff.listening_to_adapter

    # --- choosing a source -----------------------------------------------------------------------
    def set_kind(self, name):
        self.kind = name
        for key, button in self.source_buttons.items():
            button.color = ACCENT if key == name else TEXT
        self.extra.clear_widgets()
        if name == 'Adapter':
            self.extra.add_widget(self.bus_box)
            self.extra.add_widget(self.filter_box)
        elif name == 'Log file':
            self.extra.add_widget(self.log_button)
        self._explain_source()

    def _explain_source(self):
        if self.kind == 'Simulated':
            text = 'Made-up traffic from five invented messages, to practise notching on. No adapter needed.'
        elif self.kind == 'Adapter':
            if self.app_session.elm is None:
                text = 'Connect your scan adapter on the Link tab first (demo mode does not count).'
            else:
                text = ('Listens through the adapter connected on the Link tab. While it listens, Live and Scan '
                        'wait. Pick the bus speed; most cars, including GM, are 500 kbit/s 11-bit.')
        else:
            text = self.log_name or 'Play back a saved capture (candump, CSV from this app, SLCAN or ELM text).'
        self.source_note.text = text

    def choose_log(self):
        try:
            from plyer import filechooser
        except ImportError:
            filechooser = None
        if filechooser is not None:
            try:
                filechooser.open_file(on_selection=self._native_picked, filters=['*.log', '*.csv', '*.txt'],
                                      multiple=False)
                return
            except Exception:   # the platform chooser is missing or refused; use the built-in one
                pass
        self._open_picker()

    def _native_picked(self, selection):
        if selection:
            path = selection[0]
            Clock.schedule_once(lambda dt: self.load_log(path))

    def _open_picker(self):
        chooser = FileChooserListView(path=os.path.expanduser('~'), filters=['*.log', '*.csv', '*.txt'])
        body = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(8))
        body.add_widget(chooser)
        cancel = style_button(Button(text='Cancel'))
        open_button = style_button(Button(text='Open'), primary=True)
        body.add_widget(button_row(cancel, open_button))
        popup = Popup(title='Choose a CAN log', content=body, size_hint=(0.95, 0.9))
        cancel.bind(on_release=lambda *_: popup.dismiss())

        def open_selected(*_):
            popup.dismiss()
            if chooser.selection:
                self.load_log(chooser.selection[0])

        open_button.bind(on_release=open_selected)
        popup.open()

    def load_log(self, path):
        try:
            with open(path, encoding='utf-8', errors='replace') as handle:
                frames = read_log(handle.read())
        except OSError:
            self.source_note.text = 'Could not open that file. Copy it into Downloads, then choose it again.'
            return
        if not frames:
            self.source_note.text = 'No CAN frames found in that file.'
            return
        self.log_frames, self.log_name = frames, f'{os.path.basename(path)}: {len(frames)} frames'
        self._explain_source()

    # --- start and stop --------------------------------------------------------------------------
    def toggle(self):
        if self.sniff.running:
            self.stop()
        elif not self._starting:
            self.start()

    def start(self):
        try:
            if self.kind == 'Simulated':
                self.sniff.start_demo()
            elif self.kind == 'Log file':
                if not self.log_frames:
                    self.source_note.text = 'Choose a log file first.'
                    return
                self.sniff.start_log(self.log_frames, self.log_name)
            else:
                self._start_adapter()
                return
        except MonitorError as exc:
            self.state.text = str(exc)
            self.state.color = ALERT
            return
        self._started()

    def _start_adapter(self):
        elm = self.app_session.elm
        if elm is None:
            self.state.text = 'Connect your scan adapter on the Link tab first.'
            self.state.color = ALERT
            if self.on_open_link:
                self.on_open_link()
            return
        protocol = self.bus_box.text.split(':', 1)[0]
        rx_filter = self.filter_box.text.strip() or None
        self._starting = True
        self.start_button.text = 'Starting...'
        self.runner.paused = True       # the Live reader must not touch the adapter from here on

        def work():
            error = None
            try:
                self.sniff.start_adapter(elm.transport, protocol, rx_filter, lock=elm._lock, owns_transport=False,
                                         label='Adapter')
            except MonitorError as exc:
                error = str(exc)
            Clock.schedule_once(lambda dt: self._adapter_started(error))

        threading.Thread(target=work, daemon=True).start()

    def _adapter_started(self, error):
        self._starting = False
        if error:
            self.runner.paused = False
            self.start_button.text = 'Start'
            self.state.text = error
            self.state.color = ALERT
            return
        self._started()

    def _started(self):
        self.start_button.text = 'Stop'
        self.state.text = f'Listening: {self.sniff.label}.'
        self.state.color = GOOD
        if self.active:
            self.activate()

    def stop(self):
        self.sniff.stop()
        self.runner.paused = False
        self.start_button.text = 'Start'
        self.state.text = self.sniff.error or f'Stopped. {self.sniff.sniffer.frames_seen} frames seen.'
        self.state.color = ALERT if self.sniff.error else MUTED

    def clear(self):
        self.sniff.clear()
        self.table.text = 'Cleared.'
        self.bits.text = ''

    # --- filtering and drawing -------------------------------------------------------------------
    def _leave_filter(self, _box, focused):
        if not focused:
            self.apply_filter()

    def apply_filter(self):
        try:
            wanted = sniffer_view.parse_ids(self.only_box.text)
        except ValueError as exc:
            self.state.text = str(exc)
            self.state.color = ALERT
            return
        sniffer = self.sniff.sniffer
        if not wanted:
            sniffer.show_all()
            return
        sniffer.hide_all()
        for can_id in wanted:
            sniffer.set_visible(can_id, True)

    def _poll(self, _dt):
        self.sniff.poll()
        if self.start_button.text == 'Stop' and not self.sniff.running:   # the log ended or the adapter dropped
            self.stop()

    def _refresh(self, _dt):
        self.sniff.tick()
        if self.active:
            self._draw()

    def _draw(self):
        sniffer = self.sniff.sniffer
        rows = sniffer.rows()
        if rows:
            self.table.text = sniffer_view.table_text(rows)
        elif self.sniff.running:
            self.table.text = 'Listening... no frames yet.'
        status = f'Listening: {self.sniff.label}. ' if self.sniff.running else ''
        if self.sniff.overruns:
            status += f'The adapter dropped frames {self.sniff.overruns} times: use the ID filter to quieten it.'
        if status and self.sniff.running:
            self.state.text = status
        self._draw_bits()

    def _draw_bits(self):
        text = self.bits_box.text.strip()
        if not text:
            self.bits.text = ''
            return
        try:
            wanted = sniffer_view.parse_ids(text)
        except ValueError as exc:
            self.bits.text = str(exc)
            return
        can_id = next(iter(wanted), None)
        self.bits.text = sniffer_view.bits_text(self.sniff.sniffer.row_for(can_id)) if can_id is not None else ''

    # --- saving ----------------------------------------------------------------------------------
    def save(self):
        if not self.sniff.captured:
            self.save_note.text = 'Nothing captured yet.'
            return
        try:
            path, count = sniffer_view.save_capture(self.sniff, self.folder)
        except OSError as exc:
            self.save_note.text = f'Could not save: {exc}'
            return
        self.save_note.text = f'Saved {count} frames to {path}'
