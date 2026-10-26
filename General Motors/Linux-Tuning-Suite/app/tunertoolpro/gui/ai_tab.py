"""AI Assistant tab: questions to the Anthropic API, with tools that read the settings and propose changes.

Every proposal appears here with Apply and Reject. Only Apply changes a setting, and it goes
through the tab that owns the setting, so the same range limits apply.
"""

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QCheckBox, QComboBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                             QMessageBox, QPlainTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget)

from .. import ai_assistant, core, settings
from ..ai_tools import Session
from ..legal import AI_NOTICE
from .theme import icon

VEHICLE_PREFIX = 'vehicle.'


class SettingsBridge:
    """What the assistant can read and change: the Shift Points inputs and the vehicle's own numbers.

    Shift Points names are used as they are. Vehicle names carry the 'vehicle.' prefix, so the two
    tabs never share a name.
    """

    def __init__(self, shift, vehicle_tab):
        self.shift = shift
        self.vehicle = vehicle_tab

    def snapshot(self):
        cfg = self.shift.inputs_or_none()
        findings = self.vehicle.current_findings() or []
        return {
            'shift_inputs': cfg if cfg is not None else 'Not readable: check the gear ratios in the Shift Points tab.',
            'vehicle': self.vehicle.read().to_dict(),
            'findings': [f.as_dict() for f in findings],
            'calibration_export': self.vehicle.calibration_text() or 'No EFILive export is loaded.',
        }

    def bounds(self):
        out = {key: (w.minimum(), w.maximum()) for key, w in self.shift.widgets().items()}
        for name, spin in self.vehicle.spins().items():
            out[VEHICLE_PREFIX + name] = (spin.minimum(), spin.maximum())
        return out

    def value(self, name):
        if name.startswith(VEHICLE_PREFIX):
            return self.vehicle.spins()[name[len(VEHICLE_PREFIX):]].value()
        return self.shift.value(name)

    def apply(self, name, value):
        """Set one value. Returns False if the tab that owns the name does not have it."""
        if name.startswith(VEHICLE_PREFIX):
            return self.vehicle.set_value(name[len(VEHICLE_PREFIX):], value)
        return self.shift.set_value(name, value)

    def refresh_checks(self):
        self.vehicle.check()


class _AskWorker(QThread):
    answered = pyqtSignal(object)  # (text, proposals, questions)
    failed = pyqtSignal(str)

    def __init__(self, question, api_key, model, session, context, parent=None):
        super().__init__(parent)
        self._args = (question, api_key, model, session, context)

    def run(self):
        try:
            self.answered.emit(ai_assistant.ask_with_tools(*self._args))
        except ai_assistant.AIError as exc:
            self.failed.emit(str(exc))


class AiTab(QWidget):
    def __init__(self, bridge, context_provider=None, parent=None):
        """bridge: a SettingsBridge. context_provider() returns table text to send, or '' for none."""
        super().__init__(parent)
        self._bridge = bridge
        self._context_provider = context_provider or (lambda: '')
        self._worker = None
        self._build()
        self._load()

    def _build(self):
        self.enabled_box = QCheckBox('Use the AI assistant')
        self.key_edit = QLineEdit()
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_edit.setPlaceholderText('Anthropic API key (sk-ant-...)')
        self.model_box = QComboBox()
        self.model_box.addItems(settings.AI_MODELS)
        save_btn = QPushButton(icon(self, 'save'), 'Save settings')
        setup = QHBoxLayout()
        setup.addWidget(QLabel('API key'))
        setup.addWidget(self.key_edit, 1)
        setup.addWidget(QLabel('Model'))
        setup.addWidget(self.model_box)
        setup.addWidget(save_btn)
        save_btn.clicked.connect(self.save)

        self.include_tables = QCheckBox('Include the Shift Points tables from the last calculation')
        self.question = QPlainTextEdit()
        self.question.setPlaceholderText('Ask about the tables, the settings or a shift problem. '
                                         'If the assistant asks you something, answer it here.')
        self.question.setMaximumHeight(110)
        self.ask_btn = QPushButton(icon(self, 'ask'), 'Ask')
        self.ask_btn.clicked.connect(self.ask)
        self.status = QLabel()
        self.status.setWordWrap(True)

        self.proposals = QTableWidget(0, 5)
        self.proposals.setHorizontalHeaderLabels(['Setting', 'Now', 'Proposed', 'Why', 'Decision'])
        self.proposals.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        header = self.proposals.horizontalHeader()
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.proposals.setColumnWidth(4, 210)  # room for Apply and Reject side by side
        self.proposals.verticalHeader().setVisible(False)
        self.answer = QPlainTextEdit()
        self.answer.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.enabled_box)
        layout.addLayout(setup)
        layout.addWidget(QLabel(AI_NOTICE))
        layout.addWidget(self.include_tables)
        layout.addWidget(self.question)
        layout.addWidget(self.ask_btn)
        layout.addWidget(self.status)
        layout.addWidget(QLabel('Proposed changes. Nothing changes until you press Apply.'))
        layout.addWidget(self.proposals, 1)
        layout.addWidget(self.answer, 1)

    def _load(self):
        data = settings.load()['ai']
        self.enabled_box.setChecked(bool(data['enabled']))
        self.key_edit.setText(data['api_key'])
        if data['model'] in settings.AI_MODELS:
            self.model_box.setCurrentText(data['model'])
        self._refresh_status()

    def _refresh_status(self):
        if not self.enabled_box.isChecked():
            self.status.setText('The AI assistant is off. Tick "Use the AI assistant" and save to turn it on.')
        elif not self.key_edit.text().strip():
            self.status.setText('Add an API key and save before asking a question.')
        else:
            self.status.setText('Ready. Questions go to the Anthropic API.')

    def save(self):
        data = settings.load()
        data['ai'] = {
            'enabled': self.enabled_box.isChecked(),
            'api_key': self.key_edit.text().strip(),
            'model': self.model_box.currentText(),
        }
        try:
            path = settings.save(data)
        except OSError as exc:
            QMessageBox.warning(self, 'Cannot save settings', str(exc))
            return
        self._refresh_status()
        self.status.setText(self.status.text() + f' Saved to {path}.')

    def ask(self):
        if self._worker is not None and self._worker.isRunning():
            return
        if not self.enabled_box.isChecked():
            self.status.setText('Turn the AI assistant on and save settings first.')
            return
        context = self._context_provider() if self.include_tables.isChecked() else ''
        session = Session(snapshot=self._bridge.snapshot(), bounds=self._bridge.bounds())
        self.proposals.setRowCount(0)
        self.ask_btn.setEnabled(False)
        self.status.setText('Asking...')
        self._worker = _AskWorker(self.question.toPlainText(), self.key_edit.text().strip(),
                                  self.model_box.currentText(), session, context, parent=self)
        self._worker.answered.connect(self._show_answer)
        self._worker.failed.connect(self._show_error)
        self._worker.finished.connect(lambda: self.ask_btn.setEnabled(True))
        self._worker.start()

    def shutdown(self):
        """Wait for a running request to finish before the window closes."""
        if self._worker is not None and self._worker.isRunning():
            self._worker.wait(70000)  # longer than the request timeout

    def _show_answer(self, result):
        text, proposals, questions = result
        lines = [text]
        if questions:
            lines += ['', 'The assistant needs:'] + [f'- {q}' for q in questions]
        self.answer.setPlainText('\n'.join(lines).strip())
        for row, proposal in enumerate(proposals):
            self._add_proposal(row, proposal)
        if proposals:
            self.status.setText(f'{len(proposals)} proposed change(s). Apply or reject each one.')
        else:
            self.status.setText('Answer received. Check it against your vehicle before you use it.')

    def _add_proposal(self, row, proposal):
        name = proposal['field']
        self.proposals.insertRow(row)
        self.proposals.setItem(row, 0, QTableWidgetItem(name))
        self.proposals.setItem(row, 1, QTableWidgetItem(f'{self._bridge.value(name):g}'))
        self.proposals.setItem(row, 2, QTableWidgetItem(f'{proposal["value"]:g}'))
        self.proposals.setItem(row, 3, QTableWidgetItem(proposal['reason']))
        apply_btn = QPushButton(icon(self, 'apply'), 'Apply')
        reject_btn = QPushButton(icon(self, 'reject'), 'Reject')
        reject_btn.setProperty('role', 'secondary')
        holder = QWidget()
        box = QHBoxLayout(holder)
        box.setContentsMargins(2, 2, 2, 2)
        box.addWidget(apply_btn)
        box.addWidget(reject_btn)
        self.proposals.setCellWidget(row, 4, holder)

        def resolve(outcome):
            holder.deleteLater()
            self.proposals.setCellWidget(row, 4, None)
            self.proposals.setItem(row, 4, QTableWidgetItem(outcome))

        def on_apply():
            if self._bridge.apply(name, proposal['value']):
                resolve('Applied')
                self._bridge.refresh_checks()
                self.status.setText(f'Applied {name} = {proposal["value"]:g}. Check the Vehicle tab findings.')
            else:
                resolve('Not applied')
                self.status.setText(f'{name} is not a setting this tab can change.')

        apply_btn.clicked.connect(on_apply)
        reject_btn.clicked.connect(lambda: resolve('Rejected'))

    def _show_error(self, message):
        self.status.setText(message)


def tables_context(shift_tab):
    """Text of the last Shift Points calculation, or '' when nothing has been calculated."""
    tables = getattr(shift_tab, '_tables_data', None)
    if not tables:
        return ''
    return 'Shift Points tables (TPS x Gear, MPH):\n' + core.tps_gear_text(tables)
