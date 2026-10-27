import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tunertoolpro import settings  # noqa: E402


class WindowsSettingsTests(unittest.TestCase):
    def test_windows_keeps_settings_under_appdata(self):
        env = {'APPDATA': r'C:\Users\Sam\AppData\Roaming'}
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch.object(settings.sys, 'platform', 'win32'):
            folder = settings.user_dir()
        self.assertEqual(folder.name, 'TunerToolPro')
        self.assertIn('AppData', str(folder))
        self.assertNotIn('.config', str(folder))

    def test_linux_still_uses_the_config_folder(self):
        with mock.patch.dict(os.environ, {'XDG_CONFIG_HOME': '/tmp/xdg-test'}, clear=True), \
                mock.patch.object(settings.sys, 'platform', 'linux'):
            self.assertEqual(settings.user_dir(), Path('/tmp/xdg-test') / 'TunerToolPro')

    def test_saving_works_where_the_system_has_no_fchmod(self):
        with tempfile.TemporaryDirectory() as home, \
                mock.patch.dict(os.environ, {'TUNERTOOLPRO_HOME': home}):
            real = getattr(os, 'fchmod', None)
            if real is not None:
                del os.fchmod                  # Windows has no os.fchmod
            try:
                path = settings.save({'ai': {'enabled': True}})
            finally:
                if real is not None:
                    os.fchmod = real
            self.assertTrue(settings.load()['ai']['enabled'])
            self.assertEqual(path.parent, Path(home))


if __name__ == '__main__':
    unittest.main()
