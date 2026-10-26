import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / 'app' / 'tunertoolpro'
TARGET = ROOT / 'tunertoolpro'
sys.path.insert(0, str(ROOT))

from sync_core import LEFT_OUT  # noqa: E402


def python_files(root):
    """Relative path -> bytes for every file the Android copy should contain."""
    files = {}
    for path in root.rglob('*.py'):
        rel = path.relative_to(root)
        if '__pycache__' in rel.parts or rel.parts[0] in LEFT_OUT or rel.name in LEFT_OUT:
            continue
        files[rel.as_posix()] = path.read_bytes()
    return files


@unittest.skipUnless(SOURCE.exists(), 'the desktop package is not in this checkout')
class CoreInSyncTests(unittest.TestCase):
    def test_android_copy_matches_the_desktop_package(self):
        self.assertEqual(python_files(TARGET), python_files(SOURCE),
                         'android/tunertoolpro is out of date: run python3 android/sync_core.py')


if __name__ == '__main__':
    unittest.main()
