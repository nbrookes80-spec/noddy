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
    if not isinstance(data, dict):
        return merged
    # Keep keys this version does not know, so a save never drops another section.
    for key, value in data.items():
        if key != 'ai':
            merged[key] = value
    ai = data.get('ai')
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
    if tmp.is_symlink() or tmp.exists():
        tmp.unlink()  # a leftover file could have looser permissions or be a link
    # O_EXCL refuses to follow a link; the mode is set on the open file before any key is written.
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        os.fchmod(fh.fileno(), 0o600)
        json.dump(data, fh, indent=2)
    os.replace(tmp, path)
    return path
