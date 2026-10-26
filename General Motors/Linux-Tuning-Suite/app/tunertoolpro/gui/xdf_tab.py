"""XDF/BIN tab: browse XDF definitions and read values from a calibration .bin."""

from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget,
                             QMessageBox, QPushButton, QVBoxLayout, QWidget, QSplitter)

from ..engines.bin_reader import BinReader
from ..engines.xdf import XDFDefinition
from .widgets import fill_grid, fill_pairs, make_read_only_table


class XdfTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.xdf = None
        self.reader = BinReader(b'')
        self._shown = []
        self.open_xdf_btn = QPushButton('Open XDF...')
        self.open_bin_btn = QPushButton('Open BIN...')
        self.status = QLabel('Open an XDF definition, then a BIN calibration file.')
        self.search = QLineEdit()
        self.search.setPlaceholderText('Filter parameters (e.g. shift, TCC, pressure)')
        self.params = QListWidget()
        self.detail = QLabel('Select a parameter.')
        self.detail.setWordWrap(True)
        self.values = make_read_only_table()

        header = QHBoxLayout()
        header.addWidget(self.open_xdf_btn)
        header.addWidget(self.open_bin_btn)
        header.addWidget(self.search, 1)

        right = QVBoxLayout()
        right.addWidget(self.detail)
        right.addWidget(self.values, 1)
        right_host = QWidget()
        right_host.setLayout(right)

        splitter = QSplitter()
        splitter.addWidget(self.params)
        splitter.addWidget(right_host)
        splitter.setStretchFactor(1, 2)

        layout = QVBoxLayout(self)
        layout.addLayout(header)
        layout.addWidget(self.status)
        layout.addWidget(splitter, 1)

        self.open_xdf_btn.clicked.connect(self.open_xdf)
        self.open_bin_btn.clicked.connect(self.open_bin)
        self.search.textChanged.connect(self.refresh_list)
        self.params.currentRowChanged.connect(self.show_selected)

    def open_xdf(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open XDF', '', 'XDF files (*.xdf)')
        if not path:
            return
        try:
            self.xdf = XDFDefinition.from_file(path)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, 'Could not read XDF', str(exc))
            return
        self.reader.attach_xdf(self.xdf)
        self.status.setText(f'{self.xdf.title or path}: {len(self.xdf.parameters)} parameters')
        self.refresh_list()

    def open_bin(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open BIN', '', 'Calibration files (*.bin)')
        if not path:
            return
        try:
            self.reader = BinReader.from_file(path, self.xdf)
        except OSError as exc:
            QMessageBox.warning(self, 'Could not read BIN', str(exc))
            return
        self.status.setText(self.reader.info().replace('\n', '   '))
        self.show_selected(self.params.currentRow())

    def refresh_list(self):
        if self.xdf is None:
            return
        needle = self.search.text().strip().lower()
        self._shown = [p for p in self.xdf.parameters if needle in p.title.lower()][:2000]
        self.params.clear()
        self.params.addItems([f'{p.title}  [{p.kind}]' for p in self._shown])

    def show_selected(self, row):
        if row is None or row < 0 or row >= len(self._shown):
            return
        param = self._shown[row]
        self.detail.setText(f'{param.title}\nCategory: {param.category or "—"}   '
                            f'Units: {param.units or "—"}\n{param.description}')
        if not self.reader.data:
            self.values.clear()
            self.values.setRowCount(0)
            self.values.setColumnCount(0)
            return
        try:
            value = param.read(self.reader.data)
        except (IndexError, ValueError) as exc:
            QMessageBox.warning(self, 'Read failed', str(exc))
            return
        if isinstance(value, dict):
            z = value.get('z', [])
            cols = value.get('x_breakpoints', list(range(len(z[0]) if z else 0)))
            rows = value.get('y_breakpoints', list(range(len(z))))
            fill_grid(self.values, [f'{r:g}' for r in rows], [f'{c:g}' for c in cols], z,
                      '{:.2f}')
        else:
            fill_pairs(self.values, [('Value', value)], '{:.3f}')
