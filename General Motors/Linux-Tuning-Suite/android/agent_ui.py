"""The Agent screen: connect your own AI agent so it can watch the tune and the live data and advise.

The agent bridge (agent_bridge.py) does the work. This screen starts and stops it, shows the address
and the token, and puts any change the agent proposes in front of the user to approve or reject.
"""

from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from agent_bridge import DEFAULT_PORT, AgentBridge, build_agent_prompt, local_ip
from table_view import HEX
from ui_kit import (BORDER, GAP, MUTED, STATUS, TEXT, Card, button_row, make_button, panel_label,
                    section_title, stack)

NOTE_COLOUR = {'info': 'good', 'warn': 'ok', 'alert': 'bad'}


class AgentScreen(BoxLayout):
    def __init__(self, get_state, bounds, labels, get_value, apply_change, check_pid=None, apply_pid=None,
                 **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.get_state, self.bounds, self.labels = get_state, bounds, labels
        self.get_value, self.apply_change = get_value, apply_change
        self.check_pid, self.apply_pid = check_pid, apply_pid
        self.focus_text = ''
        self.bridge = None
        self.url = ''
        self._event = None
        self._shown = None

        intro = Card()
        intro.add_widget(section_title('Your AI agent'))
        intro.add_widget(panel_label('Start the bridge, then give your agent the address and token. It can '
                                     'read your settings, the graded shift tables and the live engine and '
                                     'transmission data, leave you notes, and propose changes. Nothing '
                                     'changes until you approve it here, and it cannot send anything to '
                                     'the car.', color=MUTED, font_size=dp(13)))
        self.status = panel_label('Bridge is off.', color=TEXT)
        self.start_wifi = make_button('Start on this Wi-Fi network', lambda: self.start(False), primary=True)
        self.start_local = make_button('Start for this phone only', lambda: self.start(True))
        self.stop_button = make_button('Stop bridge', self.stop)
        self.address = panel_label('', font_size=dp(13), color=TEXT)
        self.copy_prompt = make_button('Copy agent prompt', self.copy_the_prompt, primary=True)
        self.copy_token = make_button('Copy token', lambda: Clipboard.copy(self.bridge.token if self.bridge else ''))
        self.controls = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        self.controls.bind(minimum_height=self.controls.setter('height'))
        for widget in (self.status, self.controls):
            intro.add_widget(widget)

        self.focus_card = Card()
        self.focus_card.add_widget(section_title('Sensor you asked about'))
        self.focus_label = panel_label('Triple tap any sensor on Live or Scan to ask your agent about it. It will '
                                       'show here, and your agent can read it from the bridge.', markup=False,
                                       color=MUTED, font_size=dp(13))
        self.focus_card.add_widget(self.focus_label)
        self.focus_copy = make_button('Copy a question for my agent', self.copy_question, primary=True)

        self.proposals_card = Card()
        self.proposals_card.add_widget(section_title('Waiting for your approval'))
        self.proposals_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        self.proposals_box.bind(minimum_height=self.proposals_box.setter('height'))
        self.proposals_card.add_widget(self.proposals_box)

        self.notes_card = Card()
        self.notes_card.add_widget(section_title('Notes from your agent'))
        self.notes_label = panel_label('Nothing yet.', markup=True, color=MUTED, font_size=dp(13))
        self.notes_card.add_widget(self.notes_label)

        security = panel_label('The address works only for devices on the same Wi-Fi, and only with the '
                               'token. The data travels unencrypted on that network, so use your own '
                               'network or hotspot, and stop the bridge when you are done.',
                               color=MUTED, font_size=dp(12))
        self.add_widget(stack(intro, self.focus_card, self.proposals_card, self.notes_card, security))
        self.show_idle()

    # --- lifecycle -------------------------------------------------------------------------------

    def activate(self):
        if self._event is None:
            self._event = Clock.schedule_interval(self.refresh, 1.0)
        self.refresh(0)

    def deactivate(self):
        if self._event is not None:
            self._event.cancel()
            self._event = None

    def shutdown(self):
        self.stop()

    # --- the bridge ------------------------------------------------------------------------------

    def start(self, local_only):
        host = '127.0.0.1' if local_only else '0.0.0.0'
        for port in (DEFAULT_PORT, 0):
            try:
                bridge = AgentBridge(self.get_state, self.bounds, host=host, port=port, check_pid=self.check_pid)
                bridge.start()
            except OSError:
                continue
            self.bridge = bridge
            self.url = f'http://{"127.0.0.1" if local_only else local_ip()}:{bridge.port}'
            self.show_running()
            return
        self.status.text = 'Could not start the bridge. Is another app using the network port?'
        self.status.color = STATUS['bad']

    def stop(self):
        if self.bridge is not None:
            self.bridge.stop()
        self.bridge, self.url = None, ''
        self.show_idle()
        self.refresh(0)

    def show_idle(self):
        self.status.text = 'Bridge is off.'
        self.status.color = TEXT
        self.controls.clear_widgets()
        for widget in (self.start_wifi, self.start_local):
            self.controls.add_widget(widget)

    def show_running(self):
        self.status.text = 'Bridge is on. Give your agent this address and token.'
        self.status.color = STATUS['good']
        self.address.text = f'Address: {self.url}\nToken: {self.bridge.token}'
        self.controls.clear_widgets()
        self.controls.add_widget(self.address)
        self.controls.add_widget(button_row(self.copy_prompt, self.copy_token))
        self.controls.add_widget(self.stop_button)

    def copy_the_prompt(self):
        if self.bridge is not None:
            Clipboard.copy(build_agent_prompt(self.url, self.bridge.token, self.bridge.help()))

    # --- the sensor you asked about --------------------------------------------------------------

    def set_focus(self, info):
        """Show the sensor that was triple tapped, and remember a question to give the agent about it."""
        lines = [f'{info["name"]} ({info["pid"]})', f'Mode {info["mode"]}, module {info["module"]}, '
                 f'unit {info["unit"] or "none"}, range {info["low"]:g} to {info["high"]:g}']
        lines.append('Latest reading: ' + (f'{info["latest"]:g}' if info.get('latest') is not None else 'none'))
        lines.append(info['car_answer'])
        self.focus_label.text = '\n'.join(lines)
        self.focus_label.color = TEXT
        self.focus_text = (f'I need help with the sensor {info["name"]} (PID {info["pid"]}) in TunerToolPro. '
                           'Read GET /v1/focus for its details and raw replies, work out the right module, mode, '
                           'bytes and equation, explain what is wrong or how to use it, and if it needs '
                           'changing, propose it with POST /v1/propose_pid.')
        if self.focus_copy.parent is None:
            self.focus_card.add_widget(self.focus_copy)

    def copy_question(self):
        Clipboard.copy(self.focus_text)
        self.focus_label.text += '\n\nQuestion copied. Paste it to your agent.'

    # --- approvals -------------------------------------------------------------------------------

    def refresh(self, _dt):
        try:
            self._refresh()
        except Exception:   # show the problem on screen rather than leaving a blank tab
            import traceback
            self.status.text = 'Agent screen error:\n' + traceback.format_exc()[-900:]
            self.status.color = STATUS['bad']

    def _refresh(self):
        pending = self.bridge.pending() if self.bridge else []
        pending_pids = self.bridge.pending_pids() if self.bridge else []
        notes = self.bridge.notes() if self.bridge else []
        signature = (tuple(p['id'] for p in pending), tuple(p['id'] for p in pending_pids),
                     tuple(n['time'] for n in notes))
        if signature == self._shown:
            return
        self._shown = signature
        self.proposals_box.clear_widgets()
        if not pending and not pending_pids:
            self.proposals_box.add_widget(panel_label('No proposals.', color=MUTED, font_size=dp(13)))
        for proposal in pending_pids:
            self.proposals_box.add_widget(self._pid_row(proposal))
        for proposal in pending:
            self.proposals_box.add_widget(self._proposal_row(proposal))
        lines = [f'[color=#{HEX[NOTE_COLOUR[n["level"]]]}]{n["text"]}[/color]' for n in notes[:6]]
        self.notes_label.text = '\n\n'.join(lines) or 'Nothing yet.'
        self.notes_label.color = TEXT if lines else MUTED

    def _proposal_row(self, proposal):
        name = self.labels.get(proposal['field'], proposal['field'])
        current = self.get_value(proposal['field'])
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(6))
        box.bind(minimum_height=box.setter('height'))
        box.add_widget(panel_label(f'{name}: {current} to {proposal["value"]:g}', color=TEXT, bold=True))
        if proposal['reason']:
            box.add_widget(panel_label(proposal['reason'], color=MUTED, font_size=dp(13)))
        box.add_widget(button_row(
            make_button('Approve', lambda p=proposal: self.decide(p, True), primary=True),
            make_button('Reject', lambda p=proposal: self.decide(p, False))))
        return box

    def _pid_row(self, proposal):
        entry = proposal['entry']
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(6))
        box.bind(minimum_height=box.setter('height'))
        box.add_widget(panel_label(f'New sensor {entry["pid"]}: {entry["name"]}', color=TEXT, bold=True))
        box.add_widget(panel_label(f'Equation {entry["equation"]}, module {entry["header"]}, unit '
                                   f'{entry["unit"] or "none"}, range {entry["low"]} to {entry["high"]}',
                                   color=MUTED, font_size=dp(13)))
        if proposal['reason']:
            box.add_widget(panel_label(proposal['reason'], color=MUTED, font_size=dp(13)))
        box.add_widget(button_row(
            make_button('Approve and save', lambda p=proposal: self.decide_pid(p, True), primary=True),
            make_button('Reject', lambda p=proposal: self.decide_pid(p, False))))
        return box

    def decide_pid(self, proposal, approved):
        resolved = self.bridge.resolve_pid(proposal['id'], approved) if self.bridge else None
        if resolved and approved and self.apply_pid is not None:
            message = self.apply_pid(resolved['entry'])
            if message:
                self.status.text, self.status.color = message, STATUS['bad']
        self._shown = None
        self.refresh(0)

    def decide(self, proposal, approved):
        resolved = self.bridge.resolve(proposal['id'], approved) if self.bridge else None
        if resolved and approved:
            self.apply_change(resolved['field'], resolved['value'])
        self._shown = None
        self.refresh(0)
