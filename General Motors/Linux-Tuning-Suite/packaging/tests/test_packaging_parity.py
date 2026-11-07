"""The Windows and Linux packagers bundle the same things.

There are two ways this app is packaged -- the GitHub Actions Windows job and the Linux
AppImage build script -- and they name the files to bundle separately, in two different
languages, in two different files. Nothing makes them agree. So when a data folder is added to
the app, one packager gets updated and the other quietly keeps shipping without it, and the
break only shows when a user on that platform opens the screen that reads the file.

This test is the thing that makes them agree. It finds every folder under the app package that
holds files Python will not import -- the Torque PID CSVs, the splash artwork -- and insists
both packagers carry it. Add a new data folder and this fails until both are updated.

    cd "General Motors/Linux-Tuning-Suite/packaging" && python3 -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

SUITE = Path(__file__).resolve().parent.parent.parent
APP_PKG = SUITE / 'app' / 'tunertoolpro'
WINDOWS_WORKFLOW = SUITE.parent.parent / '.github' / 'workflows' / 'windows.yml'
LINUX_BUILD = SUITE / 'packaging' / 'linux' / 'build-in-container.sh'

CODE_SUFFIXES = {'.py', '.pyc', '.pyo'}


def data_folders():
    """Folders inside the app package holding files Python will not import, as 'tunertoolpro/...'."""
    found = set()
    for path in APP_PKG.rglob('*'):
        if not path.is_file() or path.suffix.lower() in CODE_SUFFIXES:
            continue
        if '__pycache__' in path.parts:
            continue
        found.add('tunertoolpro/' + path.parent.relative_to(APP_PKG).as_posix().strip('.'))
    return {f.rstrip('/') for f in found}


class TheAppHasDataToBundle(unittest.TestCase):

    def test_the_known_data_folders_are_found(self):
        """A guard on the test itself: if this finds nothing, the checks below pass vacuously."""
        found = data_folders()
        self.assertIn('tunertoolpro/data', found)
        self.assertIn('tunertoolpro/gui/assets', found)


class BothPackagersBundleIt(unittest.TestCase):

    def test_the_windows_build_bundles_every_data_folder(self):
        # PyInstaller on Windows separates source from destination with ';'.
        text = WINDOWS_WORKFLOW.read_text(encoding='utf-8')
        for folder in sorted(data_folders()):
            with self.subTest(folder=folder):
                self.assertRegex(
                    text, re.escape(f'app/{folder};{folder}'),
                    f'the Windows workflow does not --add-data {folder}: a Windows build ships '
                    f'without those files and breaks when the app reads them')

    def test_the_linux_build_bundles_every_data_folder(self):
        # PyInstaller on Linux separates source from destination with ':'.
        text = LINUX_BUILD.read_text(encoding='utf-8')
        for folder in sorted(data_folders()):
            with self.subTest(folder=folder):
                self.assertRegex(
                    text, re.escape(f'{folder}:{folder}'),
                    f'the Linux build script does not --add-data {folder}')


class TheTwoBuildsAgree(unittest.TestCase):

    def test_they_build_the_same_entry_point(self):
        for path in (WINDOWS_WORKFLOW, LINUX_BUILD):
            with self.subTest(path=path.name):
                self.assertIn('run_tunertoolpro.py', path.read_text(encoding='utf-8'))

    def test_they_both_collect_the_package_submodules(self):
        for path in (WINDOWS_WORKFLOW, LINUX_BUILD):
            with self.subTest(path=path.name):
                self.assertIn('--collect-submodules tunertoolpro', path.read_text(encoding='utf-8'))

    def test_the_installer_script_reads_the_pyinstaller_output(self):
        iss = (SUITE / 'packaging' / 'windows' / 'TunerToolPro.iss').read_text(encoding='utf-8')
        self.assertIn(r'..\..\dist\TunerToolPro\*', iss)
        self.assertIn('TunerToolPro.exe', iss)


if __name__ == '__main__':
    unittest.main()
