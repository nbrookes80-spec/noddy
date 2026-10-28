"""The flash intro: car pictures fade in and out over the app background, then the app shows. Tap to skip."""

import os

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from splash_plan import SplashPlan
from ui_kit import ACCENT, BG, MUTED

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
INTRO = ['intro_side.png', 'intro_bay.png']


class SplashOverlay(FloatLayout):
    """Sits on top of the whole app until the plan finishes or the user taps."""

    def __init__(self, plan=None, on_done=None, **kwargs):
        super().__init__(**kwargs)
        self.plan = plan or SplashPlan(INTRO)
        self.on_done = on_done
        self._elapsed = 0.0
        self._finished = False
        with self.canvas.before:
            Color(*BG)
            self._back = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._resize, size=self._resize)
        self.picture = Image(allow_stretch=True, keep_ratio=True, opacity=0,
                             size_hint=(0.92, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.58})
        self.title = Label(text='TunerToolPro', bold=True, font_size=dp(30), color=ACCENT,
                           size_hint=(1, None), height=dp(44), pos_hint={'center_x': 0.5, 'center_y': 0.28})
        self.subtitle = Label(text='GM 4L60E and 6L80E calibration', font_size=dp(13), color=MUTED,
                              size_hint=(1, None), height=dp(24), pos_hint={'center_x': 0.5, 'center_y': 0.23})
        for widget in (self.picture, self.title, self.subtitle):
            self.add_widget(widget)
        self._shown = None
        self._event = Clock.schedule_interval(self._tick, 1 / 30)
        self._tick(0)

    def _resize(self, *_):
        self._back.pos, self._back.size = self.pos, self.size

    def _tick(self, dt):
        self._elapsed += dt
        state = self.plan.at(int(self._elapsed * 1000))
        if state is None:
            self.finish()
            return
        name, opacity = state
        if name != self._shown:
            self._shown = name
            self.picture.source = os.path.join(ASSETS, name)
        self.picture.opacity = opacity

    def on_touch_down(self, touch):
        self.finish()
        return True

    def finish(self):
        if self._finished:
            return
        self._finished = True
        self._event.cancel()
        if self.parent is not None:
            self.parent.remove_widget(self)
        if self.on_done:
            self.on_done()
