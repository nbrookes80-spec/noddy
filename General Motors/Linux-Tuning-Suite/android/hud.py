"""HUD mode: the screen drawn mirrored, so a phone lying flat on the dashboard reads correctly as a reflection in
the windscreen.

Mirror holds the whole app. While `flipped` it draws everything reversed left to right and takes no touches:
Kivy tests a touch against where a widget would be unflipped, so a tap on the mirrored picture would land on the
wrong sensor. The buttons that matter (Exit, HUD, Record) sit outside the Mirror, over it, and stay readable.
"""

from kivy.graphics import PopMatrix, PushMatrix, Scale, Translate
from kivy.properties import BooleanProperty
from kivy.uix.floatlayout import FloatLayout


class Mirror(FloatLayout):
    flipped = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self._shift = Translate()
            self._scale = Scale(1, 1, 1)
        with self.canvas.after:
            PopMatrix()
        self.bind(pos=self._place, size=self._place, flipped=self._place)

    def _place(self, *_):
        """Reverse left to right about the middle of this widget, or draw as normal."""
        self._shift.x = self.x + self.right if self.flipped else 0
        self._scale.x = -1 if self.flipped else 1

    def on_touch_down(self, touch):
        if self.flipped:
            return self.collide_point(*touch.pos)    # swallowed: nothing under a mirrored picture can be pressed
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        return self.flipped or super().on_touch_move(touch)

    def on_touch_up(self, touch):
        return self.flipped or super().on_touch_up(touch)
