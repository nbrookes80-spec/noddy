"""When each intro picture shows and how opaque it is. No Qt, so it can be tested without a screen."""


class SplashPlan:
    """Each picture fades in, holds, then fades out; the pictures play one after another."""

    def __init__(self, names, hold_ms=1000, fade_ms=250):
        self.names = list(names)
        self.hold_ms = hold_ms
        self.fade_ms = fade_ms

    def _each_ms(self):
        return 2 * self.fade_ms + self.hold_ms

    def total_ms(self):
        return len(self.names) * self._each_ms()

    def at(self, ms):
        """(picture name, opacity 0..1) at this time, or None when the intro is over."""
        if ms < 0 or ms >= self.total_ms():
            return None
        index, local = divmod(ms, self._each_ms())
        if local < self.fade_ms:
            opacity = local / self.fade_ms
        elif local < self.fade_ms + self.hold_ms:
            opacity = 1.0
        else:
            opacity = (self._each_ms() - local) / self.fade_ms
        return self.names[int(index)], opacity
