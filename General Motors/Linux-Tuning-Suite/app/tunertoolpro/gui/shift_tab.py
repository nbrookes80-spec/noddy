"""Shift Points tab: edit a profile, calculate upshift, downshift and TCC tables, export TPS x Gear."""

from PyQt6.QtWidgets import (QComboBox, QDoubleSpinBox, QFileDialog,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QPushButton, QSpinBox, QTabWidget, QVBoxLayout,
                             QWidget)

from .. import core
from ..bct.shift_cfg import shift_cfg_from_btc
from ..bct.tune import BtcTune
from .widgets import fill_grid, make_read_only_table

# (cfg key, label, minimum, maximum, step, decimals)
FIELDS = [
    ('tire_dia', 'Tire diameter (in)', 20.0, 40.0, 0.1, 2),
    ('axle', 'Axle ratio', 1.5, 6.0, 0.01, 2),
    ('chain', 'Transfer / chain ratio', 0.5, 3.0, 0.01, 2),
    ('weight', 'Weight (lb)', 1500, 8000, 10, 0),
    ('rwhp', 'Rear-wheel HP', 50, 2000, 5, 0),
    ('idle_rpm', 'Idle RPM', 400, 1200, 10, 0),
    ('stall_rpm', 'Stall RPM', 1000, 4500, 10, 0),
    ('shift_rpm', 'Shift RPM (WOT)', 3000, 9000, 50, 0),
    ('downshift_rpm', 'Downshift RPM', 1000, 9900, 50, 0),
    ('min_tcc_rpm', 'Minimum TCC RPM', 800, 3000, 10, 0),
    ('min_tcc_gear', 'Minimum TCC gear', 1, 10, 1, 0),
    ('accel_lock_gear', 'Accelerator-lock gear', 1, 10, 1, 0),
    ('wot_lock_gear', 'WOT-lock gear', 1, 10, 1, 0),
    ('tps_offset', 'TPS offset (%)', -20, 50, 1, 1),
    ('tps_factor', 'TPS factor', 0.5, 4.0, 0.05, 2),
    ('up_firmness', 'Upshift firmness', 0.0, 10.0, 0.5, 1),
    ('down_firmness', 'Downshift firmness', 0.0, 10.0, 0.5, 1),
    ('spread_up', 'Upshift spread (mph)', 0.5, 15.0, 0.5, 2),
    ('spread_lock', 'Lock spread (mph)', 0.5, 10.0, 0.5, 2),
    ('spread_lock_up', 'Lock-up spread (mph)', 0.5, 10.0, 0.5, 2),
    ('spread_unlock_dn', 'Unlock spread (mph)', 0.5, 10.0, 0.5, 2),
    ('lead_value', 'Lead value', 0.0, 8.0, 0.25, 2),
    ('down_time', 'Downshift time (s)', 0.0, 2.0, 0.05, 2),
]
INTEGER_FIELDS = {'idle_rpm', 'stall_rpm', 'shift_rpm', 'downshift_rpm', 'min_tcc_rpm', 'weight',
                  'rwhp', 'min_tcc_gear', 'accel_lock_gear', 'wot_lock_gear'}


class ShiftTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgets = {}
        self._build()
        self.profile_box.setCurrentIndex(0)
        self.load_profile()

    def _build(self):
        top = QHBoxLayout()
        self.profile_box = QComboBox()
        self.profile_box.addItems(core.profile_names())
        self.intent_box = QComboBox()
        self.intent_box.addItems([core.CUSTOM_INTENT] + core.intent_names())
        self.lead_box = QComboBox()
        self.lead_box.addItems(['rpm', 'torque'])
        self.stall_logic = QComboBox()
        self.stall_logic.addItems(['Off', 'On'])
        self.engine_box = QComboBox()
        self.engine_box.addItems([core.ENGINE_CALC, core.ENGINE_BC])
        load_btn = QPushButton('Reload profile')
        btc_btn = QPushButton('Load .BTC tune...')
        top.addWidget(QLabel('Profile'))
        top.addWidget(self.profile_box, 2)
        top.addWidget(QLabel('Intent'))
        top.addWidget(self.intent_box, 1)
        top.addWidget(QLabel('Engine'))
        top.addWidget(self.engine_box, 2)
        top.addWidget(load_btn)
        top.addWidget(btc_btn)
        self.profile_box.currentIndexChanged.connect(lambda _: self.load_profile())
        load_btn.clicked.connect(self.load_profile)
        btc_btn.clicked.connect(self.load_btc)
        self.engine_box.currentIndexChanged.connect(lambda _: self._engine_changed())
        self.btc_label = QLabel()
        self.btc_label.setWordWrap(True)
        self._btc = None   # per-shift data from a loaded tune; None when no tune is loaded
        self._tune = None  # the parsed BtcTune, needed by the BC Trans engine

        self.form_box = QGroupBox('Vehicle and calibration')
        form_box = self.form_box
        grid = QGridLayout(form_box)
        half = (len(FIELDS) + 1) // 2
        for i, (key, label, lo, hi, step, decimals) in enumerate(FIELDS):
            if key in INTEGER_FIELDS:
                widget = QSpinBox()
                widget.setRange(int(lo), int(hi))
                widget.setSingleStep(int(step))
            else:
                widget = QDoubleSpinBox()
                widget.setRange(lo, hi)
                widget.setSingleStep(step)
                widget.setDecimals(decimals)
            self._widgets[key] = widget
            col = 0 if i < half else 2
            row = i if i < half else i - half
            grid.addWidget(QLabel(label), row, col)
            grid.addWidget(widget, row, col + 1)
        row = half
        grid.addWidget(QLabel('Ratios (1st to top, comma-separated)'), row, 0)
        self.ratios = QLineEdit()
        grid.addWidget(self.ratios, row, 1, 1, 3)
        row += 1
        grid.addWidget(QLabel('Lead mode'), row, 0)
        grid.addWidget(self.lead_box, row, 1)
        grid.addWidget(QLabel('Stall-based lock floor'), row, 2)
        grid.addWidget(self.stall_logic, row, 3)

        buttons = QHBoxLayout()
        calc_btn = QPushButton('Calculate')
        export_btn = QPushButton('Export TPS x Gear...')
        buttons.addStretch(1)
        buttons.addWidget(calc_btn)
        buttons.addWidget(export_btn)
        calc_btn.clicked.connect(self.calculate)
        export_btn.clicked.connect(self.export)
        self.intent_box.currentIndexChanged.connect(lambda _: self.load_profile())

        self.results = QTabWidget()
        self.tables = {}
        for key, title in [('upshift', 'Upshift MPH'), ('downshift', 'Downshift MPH'),
                           ('tcc_unlock', 'TCC unlock MPH'), ('tcc_lock', 'TCC lock MPH')]:
            table = make_read_only_table()
            self.tables[key] = table
            self.results.addTab(table, title)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(form_box)
        layout.addWidget(self.btc_label)
        self.calc_note = QLabel()
        self.calc_note.setWordWrap(True)
        layout.addWidget(self.calc_note)
        layout.addLayout(buttons)
        layout.addWidget(self.results, 1)
        self._tables_data = None

    def load_profile(self):
        """Fill the form from the chosen profile and intent."""
        cfg = core.shift_cfg_from_profile(self.profile_box.currentText(),
                                          self.intent_box.currentText())
        for key, widget in self._widgets.items():
            if key in cfg:
                widget.setValue(int(cfg[key]) if key in INTEGER_FIELDS else float(cfg[key]))
        self.ratios.setText(', '.join(f'{r:g}' for r in cfg['ratios']))
        self.lead_box.setCurrentText('torque' if cfg['lead_mode'] != 'rpm' else 'rpm')
        self.stall_logic.setCurrentIndex(0)
        self._btc = None
        self._tune = None
        self.btc_label.setText('')
        self._engine_changed()

    def load_btc(self):
        """Fill the form from a Bluecat .BTC tune. The intent is set to Custom so no clamp applies."""
        path, _ = QFileDialog.getOpenFileName(self, 'Open BC Trans tune', '',
                                              'BC Trans tunes (*.BTC *.btc);;All files (*)')
        if not path:
            return
        try:
            tune = BtcTune.load(path)
            cfg = shift_cfg_from_btc(tune)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, 'Cannot load tune', str(exc))
            return
        self.intent_box.setCurrentText(core.CUSTOM_INTENT)  # runs load_profile, which clears _btc
        clipped = []
        for key, widget in self._widgets.items():
            value = cfg[key]
            widget.setValue(int(value) if key in INTEGER_FIELDS else float(value))
            if abs(widget.value() - value) > 1e-6:
                clipped.append(key)
        self.ratios.setText(', '.join(f'{r:g}' for r in cfg['ratios']))
        self.lead_box.setCurrentText(cfg['lead_mode'])
        self.stall_logic.setCurrentIndex(1 if cfg['stall_lock_logic'] else 0)
        self._btc = {'delays': cfg['delays'], 'per_gear_rpm': cfg['per_gear_rpm']}
        self._tune = tune
        note = f'Loaded {path.rsplit("/", 1)[-1]}: {len(cfg["ratios"])} gears. Lead mode: {cfg["lead_mode"]}.'
        if clipped:
            note += ' Outside the form range, so the form shows the nearest value: ' + ', '.join(clipped) + '.'
        self.btc_label.setText(note)
        self._engine_changed()

    def _engine_changed(self):
        """BC Trans runs on the loaded tune as written, so the form is read-only in that mode."""
        bc = self.engine_box.currentText() == core.ENGINE_BC
        self.form_box.setEnabled(not bc)
        self.calc_note.setText(
            'BC Trans engine: the tables come from the loaded .BTC tune as written. '
            'The form is disabled; change the tune file to change the result.'
            if bc else '')
        self._tables_data = None

    def build_cfg(self):
        cfg = {}
        for key, widget in self._widgets.items():
            cfg[key] = widget.value()
        cfg['ratios'] = [float(x) for x in self.ratios.text().replace(' ', '').split(',') if x]
        if len(cfg['ratios']) < 2:
            raise ValueError('enter at least two gear ratios')
        n = len(cfg['ratios'])
        cfg['lead_mode'] = self.lead_box.currentText()
        cfg['lead_value'] = float(self._widgets['lead_value'].value())
        cfg['delays'] = [core.DEFAULT_DELAY] * n
        cfg['stall_lock_logic'] = self.stall_logic.currentIndex() == 1
        if self._btc is not None:
            # Per-shift delays and RPMs from the tune. A shorter list keeps its last entry.
            delays = self._btc['delays']
            cfg['delays'] = [delays[min(g, len(delays) - 1)] for g in range(n)]
            if len(self._btc['per_gear_rpm']) == n:
                cfg['per_gear_rpm'] = list(self._btc['per_gear_rpm'])
        return cfg

    def calculate(self):
        self.calc_note.setText('')
        if self.engine_box.currentText() == core.ENGINE_BC:
            if self._tune is None:
                QMessageBox.warning(self, 'Cannot calculate',
                                    'The BC Trans engine needs a .BTC tune. Load one first.')
                return
            try:
                tables = core.bc_shift_tables(self._tune)
            except (ValueError, KeyError, ZeroDivisionError) as exc:
                QMessageBox.warning(self, 'Cannot calculate', str(exc))
                return
            if tables['logic_error']:
                self.calc_note.setText(
                    f'BC Trans reports a logic error: {tables["logic_error"]} cells still changing '
                    f'after {tables["iterations"]} passes. The tables are shown as BC Trans leaves them.')
            else:
                self.calc_note.setText(
                    f'BC Trans Calc_Shifts converged in {tables["iterations"]} pass(es). '
                    'Disabled TCC cells show BC Trans markers (318/317, or 255/254 on 4 gears).')
        else:
            try:
                cfg = self.build_cfg()
                tables = core.calc_shift_tables(cfg)
            except (ValueError, ZeroDivisionError, KeyError) as exc:
                QMessageBox.warning(self, 'Cannot calculate', str(exc))
                return
        self._tables_data = tables
        tps = [f'{v:g}%' for v in core.tps_axis()]
        shifts = [f'{g + 1}-{g + 2}' for g in range(len(tables['upshift']))]
        gears = [f'Gear {g + 1}' for g in range(tables['n_gears'])]
        fill_grid(self.tables['upshift'], shifts, tps, tables['upshift'], '{:.1f}')
        fill_grid(self.tables['downshift'], shifts, tps, tables['downshift'], '{:.1f}')
        fill_grid(self.tables['tcc_unlock'], gears, tps, tables['tcc_unlock'], '{:.1f}')
        fill_grid(self.tables['tcc_lock'], gears, tps, tables['tcc_lock'], '{:.1f}')

    def export(self):
        if self._tables_data is None:
            self.calculate()
            if self._tables_data is None:
                return
        path, _ = QFileDialog.getSaveFileName(self, 'Save TPS x Gear matrices', 'tps_gear.txt',
                                              'Text files (*.txt)')
        if not path:
            return
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(core.tps_gear_text(self._tables_data))
