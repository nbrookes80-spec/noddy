"""Pressure & Timing tab: pressure tables, 4-speed shift times and TCC duty maximums."""

from PyQt6.QtWidgets import (QComboBox, QDoubleSpinBox, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout, QWidget)

from .. import core
from ..engines import constants as C
from .widgets import fill_grid, make_read_only_table


def _intents_for(kind):
    if kind == 'Shift time 4-speed':
        return list(C.SHIFT_TIME_INTENTS_4SPD)
    if kind == 'TCC duty maximum':
        return ['(no intent)']
    if kind == 'Base shift pressure 4-speed':
        return list(C.PRESSURE_INTENTS_4SPD)
    if kind == 'TCC apply ramp':
        return list(C.TCC_APPLY_INTENTS)
    return list(C.PRESSURE_INTENTS)


TORQUE_KINDS = ('Base shift pressure', 'TCC apply pressure', 'Coast pressure')


class PressureTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.kind_box = QComboBox()
        self.kind_box.addItems(core.PRESSURE_KINDS)
        self.intent_box = QComboBox()
        self.torque = QDoubleSpinBox()
        self.torque.setRange(50, 1000)
        self.torque.setValue(640)
        self.torque.setSuffix(' lb-ft')
        self.max_psi = QDoubleSpinBox()
        self.max_psi.setRange(50, 400)
        self.max_psi.setValue(C.MAX_PRESSURE_PSI)
        self.max_psi.setSuffix(' psi cap')
        self.era_box = QComboBox()
        self.era_box.addItems(list(C.TCC_RAMP_ERAS))
        self.unit_label = QLabel()
        self.table = make_read_only_table()

        top = QHBoxLayout()
        top.addWidget(QLabel('Table'))
        top.addWidget(self.kind_box, 2)
        top.addWidget(QLabel('Intent'))
        top.addWidget(self.intent_box, 2)
        top.addWidget(QLabel('Max torque'))
        top.addWidget(self.torque)
        top.addWidget(self.max_psi)
        show = QPushButton('Show')
        top.addWidget(QLabel('Model years'))
        top.addWidget(self.era_box)
        top.addWidget(show)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.unit_label)
        layout.addWidget(self.table, 1)

        self.kind_box.currentIndexChanged.connect(self._reload_intents)
        self.intent_box.currentIndexChanged.connect(lambda _: self.show_table())
        self.era_box.currentIndexChanged.connect(lambda _: self.show_table())
        show.clicked.connect(self.show_table)
        self._reload_intents()

    def _reload_intents(self):
        kind = self.kind_box.currentText()
        self.intent_box.blockSignals(True)
        self.intent_box.clear()
        self.intent_box.addItems(_intents_for(kind))
        self.intent_box.blockSignals(False)
        # The original's TCC ramp does not read max torque, so those inputs are off for it.
        self.torque.setEnabled(kind in TORQUE_KINDS)
        self.max_psi.setEnabled(kind in TORQUE_KINDS)
        self.era_box.setEnabled(kind == 'TCC apply ramp')
        self.show_table()

    def show_table(self):
        kind = self.kind_box.currentText()
        intent = self.intent_box.currentText()
        rows, cols, data, unit = core.pressure_table(kind, intent, self.torque.value(),
                                                     self.max_psi.value(),
                                                     era=self.era_box.currentText())
        fmt = '{:.1f}' if unit == 'psi' else '{:.2f}'
        fill_grid(self.table, rows, cols, data, fmt)
        self.unit_label.setText(f'{kind} ({unit}). Rows and columns are the table axes.')
        self.table.setToolTip('Slip values use the table units from the original.')
