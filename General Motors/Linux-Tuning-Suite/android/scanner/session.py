"""Which data source the screens read from: the demo drive, a connected adapter, or nothing."""

from .demo import DemoSource

DEMO, LIVE, OFFLINE = 'DEMO', 'LIVE', 'OFFLINE'


class Session:
    """Shared by the Link and Scan screens. Demo mode wins while it is on; the adapter stays connected."""

    def __init__(self):
        self.demo = DemoSource()
        self.demo_on = False
        self.elm = None
        self.listeners = []

    def active(self):
        if self.demo_on:
            return self.demo
        return self.elm

    @property
    def status(self):
        if self.demo_on:
            return DEMO
        return LIVE if self.elm is not None else OFFLINE

    def set_demo(self, on):
        self.demo_on = bool(on)
        self._notify()

    def attach(self, elm):
        self.elm = elm
        self._notify()

    def detach(self):
        elm, self.elm = self.elm, None
        if elm is not None:
            elm.close()
        self._notify()

    def _notify(self):
        for listener in self.listeners:
            listener(self.status)
