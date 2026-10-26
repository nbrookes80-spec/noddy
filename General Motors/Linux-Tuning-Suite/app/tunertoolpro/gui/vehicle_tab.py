"""Vehicle tab: the car, engine, transmission, differential, power and ECU limits.

Tire, final drive and weight are also Shift Points inputs. Save copies them into the Shift Points
tab, and the consistency check reads them from there, because that is what the calculation uses.
Nothing in this tab writes to a vehicle.
"""

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QComboBox, QDoubleSpinBox, QFileDialog, QFormLayout, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPlainTextEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from .. import consistency, efilive_export, vehicle
from .theme import PALETTE, icon

CALIBRATION_TEXT_LIMIT = 8000  # characters of the export summary sent to the AI

LEVEL_TEXT = {'error': 'Error', 'warn': 'Check', 'info': 'Note'}
LEVEL_COLOUR = {'error': PALETTE['bad'], 'warn': PALETTE['warn'], 'info': PALETTE['highlight']}


class VehicleTab(QWidget):
    def __init__(self, shift_inputs=None, on_saved=None, parent=None):
        """shift_inputs() returns the Shift Points inputs as a dict, or None if they cannot be read.
        on_saved(profile) is called after a successful save."""
        super().__init__(parent)
        self._shift_inputs = shift_inputs or (lambda: None)
        self._on_saved = on_saved or (lambda profile: None)
        self.findings = []
        self.calibration = None  # an EFILive export, read from a file the user chose; kept in memory only
        self._build()
        self.load()

    def _spin(self, lo, hi, step=1.0, decimals=0):
        box = QDoubleSpinBox()
        box.setRange(lo, hi)
        box.setSingleStep(step)
        box.setDecimals(decimals)
        box.setSpecialValueText('not set')  # the minimum shows as 'not set'
        return box

    def _build(self):
        vehicle_box = QGroupBox('Vehicle')
        form = QFormLayout(vehicle_box)
        self.car = QLineEdit()
        self.car.setPlaceholderText('e.g. 2014 Camaro SS')
        self.engine = QLineEdit()
        self.engine.setPlaceholderText('e.g. LT1 6.2 V8, supercharged')
        self.transmission = QComboBox()
        self.transmission.addItems(vehicle.transmission_keys())
        self.transmission.currentTextChanged.connect(self._show_transmission)
        self.transmission_note = QLabel()
        self.transmission_note.setWordWrap(True)
        self.transmission_note.setProperty('role', 'muted')
        self.final_drive = self._spin(1.0, 6.0, 0.01, 3)
        self.tire = self._spin(20.0, 40.0, 0.1, 2)
        self.weight = self._spin(0, 10000, 10, 0)
        self.power = self._spin(0, 3000, 5, 0)
        self.torque = self._spin(0, 3000, 5, 0)
        form.addRow('Car', self.car)
        form.addRow('Engine', self.engine)
        form.addRow('Transmission', self.transmission)
        form.addRow('', self.transmission_note)
        form.addRow('Final drive (differential) ratio', self.final_drive)
        form.addRow('Tire diameter (in)', self.tire)
        form.addRow('Weight (lb)', self.weight)
        form.addRow('Engine power (hp)', self.power)
        form.addRow('Engine torque (lb-ft)', self.torque)

        ecu_box = QGroupBox('ECU limits (from the calibration or scan tool)')
        ecu = QFormLayout(ecu_box)
        self.ecu_torque = self._spin(0, 3000, 5, 0)
        self.redline = self._spin(0, 12000, 50, 0)
        ecu.addRow('ECU torque limit (lb-ft)', self.ecu_torque)
        ecu.addRow('Redline (rpm)', self.redline)
        note = QLabel('Enter these from your calibration file. The app does not read ECU files yet.')
        note.setWordWrap(True)
        ecu.addRow('', note)

        self.notes = QPlainTextEdit()
        self.notes.setPlaceholderText('Anything else: mods, converter, shift kit, what you want from the car.')
        self.notes.setMaximumHeight(80)

        self.save_btn = QPushButton(icon(self, 'save'), 'Save vehicle')
        self.check_btn = QPushButton(icon(self, 'check'), 'Check consistency')
        self.check_btn.setProperty('role', 'secondary')
        self.import_btn = QPushButton(icon(self, 'open'), 'Import EFILive export...')
        self.import_btn.setProperty('role', 'secondary')
        self.save_btn.clicked.connect(self.save)
        self.check_btn.clicked.connect(self.check)
        self.import_btn.clicked.connect(self.import_export)
        buttons = QHBoxLayout()
        buttons.addWidget(self.import_btn)
        buttons.addStretch(1)
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.check_btn)

        self.calibration_label = QLabel('No calibration export loaded.')
        self.calibration_label.setWordWrap(True)
        self.calibration_label.setProperty('role', 'muted')

        self.status = QLabel()
        self.status.setWordWrap(True)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(['Level', 'Setting', 'Finding'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        grid = QGridLayout()
        grid.addWidget(vehicle_box, 0, 0)
        grid.addWidget(ecu_box, 0, 1)
        layout = QVBoxLayout(self)
        layout.addLayout(grid)
        layout.addWidget(QLabel('Notes'))
        layout.addWidget(self.notes)
        layout.addLayout(buttons)
        layout.addWidget(self.calibration_label)
        layout.addWidget(self.status)
        layout.addWidget(self.table, 1)

    def _show_transmission(self, key):
        try:
            entry = vehicle.transmission(key)
        except KeyError:
            self.transmission_note.setText('')
            return
        ratios = ', '.join(f'{r:g}' for r in entry['ratios'])
        reverse = f'{entry["reverse"]:g}' if entry.get('reverse') else 'not known'
        self.transmission_note.setText(
            f'Ratios: {ratios}. Reverse: {reverse}. {entry["note"]} Source: {entry["source"]}')

    def read(self):
        """The profile as currently shown in the tab. Zero or 'not set' limits read as None."""
        def limit(spin):
            return spin.value() if spin.value() > spin.minimum() else None
        return vehicle.VehicleProfile(
            car=self.car.text().strip(), engine=self.engine.text().strip(),
            transmission=self.transmission.currentText(), final_drive=self.final_drive.value(),
            tire_dia=self.tire.value(), power_hp=limit(self.power), torque_lbft=limit(self.torque),
            weight_lb=limit(self.weight), ecu_max_torque_lbft=limit(self.ecu_torque),
            redline_rpm=limit(self.redline), notes=self.notes.toPlainText().strip(),
            sources=[vehicle.transmission(self.transmission.currentText())['source']],
        )

    def load(self):
        profile = vehicle.load_profile()
        self.car.setText(profile.car)
        self.engine.setText(profile.engine)
        if profile.transmission in vehicle.TRANSMISSIONS:
            self.transmission.setCurrentText(profile.transmission)
        self.final_drive.setValue(profile.final_drive)
        self.tire.setValue(profile.tire_dia)
        self.weight.setValue(profile.weight_lb or 0)
        self.power.setValue(profile.power_hp or 0)
        self.torque.setValue(profile.torque_lbft or 0)
        self.ecu_torque.setValue(profile.ecu_max_torque_lbft or 0)
        self.redline.setValue(profile.redline_rpm or 0)
        self.notes.setPlainText(profile.notes)
        self._show_transmission(self.transmission.currentText())

    def spins(self):
        """The numeric values the AI may change, by name. Tire, final drive and weight belong to the Shift Points tab."""
        return {'power_hp': self.power, 'torque_lbft': self.torque,
                'ecu_max_torque_lbft': self.ecu_torque, 'redline_rpm': self.redline}

    def set_value(self, name, value):
        """Set one value from an approved AI proposal. Returns False if the name is not one of ours."""
        spin = self.spins().get(name)
        if spin is None:
            return False
        spin.setValue(float(value))
        return True

    def save(self):
        profile = self.read()
        try:
            path = vehicle.save_profile(profile)
        except OSError as exc:
            QMessageBox.warning(self, 'Cannot save', str(exc))
            return
        self._on_saved(profile)
        self.status.setProperty('role', 'good')
        self.status.setText(f'Saved to {path}. Tire, final drive and weight were copied to the Shift Points tab.')
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    def import_export(self):
        """Read an EFILive calibration export the user chooses. Only the text is read; nothing in it is run."""
        path, _ = QFileDialog.getOpenFileName(self, 'Open EFILive calibration export', '',
                                              'EFILive exports (*.csv *.HPT *.hpt *.txt);;All files (*)')
        if not path:
            return
        try:
            self.calibration = efilive_export.load(path)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, 'Cannot read export', str(exc))
            return
        tables = len(self.calibration.tables())
        values = len(self.calibration.scalars())
        self.calibration_label.setText(
            f'Loaded {self.calibration.meta.get("File", path)}: {values} values, {tables} tables, '
            f'exported {self.calibration.meta.get("Exported", "unknown date")}. The AI can read this summary.')

    def calibration_text(self):
        """The export summary for the AI, or None when no export is loaded."""
        if self.calibration is None:
            return None
        return self.calibration.readable(table_rows=3)[:CALIBRATION_TEXT_LIMIT]

    def current_findings(self):
        """Consistency findings for the values now in the tabs, or None if the Shift Points inputs are not readable."""
        cfg = self._shift_inputs()
        if cfg is None:
            return None
        profile = self.read()
        # The calculation's own values win, so an edit made in the Shift Points tab is checked too.
        profile.tire_dia = cfg['tire_dia']
        profile.final_drive = cfg['axle']
        profile.weight_lb = cfg['weight']
        try:
            entry = vehicle.transmission(profile.transmission)
        except KeyError:
            entry = None
        return consistency.check(profile, cfg, entry)

    def check(self):
        findings = self.current_findings()
        if findings is None:
            self.status.setText('The Shift Points inputs could not be read. Fix the ratios in the Shift Points tab first.')
            return
        self.show_findings(findings)

    def show_findings(self, findings):
        self.findings = findings
        self.table.setRowCount(len(findings))
        for row, f in enumerate(findings):
            level = QTableWidgetItem(LEVEL_TEXT[f.level])
            level.setForeground(QColor(LEVEL_COLOUR[f.level]))
            self.table.setItem(row, 0, level)
            self.table.setItem(row, 1, QTableWidgetItem(f.field))
            self.table.setItem(row, 2, QTableWidgetItem(f.message))
        self.table.resizeColumnsToContents()
        errors = sum(1 for f in findings if f.level == 'error')
        self.status.setText(f'{len(findings)} findings, {errors} errors. Read each one before changing a setting.'
                            if findings else 'No findings for these inputs.')
