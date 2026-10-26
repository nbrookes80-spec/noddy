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

TOOL_ROUNDS = 6

TOOL_PROMPT = (
    ' You can read the user\'s current settings with read_settings, propose changes with '
    'propose_change, and ask for missing values with ask_user. Read the settings before you advise. '
    'Keep every proposal consistent with the ECU torque limit, the redline and the transmission data. '
    'If a proposal conflicts with the consistency findings, say so. You cannot write to the vehicle; '
    'the user applies approved changes in the app and then tests on the road.'
)

SYSTEM_PROMPT = (
    'You are the assistant inside TunerToolPro, a calculation aid for GM 4L60E and 6L80E '
    'transmission calibration. Explain tables, settings and trade-offs in plain language. '
    'Use only the numbers the user gives you. If the answer depends on data you do not have, say '
    'so. Do not claim a value is safe or correct for a real vehicle: the user must check it on '
    'their own vehicle and in a road test before writing it to a controller.'
) + TOOL_PROMPT


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


def ask_with_tools(question, api_key, model, session, context='', timeout=120, opener=urllib.request.urlopen):
    """Ask with the settings tools. Returns (answer text, proposals, questions).

    The loop runs until the model stops asking for tools, or TOOL_ROUNDS is reached. Each round
    sends the tool results back. Nothing is applied here; proposals are returned for the user.
    """
    # Imported here so ai_assistant stays importable without the tool module.
    from .ai_tools import TOOL_DEFINITIONS, run_tool
    question = (question or '').strip()
    if not question:
        raise AIError('Type a question first.')
    if not api_key:
        raise AIError('No API key is set. Add one in the AI Assistant tab.')
    first = question if not context else f'{context}\n\nQuestion: {question}'
    messages = [{'role': 'user', 'content': first}]
    text = ''
    for _ in range(TOOL_ROUNDS):
        body = {'model': model, 'max_tokens': MAX_TOKENS, 'system': SYSTEM_PROMPT,
                'tools': TOOL_DEFINITIONS, 'messages': messages}
        payload = _post(body, api_key, timeout, opener)
        content = payload.get('content') if isinstance(payload, dict) else None
        if not isinstance(content, list):
            raise AIError('The AI service returned a reply that could not be read.')
        text = ''.join(b.get('text', '') for b in content
                       if isinstance(b, dict) and b.get('type') == 'text').strip() or text
        if payload.get('stop_reason') != 'tool_use':
            break
        messages.append({'role': 'assistant', 'content': content})
        results = []
        for block in content:
            if isinstance(block, dict) and block.get('type') == 'tool_use':
                output = run_tool(session, block.get('name', ''), block.get('input') or {})
                results.append({'type': 'tool_result', 'tool_use_id': block.get('id'), 'content': output})
        if not results:
            break
        messages.append({'role': 'user', 'content': results})
    if not text and not session.questions and not session.proposals:
        raise AIError('The AI service returned no text.')
    return text, list(session.proposals), list(session.questions)


def _post(body, api_key, timeout, opener):
    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data, method='POST', headers={
        'content-type': 'application/json', 'x-api-key': api_key, 'anthropic-version': API_VERSION})
    try:
        with opener(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise AIError(f'The API key was rejected (HTTP {exc.code}). Check the key in the AI Assistant tab.') from None
        if exc.code == 429:
            raise AIError('The AI service is rate-limiting this key. Wait a minute and ask again.') from None
        if exc.code >= 500 or exc.code == 529:
            raise AIError(f'The AI service is busy or unavailable (HTTP {exc.code}). Try again shortly.') from None
        raise AIError(f'The AI service refused the request (HTTP {exc.code}).') from None
    except (urllib.error.URLError, OSError) as exc:
        raise AIError(f'Could not reach the AI service: {exc.__class__.__name__}.') from None
    except ValueError:
        raise AIError('The AI service returned a reply that could not be read.') from None
