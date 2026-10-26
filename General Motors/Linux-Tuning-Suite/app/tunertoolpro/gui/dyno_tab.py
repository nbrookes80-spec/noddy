"""Dyno & Drag tab: torque curve from CSV, boost overlay, launch-to-quarter-mile simulation."""

from PyQt6.QtWidgets import (QComboBox, QDoubleSpinBox, QFileDialog, QGridLayout, QGroupBox,
                             QHBoxLayout, QLabel, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)

from .. import core
from ..engines.torque_curve import TorqueCurve
from .widgets import LineChart, fill_pairs, make_read_only_table


def _spin(lo, hi, value, step=1.0, decimals=0):
    box = QDoubleSpinBox()
    box.setRange(lo, hi)
    box.setValue(value)
    box.setSingleStep(step)
    box.setDecimals(decimals)
    return box


class DynoDragTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.curve = TorqueCurve()
        self._build()
        self.profile_box.setCurrentIndex(0)
        self._reload_profile()

    def _build(self):
        # Dyno inputs
        self.load_btn = QPushButton('Load dyno CSV (rpm, hp, tq)...')
        self.dyno_summary = make_read_only_table()
        self.dyno_chart = LineChart()
        self.spool = _spin(500, 6000, 2500, 50)
        self.peak_psi = _spin(0, 40, 0.0, 0.5, 1)
        self.peak_rpm = _spin(1000, 9000, 4000, 100)
        self.redline_psi = _spin(0, 40, 0.0, 0.5, 1)
        self.torque_per_psi = _spin(0, 30, 7.5, 0.5, 1)
        self.boost_btn = QPushButton('Apply boost to curve')
        self.boost_unit = QLabel('Boost multiplies torque: 1 + PSI x torque-per-PSI % / 100')

        dyno_box = QGroupBox('Dyno curve')
        dyno_layout = QVBoxLayout(dyno_box)
        dyno_layout.addWidget(self.load_btn)
        dyno_layout.addWidget(self.dyno_summary)
        dyno_layout.addWidget(self.dyno_chart, 1)

        boost_box = QGroupBox('Forced induction (optional)')
        grid = QGridLayout(boost_box)
        for row, (label, widget) in enumerate([
                ('Spool RPM', self.spool), ('Peak PSI', self.peak_psi),
                ('Peak RPM', self.peak_rpm), ('Redline PSI', self.redline_psi),
                ('Torque per PSI (%)', self.torque_per_psi)]):
            grid.addWidget(QLabel(label), row, 0)
            grid.addWidget(widget, row, 1)
        grid.addWidget(self.boost_btn, 5, 0, 1, 2)
        grid.addWidget(self.boost_unit, 6, 0, 1, 2)

        # Drag inputs
        self.profile_box = QComboBox()
        self.profile_box.addItems(core.profile_names())
        self.weight = _spin(1500, 8000, 3500, 10)
        self.run_btn = QPushButton('Run drag simulation')
        self.drag_table = make_read_only_table()
        self.drag_chart = LineChart()
        self.shift_table = make_read_only_table()

        drag_box = QGroupBox('Drag simulation')
        drag_layout = QVBoxLayout(drag_box)
        row = QHBoxLayout()
        row.addWidget(QLabel('Profile'))
        row.addWidget(self.profile_box, 2)
        row.addWidget(QLabel('Weight (lb)'))
        row.addWidget(self.weight)
        drag_layout.addLayout(row)
        drag_layout.addWidget(self.run_btn)
        drag_layout.addWidget(self.drag_table)
        drag_layout.addWidget(self.drag_chart, 1)
        drag_layout.addWidget(self.shift_table)

        left = QVBoxLayout()
        left.addWidget(dyno_box, 1)
        left.addWidget(boost_box)
        right = QVBoxLayout()
        right.addWidget(drag_box, 1)
        top = QHBoxLayout(self)
        top.addLayout(left, 1)
        top.addLayout(right, 2)

        self.load_btn.clicked.connect(self.load_dyno)
        self.boost_btn.clicked.connect(self.apply_boost)
        self.run_btn.clicked.connect(self.run_drag)
        self.profile_box.currentIndexChanged.connect(lambda _: self._reload_profile())

    def _reload_profile(self):
        cfg = core.shift_cfg_from_profile(self.profile_box.currentText())
        self.weight.setValue(cfg['weight'])

    def load_dyno(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open dyno CSV', '', 'CSV files (*.csv)')
        if not path:
            return
        try:
            self.curve = core.load_dyno(path)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, 'Could not read dyno file', str(exc))
            return
        self.refresh_dyno()

    def apply_boost(self):
        boost = core.make_boost(self.spool.value(), self.peak_psi.value(), self.peak_rpm.value(),
                                self.redline_psi.value() or None, self.torque_per_psi.value())
        if self.curve.is_empty:
            QMessageBox.information(self, 'No curve', 'Load a dyno CSV first.')
            return
        self.curve = TorqueCurve(self.curve.points, boost_curve=boost)
        self.refresh_dyno()

    def refresh_dyno(self):
        fill_pairs(self.dyno_summary, core.dyno_summary(self.curve))
        if not self.curve.is_empty:
            rpms = [p[0] for p in self.curve.points]
            step = max(1, len(rpms) // 200)
            sample = list(range(0, len(rpms), step))
            xs = [rpms[i] for i in sample]
            hp = [self.curve.hp_at(x) for x in xs]
            tq = [self.curve.tq_at(x) for x in xs]
            self.dyno_chart.set_data(xs, [('HP', hp), ('Torque', tq)], 'RPM')

    def run_drag(self):
        cfg = core.shift_cfg_from_profile(self.profile_box.currentText())
        cfg['weight'] = self.weight.value()
        if self.curve.is_empty:
            QMessageBox.information(self, 'No curve', 'Load a dyno CSV first.')
            return
        boost = self.curve.boost_curve
        result = core.run_drag(cfg, self.curve, boost=boost)
        if result is None:
            QMessageBox.warning(self, 'No result', 'The simulation needs a dyno curve.')
            return
        pairs = [
            ('0-30 mph (s)', _fmt(result.get('t_0_30'))),
            ('0-60 mph (s)', _fmt(result.get('t_0_60'))),
            ('0-100 mph (s)', _fmt(result.get('t_0_100'))),
            ('1/8 mile (s)', _fmt(result.get('t_eighth'))),
            ('1/8 mile speed (mph)', _fmt(result.get('v_eighth'))),
            ('1/4 mile (s)', _fmt(result.get('t_quarter'))),
            ('1/4 mile speed (mph)', _fmt(result.get('v_quarter'))),
            ('Top speed in run (mph)', _fmt(result.get('max_v'))),
        ]
        fill_pairs(self.drag_table, pairs)
        t = result['trace_t']
        self.drag_chart.set_data(t, [('MPH', result['trace_v']),
                                     ('RPM / 100', [r / 100 for r in result['trace_rpm']])],
                                 's')
        events = result['shift_events']
        fill_pairs(self.shift_table, [(e['shift_name'] + f" at {e['t']:.2f} s",
                                       f"{e['mph_init']:.1f} mph, {e['rpm_init']:.0f} RPM")
                                      for e in events] or [('Shifts', 'none')])


def _fmt(value):
    return '—' if value is None else round(float(value), 3)
