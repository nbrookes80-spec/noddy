"""Copy the Qt-free part of the desktop calculation package into android/tunertoolpro.

The desktop package in app/tunertoolpro is the source of truth. Run this after changing it:

    python3 android/sync_core.py

tests/test_core_in_sync.py fails when the copy has drifted, so the Android app cannot quietly
run old calculations.
"""

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'app' / 'tunertoolpro'
TARGET = HERE / 'tunertoolpro'
LEFT_OUT = ('gui', '__pycache__', '__main__.py')


def sync():
    if TARGET.exists():
        shutil.rmtree(TARGET)
    shutil.copytree(SOURCE, TARGET, ignore=shutil.ignore_patterns(*LEFT_OUT))


if __name__ == '__main__':
    sync()
    print(f'Copied {SOURCE} to {TARGET}')
