"""The shared core files must be exactly the release pinned in core.lock."""

import importlib.util
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[2] / 'tools' / 'update_core.py'
spec = importlib.util.spec_from_file_location('update_core', TOOL)
update_core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update_core)


class CorePinnedTest(unittest.TestCase):
    def test_core_matches_lock(self):
        problems = update_core.check()
        self.assertEqual(problems, [], '\n'.join(problems) +
                         '\nDo not edit core files here. Change tunertoolpro-core, tag a release, '
                         'then run: python3 tools/update_core.py <tag>')

    def test_lock_names_a_tag(self):
        lock = update_core.read_lock()
        self.assertRegex(lock['tag'], r'^v\d+\.\d+\.\d+$')
        self.assertRegex(lock['commit'], r'^[0-9a-f]{40}$')

    def test_app_only_files_are_not_core(self):
        files = update_core.core_files(update_core.CORE_DIR)
        self.assertNotIn('__init__.py', files)
        self.assertFalse([f for f in files if f.startswith('gui/')])
        self.assertIn('core.py', files)


if __name__ == '__main__':
    unittest.main()
