"""The ways a sensor can be drawn: text, digital gauge, graph, histogram, analogue gauge.

GaugeView draws the picture under a sensor's name and number. Every picture marks the sensor's zones: red and
yellow at either end of the scale, green between two limits, blue below a cold limit (pid_view.bands says where
each one is, so the picture always agrees with the colour of the number). They show as coloured stretches on the
dial and bar, dashed lines across the graph and coloured columns on the histogram. The bar and dial also mark the
lowest and highest reading so far with a small notch. A sensor can have an accent colour that tints the moving part
(bar fill, needle, graph line) whenever no zone applies.
`height_for` says how tall each picture needs to be, so a card can size itself.
"""

import math

from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget

from tunertoolpro.scanner import pid_view, themes
from ui_kit import ALERT, BORDER, CAUTION, MUTED, TEXT

HEIGHTS = {'text': 0, 'digital': 34, 'graph': 96, 'histogram': 96, 'analogue': 150}
SWEEP = 240.0        # the dial covers this many degrees, centred on the top
BINS = 12


ZONE_COLOURS = {'red': ALERT, 'yellow': CAUTION, 'cold': themes.COLD, 'good': themes.GOOD}
LINE_COLOURS = {'red_low': ALERT, 'redline': ALERT, 'warn_low': CAUTION, 'warn': CAUTION, 'cold': themes.COLD,
                'good': themes.GOOD, 'good_to': themes.GOOD}      # the dashed line the graph draws at each limit


def height_for(mode):
    return dp(HEIGHTS.get(mode, 34))


def fraction(value, low, high):
    span = max(high - low, 1e-9)
    return min(max((value - low) / span, 0.0), 1.0)


def histogram_bins(series, low, high, bins=BINS):
    """Counts of the readings in each of `bins` equal slices between low and high."""
    counts = [0] * bins
    for value in series:
        counts[min(int(fraction(value, low, high) * bins), bins - 1)] += 1
    return counts


def needle_point(centre, radius, share):
    """Where the dial needle ends. share 0 is the left end of the arc, 1 the right end."""
    angle = math.radians(-SWEEP / 2 + SWEEP * share)    # degrees clockwise from straight up
    return centre[0] + radius * math.sin(angle), centre[1] + radius * math.cos(angle)


class GaugeView(Widget):
    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, **kwargs)
        self.mode = 'digital'
        self.value = None
        self.series = []
        self.low, self.high, self.redline = 0.0, 100.0, None
        self.limits = {}                # the zone limits (pid_view.ZONE_KEYS) in the units shown
        self.accent = None              # a colour for the moving part when no zone applies
        self.marks = (None, None)       # the lowest and highest reading so far
        self.height = height_for(self.mode)
        self.bind(pos=self._draw, size=self._draw)

    def configure(self, mode, low, high, shown):
        """`shown` is what PidViews.apply gives: the zone limits and the accent colour, in the shown unit."""
        self.mode, self.low, self.high = mode, low, high
        self.limits = {key: shown.get(key) for key in pid_view.ZONE_KEYS}
        self.redline = self.limits['redline']
        self.accent = pid_view.rgba(shown.get('color'))
        self.height = height_for(mode)
        self._draw()

    def update(self, value, series, marks=(None, None)):
        self.value, self.series, self.marks = value, list(series), marks
        self._draw()

    # --- drawing ---------------------------------------------------------------------------------

    def _bands(self):
        """The coloured stretches of the scale as (from share, to share, colour), 0 to 1 along the gauge."""
        return [(fraction(start, self.low, self.high), fraction(end, self.low, self.high), ZONE_COLOURS[name])
                for start, end, name in pid_view.bands(self.limits, self.low, self.high)]

    def _tint(self, fallback):
        """The colour of the moving part when no zone applies: the sensor's own colour, else the theme's."""
        return self.accent or fallback

    def _colour(self, fallback):
        """The colour of the moving part (bar fill, needle) for the current reading."""
        return ZONE_COLOURS.get(pid_view.zone(self.value, self.limits), self._tint(fallback))

    def _draw(self, *_):
        self.canvas.clear()
        if self.mode == 'text' or self.width <= 0 or self.height <= 0:
            return
        with self.canvas:
            {'digital': self._bar, 'graph': self._graph, 'histogram': self._histogram,
             'analogue': self._dial}.get(self.mode, self._bar)()

    def _bar(self):
        y = self.center_y - dp(4)
        Color(*BORDER)
        RoundedRectangle(pos=(self.x, y), size=(self.width, dp(8)), radius=[dp(4)])
        for start, end, colour in self._bands():
            Color(*colour[:3], 0.55)
            RoundedRectangle(pos=(self.x + self.width * start, y), size=(self.width * (end - start), dp(8)),
                             radius=[dp(4)])
        if self.value is not None:
            Color(*self._colour(themes.current().bar))
            RoundedRectangle(pos=(self.x, y), size=(max(self.width * fraction(self.value, self.low, self.high),
                                                       dp(8)), dp(8)), radius=[dp(4)])
        Color(*TEXT)
        for mark in self.marks:
            if mark is not None:
                x = self.x + self.width * fraction(mark, self.low, self.high)
                Line(points=[x, y - dp(4), x, y + dp(12)], width=dp(1.4))

    def _graph(self):
        Color(*BORDER)
        Line(rectangle=(self.x, self.y + dp(2), self.width, self.height - dp(4)), width=dp(1))
        low, high = self.low, self.high
        if self.series:    # the graph scales to the readings, but never hides a red line
            low, high = min(self.series), max(self.series)
            for red in (self.limits.get('red_low'), self.redline):
                if red is not None:
                    low, high = min(low, red), max(high, red)
            if high - low < 1e-9:
                low, high = low - 1, high + 1
        top, base = self.y + self.height - dp(6), self.y + dp(6)
        for key, colour in LINE_COLOURS.items():
            limit = self.limits.get(key)
            if limit is not None and low <= limit <= high:
                level = base + (top - base) * fraction(limit, low, high)
                Color(*colour)
                Line(points=[self.x, level, self.right, level], width=dp(1.2), dash_length=dp(5), dash_offset=dp(3))
        if len(self.series) > 1:
            step = self.width / (len(self.series) - 1)
            points = []
            for i, value in enumerate(self.series):
                points += [self.x + i * step, base + (top - base) * fraction(value, low, high)]
            Color(*self._tint(themes.current().line))
            Line(points=points, width=dp(1.6))

    def _histogram(self):
        counts = histogram_bins(self.series, self.low, self.high)
        biggest = max(counts) or 1
        width = self.width / BINS
        base = self.y + dp(4)
        now = (min(int(fraction(self.value, self.low, self.high) * BINS), BINS - 1)
               if self.value is not None else -1)
        for i, count in enumerate(counts):
            theme = themes.current()
            middle = self.low + (self.high - self.low) * (i + 0.5) / BINS    # the column takes the zone of its middle
            ordinary = self._tint(theme.bar if i == now else theme.line)
            colour = ZONE_COLOURS.get(pid_view.zone(middle, self.limits), ordinary)
            Color(*colour[:3], 1.0 if i == now else 0.75)
            Rectangle(pos=(self.x + i * width + dp(1), base),
                      size=(max(width - dp(2), dp(1)), max((self.height - dp(10)) * count / biggest, dp(1) if count else 0)))
        Color(*BORDER)
        Line(points=[self.x, base, self.right, base], width=dp(1))

    def _dial(self):
        radius = min(self.width / 2, self.height - dp(10)) - dp(8)
        centre = (self.center_x, self.y + self.height / 2 - dp(2))
        start = -SWEEP / 2
        Color(*BORDER)
        Line(circle=(*centre, radius, start, SWEEP / 2), width=dp(5), cap='none')
        for begin, end, colour in self._bands():
            Color(*colour)
            Line(circle=(*centre, radius, start + SWEEP * begin, start + SWEEP * end), width=dp(5), cap='none')
        Color(*MUTED)
        for tick in range(11):
            outer = needle_point(centre, radius + dp(2), tick / 10)
            inner = needle_point(centre, radius - dp(7 if tick % 5 == 0 else 4), tick / 10)
            Line(points=[*inner, *outer], width=dp(1.2 if tick % 5 == 0 else 0.8))
        Color(*TEXT)
        for mark in self.marks:
            if mark is not None:
                share = fraction(mark, self.low, self.high)
                Line(points=[*needle_point(centre, radius - dp(1), share), *needle_point(centre, radius + dp(6), share)],
                     width=dp(2))
        share = fraction(self.value, self.low, self.high) if self.value is not None else 0.0
        Color(*self._colour(themes.current().ok if self.value is not None else MUTED))
        Line(points=[*centre, *needle_point(centre, radius - dp(10), share)], width=dp(2.2))
        Ellipse(pos=(centre[0] - dp(5), centre[1] - dp(5)), size=(dp(10), dp(10)))
