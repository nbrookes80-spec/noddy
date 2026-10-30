"""Pin the shared core (github.com/nbrookes80-spec/tunertoolpro-core) at a release tag.

    python3 tools/update_core.py v0.1.0     fetch that tag, replace the core files, rewrite core.lock
    python3 tools/update_core.py --check    verify the core files match core.lock (the test suite does this)

The core files live in app/tunertoolpro (everything except gui/, __main__.py and __init__.py) and are
copied to android/tunertoolpro by android/sync_core.py. Never edit them here: change the core repo,
tag a release, then run this.
"""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent
CORE_DIR = SUITE / 'app' / 'tunertoolpro'
LOCK = SUITE / 'core.lock'
REPO = 'https://github.com/nbrookes80-spec/tunertoolpro-core.git'
APP_ONLY = ('gui', '__main__.py', '__init__.py', '__pycache__')


def core_files(root):
    """Relative paths of the core files under a tunertoolpro package folder, sorted."""
    root = Path(root)
    found = []
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if path.is_file() and rel.parts[0] not in APP_ONLY and '__pycache__' not in rel.parts:
            found.append(rel.as_posix())
    return sorted(found)


def tree_hash(root):
    """SHA-256 over every core file's path and content (line endings normalised)."""
    digest = hashlib.sha256()
    for rel in core_files(root):
        data = (Path(root) / rel).read_bytes().replace(b'\r\n', b'\n')
        digest.update(rel.encode() + b'\0' + data + b'\0')
    return digest.hexdigest()


def read_lock():
    return json.loads(LOCK.read_text())


def check():
    """Return a list of problems; empty means the core files are exactly the pinned release."""
    lock = read_lock()
    problems = []
    have = tree_hash(CORE_DIR)
    if have != lock['tree_sha256']:
        problems.append(f"app/tunertoolpro core files differ from {lock['tag']} "
                        f"(hash {have[:12]}, lock {lock['tree_sha256'][:12]})")
    return problems


def update(tag):
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / 'core'
        subprocess.run(['git', '-c', 'advice.detachedHead=false', 'clone', '--quiet', '--branch', tag, '--depth', '1', REPO, str(clone)],
                       check=True)
        commit = subprocess.run(['git', '-C', str(clone), 'rev-parse', 'HEAD'], check=True,
                                capture_output=True, text=True).stdout.strip()
        source = clone / 'tunertoolpro'
        for rel in core_files(CORE_DIR):
            (CORE_DIR / rel).unlink()
        for rel in core_files(source):
            target = CORE_DIR / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / rel, target)
        digest = tree_hash(CORE_DIR)
    for folder in sorted(CORE_DIR.rglob('*'), reverse=True):  # drop folders emptied by removed files
        if folder.is_dir() and folder.name != 'gui' and not any(folder.iterdir()):
            folder.rmdir()
    LOCK.write_text(json.dumps({'repo': REPO, 'tag': tag, 'commit': commit, 'tree_sha256': digest},
                               indent=2) + '\n')
    subprocess.run([sys.executable, str(SUITE / 'android' / 'sync_core.py')], check=True)
    print(f'Core pinned at {tag} ({commit[:10]}). Run both test suites, then commit core.lock and the copies.')


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        issues = check()
        print('\n'.join(issues) or 'core matches core.lock')
        sys.exit(1 if issues else 0)
    if len(sys.argv) != 2 or sys.argv[1].startswith('-'):
        sys.exit(__doc__)
    update(sys.argv[1])
