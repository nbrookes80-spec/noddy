"""Settings storage and the optional AI client. No network: the HTTP opener is faked."""

import io
import json
import os
import stat
import tempfile
import unittest
import urllib.error
from unittest import mock

from tunertoolpro import ai_assistant, settings


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def opener_returning(payload):
    def opener(req, timeout=None):
        opener.request = req
        return FakeResponse(json.dumps(payload).encode('utf-8'))
    return opener


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {'TUNERTOOLPRO_HOME': self.tmp.name})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_defaults_when_no_file(self):
        data = settings.load()
        self.assertFalse(data['ai']['enabled'])
        self.assertEqual(data['ai']['api_key'], '')
        self.assertEqual(data['ai']['model'], 'claude-sonnet-5-5')

    def test_round_trip_and_owner_only_permissions(self):
        data = settings.load()
        data['ai'] = {'enabled': True, 'api_key': 'sk-test', 'model': 'claude-haiku-5-5'}
        path = settings.save(data)
        if os.name != 'nt':   # Windows has no owner-only file mode; the %APPDATA% folder is per-user
            self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600)
        again = settings.load()
        self.assertTrue(again['ai']['enabled'])
        self.assertEqual(again['ai']['api_key'], 'sk-test')

    def test_bad_file_falls_back_to_defaults(self):
        settings.settings_path().write_text('{not json', encoding='utf-8')
        self.assertEqual(settings.load()['ai']['model'], 'claude-sonnet-5-5')

    def test_wrong_types_are_ignored(self):
        settings.settings_path().write_text('{"ai": {"enabled": "yes", "api_key": 5}}', encoding='utf-8')
        data = settings.load()
        self.assertFalse(data['ai']['enabled'])
        self.assertEqual(data['ai']['api_key'], '')


class AskTests(unittest.TestCase):
    def test_request_carries_key_model_and_context(self):
        opener = opener_returning({'content': [{'type': 'text', 'text': 'Answer.'}]})
        text = ai_assistant.ask('Why 3-4?', 'sk-test', 'claude-sonnet-5-5',
                                context='TABLE', opener=opener)
        self.assertEqual(text, 'Answer.')
        req = opener.request
        self.assertEqual(req.get_header('X-api-key'), 'sk-test')
        self.assertEqual(req.get_header('Anthropic-version'), ai_assistant.API_VERSION)
        body = json.loads(req.data.decode('utf-8'))
        self.assertEqual(body['model'], 'claude-sonnet-5-5')
        self.assertIn('TABLE', body['messages'][0]['content'])
        self.assertIn('Why 3-4?', body['messages'][0]['content'])
        self.assertTrue(req.full_url.startswith('https://api.anthropic.com/'))

    def test_no_key_or_question_is_refused_before_any_request(self):
        called = []

        def opener(req, timeout=None):
            called.append(req)
        with self.assertRaises(ai_assistant.AIError):
            ai_assistant.ask('Hi', '', 'claude-sonnet-5-5', opener=opener)
        with self.assertRaises(ai_assistant.AIError):
            ai_assistant.ask('   ', 'sk-test', 'claude-sonnet-5-5', opener=opener)
        self.assertEqual(called, [])

    def test_rejected_key_message_does_not_contain_the_key(self):
        def opener(req, timeout=None):
            raise urllib.error.HTTPError(req.full_url, 401, 'Unauthorized', {}, None)
        with self.assertRaises(ai_assistant.AIError) as ctx:
            ai_assistant.ask('Hi', 'sk-secret-123', 'claude-sonnet-5-5', opener=opener)
        self.assertIn('rejected', str(ctx.exception))
        self.assertNotIn('sk-secret-123', str(ctx.exception))

    def test_network_failure_is_a_readable_error(self):
        def opener(req, timeout=None):
            raise urllib.error.URLError('no route')
        with self.assertRaises(ai_assistant.AIError) as ctx:
            ai_assistant.ask('Hi', 'sk-test', 'claude-sonnet-5-5', opener=opener)
        self.assertIn('Could not reach', str(ctx.exception))

    def test_cut_off_reply_says_so(self):
        payload = {'content': [{'type': 'thinking', 'thinking': '...'}], 'stop_reason': 'max_tokens'}
        with self.assertRaises(ai_assistant.AIError) as ctx:
            ai_assistant.ask('Hi', 'sk-test', 'claude-sonnet-5-5', opener=opener_returning(payload))
        self.assertIn('cut off', str(ctx.exception))

    def test_empty_reply_is_an_error(self):
        with self.assertRaises(ai_assistant.AIError):
            ai_assistant.ask('Hi', 'sk-test', 'claude-sonnet-5-5',
                             opener=opener_returning({'content': []}))


if __name__ == '__main__':
    unittest.main()
