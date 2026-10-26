"""Main window: one tab per tool. Every tab is independent; they share no state."""

import sys

from PyQt6.QtWidgets import (QApplication, QLabel, QMainWindow, QMessageBox, QTabWidget)

from .. import __version__
from .bct_tab import BctTab
from .dyno_tab import DynoDragTab
from .log_tab import LogTab
from .pressure_tab import PressureTab
from .shift_tab import ShiftTab
from .xdf_tab import XdfTab

DISCLAIMER = (
    'TunerToolPro is a calculation aid for transmission calibration. Every value must be '
    'checked against your own vehicle, hardware and a road test before it is written to a '
    'controller. The author and contributors accept no responsibility for damage, warranty '
    'loss or injury from its use.'
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'TunerToolPro {__version__}')
        self.resize(1200, 820)
        tabs = QTabWidget()
        tabs.addTab(ShiftTab(), 'Shift Points')
        tabs.addTab(PressureTab(), 'Pressure & Timing')
        tabs.addTab(DynoDragTab(), 'Dyno & Drag')
        tabs.addTab(LogTab(), 'Datalog')
        tabs.addTab(XdfTab(), 'XDF / BIN')
        tabs.addTab(BctTab(), 'BCT Tunes')
        self.setCentralWidget(tabs)
        self.statusBar().addPermanentWidget(QLabel('Read the user guide before use'))
        about = self.menuBar().addMenu('Help').addAction('About / Disclaimer')
        about.triggered.connect(self.show_about)

    def show_about(self):
        QMessageBox.information(self, 'About TunerToolPro',
                                f'TunerToolPro {__version__}\n\n{DISCLAIMER}')


def run(argv=None):
    app = QApplication(sys.argv if argv is None else argv)
    app.setApplicationName('TunerToolPro')
    window = MainWindow()
    window.show()
    return app.exec()
