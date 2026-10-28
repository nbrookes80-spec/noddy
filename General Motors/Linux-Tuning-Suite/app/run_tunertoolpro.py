"""Start script for the packaged Windows program (PyInstaller cannot run a module with a relative import)."""

import sys

from tunertoolpro.gui.main_window import run

if __name__ == '__main__':
    sys.exit(run())
