"""Shift Points tab: edit a profile, calculate upshift, downshift and TCC tables, export TPS x Gear."""

from PyQt6.QtWidgets import (QComboBox, QDoubleSpinBox, QFileDialog,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QPlainTextEdit, QPushButton, QSpinBox,
                             QTabWidget, QVBoxLayout, QWidget)

from .. import converter, core, settings, trans_data, vehicles
from ..bct.shift_cfg import shift_cfg_from_btc
from ..engines import constants
from ..bct.tune import BtcTune
from .theme import icon
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
        load_btn = QPushButton(icon(self, 'reload'), 'Reload profile')
        btc_btn = QPushButton(icon(self, 'open'), 'Load .BTC tune...')
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
        row += 1
        self.converter_box = QComboBox()
        self.converter_box.addItems([converter.label(k) for k in converter.type_keys()])
        self.converter_box.setToolTip('Choose the converter fitted. The stall, idle, shift RPM and minimum lock RPM '
                                      'move to match. Type the converter\'s true flash stall in Stall RPM first '
                                      'if you know it.')
        grid.addWidget(QLabel('Torque converter'), row, 0)
        grid.addWidget(self.converter_box, row, 1)
        self.diff_box = QComboBox()
        self.diff_box.setToolTip('Common differential ratios. The Axle ratio box above is set to the one you pick.')
        grid.addWidget(QLabel('Differential presets'), row, 2)
        grid.addWidget(self.diff_box, row, 3)
        row += 1
        self.advice = QPlainTextEdit()
        self.advice.setReadOnly(True)
        self.advice.setMaximumHeight(130)
        self.advice.setPlaceholderText('Converter and differential notes appear here.')
        grid.addWidget(self.advice, row, 0, 1, 4)
        self._base = None
        self.converter_box.currentIndexChanged.connect(lambda _: self._converter_changed())
        self.diff_box.activated.connect(lambda _: self._diff_picked())
        self._widgets['axle'].valueChanged.connect(lambda _: self._axle_edited())

        buttons = QHBoxLayout()
        calc_btn = QPushButton(icon(self, 'calculate'), 'Calculate')
        export_btn = QPushButton(icon(self, 'export'), 'Export TPS x Gear...')
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

        car = QHBoxLayout()
        self.make_box = QComboBox()
        self.make_box.addItems(vehicles.MAKES)
        self.trans_box = QComboBox()
        use_btn = QPushButton('Use this transmission')
        use_btn.setToolTip('Load the gear ratios and the transmission\'s own shift delays, lead and converter-lock rules.')
        car.addWidget(QLabel('Make'))
        car.addWidget(self.make_box, 1)
        car.addWidget(QLabel('Transmission'))
        car.addWidget(self.trans_box, 3)
        car.addWidget(use_btn)
        self.car_note = QLabel()
        self.car_note.setWordWrap(True)
        self._delays = None   # (prep, react) per shift for the chosen transmission; None = default
        self.make_box.currentIndexChanged.connect(lambda _: self._fill_transmissions())
        self.trans_box.currentIndexChanged.connect(lambda _: self._show_transmission())
        use_btn.clicked.connect(self.apply_transmission)
        self._fill_transmissions(initial=True)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addLayout(car)
        layout.addWidget(self.car_note)
        layout.addWidget(form_box)
        layout.addWidget(self.btc_label)
        self.calc_note = QLabel()
        self.calc_note.setWordWrap(True)
        layout.addWidget(self.calc_note)
        layout.addLayout(buttons)
        layout.addWidget(self.results, 1)
        self._tables_data = None

    def widgets(self):
        """The numeric inputs by name, for the AI's bounds and proposals."""
        return dict(self._widgets)

    def value(self, key):
        return self._widgets[key].value()

    def set_value(self, key, value):
        """Set one numeric input. Returns False if the name is not an input on this tab."""
        widget = self._widgets.get(key)
        if widget is None:
            return False
        if isinstance(widget, QSpinBox):
            widget.setValue(int(round(value)))
        else:
            widget.setValue(float(value))
        return True

    def inputs_or_none(self):
        """The calculation inputs, or None when the ratios cannot be read."""
        try:
            return self.build_cfg()
        except (ValueError, KeyError):
            return None

    def take_vehicle(self, profile):
        """Copy the tire, final drive and weight from the Vehicle tab. A value of zero means not set, so it is skipped."""
        if profile.tire_dia:
            self.set_value('tire_dia', profile.tire_dia)
        if profile.final_drive:
            self.set_value('axle', profile.final_drive)
        if profile.weight_lb:
            self.set_value('weight', profile.weight_lb)

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
        found = vehicles.find(constants.STARTER_PROFILES[self.profile_box.currentText()]['trans_name'])
        self._delays = trans_data.for_transmission(found).delays if found else None
        self.btc_label.setText('')
        self._engine_changed()
        self._reset_converter()

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
        self._reset_converter(guess=True)

    # --- car and transmission -------------------------------------------------------------------

    def _choice_path(self):
        return settings.user_dir() / 'vehicle.json'

    def _fill_transmissions(self, initial=False):
        """List the automatics for the chosen make. The first run restores the last choice."""
        if initial:
            saved = vehicles.load(self._choice_path())
            self.make_box.blockSignals(True)
            self.make_box.setCurrentText(saved['make'])
            self.make_box.blockSignals(False)
        listed = vehicles.transmissions(self.make_box.currentText())
        self.trans_box.blockSignals(True)
        self.trans_box.clear()
        self.trans_box.addItems([t.name for t in listed])
        if initial and saved['transmission'] in [t.name for t in listed]:
            self.trans_box.setCurrentText(saved['transmission'])
        self.trans_box.blockSignals(False)
        self._show_transmission()

    def _show_transmission(self):
        found = vehicles.find(self.trans_box.currentText())
        if not found:
            self.car_note.setText('')
            return
        state = 'Gear ratios checked against the shared tuning data.' if found.verified else found.note
        self.car_note.setText(f'{len(found.ratios)} gears, {found.drive}. Ratios {vehicles.ratios_text(found)}. {state}\n'
                              + trans_data.summary(trans_data.for_transmission(found)))

    def apply_transmission(self):
        """Load the gear ratios and the transmission's own data (delays, lead, converter-lock rules)."""
        found = vehicles.find(self.trans_box.currentText())
        if not found:
            return
        data = trans_data.for_transmission(found)
        current = {k: str(w.value()) for k, w in self._widgets.items()}
        applied = trans_data.apply(vehicles.fit_gears(current, len(found.ratios)), data)
        for key in ('min_tcc_rpm', 'min_tcc_gear', 'accel_lock_gear', 'wot_lock_gear', 'lead_value'):
            self.set_value(key, float(applied[key]))
        self.ratios.setText(vehicles.ratios_text(found))
        self.lead_box.setCurrentText(data.lead_mode)
        self._delays = data.delays
        self._tables_data = None
        self._reset_converter()
        try:
            self._choice_path().parent.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
        vehicles.save(self._choice_path(), {'make': self.make_box.currentText(), 'transmission': found.name,
                                            'profile': self.profile_box.currentText()})
        self._show_transmission()

    # --- converter and differential -------------------------------------------------------------

    CONVERTER_FIELDS = ('stall_rpm', 'idle_rpm', 'shift_rpm', 'min_tcc_rpm')

    def _reset_converter(self, guess=False):
        """The form now holds stock-converter numbers (or a loaded tune's). Remember them as the base."""
        self._base = {k: self._widgets[k].value() for k in self.CONVERTER_FIELDS}
        key = 'stock'
        if guess:
            key = converter.classify(self._base['stall_rpm'], 2000)
        self.converter_box.blockSignals(True)
        self.converter_box.setCurrentText(converter.label(key))
        self.converter_box.blockSignals(False)
        self._fill_diff_box()
        self._show_notes([], converter.tcm_advice(key) if key != 'stock' else [])

    def _fill_diff_box(self):
        axle = self._widgets['axle'].value()
        self.diff_box.blockSignals(True)
        self.diff_box.clear()
        options = converter.diff_options(axle)
        self.diff_box.addItems([f'{r:g}' for r in options])
        nearest = min(range(len(options)), key=lambda i: abs(options[i] - axle))
        self.diff_box.setCurrentIndex(nearest)
        self.diff_box.blockSignals(False)

    def _show_notes(self, calc_notes, advice):
        lines = list(calc_notes)
        if advice:
            lines.append('Set these in the TCM tune (the app cannot calculate them):')
            lines.extend('  ' + a for a in advice)
        try:
            cfg = self.build_cfg()
            _, diff_lines = converter.diff_effect(cfg['ratios'], cfg['axle'], cfg['tire_dia'],
                                                  cfg['shift_rpm'], cfg['chain'])
            lines.extend(diff_lines)
        except (ValueError, KeyError, ZeroDivisionError):
            pass
        self.advice.setPlainText('\n'.join(lines))

    def _converter_changed(self):
        key = converter.key_for_label(self.converter_box.currentText())
        base = self._base or {k: self._widgets[k].value() for k in self.CONVERTER_FIELDS}
        typed = self._widgets['stall_rpm'].value()
        # A stall figure typed over the base is the user's own number for this converter.
        stall = typed if abs(typed - base['stall_rpm']) > 1 and key != 'stock' else None
        changes, stall_logic, notes = converter.adjust(self._current_for(base), key, stall_rpm=stall,
                                                       base=base, n_gears=self._gear_count())
        for name, value in changes.items():
            self.set_value(name, value)
        self.stall_logic.setCurrentIndex(1 if stall_logic else 0)
        self._tables_data = None
        self._show_notes(notes, converter.tcm_advice(key))

    def _current_for(self, base):
        return {k: self._widgets[k].value() for k in self.CONVERTER_FIELDS}

    def _gear_count(self):
        try:
            return len([r for r in self.ratios.text().replace(' ', '').split(',') if r])
        except ValueError:
            return 6

    def _diff_picked(self):
        old = self._widgets['axle'].value()
        new = float(self.diff_box.currentText())
        self.set_value('axle', new)
        try:
            cfg = self.build_cfg()
            lines = converter.diff_change(cfg['ratios'], old, new, cfg['tire_dia'], cfg['shift_rpm'], cfg['chain'])
        except (ValueError, KeyError, ZeroDivisionError):
            lines = []
        self._tables_data = None
        self.advice.setPlainText('\n'.join(lines))

    def _axle_edited(self):
        if self.diff_box.count():
            self._fill_diff_box()

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
        if self._delays:
            pairs = [(float(p), float(r)) for p, r in self._delays]
            cfg['delays'] = [pairs[min(g, len(pairs) - 1)] for g in range(n)]   # one per gear, last repeats
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
