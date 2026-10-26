"""Vehicle profile, consistency rules and the AI settings tools. No network: the API is faked."""

import io
import json
import os
import tempfile
import unittest
from unittest import mock

from tunertoolpro import ai_assistant, ai_tools, consistency, vehicle


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def scripted_opener(replies):
    """Return the next reply on each call, and record every request body."""
    sent = []

    def opener(req, timeout=None):
        sent.append(json.loads(req.data.decode('utf-8')))
        return FakeResponse(json.dumps(replies.pop(0)).encode('utf-8'))
    opener.sent = sent
    return opener


BOUNDS = {'shift_rpm': (3000, 9000), 'stall_rpm': (1000, 4500)}


class TransmissionLibraryTests(unittest.TestCase):
    def test_new_transmissions_are_present_with_sources(self):
        for key in ('ZF 8HP45 / 8HP70 (8-speed)', '2-Speed Powerglide (V8 ratio)',
                    '6L80 modified (Sonnax zip kit, TransGo shift kit, billet flex plate, Circle D triple-plate converter)'):
            entry = vehicle.transmission(key)
            self.assertTrue(entry['ratios'])
            self.assertTrue(entry['source'])

    def test_stock_6l80_ratios_come_from_the_app_data(self):
        self.assertEqual(vehicle.transmission('Stock 6L80 (2006-Current)')['ratios'][0], 4.027)

    def test_unknown_transmission_lists_the_valid_names(self):
        with self.assertRaises(KeyError) as ctx:
            vehicle.transmission('Nonexistent')
        self.assertIn('8HP45', str(ctx.exception))

    def test_modified_6l80_is_flagged(self):
        self.assertTrue(vehicle.transmission(
            '6L80 modified (Sonnax zip kit, TransGo shift kit, billet flex plate, Circle D triple-plate converter)')['modified'])


class VehicleProfileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {'TUNERTOOLPRO_HOME': self.tmp.name})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_round_trip_and_missing_list(self):
        profile = vehicle.VehicleProfile(car='Camaro SS', power_hp=450, ecu_max_torque_lbft=0)
        vehicle.save_profile(profile)
        again = vehicle.load_profile()
        self.assertEqual(again.car, 'Camaro SS')
        self.assertIn('engine', again.missing())
        self.assertIn('redline_rpm', again.missing())
        self.assertNotIn('car', again.missing())

    def test_unknown_keys_in_file_are_ignored(self):
        vehicle.profile_path().write_text('{"car": "X", "future": 1}', encoding='utf-8')
        self.assertEqual(vehicle.load_profile().car, 'X')


class ConsistencyTests(unittest.TestCase):
    def cfg(self, **kw):
        base = {'shift_rpm': 6400, 'stall_rpm': 2000, 'idle_rpm': 550, 'min_tcc_rpm': 1200,
                'ratios': [4.03, 2.36, 1.53]}
        base.update(kw)
        return base

    def levels(self, findings):
        return {f.field: f.level for f in findings}

    def test_shift_above_redline_is_an_error(self):
        p = vehicle.VehicleProfile(redline_rpm=6500, ecu_max_torque_lbft=500)
        found = consistency.check(p, self.cfg(shift_rpm=6800))
        self.assertEqual(self.levels(found)['shift_rpm'], 'error')

    def test_ecu_torque_above_rating_is_a_warning(self):
        p = vehicle.VehicleProfile(redline_rpm=6500, ecu_max_torque_lbft=700)
        entry = {'rated_torque_lbft': 600, 'modified': False}
        found = consistency.check(p, self.cfg(), entry)
        self.assertEqual(self.levels(found)['ecu_max_torque_lbft'], 'warn')

    def test_missing_ecu_limit_is_a_note_not_an_error(self):
        p = vehicle.VehicleProfile(redline_rpm=6500)
        found = consistency.check(p, self.cfg())
        self.assertEqual(self.levels(found)['ecu_max_torque_lbft'], 'info')

    def test_ratio_order_is_checked(self):
        p = vehicle.VehicleProfile(redline_rpm=6500, ecu_max_torque_lbft=500)
        found = consistency.check(p, self.cfg(ratios=[1.5, 2.0]))
        self.assertEqual(self.levels(found)['ratios'], 'error')

    def test_modified_transmission_gets_a_note(self):
        p = vehicle.VehicleProfile(redline_rpm=6500, ecu_max_torque_lbft=500)
        entry = {'rated_torque_lbft': None, 'modified': True}
        found = consistency.check(p, self.cfg(), entry)
        self.assertIn('transmission', self.levels(found))


class ToolTests(unittest.TestCase):
    def test_out_of_range_proposal_is_refused(self):
        session = ai_tools.Session(snapshot={}, bounds=BOUNDS)
        result = ai_tools.run_tool(session, 'propose_change',
                                   {'field': 'shift_rpm', 'value': 12000, 'reason': 'x'})
        self.assertTrue(result.startswith('Refused'))
        self.assertEqual(session.proposals, [])

    def test_unknown_field_is_refused(self):
        ok, _ = ai_tools.validate_proposal('secret_field', 1, BOUNDS)
        self.assertFalse(ok)

    def test_valid_proposal_is_recorded_not_applied(self):
        session = ai_tools.Session(snapshot={}, bounds=BOUNDS)
        ai_tools.run_tool(session, 'propose_change', {'field': 'shift_rpm', 'value': 6000, 'reason': 'low redline'})
        self.assertEqual(session.proposals, [{'field': 'shift_rpm', 'value': 6000.0, 'reason': 'low redline'}])

    def test_read_settings_returns_the_snapshot(self):
        session = ai_tools.Session(snapshot={'shift_rpm': 6400}, bounds=BOUNDS)
        self.assertIn('6400', ai_tools.run_tool(session, 'read_settings', {}))


class AskWithToolsTests(unittest.TestCase):
    def test_tool_round_then_answer(self):
        replies = [
            {'stop_reason': 'tool_use', 'content': [
                {'type': 'tool_use', 'id': 't1', 'name': 'read_settings', 'input': {}},
                {'type': 'tool_use', 'id': 't2', 'name': 'propose_change',
                 'input': {'field': 'shift_rpm', 'value': 6000, 'reason': 'redline is 6500'}}]},
            {'stop_reason': 'end_turn', 'content': [{'type': 'text', 'text': 'Proposed a lower shift RPM.'}]},
        ]
        opener = scripted_opener(replies)
        session = ai_tools.Session(snapshot={'shift_rpm': 6400}, bounds=BOUNDS)
        text, proposals, questions = ai_assistant.ask_with_tools(
            'Is my shift RPM safe?', 'sk-test', 'claude-sonnet-5-5', session, opener=opener)
        self.assertEqual(text, 'Proposed a lower shift RPM.')
        self.assertEqual(len(proposals), 1)
        self.assertEqual(questions, [])
        second = opener.sent[1]
        results = second['messages'][-1]['content']
        self.assertEqual({r['tool_use_id'] for r in results}, {'t1', 't2'})
        self.assertTrue(second['tools'])

    def test_question_to_user_is_returned(self):
        replies = [
            {'stop_reason': 'tool_use', 'content': [
                {'type': 'tool_use', 'id': 'q1', 'name': 'ask_user', 'input': {'question': 'What is the converter stall?'}}]},
            {'stop_reason': 'end_turn', 'content': [{'type': 'text', 'text': 'I need the stall figure.'}]},
        ]
        session = ai_tools.Session(snapshot={}, bounds=BOUNDS)
        text, proposals, questions = ai_assistant.ask_with_tools(
            'Set my stall', 'sk-test', 'claude-sonnet-5-5', session, opener=scripted_opener(replies))
        self.assertEqual(questions, ['What is the converter stall?'])

    def test_key_is_not_in_errors(self):
        def opener(req, timeout=None):
            import urllib.error
            raise urllib.error.HTTPError(req.full_url, 401, 'no', {}, None)
        session = ai_tools.Session(snapshot={}, bounds=BOUNDS)
        with self.assertRaises(ai_assistant.AIError) as ctx:
            ai_assistant.ask_with_tools('Hi', 'sk-secret-9', 'claude-sonnet-5-5', session, opener=opener)
        self.assertNotIn('sk-secret-9', str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
