"""BCT tab: open and edit .BTC tunes, apply presets, and show shift speeds for a tune."""

from pathlib import Path

from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget, QComboBox, QSplitter)

from ..bct import shiftmath
from ..bct.presets import load_table, transmission_ratios
from ..bct.tune import BtcTune
from .widgets import fill_grid, make_read_only_table

DEFAULT_RPMS = '2000, 3000, 4000, 5000, 5900, 6500'


class BctTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tune = None
        self.trans_presets = []
        self.slope_presets = []
        self.open_btn = QPushButton('Open .BTC tune...')
        self.save_btn = QPushButton('Save')
        self.save_as_btn = QPushButton('Save As...')
        self.presets_btn = QPushButton('Load presets folder...')
        self.trans_box = QComboBox()
        self.slope_box = QComboBox()
        self.apply_trans_btn = QPushButton('Apply transmission preset')
        self.apply_slope_btn = QPushButton('Apply slope preset')
        self.rpm_edit = QLineEdit(DEFAULT_RPMS)
        self.speed_btn = QPushButton('Show speeds')
        self.status = QLabel('Open a .BTC tune. Edits stay in memory until you save.')
        self.keys = QTableWidget()
        self.keys.setColumnCount(2)
        self.keys.setHorizontalHeaderLabels(['Key', 'Value'])
        self.keys.horizontalHeader().setStretchLastSection(True)
        self.speeds = make_read_only_table()

        top = QHBoxLayout()
        for w in (self.open_btn, self.save_btn, self.save_as_btn):
            top.addWidget(w)
        top.addStretch(1)

        presets = QHBoxLayout()
        presets.addWidget(self.presets_btn)
        presets.addWidget(self.trans_box, 2)
        presets.addWidget(self.apply_trans_btn)
        presets.addWidget(self.slope_box, 2)
        presets.addWidget(self.apply_slope_btn)

        speed_row = QHBoxLayout()
        speed_row.addWidget(QLabel('Engine RPM (comma-separated)'))
        speed_row.addWidget(self.rpm_edit, 1)
        speed_row.addWidget(self.speed_btn)

        left = QVBoxLayout()
        left.addWidget(self.keys)
        left_host = QWidget()
        left_host.setLayout(left)
        right = QVBoxLayout()
        right.addLayout(speed_row)
        right.addWidget(self.speeds, 1)
        right_host = QWidget()
        right_host.setLayout(right)
        splitter = QSplitter()
        splitter.addWidget(left_host)
        splitter.addWidget(right_host)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.status)
        layout.addLayout(presets)
        layout.addWidget(splitter, 1)

        self.open_btn.clicked.connect(self.open_tune)
        self.save_btn.clicked.connect(self.save)
        self.save_as_btn.clicked.connect(self.save_as)
        self.presets_btn.clicked.connect(self.load_presets)
        self.apply_trans_btn.clicked.connect(self.apply_trans_preset)
        self.apply_slope_btn.clicked.connect(self.apply_slope_preset)
        self.speed_btn.clicked.connect(self.show_speeds)
        self.keys.itemChanged.connect(self._key_edited)
        self._set_enabled(False)

    def _set_enabled(self, on):
        for w in (self.save_btn, self.save_as_btn, self.speed_btn, self.apply_trans_btn,
                  self.apply_slope_btn):
            w.setEnabled(on)

    def open_tune(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open tune', '', 'BC Trans tunes (*.BTC *.btc)')
        if not path:
            return
        try:
            self.tune = BtcTune.load(path)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, 'Could not read tune', str(exc))
            return
        self._show_keys()
        missing = self.tune.missing_required()
        note = f' Missing: {", ".join(missing)}' if missing else ''
        self.status.setText(f'{path}: {self.tune.gear_count()} gears.{note}')
        self._set_enabled(True)
        self.show_speeds()

    def _show_keys(self):
        self.keys.itemChanged.disconnect(self._key_edited)
        pairs = self.tune.pairs()
        self.keys.setRowCount(len(pairs))
        for r, (k, v) in enumerate(pairs):
            key_item = QTableWidgetItem(k)
            key_item.setFlags(key_item.flags() & ~_editable())
            self.keys.setItem(r, 0, key_item)
            self.keys.setItem(r, 1, QTableWidgetItem(v))
        self.keys.resizeColumnToContents(0)
        self.keys.itemChanged.connect(self._key_edited)

    def _key_edited(self, item):
        if item.column() != 1 or self.tune is None:
            return
        key = self.keys.item(item.row(), 0).text()
        self.tune.set(key, item.text())

    def save(self):
        if self.tune is None or not self.tune.source:
            return self.save_as()
        self.tune.save(self.tune.source)
        self.status.setText(f'Saved {self.tune.source}')

    def save_as(self):
        if self.tune is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, 'Save tune as', '', 'BC Trans tunes (*.BTC)')
        if path:
            self.tune.save(path)
            self.status.setText(f'Saved {path}')

    def load_presets(self):
        folder = QFileDialog.getExistingDirectory(self, 'Folder with Trans_Presets.txt and '
                                                  'Slope_Presets.txt')
        if not folder:
            return
        try:
            self.trans_presets = load_table(Path(folder) / 'Trans_Presets.txt')
            self.slope_presets = load_table(Path(folder) / 'Slope_Presets.txt')
        except OSError as exc:
            QMessageBox.warning(self, 'Could not read presets', str(exc))
            return
        self.trans_box.clear()
        self.trans_box.addItems([r['Name'] for r in self.trans_presets])
        self.slope_box.clear()
        self.slope_box.addItems([r['Name'] for r in self.slope_presets])

    def apply_trans_preset(self):
        if self.tune is None or not self.trans_presets:
            return
        row = self.trans_presets[self.trans_box.currentIndex()]
        ratios = transmission_ratios(row)
        self.tune.set('Gears', _int_text(len(ratios)))
        for i, value in enumerate(ratios, start=1):
            self.tune.set(f'Ratio{i}', _num_text(value))
        for field in ('VSS', 'Lead'):
            if row.get(field) is not None:
                self.tune.set(field, _num_text(row[field]))
        self._show_keys()
        self.show_speeds()

    def apply_slope_preset(self):
        if self.tune is None or not self.slope_presets:
            return
        row = self.slope_presets[self.slope_box.currentIndex()]
        mapping = {'Factor': 'Factor', 'Offset': 'Offset', 'Up': 'UpFactor', 'Down': 'DownFactor'}
        for src, dst in mapping.items():
            if row.get(src) is not None:
                self.tune.set(dst, _num_text(row[src]))
        self._show_keys()

    def show_speeds(self):
        if self.tune is None:
            return
        try:
            rpms = [float(x) for x in self.rpm_edit.text().split(',') if x.strip()]
            table = shiftmath.gear_speed_table(self.tune, rpms)
        except ValueError as exc:
            self.status.setText(f'Speed table: {exc}')
            self.speeds.clear()
            self.speeds.setRowCount(0)
            self.speeds.setColumnCount(0)
            return
        gears = [f'{i} gear' for i in range(1, self.tune.gear_count() + 1)]
        fill_grid(self.speeds, [f'{r:g} RPM' for r in rpms], gears, table, '{:.1f} mph')


def _editable():
    from PyQt6.QtCore import Qt
    return Qt.ItemFlag.ItemIsEditable


def _int_text(n):
    return str(int(n))


def _num_text(value):
    return f'{value:g}'
