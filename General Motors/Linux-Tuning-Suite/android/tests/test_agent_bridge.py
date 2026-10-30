"""The agent bridge over real HTTP: who may connect, what they can read, and what they can change."""

import json
import sys
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_bridge import AgentBridge, build_agent_prompt  # noqa: E402

BOUNDS = {'shift_rpm': (3000, 9000), 'idle_rpm': (400, 1200)}


def state():
    return {'settings': {'shift_rpm': 6300, 'idle_rpm': 650}, 'source': 'DEMO',
            'live': {'values': {}, 'health': [], 'shifts': []}, 'grades': {'counts': {'bad': 0}},
            'tables': {'upshift': [[1.0, 2.0]]}}


class Bridge(unittest.TestCase):
    def setUp(self):
        self.applied = []
        self.bridge = AgentBridge(state, BOUNDS, host='127.0.0.1', port=0)
        self.bridge.start()
        self.addCleanup(self.bridge.stop)
        self.base = f'http://127.0.0.1:{self.bridge.port}'

    def call(self, path, body=None, token='default', method=None):
        token = self.bridge.token if token == 'default' else token
        data = json.dumps(body).encode() if body is not None else None
        request = urllib.request.Request(self.base + path, data=data, method=method)
        if token:
            request.add_header('Authorization', f'Bearer {token}')
        if data:
            request.add_header('Content-Type', 'application/json')
        try:
            with urllib.request.urlopen(request, timeout=3) as response:
                return response.status, json.loads(response.read() or b'null')
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read() or b'null')


class AccessTests(Bridge):
    def test_no_token_or_a_wrong_token_is_refused(self):
        self.assertEqual(self.call('/v1/state', token=None)[0], 401)
        self.assertEqual(self.call('/v1/state', token='guess')[0], 401)

    def test_the_token_is_long_and_different_each_time(self):
        other = AgentBridge(state, BOUNDS, host='127.0.0.1', port=0)
        self.assertGreaterEqual(len(self.bridge.token), 20)
        self.assertNotEqual(self.bridge.token, other.token)

    def test_the_token_also_works_in_the_address_for_agents_that_cannot_set_headers(self):
        code, body = self.call(f'/v1/state?token={self.bridge.token}', token=None)
        self.assertEqual(code, 200)
        self.assertEqual(body['settings']['shift_rpm'], 6300)

    def test_a_stopped_bridge_stops_answering(self):
        self.bridge.stop()
        with self.assertRaises(Exception):
            self.call('/v1/state')


class ReadingTests(Bridge):
    def test_state_tables_and_live_data_can_be_read(self):
        self.assertEqual(self.call('/v1/state')[1]['source'], 'DEMO')
        self.assertEqual(self.call('/v1/tables')[1]['upshift'], [[1.0, 2.0]])
        self.assertIn('health', self.call('/v1/live')[1])

    def test_help_tells_an_agent_what_it_can_do_and_the_limits(self):
        code, body = self.call('/v1/help')
        self.assertEqual(code, 200)
        text = json.dumps(body).lower()
        for word in ('propose', 'approve', 'read-only', 'shift_rpm'):
            self.assertIn(word, text)

    def test_unknown_paths_and_car_commands_do_not_exist(self):
        self.assertEqual(self.call('/v1/nope')[0], 404)
        self.assertEqual(self.call('/v1/command', {'send': '04'})[0], 404)
        self.assertEqual(self.call('/v1/state', {}, method='DELETE')[0], 405)


class ProposalTests(Bridge):
    def test_a_proposal_waits_for_the_user_and_changes_nothing(self):
        code, body = self.call('/v1/propose', {'field': 'shift_rpm', 'value': 6000, 'reason': 'Safer'})
        self.assertEqual(code, 201)
        self.assertEqual(body['status'], 'pending')
        self.assertEqual(self.call('/v1/state')[1]['settings']['shift_rpm'], 6300)
        listed = self.call('/v1/proposals')[1]['proposals']
        self.assertEqual([(p['field'], p['value'], p['status']) for p in listed],
                         [('shift_rpm', 6000.0, 'pending')])

    def test_the_user_deciding_is_visible_to_the_agent(self):
        proposal_id = self.call('/v1/propose', {'field': 'idle_rpm', 'value': 700, 'reason': 'x'})[1]['id']
        self.assertEqual(self.bridge.pending()[0]['id'], proposal_id)
        resolved = self.bridge.resolve(proposal_id, approved=True)
        self.assertEqual((resolved['field'], resolved['value']), ('idle_rpm', 700.0))
        self.assertEqual(self.call('/v1/proposals')[1]['proposals'][0]['status'], 'approved')
        self.assertEqual(self.bridge.pending(), [])

    def test_values_outside_the_allowed_range_and_unknown_settings_are_refused(self):
        code, body = self.call('/v1/propose', {'field': 'shift_rpm', 'value': 12000, 'reason': 'x'})
        self.assertEqual(code, 422)
        self.assertIn('3000', body['error'])
        self.assertEqual(self.call('/v1/propose', {'field': 'ratios', 'value': 1, 'reason': 'x'})[0], 422)
        self.assertEqual(self.call('/v1/propose', {'field': 'shift_rpm', 'value': 'high', 'reason': 'x'})[0], 422)
        self.assertEqual(self.bridge.pending(), [])

    def test_broken_or_oversized_requests_are_rejected(self):
        request = urllib.request.Request(self.base + '/v1/propose', data=b'{not json', method='POST')
        request.add_header('Authorization', f'Bearer {self.bridge.token}')
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request, timeout=3)
        self.assertEqual(caught.exception.code, 400)
        self.assertEqual(self.call('/v1/note', {'text': 'x' * 20000})[0], 413)

    def test_only_a_handful_of_proposals_can_be_waiting_at_once(self):
        for _ in range(20):
            self.call('/v1/propose', {'field': 'idle_rpm', 'value': 700, 'reason': 'x'})
        self.assertEqual(self.call('/v1/propose', {'field': 'idle_rpm', 'value': 700, 'reason': 'x'})[0], 429)


class NoteTests(Bridge):
    def test_an_agent_can_leave_a_note_for_the_screen_and_the_app_can_read_it(self):
        code, _ = self.call('/v1/note', {'text': 'Trans temp is climbing, ease off.', 'level': 'warn'})
        self.assertEqual(code, 201)
        notes = self.bridge.notes()
        self.assertEqual(notes[0]['text'], 'Trans temp is climbing, ease off.')
        self.assertEqual(notes[0]['level'], 'warn')

    def test_a_note_with_no_text_is_refused_and_odd_levels_become_info(self):
        self.assertEqual(self.call('/v1/note', {'text': '  '})[0], 422)
        self.call('/v1/note', {'text': 'hello', 'level': 'screaming'})
        self.assertEqual(self.bridge.notes()[0]['level'], 'info')


class PromptTests(unittest.TestCase):
    def test_the_copyable_prompt_has_the_address_the_token_and_the_ground_rules(self):
        bridge = AgentBridge(state, BOUNDS, host='127.0.0.1', port=0, token='abc123token')
        text = build_agent_prompt('http://192.168.0.42:8765', 'abc123token', bridge.help())
        for wanted in ('http://192.168.0.42:8765', 'abc123token', 'Authorization: Bearer',
                       '/v1/live', '/v1/propose', 'shift_rpm', 'approve'):
            self.assertIn(wanted, text)
        self.assertNotIn('/v1/command', text)



def check_pid(entry):
    if not entry.get('equation'):
        raise ValueError('The equation is missing.')
    return dict(entry, pid=str(entry['pid']).upper())


class SensorHelpTests(Bridge):
    def setUp(self):
        super().setUp()
        self.bridge.check_pid = check_pid
        self.focus = {'pid': '22194F', 'name': 'Trans Fluid Temp', 'latest': -34.0}
        self.bridge.get_state = lambda: dict(state(), focus=self.focus)

    def test_the_agent_can_read_the_sensor_the_user_asked_about(self):
        code, body = self.call('/v1/focus')
        self.assertEqual((code, body['focus']['pid']), (200, '22194F'))
        self.focus = None
        self.assertIsNone(self.call('/v1/focus')[1]['focus'])

    def test_a_sensor_proposal_waits_for_the_user_and_can_be_approved(self):
        code, body = self.call('/v1/propose_pid', {'pid': '22194f', 'name': 'Trans temp', 'equation': 'A-40',
                                                    'header': '7E2', 'reason': 'scaling looked wrong'})
        self.assertEqual(code, 201)
        pending = self.bridge.pending_pids()
        self.assertEqual([p['entry']['pid'] for p in pending], ['22194F'])
        self.assertEqual(self.bridge.resolve_pid(pending[0]['id'], True)['status'], 'approved')
        self.assertEqual(self.bridge.pending_pids(), [])
        self.assertEqual(self.call('/v1/proposals')[1]['pid_proposals'][0]['status'], 'approved')

    def test_a_bad_sensor_proposal_is_refused_with_the_reason(self):
        code, body = self.call('/v1/propose_pid', {'pid': '22194F', 'name': 'x'})
        self.assertEqual(code, 422)
        self.assertIn('equation', body['error'])
        self.assertEqual(self.bridge.pending_pids(), [])

    def test_sensor_proposals_need_the_token_and_a_checker(self):
        self.assertEqual(self.call('/v1/propose_pid', {'pid': '22194F'}, token=None)[0], 401)
        self.bridge.check_pid = None
        self.assertEqual(self.call('/v1/propose_pid', {'pid': '22194F'})[0], 422)

    def test_the_help_and_the_prompt_tell_the_agent_about_sensor_help(self):
        self.assertIn('POST /v1/propose_pid', self.call('/v1/help')[1]['endpoints'])
        self.assertIn('/v1/focus', build_agent_prompt('http://x', 't', self.bridge.help()))


if __name__ == '__main__':
    unittest.main()
