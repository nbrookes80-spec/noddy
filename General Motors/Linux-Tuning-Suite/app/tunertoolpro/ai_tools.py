"""Tools the AI may use. Pure Python: the app decides what each tool does.

The model can read the settings and propose changes. A proposal is never applied here. The app
shows it, and only the user's approval changes a setting. Values outside the allowed range are
refused before they reach the user.
"""

import json
from dataclasses import dataclass, field

TOOL_DEFINITIONS = [
    {
        'name': 'read_settings',
        'description': ('Return the current Shift Points inputs, the vehicle profile, the ECU limits and the '
                        'consistency findings as JSON. Call this before you advise on any value.'),
        'input_schema': {'type': 'object', 'properties': {}},
    },
    {
        'name': 'propose_change',
        'description': ('Propose one change to a setting. The user must approve it in the app before it is '
                        'applied. Do not say a change is applied; say it is proposed and why.'),
        'input_schema': {
            'type': 'object',
            'properties': {
                'field': {'type': 'string', 'description': 'Name of the setting, as read_settings lists it.'},
                'value': {'type': 'number', 'description': 'The new value.'},
                'reason': {'type': 'string', 'description': 'Why this value, in one or two sentences.'},
            },
            'required': ['field', 'value', 'reason'],
        },
    },
    {
        'name': 'ask_user',
        'description': ('Ask the user for a value you need and cannot find in the settings or the library. '
                        'Use it only for data that is missing, not for things you can read.'),
        'input_schema': {
            'type': 'object',
            'properties': {'question': {'type': 'string'}},
            'required': ['question'],
        },
    },
]


@dataclass
class Session:
    snapshot: dict
    bounds: dict  # field -> (low, high)
    proposals: list = field(default_factory=list)
    questions: list = field(default_factory=list)


def validate_proposal(name, value, bounds):
    """Return (True, '') or (False, reason). Only numbers inside the allowed range pass."""
    if name not in bounds:
        return False, f'"{name}" is not a setting the app lets the AI change.'
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False, f'"{name}" needs a number.'
    low, high = bounds[name]
    if not (low <= number <= high):
        return False, f'{number:g} is outside the allowed range {low:g} to {high:g} for {name}.'
    return True, ''


def run_tool(session, name, tool_input):
    """Run one tool call and return the text the model receives back."""
    if name == 'read_settings':
        return json.dumps(session.snapshot, indent=2)
    if name == 'propose_change':
        field_name = str(tool_input.get('field', ''))
        ok, reason = validate_proposal(field_name, tool_input.get('value'), session.bounds)
        if not ok:
            return f'Refused: {reason}'
        proposal = {'field': field_name, 'value': float(tool_input['value']),
                    'reason': str(tool_input.get('reason', ''))[:500]}
        session.proposals.append(proposal)
        return 'Proposed to the user. It is not applied until the user approves it.'
    if name == 'ask_user':
        question = str(tool_input.get('question', '')).strip()
        if question:
            session.questions.append(question[:500])
        return 'The question was shown to the user. Wait for their answer in the next message.'
    return f'Unknown tool {name!r}.'
