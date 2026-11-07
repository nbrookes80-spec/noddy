"""The AppImage runs on a machine that has none of the app's dependencies installed.

This is the claim the packaging rests on, and it cannot be checked by looking at the file.
Running it on the machine that built it proves nothing: that machine already has Python,
PyQt6 and every Qt library system-wide, so a bundle that quietly borrows them looks identical
to one that is self-contained. A bare distribution image tells the two apart.

What the base image provides is libgl1 and libegl1 and nothing else. Those two are the host's
graphics stack: they are on the AppImage project's exclude list because the host's libGL must
match the host's GPU driver, so bundling Mesa's copy breaks hardware acceleration on a machine
with, say, an NVIDIA driver. Every Linux desktop has them. Everything else the app needs --
Python, PyQt6, pandas, pyserial, Qt and libxcb-cursor -- must come out of the bundle, and this
test fails if any of it does not.

Opt-in: skipped unless Docker is reachable and an AppImage has been built. Build one with
packaging/linux/build_appimage.sh.
"""

import shutil
import subprocess
import unittest
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent.parent.parent / 'dist'

# The only host packages a desktop is assumed to have. Keep this list short: every addition
# is a thing the user must already have installed, and the point of the AppImage is that
# there are none.
HOST_GRAPHICS = 'libgl1 libegl1'

# Qt's offscreen platform still loads Qt, the platform plugin and every bundled library, so
# the test needs no display. A bare image has no FUSE, so the AppImage is started the way a
# user on such a machine would have to start it.
SCRIPT = (
    'apt-get update -qq >/dev/null 2>&1 && '
    f'apt-get install -y -qq {HOST_GRAPHICS} >/dev/null 2>&1; '
    'timeout 40 /opt/TunerToolPro.AppImage --appimage-extract-and-run; echo "EXIT:$?"'
)
STILL_RUNNING = 'EXIT:124'      # killed by the timer, i.e. it started and stayed up


def built_appimage():
    found = sorted(DIST.glob('TunerToolPro-*-x86_64.AppImage'))
    return found[-1] if found else None


def docker_works():
    if not shutil.which('docker'):
        return False
    return subprocess.run(['docker', 'info'], capture_output=True, timeout=60).returncode == 0


def start_on(image, appimage):
    """Start the AppImage inside a bare distribution image. Returns the combined output."""
    done = subprocess.run(
        ['docker', 'run', '--rm',
         '-v', f'{appimage}:/opt/TunerToolPro.AppImage:ro',
         '-w', '/tmp',
         '-e', 'QT_QPA_PLATFORM=offscreen',
         '-e', 'TUNERTOOLPRO_NO_SPLASH=1',
         '-e', 'DEBIAN_FRONTEND=noninteractive',
         image, 'bash', '-c', SCRIPT],
        capture_output=True, text=True, timeout=1800)
    return done.stdout + done.stderr


APPIMAGE = built_appimage()


@unittest.skipUnless(APPIMAGE, 'no AppImage in dist/: run packaging/linux/build_appimage.sh')
@unittest.skipUnless(docker_works(), 'docker is not reachable')
class StartsOnACleanMachine(unittest.TestCase):

    def test_on_the_oldest_system_it_claims(self):
        """Ubuntu 22.04, glibc 2.35: the floor the README and INSTALL.md promise."""
        output = start_on('ubuntu:22.04', APPIMAGE)
        self.assertIn(STILL_RUNNING, output, f'did not start on a clean Ubuntu 22.04:\n{output}')

    def test_on_a_newer_system_than_it_was_built_on(self):
        """A bundled library can also collide with a newer host. Ubuntu 24.04, glibc 2.39."""
        output = start_on('ubuntu:24.04', APPIMAGE)
        self.assertIn(STILL_RUNNING, output, f'did not start on a clean Ubuntu 24.04:\n{output}')


if __name__ == '__main__':
    unittest.main()
