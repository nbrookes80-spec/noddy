"""Main window: one tab per tool. Tabs share state only where the AI needs it: Shift Points and Vehicle."""

import sys

from PyQt6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow, QMessageBox, QScrollArea,
                             QTabWidget)

from .. import __version__
from ..legal import DISCLAIMER
from . import theme
from .ai_tab import AiTab, SettingsBridge, tables_context
from .bct_tab import BctTab
from .dyno_tab import DynoDragTab
from .log_tab import LogTab
from .pressure_tab import PressureTab
from .shift_tab import ShiftTab
from .vehicle_tab import VehicleTab
from .xdf_tab import XdfTab


def scrollable(page):
    """Put a tab page in a scroll area. The window can then be made smaller than the page; the page scrolls."""
    area = QScrollArea()
    area.setWidgetResizable(True)
    area.setFrameShape(QFrame.Shape.NoFrame)
    area.setWidget(page)
    return area


def tab_page(tabs, index):
    """The tab's own widget, whether or not it is wrapped in a scroll area."""
    widget = tabs.widget(index)
    return widget.widget() if isinstance(widget, QScrollArea) else widget


def wrap_long_labels(window, limit=60):
    """Long labels wrap onto several lines. Unwrapped, one long line sets the window's minimum width."""
    for label in window.findChildren(QLabel):
        if len(label.text()) > limit:
            label.setWordWrap(True)


def fit_to_screen(window, width, height, margin=60):
    """Size the window to the default, but never larger than the screen it opens on."""
    screen = QApplication.primaryScreen()
    if screen is None:
        window.resize(width, height)
        return
    available = screen.availableGeometry()
    window.resize(min(width, available.width() - margin), min(height, available.height() - margin))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'TunerToolPro {__version__}')
        fit_to_screen(self, 1200, 820)
        tabs = QTabWidget()
        shift = ShiftTab()
        vehicle_tab = VehicleTab(shift_inputs=shift.inputs_or_none, on_saved=shift.take_vehicle)
        self.ai_tab = AiTab(SettingsBridge(shift, vehicle_tab), context_provider=lambda: tables_context(shift))
        pages = [('Shift Points', shift), ('Vehicle', vehicle_tab), ('Pressure & Timing', PressureTab()),
                 ('Dyno & Drag', DynoDragTab()), ('Datalog', LogTab()), ('XDF / BIN', XdfTab()),
                 ('BCT Tunes', BctTab()), ('AI Assistant', self.ai_tab)]
        for title, page in pages:
            tabs.addTab(scrollable(page), title)
        self.setCentralWidget(tabs)
        wrap_long_labels(self)
        self.statusBar().addPermanentWidget(QLabel('Read the user guide before use'))
        about = self.menuBar().addMenu('Help').addAction('About / Disclaimer')
        about.triggered.connect(self.show_about)

    def closeEvent(self, event):
        self.ai_tab.shutdown()
        super().closeEvent(event)

    def show_about(self):
        QMessageBox.information(self, 'About TunerToolPro',
                                f'TunerToolPro {__version__}\n\n{DISCLAIMER}')


def run(argv=None):
    app = QApplication(sys.argv if argv is None else argv)
    app.setApplicationName('TunerToolPro')
    theme.apply(app)
    window = MainWindow()
    window.show()
    return app.exec()
