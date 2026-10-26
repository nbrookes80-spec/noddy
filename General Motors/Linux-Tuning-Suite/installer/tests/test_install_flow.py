"""Install and uninstall end to end, with HOME pointed at a scratch folder and no package download.

Run from the installer folder:  python3 -m unittest discover -s tests -t .
"""

import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import install_tunertoolpro as setup  # noqa: E402


class InstallFlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / 'home'
        self.home.mkdir()
        self.env = mock.patch.dict(os.environ, {'HOME': str(self.home)})
        self.env.start()
        os.environ.pop('TUNERTOOLPRO_HOME', None)
        os.environ.pop('XDG_CONFIG_HOME', None)
        self.target = Path(self.tmp.name) / 'Program' / 'TunerToolPro'
        self.lines = []

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def options(self, **kw):
        base = {'desktop': True, 'menu': True, 'command': True, 'ai_enabled': False, 'ai_key': '',
                'ai_model': 'claude-sonnet-5-5'}
        base.update(kw)
        return base

    def test_install_writes_layout_and_entries(self):
        launcher = setup.install(self.target, self.options(), log=self.lines.append, pip_install=False)
        self.assertEqual(launcher, self.target / 'run-tunertoolpro.sh')
        self.assertTrue(os.access(launcher, os.X_OK))
        self.assertTrue((self.target / 'app' / 'tunertoolpro' / '__main__.py').exists())
        self.assertTrue((self.target / setup.UNINSTALLER).exists())
        manifest = json.loads((self.target / setup.MANIFEST).read_text(encoding='utf-8'))
        self.assertEqual(manifest['product'], 'TunerToolPro')
        self.assertEqual(manifest['version'], setup.app_version())
        apps = self.home / '.local' / 'share' / 'applications'
        self.assertTrue((apps / 'tunertoolpro.desktop').exists())
        self.assertTrue((apps / 'tunertoolpro-uninstall.desktop').exists())
        self.assertTrue(os.path.islink(self.home / '.local' / 'bin' / 'tunertoolpro'))

    def test_desktop_shortcut_only_when_desktop_folder_exists(self):
        (self.home / 'Desktop').mkdir()
        with mock.patch.object(setup, 'desktop_dir', return_value=self.home / 'Desktop'):
            setup.install(self.target, self.options(), log=self.lines.append, pip_install=False)
        self.assertTrue((self.home / 'Desktop' / 'TunerToolPro.desktop').exists())

    def test_ai_key_is_saved_owner_only_and_not_logged(self):
        setup.install(self.target, self.options(ai_enabled=True, ai_key='sk-test-999',
                                                ai_model='claude-haiku-5-5'),
                      log=self.lines.append, pip_install=False)
        from tunertoolpro import settings
        path = settings.settings_path()
        self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600)
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(data['ai']['api_key'], 'sk-test-999')
        self.assertEqual(data['ai']['model'], 'claude-haiku-5-5')
        self.assertNotIn('sk-test-999', '\n'.join(self.lines))

    def test_ai_key_not_saved_when_ai_is_off(self):
        setup.install(self.target, self.options(ai_enabled=False, ai_key='sk-off-1'),
                      log=self.lines.append, pip_install=False)
        from tunertoolpro import settings
        self.assertFalse(settings.settings_path().exists())

    def test_settings_keep_unknown_sections_on_save(self):
        from tunertoolpro import settings
        settings.save({'future': {'x': 1}})
        setup.install(self.target, self.options(ai_enabled=True, ai_key='sk-keep-2'),
                      log=self.lines.append, pip_install=False)
        data = json.loads(settings.settings_path().read_text(encoding='utf-8'))
        self.assertEqual(data['future'], {'x': 1})
        self.assertEqual(data['ai']['api_key'], 'sk-keep-2')

    def test_refuses_home_and_non_empty_folders(self):
        with self.assertRaises(ValueError):
            setup.check_target(self.home)
        self.target.mkdir(parents=True)
        (self.target / 'keep.txt').write_text('x', encoding='utf-8')
        with self.assertRaises(ValueError):
            setup.check_target(self.target)
        with self.assertRaises(ValueError):
            setup.check_target('relative/path')

    def test_uninstall_keeps_settings_by_default(self):
        setup.install(self.target, self.options(ai_enabled=True, ai_key='sk-keep'),
                      log=self.lines.append, pip_install=False)
        from tunertoolpro import settings
        settings_file = settings.settings_path()
        setup.uninstall(self.target, delete_settings=False, log=self.lines.append)
        self.assertFalse(self.target.exists())
        self.assertFalse((self.home / '.local' / 'share' / 'applications' / 'tunertoolpro.desktop').exists())
        self.assertFalse(os.path.lexists(self.home / '.local' / 'bin' / 'tunertoolpro'))
        self.assertTrue(settings_file.exists())

    def test_uninstall_can_delete_settings(self):
        setup.install(self.target, self.options(ai_enabled=True, ai_key='sk-gone'),
                      log=self.lines.append, pip_install=False)
        from tunertoolpro import settings
        setup.uninstall(self.target, delete_settings=True, log=self.lines.append)
        self.assertFalse(settings.user_dir().exists())

    def test_uninstall_refuses_a_folder_without_manifest(self):
        self.target.mkdir(parents=True)
        with self.assertRaises(ValueError):
            setup.uninstall(self.target, log=self.lines.append)


if __name__ == '__main__':
    unittest.main()


class QtLibraryCheckTests(unittest.TestCase):
    def test_reports_missing_xcb_cursor_package(self):
        self.assertEqual(setup.missing_qt_libraries(find=lambda name: None), ['libxcb-cursor0'])

    def test_no_warning_when_library_present(self):
        self.assertEqual(setup.missing_qt_libraries(find=lambda name: '/usr/lib/libxcb-cursor.so.0'), [])


class FolderPermissionTests(unittest.TestCase):
    @unittest.skipIf(hasattr(os, 'geteuid') and os.geteuid() == 0, 'root can write anywhere')
    def test_refuses_a_folder_the_user_cannot_create(self):
        import tempfile
        with tempfile.TemporaryDirectory() as base:
            locked = Path(base) / 'locked'
            locked.mkdir()
            locked.chmod(0o555)
            try:
                with self.assertRaises(ValueError) as ctx:
                    setup.check_target(str(locked / 'TunerToolPro'))
                self.assertIn('permission', str(ctx.exception))
            finally:
                locked.chmod(0o755)

    def test_accepts_a_folder_inside_the_home_folder(self):
        setup.check_target(str(setup.DEFAULT_TARGET))
