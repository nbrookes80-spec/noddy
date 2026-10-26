"""Datalog tab: import a CSV datalog, list detected columns, summarise shifts, stall and WOT slip."""

from PyQt6.QtWidgets import (QComboBox, QFileDialog, QHBoxLayout, QLabel, QMessageBox,
                             QProgressBar, QPushButton, QVBoxLayout, QWidget)

from .. import core
from .widgets import fill_grid, fill_pairs, make_read_only_table


class LogTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.imp = None
        self.open_btn = QPushButton('Open datalog CSV...')
        self.profile_box = QComboBox()
        self.profile_box.addItems(core.profile_names())
        self.analyze_btn = QPushButton('Analyze')
        self.analyze_btn.setEnabled(False)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.file_label = QLabel('No log loaded. Use a CSV exported from your scan tool.')
        self.columns = make_read_only_table()
        self.summary = make_read_only_table()
        self.shifts = make_read_only_table()
        self.warnings = QLabel()
        self.warnings.setWordWrap(True)

        top = QHBoxLayout()
        top.addWidget(self.open_btn)
        top.addWidget(QLabel('Ratios and tire from'))
        top.addWidget(self.profile_box, 2)
        top.addWidget(self.analyze_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.file_label)
        layout.addWidget(self.progress)
        layout.addWidget(QLabel('Detected columns'))
        layout.addWidget(self.columns)
        layout.addWidget(QLabel('Analysis'))
        layout.addWidget(self.summary)
        layout.addWidget(QLabel('Shift events (TPS over 70%)'))
        layout.addWidget(self.shifts, 1)
        layout.addWidget(self.warnings)

        self.open_btn.clicked.connect(self.open_log)
        self.analyze_btn.clicked.connect(self.analyze)

    def _progress(self, value):
        self.progress.setValue(int(value))

    def open_log(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open datalog', '', 'CSV files (*.csv)')
        if not path:
            return
        self.progress.setValue(0)
        try:
            self.imp, _ = core.analyze_log(path, cfg=None, progress_cb=self._progress)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, 'Could not read log', str(exc))
            self.imp = None
            return
        self.file_label.setText(f'{path}: {self.imp.n_samples} samples')
        detected = self.imp.detected_columns()
        fill_grid(self.columns, [key for key, _ in detected], ['Source header'],
                  [[header] for _, header in detected])
        self.analyze_btn.setEnabled(not self.imp.is_empty)
        self.analyze()

    def analyze(self):
        if self.imp is None:
            return
        cfg = core.shift_cfg_from_profile(self.profile_box.currentText())
        result = self.imp.analyze(cfg)
        pairs = [
            ('Samples', result['n_samples']),
            ('Stall peak RPM', _fmt(result['stall_peak_rpm'], '{:.0f}')),
            ('WOT slip (%)', _fmt(result['wot_slip_pct'], '{:.2f}')),
            ('Trans temp range', _range(result['temp_range'])),
        ]
        fill_pairs(self.summary, pairs)
        events = result['shift_events']
        fill_grid(self.shifts, [str(i + 1) for i in range(len(events))],
                  ['From', 'To', 'MPH', 'RPM', 'TPS %'],
                  [[e['gear_from'], e['gear_to'], e['mph'], e['rpm'], e['tps']] for e in events],
                  '{:.1f}')
        self.warnings.setText('\n'.join(result['warnings']))


def _fmt(value, pattern):
    return '—' if value is None else pattern.format(value)


def _range(value):
    if value is None:
        return '—'
    return f'{value[0]:.0f} – {value[1]:.0f} (units as logged)'
