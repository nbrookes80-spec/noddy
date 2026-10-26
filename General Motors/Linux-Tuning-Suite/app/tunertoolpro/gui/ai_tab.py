"""AI Assistant tab: optional questions to the Anthropic API about the tables and settings."""

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QCheckBox, QComboBox, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget)

from .. import ai_assistant, core, settings
from ..legal import AI_NOTICE


class _AskWorker(QThread):
    answered = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, question, api_key, model, context):
        super().__init__()
        self._args = (question, api_key, model, context)

    def run(self):
        try:
            self.answered.emit(ai_assistant.ask(*self._args))
        except ai_assistant.AIError as exc:
            self.failed.emit(str(exc))


class AiTab(QWidget):
    def __init__(self, context_provider=None, parent=None):
        """context_provider() returns text to send with the question, or '' for none."""
        super().__init__(parent)
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
        save_btn = QPushButton('Save settings')
        setup = QHBoxLayout()
        setup.addWidget(QLabel('API key'))
        setup.addWidget(self.key_edit, 1)
        setup.addWidget(QLabel('Model'))
        setup.addWidget(self.model_box)
        setup.addWidget(save_btn)
        save_btn.clicked.connect(self.save)

        self.include_tables = QCheckBox('Include the Shift Points tables from the last calculation')
        self.question = QPlainTextEdit()
        self.question.setPlaceholderText('Ask about the tables, the settings or a shift problem.')
        self.question.setMaximumHeight(110)
        self.ask_btn = QPushButton('Ask')
        self.ask_btn.clicked.connect(self.ask)
        self.answer = QPlainTextEdit()
        self.answer.setReadOnly(True)
        self.status = QLabel()
        self.status.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.enabled_box)
        layout.addLayout(setup)
        layout.addWidget(QLabel(AI_NOTICE))
        layout.addWidget(self.include_tables)
        layout.addWidget(self.question)
        layout.addWidget(self.ask_btn)
        layout.addWidget(self.status)
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
        self.ask_btn.setEnabled(False)
        self.status.setText('Asking...')
        self._worker = _AskWorker(self.question.toPlainText(), self.key_edit.text().strip(),
                                  self.model_box.currentText(), context)
        self._worker.answered.connect(self._show_answer)
        self._worker.failed.connect(self._show_error)
        self._worker.finished.connect(lambda: self.ask_btn.setEnabled(True))
        self._worker.start()

    def _show_answer(self, text):
        self.answer.setPlainText(text)
        self.status.setText('Answer received. Check it against your vehicle before you use it.')

    def _show_error(self, message):
        self.status.setText(message)


def tables_context(shift_tab):
    """Text of the last Shift Points calculation, or '' when nothing has been calculated."""
    tables = getattr(shift_tab, '_tables_data', None)
    if not tables:
        return ''
    return 'Shift Points tables (TPS x Gear, MPH):\n' + core.tps_gear_text(tables)
