"""The Link tab: talk to the car through an ELM327 adapter and read back what it answers.

The CAN Sniffer tab listens: it puts the adapter in monitor mode and watches frames go past. This tab
holds a conversation instead — it sends a request and shows the reply, which is what reading a PID or a
trouble code needs. The engine is `link.obd.Elm327` from the shared core, the same one the Android app
uses; this file is only the desktop face of it.

**It is read-only.** The link is built with allow_clear=False, so `obd.is_allowed` refuses Mode 04 and
anything else that writes. There is no button here that changes the car, and a refused command appears
in the traffic log as REFUSED rather than being quietly dropped.

Every adapter call blocks — a PID read is a round trip over Bluetooth or a serial port, and a search for
the protocol can take seconds — so the conversation runs on its own thread (`LinkWorker`) and the tab
polls for results on a timer. This is the pattern `canbus.session.SnifferSession` already uses.

On Windows a paired Bluetooth ELM327 is a COM port, so "USB / Bluetooth serial" covers both; the port
list says which is which, because COM5 on its own tells the user nothing.
"""

import queue
import threading

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QComboBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPlainTextEdit, QPushButton, QVBoxLayout, QWidget)

from ..link import obd
from ..link.devices import LIKELY_WORDS

SERIAL, WIFI = 'USB / Bluetooth serial', 'Wi-Fi adapter'
SOURCES = (SERIAL, WIFI)
BAUDS = ('38400', '9600', '115200', '500000')
POLL_MS = 100
TRAFFIC_LINES = 200

# On Windows a paired Bluetooth adapter is "Standard Serial over Bluetooth link"; the name never
# mentions OBD, so the Bluetooth words matter as much as the adapter brand names the core lists.
BLUETOOTH_WORDS = ('bluetooth', 'rfcomm', 'bthenum')

# Starting points for the PID box. Every one is in the shared catalogue, so the reply is decoded
# into a value and a unit rather than shown as raw hex.
SUGGESTED_PIDS = (
    ('010C', 'Engine speed'),
    ('010D', 'Vehicle speed'),
    ('0105', 'Coolant temperature'),
    ('0111', 'Throttle position'),
    ('0142', 'Control module voltage'),
    ('221940', 'Transmission fluid temperature (T43)'),
)

READ_ONLY_NOTICE = ('This link is read-only. It asks the car for values and codes; it never writes to a '
                    'controller and cannot flash a calibration.')


def describe_ports(ports=None):
    """[(label, device)] for the serial ports, the ones that look like an adapter first.

    `ports` is the pyserial list; it is passed in by the tests. A label is "COM5 - Standard Serial over
    Bluetooth link" rather than "COM5", because on Windows the bare name does not say which port is the
    dongle, and picking the wrong one is the usual reason a connection goes nowhere.
    """
    if ports is None:
        try:
            from serial.tools import list_ports
        except ImportError:
            return []
        ports = list_ports.comports()

    described = []
    for port in ports:
        device = getattr(port, 'device', '') or ''
        if not device:
            continue
        description = (getattr(port, 'description', '') or '').strip()
        haystack = f'{device} {description} {getattr(port, "hwid", "") or ""}'.lower()
        likely = any(word in haystack for word in LIKELY_WORDS + BLUETOOTH_WORDS)
        label = f'{device} - {description}' if description and description.lower() != 'n/a' else device
        described.append((not likely, device.lower(), label, device))
    described.sort()
    return [(label, device) for _, _, label, device in described]


class LinkWorker:
    """Runs the blocking adapter conversation on one background thread.

    Jobs go in, results come out: ('ok', name, value), ('err', name, message), or ('traffic', kind, text)
    for the adapter's own TX/RX/REFUSED lines. The tab drains the results on a timer, so nothing that
    waits on the car ever runs on the thread drawing the window.
    """

    def __init__(self):
        self.jobs = queue.Queue()
        self.results = queue.Queue()
        self.elm = None
        self._thread = None
        self._stop = threading.Event()

    @property
    def running(self):
        return self._thread is not None and self._thread.is_alive()

    def start(self):
        if self.running:
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def submit(self, name, job):
        self.jobs.put((name, job))

    def stop(self, timeout=5.0):
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout)
            self._thread = None

    def note_traffic(self, kind, text):
        self.results.put(('traffic', kind, text))

    def _serve(self):
        while not self._stop.is_set():
            try:
                name, job = self.jobs.get(timeout=0.1)
            except queue.Empty:
                continue
            try:
                self.results.put(('ok', name, job()))
            except Exception as exc:        # any adapter failure belongs on screen, not in a traceback
                self.results.put(('err', name, str(exc)))


class LinkTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = LinkWorker()
        self.connected = False
        self._build()
        self.timer = QTimer(self)
        self.timer.setInterval(POLL_MS)
        self.timer.timeout.connect(self.pump)
        self.refresh_ports()
        self._show_source()

    # --- the window ------------------------------------------------------------------------------
    def _build(self):
        page = QVBoxLayout(self)

        notice = QLabel(READ_ONLY_NOTICE)
        notice.setWordWrap(True)
        notice.setStyleSheet('color: #f5a623; font-weight: bold;')
        page.addWidget(notice)

        adapter = QGroupBox('Adapter')
        form = QFormLayout(adapter)

        self.source_box = QComboBox()
        self.source_box.addItems(SOURCES)
        self.source_box.currentTextChanged.connect(self._show_source)
        form.addRow('Connect over', self.source_box)

        self.port_box = QComboBox()
        self.port_box.setEditable(True)
        self.refresh_btn = QPushButton('Refresh list')
        self.refresh_btn.clicked.connect(self.refresh_ports)
        ports = QWidget()
        ports_row = QHBoxLayout(ports)
        ports_row.setContentsMargins(0, 0, 0, 0)
        ports_row.addWidget(self.port_box, 1)
        ports_row.addWidget(self.refresh_btn)
        self.port_row = ports
        self.port_label = QLabel('Serial port')
        form.addRow(self.port_label, ports)

        self.baud_box = QComboBox()
        self.baud_box.setEditable(True)
        self.baud_box.addItems(BAUDS)
        self.baud_label = QLabel('Baud rate')
        form.addRow(self.baud_label, self.baud_box)

        self.host_edit = QLineEdit(f'{obd.DEFAULT_WIFI[0]}:{obd.DEFAULT_WIFI[1]}')
        self.host_label = QLabel('Address')
        form.addRow(self.host_label, self.host_edit)

        self.connect_btn = QPushButton('Connect')
        self.connect_btn.clicked.connect(self.toggle_connection)
        form.addRow('', self.connect_btn)
        page.addWidget(adapter)

        self.status = QLabel('Not connected.')
        self.status.setWordWrap(True)
        page.addWidget(self.status)

        info = QGroupBox('What the adapter says')
        info_form = QFormLayout(info)
        self.firmware_label = QLabel('-')
        self.adapter_volts_label = QLabel('-')
        self.protocol_label = QLabel('-')
        self.car_volts_label = QLabel('-')
        info_form.addRow('Firmware', self.firmware_label)
        info_form.addRow('Adapter voltage', self.adapter_volts_label)
        info_form.addRow('Protocol', self.protocol_label)
        info_form.addRow('Car battery', self.car_volts_label)
        page.addWidget(info)

        ask = QGroupBox('Ask the car')
        ask_layout = QVBoxLayout(ask)
        pid_row = QHBoxLayout()
        self.pid_box = QComboBox()
        self.pid_box.setEditable(True)
        for pid, name in SUGGESTED_PIDS:
            self.pid_box.addItem(f'{pid} - {name}', pid)
        self.read_btn = QPushButton('Read value')
        self.read_btn.clicked.connect(self.read_pid)
        self.codes_btn = QPushButton('Read trouble codes')
        self.codes_btn.clicked.connect(self.read_codes)
        pid_row.addWidget(QLabel('PID'))
        pid_row.addWidget(self.pid_box, 1)
        pid_row.addWidget(self.read_btn)
        pid_row.addWidget(self.codes_btn)
        ask_layout.addLayout(pid_row)
        self.answer = QLabel('No reading yet.')
        self.answer.setWordWrap(True)
        ask_layout.addWidget(self.answer)
        page.addWidget(ask)

        traffic = QGroupBox('Traffic (what was sent, and what came back)')
        traffic_layout = QVBoxLayout(traffic)
        self.traffic_view = QPlainTextEdit()
        self.traffic_view.setReadOnly(True)
        self.traffic_view.setMaximumBlockCount(TRAFFIC_LINES)
        self.traffic_view.setPlaceholderText('Nothing sent yet.')
        traffic_layout.addWidget(self.traffic_view)
        page.addWidget(traffic, 1)

        self._enable_requests(False)

    def _show_source(self, *_):
        serial = self.source_box.currentText() == SERIAL
        for widget in (self.port_row, self.port_label, self.baud_box, self.baud_label):
            widget.setVisible(serial)
        for widget in (self.host_edit, self.host_label):
            widget.setVisible(not serial)

    def _enable_requests(self, on):
        self.read_btn.setEnabled(on)
        self.codes_btn.setEnabled(on)

    # --- ports -----------------------------------------------------------------------------------
    def refresh_ports(self, ports=None):
        """Fill the port list again.

        A port the user typed by hand survives, because the list may never have offered it. A port they
        picked from the list survives only while it is still there: an adapter that has been unplugged
        must stop looking selected, or the next Connect tries a port that is gone.
        """
        previous = self.chosen_port()
        typed_by_hand = not self._current_is_a_list_choice()
        typed = self.port_box.currentText()
        self.port_box.clear()
        for label, device in describe_ports(ports):
            self.port_box.addItem(label, device)
        if typed_by_hand and typed.strip():
            self.port_box.setCurrentText(typed)
            return
        for index in range(self.port_box.count()):
            if self.port_box.itemData(index) == previous:
                self.port_box.setCurrentIndex(index)
                return
        self.port_box.setCurrentIndex(0) if self.port_box.count() else self.port_box.setCurrentText('')

    def _current_is_a_list_choice(self):
        index = self.port_box.currentIndex()
        return index >= 0 and self.port_box.itemText(index) == self.port_box.currentText()

    def chosen_port(self):
        """The device name, whether it was picked from the list or typed in."""
        if self._current_is_a_list_choice():
            index = self.port_box.currentIndex()
            return self.port_box.itemData(index) or self.port_box.currentText().strip()
        return self.port_box.currentText().strip()

    # --- connecting ------------------------------------------------------------------------------
    def build_transport(self):
        """The transport for the chosen source. Raises ValueError with a message meant for the user."""
        if self.source_box.currentText() == WIFI:
            host, _, port = self.host_edit.text().strip().partition(':')
            if not host:
                raise ValueError('Enter the adapter address, for example 192.168.0.10:35000.')
            try:
                return obd.WifiTransport(host, int(port or obd.DEFAULT_WIFI[1]))
            except ValueError:
                raise ValueError('The port after the colon must be a number, for example 35000.') from None
        port = self.chosen_port()
        if not port:
            raise ValueError('Choose the adapter\'s serial port first (COM3 on Windows, /dev/ttyUSB0 or '
                             '/dev/rfcomm0 on Linux). Pair a Bluetooth adapter in the system settings '
                             'first and it appears in this list.')
        try:
            baud = int(self.baud_box.currentText())
        except ValueError:
            raise ValueError('The baud rate must be a number such as 38400 or 115200.') from None
        return obd.SerialTransport(port, baud)

    # Named open_link/close_link, not connect/disconnect: QObject already has disconnect(),
    # and shadowing it on a QWidget is a trap waiting for whoever reads this next.
    def toggle_connection(self):
        if self.connected or self.worker.running:
            self.close_link()
        else:
            self.open_link()

    def open_link(self):
        try:
            transport = self.build_transport()
        except ValueError as exc:
            self.status.setText(str(exc))
            return
        self.status.setText('Connecting...')
        self.connect_btn.setEnabled(False)
        self.worker.start()
        self.worker.submit('connect', lambda: self._open(transport))
        self.timer.start()

    def _open(self, transport):
        """Runs on the worker thread: open the link read-only and ask the adapter about itself."""
        elm = obd.Elm327(transport, allow_clear=False)
        elm.on_traffic = self.worker.note_traffic
        elm.open()
        self.worker.elm = elm
        return obd.read_adapter_info(elm)

    def close_link(self):
        elm = self.worker.elm
        self.worker.stop()
        self.worker.elm = None
        if elm is not None:
            try:
                elm.close()
            except Exception:       # a dropped adapter must not stop the tab closing the link
                pass
        self.timer.stop()
        self.connected = False
        self.connect_btn.setText('Connect')
        self.connect_btn.setEnabled(True)
        self._enable_requests(False)
        self.status.setText('Not connected.')

    # --- asking the car --------------------------------------------------------------------------
    def chosen_pid(self):
        index = self.pid_box.currentIndex()
        if index >= 0 and self.pid_box.itemText(index) == self.pid_box.currentText():
            return (self.pid_box.itemData(index) or '').strip().upper()
        return self.pid_box.currentText().split(' - ')[0].strip().upper()

    def read_pid(self):
        pid = self.chosen_pid()
        if not pid or self.worker.elm is None:
            return
        self.answer.setText(f'Asking for {pid}...')
        self.worker.submit('read', lambda: (pid, self.worker.elm.read(pid)))

    def read_codes(self):
        if self.worker.elm is None:
            return
        self.answer.setText('Reading trouble codes...')
        self.worker.submit('codes', self.worker.elm.read_dtcs)

    # --- results in, screen out --------------------------------------------------------------------
    def pump(self):
        """Drain whatever the worker has finished. Called by the timer, and directly by the tests."""
        while True:
            try:
                kind, name, payload = self.worker.results.get_nowait()
            except queue.Empty:
                return
            if kind == 'traffic':
                self.traffic_view.appendPlainText(f'{name}: {payload}')
            elif kind == 'err':
                self._failed(name, payload)
            else:
                self._succeeded(name, payload)

    def _succeeded(self, name, payload):
        if name == 'connect':
            self.connected = True
            self.connect_btn.setText('Disconnect')
            self.connect_btn.setEnabled(True)
            self._enable_requests(True)
            self.firmware_label.setText(payload.get('firmware') or '-')
            self.adapter_volts_label.setText(payload.get('adapter_volts') or '-')
            self.protocol_label.setText(payload.get('protocol') or '-')
            self.car_volts_label.setText(payload.get('car_volts') or '-')
            self.status.setText('Connected. The link is read-only.')
        elif name == 'read':
            pid, (value, unit) = payload
            self.answer.setText(f'{pid}: {value} {unit}'.strip())
        elif name == 'codes':
            self.answer.setText('No stored trouble codes.' if not payload
                                else 'Stored trouble codes: ' + ', '.join(payload))

    def _failed(self, name, message):
        if name == 'connect':
            self.connected = False
            self.connect_btn.setText('Connect')
            self.connect_btn.setEnabled(True)
            self._enable_requests(False)
            self.timer.stop()
            self.worker.stop()
            self.status.setText(f'Could not connect: {message}')
        else:
            self.answer.setText(f'That did not work: {message}')

    def shutdown(self):
        if self.worker.running or self.connected:
            self.close_link()
