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
    def __init__(self, get_state, bounds, labels, get_value, apply_change, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.get_state, self.bounds, self.labels = get_state, bounds, labels
        self.get_value, self.apply_change = get_value, apply_change
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
        self.add_widget(stack(intro, self.proposals_card, self.notes_card, security))
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
                bridge = AgentBridge(self.get_state, self.bounds, host=host, port=port)
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
        notes = self.bridge.notes() if self.bridge else []
        signature = (tuple(p['id'] for p in pending), tuple(n['time'] for n in notes))
        if signature == self._shown:
            return
        self._shown = signature
        self.proposals_box.clear_widgets()
        if not pending:
            self.proposals_box.add_widget(panel_label('No proposals.', color=MUTED, font_size=dp(13)))
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

    def decide(self, proposal, approved):
        resolved = self.bridge.resolve(proposal['id'], approved) if self.bridge else None
        if resolved and approved:
            self.apply_change(resolved['field'], resolved['value'])
        self._shown = None
        self.refresh(0)
