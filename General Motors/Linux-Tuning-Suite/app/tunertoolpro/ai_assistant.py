"""Optional AI assistant: asks the Anthropic Messages API about the tables and settings.

Standard library only (urllib). Nothing is sent until the user asks a question. The API key
is passed in by the caller and is never written to logs or error messages.
"""

import json
import urllib.error
import urllib.request

API_URL = 'https://api.anthropic.com/v1/messages'
API_VERSION = '2023-06-01'
# Room for the model's own reasoning as well as the answer; 1024 was cut off with no text.
MAX_TOKENS = 4096

SYSTEM_PROMPT = (
    'You are the assistant inside TunerToolPro, a calculation aid for GM 4L60E and 6L80E '
    'transmission calibration. Explain tables, settings and trade-offs in plain language. '
    'Use only the numbers the user gives you. If the answer depends on data you do not have, say '
    'so. Do not claim a value is safe or correct for a real vehicle: the user must check it on '
    'their own vehicle and in a road test before writing it to a controller.'
)


class AIError(Exception):
    """A message the user can read. It never contains the API key."""


def build_request(question, model, context=''):
    text = question if not context else f'{context}\n\nQuestion: {question}'
    return {
        'model': model,
        'max_tokens': MAX_TOKENS,
        'system': SYSTEM_PROMPT,
        'messages': [{'role': 'user', 'content': text}],
    }


def ask(question, api_key, model, context='', timeout=60, opener=urllib.request.urlopen):
    question = (question or '').strip()
    if not question:
        raise AIError('Type a question first.')
    if not api_key:
        raise AIError('No API key is set. Add one in the AI Assistant tab.')
    body = json.dumps(build_request(question, model, context)).encode('utf-8')
    req = urllib.request.Request(API_URL, data=body, method='POST', headers={
        'content-type': 'application/json',
        'x-api-key': api_key,
        'anthropic-version': API_VERSION,
    })
    try:
        with opener(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise AIError('The API key was rejected (HTTP %d). Check the key in the AI Assistant tab.'
                          % exc.code) from None
        if exc.code == 404:
            raise AIError('The AI service does not know the model. Pick another model in the AI Assistant tab.') from None
        if exc.code == 429:
            raise AIError('The AI service is rate-limiting this key. Wait a minute and ask again.') from None
        if exc.code >= 500 or exc.code == 529:
            raise AIError(f'The AI service is busy or unavailable (HTTP {exc.code}). Try again shortly.') from None
        raise AIError(f'The AI service refused the request (HTTP {exc.code}).') from None
    except (urllib.error.URLError, OSError) as exc:
        raise AIError(f'Could not reach the AI service: {exc.__class__.__name__}.') from None
    except ValueError:
        raise AIError('The AI service returned a reply that could not be read.') from None
    if not isinstance(payload, dict):
        raise AIError('The AI service returned a reply that could not be read.')
    content = payload.get('content')
    if not isinstance(content, list):
        content = []
    text = ''.join(block.get('text', '') for block in content
                   if isinstance(block, dict) and block.get('type') == 'text').strip()
    if not text:
        if payload.get('stop_reason') == 'max_tokens':
            raise AIError('The answer was cut off before it was written. Ask a shorter question.')
        raise AIError('The AI service returned no text.')
    return text
