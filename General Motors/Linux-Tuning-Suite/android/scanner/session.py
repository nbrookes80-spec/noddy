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

    def adapter_info(self, recent=40):
        """What the Agent may read about the adapter: whether it is connected and the latest commands and replies.

        Read only. Nothing here can send a command; it only copies the traffic log the adapter already keeps.
        """
        elm = self.elm
        if elm is None:
            return {'connected': False, 'demo': self.demo_on, 'recent': []}
        with elm._lock:
            traffic = [[direction, text] for direction, text in elm.traffic[-recent:]]
        return {'connected': True, 'demo': self.demo_on, 'recent': traffic}

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
