"""Load the ORIGINAL module from its .pyc with PyQt6 replaced by inert stubs.

The original module only imports PyQt6 classes at import time and only starts
the GUI under `if __name__ == '__main__'`. Here it is loaded under the name
'orig_module' with every PyQt6 name replaced by a dummy, so its pure-Python
engines and constant tables can be used as a reference, with no window,
no file access beyond reading the .pyc, and no network.

    from oracle import load_original
    orig = load_original("/path/to/app.pyc")
    orig.PressureEngine.base_shift_pressure(...)
"""

import marshal
import sys
import types


class _DummyMeta(type):
    def __getattr__(cls, name):
        return _make_dummy(name)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class _Dummy(metaclass=_DummyMeta):
    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        return _make_dummy(name)

    def __call__(self, *args, **kwargs):
        return _Dummy()


def _make_dummy(name):
    return type(name, (_Dummy,), {})


def _stub_module(name):
    mod = types.ModuleType(name)
    mod.__getattr__ = lambda attr: _make_dummy(attr)
    mod.__path__ = []
    return mod


def load_original(pyc_path):
    for name in ('PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'):
        sys.modules.setdefault(name, _stub_module(name))
    sys.modules['PyQt6'].QtCore = sys.modules['PyQt6.QtCore']
    sys.modules['PyQt6'].QtGui = sys.modules['PyQt6.QtGui']
    sys.modules['PyQt6'].QtWidgets = sys.modules['PyQt6.QtWidgets']

    raw = open(pyc_path, 'rb').read()
    code = marshal.loads(raw[16:])
    mod = types.ModuleType('orig_module')
    mod.__file__ = pyc_path
    sys.modules['orig_module'] = mod
    exec(code, mod.__dict__)
    return mod
