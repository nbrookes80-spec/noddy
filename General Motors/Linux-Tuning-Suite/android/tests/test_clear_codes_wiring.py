"""The code clear (Mode 04) is off unless the app turns it on. Every place the app builds an adapter link must say
which, so a new call site cannot quietly drop the build's CLEAR_CODES switch. No Kivy."""

import ast
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))


def elm_calls(path):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = getattr(node.func, 'attr', getattr(node.func, 'id', ''))
            if name == 'Elm327':
                yield node


class ClearCodesWiringTests(unittest.TestCase):
    def test_every_app_link_says_whether_the_clear_is_allowed(self):
        found = 0
        for path in sorted(HERE.glob('*.py')):
            for call in elm_calls(path):
                found += 1
                keywords = {k.arg: k.value for k in call.keywords}
                self.assertIn('allow_clear', keywords, f'{path.name}:{call.lineno} builds Elm327 without allow_clear')
        self.assertGreaterEqual(found, 1, 'the app should build at least one adapter link')

    def test_every_app_link_says_whether_other_modules_may_be_read(self):
        """Mode 21 and the 7B0/7C0/7C4/7E1 headers are refused unless a link is built with extra_modules=True, so
        each call site must pass the choice on purpose instead of leaning on the default."""
        for path in sorted(HERE.glob('*.py')):
            for call in elm_calls(path):
                keywords = {k.arg for k in call.keywords}
                self.assertIn('extra_modules', keywords, f'{path.name}:{call.lineno} builds Elm327 without extra_modules')

    def test_the_connect_screen_passes_the_saved_module_switch(self):
        self.assertIn("extra_modules=self.saved['extra_modules']", (HERE / 'link_ui.py').read_text())

    def test_the_connect_screen_follows_the_build_switch(self):
        source = (HERE / 'link_ui.py').read_text()
        self.assertIn('allow_clear=variant.CLEAR_CODES', source)


if __name__ == '__main__':
    unittest.main()
