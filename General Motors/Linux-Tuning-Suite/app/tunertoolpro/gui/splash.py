"""The flash intro: the car pictures fade in and out over the app's dark background, then the app opens.

A click or any key skips it. Set TUNERTOOLPRO_NO_SPLASH=1 to turn it off.
"""

import os
import sys
import time
from pathlib import Path

from PyQt6.QtCore import QRectF, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget

from ..splash_plan import SplashPlan

INTRO = ['intro_side.png', 'intro_bay.png']
BACKGROUND = QColor('#141a24')
ACCENT = QColor('#f5a623')


def asset_path(name):
    """Works from the source tree and from a PyInstaller bundle."""
    base = Path(getattr(sys, '_MEIPASS', '')) / 'tunertoolpro' / 'gui' / 'assets'
    if not base.is_dir():
        base = Path(__file__).resolve().parent / 'assets'
    return base / name


def splash_enabled():
    return os.environ.get('TUNERTOOLPRO_NO_SPLASH', '') not in ('1', 'true', 'yes')


class SplashScreen(QWidget):
    finished = pyqtSignal()

    def __init__(self, plan=None):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.plan = plan or SplashPlan(INTRO)
        self.pictures = {name: QPixmap(str(asset_path(name))) for name in self.plan.names}
        self.setFixedSize(760, 460)
        self._started = time.monotonic()
        self._current = self.plan.at(0)
        self._done = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    def start(self):
        screen = QApplication.primaryScreen()
        if screen is not None:
            self.move(screen.availableGeometry().center() - self.rect().center())
        self._started = time.monotonic()
        self.show()
        self._timer.start(16)

    def _tick(self):
        self._current = self.plan.at(int((time.monotonic() - self._started) * 1000))
        if self._current is None:
            self.skip()
        self.update()

    def skip(self):
        if not self._done:
            self._done = True
            self._timer.stop()
            self.finished.emit()   # open the main window first, or closing this one would quit the app
            self.close()

    def mousePressEvent(self, _event):
        self.skip()

    def keyPressEvent(self, _event):
        self.skip()

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        p.fillRect(self.rect(), BACKGROUND)
        if self._current is not None:
            name, opacity = self._current
            pic = self.pictures[name]
            if not pic.isNull():
                room = QRectF(30, 20, self.width() - 60, self.height() - 120)
                scale = min(room.width() / pic.width(), room.height() / pic.height())
                w, h = pic.width() * scale, pic.height() * scale
                p.setOpacity(opacity)
                p.drawPixmap(QRectF(room.center().x() - w / 2, room.center().y() - h / 2, w, h), pic,
                             QRectF(pic.rect()))
        p.setOpacity(1.0)
        p.setPen(ACCENT)
        title = QFont(self.font())
        title.setPointSize(26)
        title.setBold(True)
        p.setFont(title)
        p.drawText(QRectF(0, self.height() - 95, self.width(), 50), Qt.AlignmentFlag.AlignCenter, 'TunerToolPro')
        p.setPen(QColor('#9aa7b8'))
        small = QFont(self.font())
        small.setPointSize(10)
        p.setFont(small)
        p.drawText(QRectF(0, self.height() - 48, self.width(), 30), Qt.AlignmentFlag.AlignCenter,
                   'Transmission calibration for GM 4L60E and 6L80E')
