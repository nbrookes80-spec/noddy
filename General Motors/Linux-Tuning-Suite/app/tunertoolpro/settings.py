"""User settings, kept outside the program folder so an uninstall does not remove them.

Windows equivalent: %APPDATA%\\TunerToolPro. Linux: ~/.config/TunerToolPro (or $XDG_CONFIG_HOME).
Set TUNERTOOLPRO_HOME to use another folder. Standard library only.
"""

import copy
import json
import os
from pathlib import Path

DEFAULTS = {
    'ai': {'enabled': False, 'api_key': '', 'model': 'claude-sonnet-5-5'},
}
AI_MODELS = ['claude-sonnet-5-5', 'claude-haiku-5-5', 'claude-opus-5-5']


def user_dir():
    override = os.environ.get('TUNERTOOLPRO_HOME')
    if override:
        return Path(override).expanduser()
    base = os.environ.get('XDG_CONFIG_HOME') or (Path.home() / '.config')
    return Path(base) / 'TunerToolPro'


def settings_path():
    return user_dir() / 'settings.json'


def load():
    """Return the settings, with defaults for anything missing or unreadable."""
    merged = copy.deepcopy(DEFAULTS)
    try:
        data = json.loads(settings_path().read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return merged
    ai = data.get('ai') if isinstance(data, dict) else None
    if isinstance(ai, dict):
        for key in DEFAULTS['ai']:
            if key in ai and type(ai[key]) is type(DEFAULTS['ai'][key]):
                merged['ai'][key] = ai[key]
    return merged


def save(data):
    """Write the settings. The file is readable by the owner only, because it can hold an API key."""
    path = settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2)
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)
    return path
