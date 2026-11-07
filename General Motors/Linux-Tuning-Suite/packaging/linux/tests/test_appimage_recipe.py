"""The AppImage recipe: the parts that can be checked without running a build.

A build needs Docker and several minutes, so it does not run here. What these tests protect is
the recipe's agreement with the app: the version the build reads, the paths it bundles, the
entry point it starts, and a desktop entry a Linux desktop will accept. Each of those breaks
silently -- the build still succeeds and the AppImage still appears -- so they are worth a test.
"""

import os
import re
import struct
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent      # packaging/linux
SUITE = HERE.parent.parent                          # the Linux-Tuning-Suite folder
APP = SUITE / 'app'

DESKTOP = HERE / 'TunerToolPro.desktop'
ICON = HERE / 'tunertoolpro.png'
HOST_SCRIPT = HERE / 'build_appimage.sh'
BUILD_SCRIPT = HERE / 'build-in-container.sh'
DOCKERFILE = HERE / 'Dockerfile'

# The expression build-in-container.sh uses to read the version out of the app.
VERSION_SED = re.compile(r'^__version__ = "(.*)"', re.M)


def desktop_entries():
    entries = {}
    for line in DESKTOP.read_text(encoding='utf-8').splitlines():
        if '=' in line and not line.startswith(('[', '#')):
            key, value = line.split('=', 1)
            entries[key] = value
    return entries


class Recipe(unittest.TestCase):

    def test_every_piece_is_present(self):
        for path in (DESKTOP, ICON, HOST_SCRIPT, BUILD_SCRIPT, DOCKERFILE):
            self.assertTrue(path.is_file(), f'missing {path.name}')

    def test_both_scripts_are_executable(self):
        for script in (HOST_SCRIPT, BUILD_SCRIPT):
            self.assertTrue(os.access(script, os.X_OK), f'{script.name} is not executable')


class Version(unittest.TestCase):

    def test_the_build_can_read_the_version(self):
        """The build fails loudly on an empty version, so the pattern must match the real file."""
        found = VERSION_SED.search((APP / 'tunertoolpro' / '__init__.py').read_text(encoding='utf-8'))
        self.assertIsNotNone(found, 'build-in-container.sh would read an empty version')
        self.assertRegex(found.group(1), r'^\d+\.\d+\.\d+')


class Bundled(unittest.TestCase):
    """What the build copies in has to still be where the build looks for it."""

    def test_the_entry_point_exists(self):
        self.assertTrue((APP / 'run_tunertoolpro.py').is_file())

    def test_the_data_and_asset_folders_exist(self):
        # Addressed at runtime by profiles.DATA_DIR and splash.asset_path, so they must be in
        # the bundle under tunertoolpro/ or the Scan profiles and the splash screen come up empty.
        self.assertTrue((APP / 'tunertoolpro' / 'data').is_dir())
        self.assertTrue((APP / 'tunertoolpro' / 'gui' / 'assets').is_dir())

    def test_the_build_bundles_every_data_folder_it_should(self):
        script = BUILD_SCRIPT.read_text(encoding='utf-8')
        for fragment in ('tunertoolpro/data', 'tunertoolpro/gui/assets', 'run_tunertoolpro.py'):
            self.assertIn(fragment, script, f'{fragment} is not in the PyInstaller command')

    def test_requirements_are_installed_by_the_build(self):
        self.assertIn('requirements.txt', BUILD_SCRIPT.read_text(encoding='utf-8'))
        self.assertTrue((APP / 'requirements.txt').is_file())


class Desktop(unittest.TestCase):

    def test_it_has_what_a_desktop_needs(self):
        entries = desktop_entries()
        self.assertEqual(entries.get('Type'), 'Application')
        self.assertEqual(entries.get('Name'), 'TunerToolPro')
        self.assertEqual(entries.get('Terminal'), 'false')
        self.assertTrue(entries.get('Comment'))

    def test_the_icon_name_matches_the_icon_file(self):
        self.assertEqual(desktop_entries().get('Icon'), ICON.stem)

    def test_categories_are_registered_names(self):
        # desktop-file-validate rejects unregistered main categories, and appimagetool runs it,
        # so a bad category fails the build rather than the app.
        main = {'AudioVideo', 'Audio', 'Video', 'Development', 'Education', 'Game', 'Graphics',
                'Network', 'Office', 'Science', 'Settings', 'System', 'Utility'}
        additional = {'Engineering'}
        got = [c for c in desktop_entries()['Categories'].split(';') if c]
        self.assertTrue(set(got) & main, 'needs at least one registered main category')
        for category in got:
            self.assertIn(category, main | additional, f'{category} is not a registered category')

    def test_engineering_comes_with_its_main_category(self):
        got = desktop_entries()['Categories'].split(';')
        if 'Engineering' in got:
            self.assertIn('Science', got, 'Engineering is only valid alongside Science')


class Icon(unittest.TestCase):

    def test_it_is_a_256_square_png(self):
        """appimagetool wants a real PNG, and 256x256 is the size a desktop asks for first."""
        head = ICON.read_bytes()[:24]
        self.assertEqual(head[:8], b'\x89PNG\r\n\x1a\n', 'not a PNG')
        width, height = struct.unpack('>II', head[16:24])
        self.assertEqual((width, height), (256, 256))


class BuildBase(unittest.TestCase):

    def test_the_base_image_is_the_old_one_on_purpose(self):
        """Ubuntu 22.04 sets the glibc floor. Bumping it drops users, so it should be deliberate."""
        self.assertIn('FROM ubuntu:22.04', DOCKERFILE.read_text(encoding='utf-8'))

    def test_the_shared_libpython_is_installed(self):
        # Ubuntu's python3.10 package ships only the static interpreter. Without libpython3.10,
        # PyInstaller stops with "Python shared library ('libpython3.10.so.1.0') was not found".
        self.assertIn('libpython3.10', DOCKERFILE.read_text(encoding='utf-8'))

    def test_the_qt_library_that_breaks_startup_is_installed(self):
        # Without libxcb-cursor0 in the build container, PyInstaller cannot copy it in, and the
        # AppImage starts to a "could not load the Qt platform plugin xcb" error on a clean machine.
        self.assertIn('libxcb-cursor0', DOCKERFILE.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
