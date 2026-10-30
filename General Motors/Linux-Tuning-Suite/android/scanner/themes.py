"""Gauge colour themes for the dashboard. No Kivy.

A theme picks the colours of the gauge bar, the graph line and the "all good" needle. The red line is always
red, in every theme, so a limit can never be mistaken for a style choice.
"""

from collections import namedtuple

Theme = namedtuple('Theme', 'key label bar line ok')

THEMES = {t.key: t for t in (
    Theme('classic', 'Classic (amber and blue)', (0.96, 0.65, 0.14, 1), (0.47, 0.78, 1.0, 1), (0.40, 0.80, 0.55, 1)),
    Theme('green', 'Green', (0.40, 0.85, 0.50, 1), (0.55, 0.95, 0.65, 1), (0.40, 0.85, 0.50, 1)),
    Theme('ice', 'Ice blue', (0.47, 0.78, 1.0, 1), (0.80, 0.92, 1.0, 1), (0.47, 0.78, 1.0, 1)),
    Theme('amber', 'Amber', (1.0, 0.72, 0.20, 1), (1.0, 0.85, 0.45, 1), (1.0, 0.72, 0.20, 1)),
    Theme('white', 'White', (1.0, 1.0, 1.0, 1), (0.85, 0.88, 0.92, 1), (1.0, 1.0, 1.0, 1)),
)}
DEFAULT = 'classic'
_current = DEFAULT


def use(key):
    """Switch the gauges to a theme. An unknown name keeps the current one. Returns the theme now in use."""
    global _current
    if key in THEMES:
        _current = key
    return THEMES[_current]


def current():
    return THEMES[_current]


def key_for(label):
    return next((t.key for t in THEMES.values() if t.label == label), DEFAULT)
