"""CAN Sniffer tab: watch which CAN IDs are active and which bytes and bits are changing.

Receive only. With a scan adapter it listens with the ELM327 "monitor all" command and sends nothing
to the car (see canbus/monitor.py). It can also play back a log file or a simulated bus, so it can be
learned with no hardware. Based on the Sniffer window in SavvyCAN; see docs/THIRD_PARTY.md.
"""

import queue
import threading
import time

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import (QAbstractItemView, QCheckBox, QComboBox, QFileDialog, QHBoxLayout, QLabel,
                             QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QPushButton, QSpinBox,
                             QStyledItemDelegate, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from ..canbus import (DemoBus, ElmMonitor, LogPlayer, MonitorError, PROTOCOLS, Sniffer, format_candump,
                      format_csv, read_log)
from ..canbus.sniffer import DEC, INC
from ..canbus.transports import DEFAULT_WIFI, SerialTransport, TcpTransport, TransportError, serial_ports

SOURCES = ('Simulated bus', 'Log file', 'Wi-Fi adapter', 'Serial / USB / Bluetooth adapter')
FIXED_COLUMNS = ('ID', 'Delta', 'Frequency')
CAPTURE_LIMIT = 500_000
POLL_MS = 50
REFRESH_MS = 200


def _dark(widget):
    colour = widget.palette().color(widget.foregroundRole())
    return colour.red() + colour.green() + colour.blue() >= 380


class BitsDelegate(QStyledItemDelegate):
    """Draws a byte as eight squares: black set, white unset, green just set, red just cleared, grey notched."""

    def __init__(self, dark, parent=None):
        super().__init__(parent)
        self.colours = {'notched': QColor(230, 230, 230), 'set': QColor(0, 0, 0), 'unset': QColor(255, 255, 255),
                        'rose': QColor(0, 128, 0) if dark else QColor(0, 200, 0),
                        'fell': QColor(128, 0, 0) if dark else QColor(220, 0, 0)}

    def paint(self, painter, option, index):
        cell = index.data(Qt.ItemDataRole.UserRole)
        if not cell:
            return
        painter.save()
        rect = option.rect
        size = max(4, min(rect.width() // 8, rect.height() - 14))
        left = rect.left() + (rect.width() - 8 * size) // 2
        painter.setOpacity(1 - cell['fade'] / 255)
        for i, state in enumerate(cell['bits']):
            painter.setBrush(self.colours[state])
            painter.setPen(QColor(120, 120, 120))
            painter.drawRect(left + i * size, rect.top() + 1, size, size)
        painter.setOpacity(1)
        painter.setPen(option.palette.text().color())
        painter.drawText(rect.adjusted(0, size + 2, 0, 0), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                         cell['text'])
        painter.restore()

    def sizeHint(self, option, index):
        hint = super().sizeHint(option, index)
        hint.setHeight(hint.height() * 2)
        return hint


class SnifferTab(QWidget):
    def __init__(self, parent=None, clock=time.monotonic):
        super().__init__(parent)
        self.clock = clock
        self.sniffer = Sniffer(clock)
        self.source = None
        self.monitor = None
        self.worker = None
        self.stop_flag = threading.Event()
        self.inbox = queue.Queue()
        self.captured = []
        self.log_frames = None
        self.log_path = ''
        self.error = ''
        self._known_ids = set()
        self._dark = _dark(self)

        self.source_box = QComboBox()
        self.source_box.addItems(SOURCES)
        self.choose_log = QPushButton('Choose log file...')
        self.host_edit = QLineEdit(f'{DEFAULT_WIFI[0]}:{DEFAULT_WIFI[1]}')
        self.port_box = QComboBox()
        self.port_box.setEditable(True)
        self.refresh_ports = QPushButton('Refresh')
        self.protocol_box = QComboBox()
        for key, label in PROTOCOLS.items():
            self.protocol_box.addItem(f'{key}: {label}', key)
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText('only this ID, hex (optional), e.g. 7E8')
        self.filter_edit.setMaximumWidth(260)
        self.start_btn = QPushButton('Start')
        self.start_btn.setProperty('primary', True)

        self.notch_btn = QPushButton('Notch')
        self.unnotch_btn = QPushButton('Un-notch')
        self.clear_btn = QPushButton('Clear')
        self.save_btn = QPushButton('Save log...')
        self.never_expire = QCheckBox('Never expire IDs')
        self.mute = QCheckBox('Mute notched bits')
        self.fade = QCheckBox('Fade inactive bytes')
        self.view_bits = QCheckBox('View bits')
        self.expire_spin = QSpinBox()
        self.expire_spin.setRange(1, 60)
        self.expire_spin.setValue(5)
        self.expire_spin.setSuffix(' s')
        self.notch_spin = QSpinBox()
        self.notch_spin.setRange(100, 5000)
        self.notch_spin.setSingleStep(100)
        self.notch_spin.setValue(200)
        self.notch_spin.setSuffix(' ms')

        self.table = QTableWidget(0, len(FIXED_COLUMNS) + 8)
        self.table.setHorizontalHeaderLabels(list(FIXED_COLUMNS) + [str(i) for i in range(8)])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 90)
        self.id_list = QListWidget()
        self.id_list.setMaximumWidth(150)
        self.show_all_btn = QPushButton('All')
        self.hide_all_btn = QPushButton('None')
        self.bits_delegate = BitsDelegate(self._dark, self.table)
        self.status = QLabel('Stopped. Pick a source and press Start.')
        self.status.setWordWrap(True)
        self.help = QLabel(
            'Only IDs that are updating are listed; one that goes quiet turns red and drops off. A byte that '
            'went up is green and one that went down is red. Hold still, press Notch a few times to mute the '
            'bits that always change, then move the control you are hunting for (steering, a pedal, a switch) '
            'and watch which ID lights up. Receive only: nothing is sent to the car.')
        self.help.setWordWrap(True)

        source_row = QHBoxLayout()
        for widget in (QLabel('Source'), self.source_box, self.choose_log, self.host_edit, self.port_box,
                       self.refresh_ports, QLabel('Bus'), self.protocol_box, self.filter_edit, self.start_btn):
            source_row.addWidget(widget)
        source_row.addStretch(1)
        tool_row = QHBoxLayout()
        for widget in (self.notch_btn, self.unnotch_btn, self.never_expire, self.mute, self.fade, self.view_bits,
                       QLabel('Expire after'), self.expire_spin, QLabel('Notch every'), self.notch_spin,
                       self.clear_btn, self.save_btn):
            tool_row.addWidget(widget)
        tool_row.addStretch(1)
        side = QVBoxLayout()
        side.addWidget(QLabel('Show IDs'))
        buttons = QHBoxLayout()
        buttons.addWidget(self.show_all_btn)
        buttons.addWidget(self.hide_all_btn)
        side.addLayout(buttons)
        side.addWidget(self.id_list, 1)
        body = QHBoxLayout()
        body.addLayout(side)
        body.addWidget(self.table, 1)
        layout = QVBoxLayout(self)
        layout.addWidget(self.help)
        layout.addLayout(source_row)
        layout.addLayout(tool_row)
        layout.addLayout(body, 1)
        layout.addWidget(self.status)

        self.source_box.currentIndexChanged.connect(self._source_changed)
        self.choose_log.clicked.connect(self._pick_log)
        self.refresh_ports.clicked.connect(self._fill_ports)
        self.start_btn.clicked.connect(self.toggle)
        self.notch_btn.clicked.connect(self.sniffer.notch)
        self.unnotch_btn.clicked.connect(self.sniffer.unnotch)
        self.clear_btn.clicked.connect(self.clear)
        self.save_btn.clicked.connect(self.save_log)
        self.never_expire.toggled.connect(lambda on: setattr(self.sniffer, 'never_expire', on))
        self.mute.toggled.connect(lambda on: setattr(self.sniffer, 'mute_notched', on))
        self.fade.toggled.connect(lambda on: setattr(self.sniffer, 'fade_inactive', on))
        self.view_bits.toggled.connect(self._bits_toggled)
        self.expire_spin.valueChanged.connect(lambda v: setattr(self.sniffer, 'expire_seconds', float(v)))
        self.notch_spin.valueChanged.connect(lambda v: self.notch_timer.setInterval(v))
        self.show_all_btn.clicked.connect(self._show_all)
        self.hide_all_btn.clicked.connect(self._hide_all)
        self.id_list.itemChanged.connect(self._id_toggled)

        self.poll_timer = QTimer(self)
        self.poll_timer.setInterval(POLL_MS)
        self.poll_timer.timeout.connect(self.poll)
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(REFRESH_MS)
        self.refresh_timer.timeout.connect(self.refresh)
        self.notch_timer = QTimer(self)
        self.notch_timer.setInterval(self.notch_spin.value())
        self.notch_timer.timeout.connect(self.sniffer.tick_notch)

        self._bits_toggled(False)
        self._fill_ports()
        self._source_changed()

    # --- source controls -------------------------------------------------------------------------
    @property
    def source_name(self):
        return SOURCES[self.source_box.currentIndex()]

    def _source_changed(self):
        name = self.source_name
        adapter = name in SOURCES[2:]
        self.choose_log.setVisible(name == 'Log file')
        self.host_edit.setVisible(name == 'Wi-Fi adapter')
        self.port_box.setVisible(name == SOURCES[3])
        self.refresh_ports.setVisible(name == SOURCES[3])
        self.protocol_box.setVisible(adapter)
        self.filter_edit.setVisible(adapter)

    def _fill_ports(self):
        current = self.port_box.currentText()
        self.port_box.clear()
        self.port_box.addItems(serial_ports())
        if current:
            self.port_box.setCurrentText(current)

    def _pick_log(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open a CAN log', '',
                                              'CAN logs (*.log *.csv *.txt);;All files (*)')
        if not path:
            return
        try:
            with open(path, encoding='utf-8', errors='replace') as handle:
                frames = read_log(handle.read())
        except OSError as exc:
            QMessageBox.warning(self, 'Could not read the log', str(exc))
            return
        if not frames:
            QMessageBox.warning(self, 'No frames found',
                                'That file has no CAN frames in a format the sniffer reads '
                                '(candump, CSV from this tool, SLCAN or ELM327 monitor text).')
            return
        self.log_frames, self.log_path = frames, path
        self.choose_log.setText(f'{path.rsplit("/", 1)[-1]}  ({len(frames)} frames)')

    # --- start and stop --------------------------------------------------------------------------
    @property
    def running(self):
        return self.source is not None or self.worker is not None

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        name = self.source_name
        self.error = ''
        try:
            if name == SOURCES[0]:
                self.source = DemoBus(self.clock)
            elif name == 'Log file':
                if not self.log_frames:
                    self._pick_log()
                    if not self.log_frames:
                        return
                self.source = LogPlayer(self.log_frames, self.clock)
            else:
                self._start_adapter(name)
        except (MonitorError, TransportError, ValueError) as exc:
            QMessageBox.warning(self, 'Could not start', str(exc))
            self.source = None
            return
        self.start_btn.setText('Stop')
        self.poll_timer.start()
        self.refresh_timer.start()
        self.notch_timer.start()
        self.status.setText(f'Listening: {name}.')

    def _start_adapter(self, name):
        if name == 'Wi-Fi adapter':
            host, _, port = self.host_edit.text().strip().partition(':')
            transport = TcpTransport(host or DEFAULT_WIFI[0], int(port or DEFAULT_WIFI[1]))
        else:
            if not self.port_box.currentText().strip():
                raise ValueError('Choose the serial port of the adapter first (for example /dev/ttyUSB0, '
                                 '/dev/rfcomm0 or COM3).')
            transport = SerialTransport(self.port_box.currentText().strip())
        transport.open()
        monitor = ElmMonitor(transport, self.clock)
        try:
            monitor.start(self.protocol_box.currentData(), self.filter_edit.text().strip() or None)
        except Exception:
            transport.close()
            raise
        self.monitor = monitor
        self.stop_flag.clear()
        self.worker = threading.Thread(target=self._read_loop, args=(monitor, transport), daemon=True)
        self.worker.start()

    def _read_loop(self, monitor, transport):
        try:
            while not self.stop_flag.is_set():
                frames = monitor.poll(0.1)
                if frames:
                    self.inbox.put(frames)
        except Exception as exc:
            self.inbox.put(str(exc))
        finally:
            try:
                monitor.stop()
            except Exception:
                pass
            transport.close()

    def stop(self):
        self.poll_timer.stop()
        self.refresh_timer.stop()
        self.notch_timer.stop()
        self.stop_flag.set()
        if self.worker is not None:
            self.worker.join(timeout=5)
        self.worker = self.monitor = self.source = None
        self.start_btn.setText('Start')
        self.status.setText(self.error or f'Stopped. {self.sniffer.frames_seen} frames seen.')

    def shutdown(self):
        if self.running:
            self.stop()

    # --- frames in, rows out ---------------------------------------------------------------------
    def poll(self):
        incoming = []
        if self.source is not None:
            incoming = self.source.poll()
            if getattr(self.source, 'finished', False):
                self.stop()
        while True:
            try:
                item = self.inbox.get_nowait()
            except queue.Empty:
                break
            if isinstance(item, str):
                self.error = f'Stopped: {item}'
                self.stop()
                break
            incoming.extend(item)
        if incoming:
            self.sniffer.feed(incoming)
            room = CAPTURE_LIMIT - len(self.captured)
            if room > 0:
                self.captured.extend(incoming[:room])

    def feed(self, frames):
        """Hand frames in directly (used by tests and by anything that already has them)."""
        self.sniffer.feed(frames)
        self.captured.extend(frames[:max(0, CAPTURE_LIMIT - len(self.captured))])

    def refresh(self):
        gone = self.sniffer.tick()
        for can_id in gone:
            self._remove_id(can_id)
        rows = self.sniffer.rows()
        for row in rows:
            self._ensure_id(row['id'], row['id_text'])
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            self._paint_row(r, row)
        overruns = self.monitor.overruns if self.monitor else 0
        text = f'{self.sniffer.frames_seen} frames seen, {len(rows)} IDs shown'
        if overruns:
            text += f'. The adapter dropped frames {overruns} times: set a receive filter to quieten the bus.'
        if self.running or self.sniffer.frames_seen:
            self.status.setText(text)

    def _cell(self, r, c):
        item = self.table.item(r, c)
        if item is None:
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(r, c, item)
        return item

    def _paint_row(self, r, row):
        id_item = self._cell(r, 0)
        id_item.setText('0x' + row['id_text'])
        id_item.setBackground(QBrush(QColor(128, 0, 0) if self._dark else QColor(255, 80, 80))
                              if row['stale'] else QBrush())
        self._cell(r, 1).setText(f"{row['delta']:.4f}")
        self._cell(r, 2).setText(row['freq'])
        for i, cell in enumerate(row['bytes']):
            item = self._cell(r, 3 + i)
            if cell is None:
                item.setText('')
                item.setData(Qt.ItemDataRole.UserRole, None)
                item.setBackground(QBrush())
                continue
            item.setText(cell['text'])
            item.setData(Qt.ItemDataRole.UserRole, cell)
            item.setBackground(self._brush(cell['change']))
            grey = max(0, min(225, cell['fade']))
            item.setForeground(QBrush(QColor(255 - grey, 255 - grey, 255 - grey) if self._dark
                                      else QColor(grey, grey, grey)) if cell['fade'] else QBrush())

    def _brush(self, change):
        if change == INC:
            return QBrush(QColor(0, 128, 0) if self._dark else QColor(120, 220, 120))
        if change == DEC:
            return QBrush(QColor(128, 0, 0) if self._dark else QColor(240, 120, 120))
        return QBrush()

    def _bits_toggled(self, on):
        for c in range(3, 11):
            self.table.setItemDelegateForColumn(c, self.bits_delegate if on else None)
        self.table.verticalHeader().setDefaultSectionSize(40 if on else 24)
        for c in range(3, 11):
            self.table.setColumnWidth(c, 96 if on else 56)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 90)

    # --- ID filter list --------------------------------------------------------------------------
    def _ensure_id(self, can_id, text):
        if can_id in self._known_ids:
            return
        self._known_ids.add(can_id)
        item = QListWidgetItem('0x' + text)
        item.setData(Qt.ItemDataRole.UserRole, can_id)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Checked if self.sniffer.is_visible(can_id) else Qt.CheckState.Unchecked)
        self.id_list.blockSignals(True)
        self.id_list.addItem(item)
        self.id_list.sortItems()
        self.id_list.blockSignals(False)

    def _remove_id(self, can_id):
        self._known_ids.discard(can_id)
        for i in range(self.id_list.count()):
            if self.id_list.item(i).data(Qt.ItemDataRole.UserRole) == can_id:
                self.id_list.takeItem(i)
                return

    def _id_toggled(self, item):
        self.sniffer.set_visible(item.data(Qt.ItemDataRole.UserRole), item.checkState() == Qt.CheckState.Checked)

    def _set_all_checks(self, state):
        self.id_list.blockSignals(True)
        for i in range(self.id_list.count()):
            self.id_list.item(i).setCheckState(state)
        self.id_list.blockSignals(False)

    def _show_all(self):
        self.sniffer.show_all()
        self._set_all_checks(Qt.CheckState.Checked)

    def _hide_all(self):
        self.sniffer.hide_all()
        self._set_all_checks(Qt.CheckState.Unchecked)

    # --- housekeeping ----------------------------------------------------------------------------
    def clear(self):
        self.sniffer.clear()
        self.captured.clear()
        self._known_ids.clear()
        self.id_list.clear()
        self.table.setRowCount(0)
        self.status.setText('Cleared.')

    def save_log(self):
        if not self.captured:
            QMessageBox.information(self, 'Nothing to save', 'No frames have been captured yet.')
            return
        path, chosen = QFileDialog.getSaveFileName(self, 'Save the captured frames', 'capture.log',
                                                   'candump log (*.log);;CSV (*.csv)')
        if not path:
            return
        text = format_csv(self.captured) if chosen.startswith('CSV') or path.endswith('.csv') \
            else format_candump(self.captured)
        try:
            with open(path, 'w', encoding='utf-8') as handle:
                handle.write(text)
        except OSError as exc:
            QMessageBox.warning(self, 'Could not save', str(exc))
            return
        self.status.setText(f'Saved {len(self.captured)} frames to {path}.')
