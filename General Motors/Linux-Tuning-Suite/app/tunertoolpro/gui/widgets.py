"""Small reusable Qt widgets: table filling and a line chart."""

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import QSizePolicy, QTableWidget, QTableWidgetItem, QWidget

PALETTE = ['#2a6fdb', '#d9534f', '#5cb85c', '#f0ad4e', '#8e44ad', '#16a085']


def _item(value, fmt):
    if isinstance(value, float):
        text = fmt.format(value)
    else:
        text = str(value)
    item = QTableWidgetItem(text)
    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    return item


def fill_grid(table, row_labels, col_labels, data, fmt='{:.2f}'):
    """Show a 2D list in a read-only QTableWidget with row and column headers."""
    table.clear()
    table.setRowCount(len(data))
    table.setColumnCount(len(col_labels))
    table.setVerticalHeaderLabels([str(r) for r in row_labels])
    table.setHorizontalHeaderLabels([str(c) for c in col_labels])
    for r, row in enumerate(data):
        for c, value in enumerate(row):
            table.setItem(r, c, _item(value, fmt))
    table.resizeColumnsToContents()


def fill_pairs(table, pairs, fmt='{:.3f}'):
    """Show (label, value) pairs as a two-column table."""
    table.clear()
    table.setRowCount(len(pairs))
    table.setColumnCount(2)
    table.setHorizontalHeaderLabels(['Item', 'Value'])
    table.verticalHeader().setVisible(False)
    for r, (label, value) in enumerate(pairs):
        table.setItem(r, 0, _item(str(label), fmt))
        table.setItem(r, 1, _item(value, fmt))
    table.resizeColumnsToContents()


def make_read_only_table():
    table = QTableWidget()
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setAlternatingRowColors(True)
    table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    return table


class LineChart(QWidget):
    """Plots one or more series against a shared x axis. Draws its own axes."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._x = []
        self._series = []  # list of (name, ys)
        self._x_label = ''
        self.setMinimumHeight(220)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_data(self, x, series, x_label=''):
        self._x = list(x)
        self._series = [(name, list(ys)) for name, ys in series]
        self._x_label = x_label
        self.update()

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor('#ffffff'))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        left, top, right, bottom = 56, 14, self.width() - 14, self.height() - 36
        plot = QRectF(left, top, max(10, right - left), max(10, bottom - top))
        painter.setPen(QPen(QColor('#888888')))
        painter.drawRect(plot)
        if len(self._x) < 2 or not self._series:
            painter.drawText(plot, Qt.AlignmentFlag.AlignCenter, 'No data')
            painter.end()
            return
        x0, x1 = min(self._x), max(self._x)
        ys_all = [y for _, ys in self._series for y in ys]
        y0, y1 = min(ys_all), max(ys_all)
        if y1 == y0:
            y1 = y0 + 1.0
        if x1 == x0:
            x1 = x0 + 1.0

        def to_px(x, y):
            px = plot.left() + (x - x0) / (x1 - x0) * plot.width()
            py = plot.bottom() - (y - y0) / (y1 - y0) * plot.height()
            return QPointF(px, py)

        painter.setFont(QFont(painter.font().family(), 8))
        painter.setPen(QColor('#333333'))
        painter.drawText(QRectF(0, plot.top() - 2, left - 6, 14),
                         Qt.AlignmentFlag.AlignRight, f'{y1:.0f}')
        painter.drawText(QRectF(0, plot.bottom() - 12, left - 6, 14),
                         Qt.AlignmentFlag.AlignRight, f'{y0:.0f}')
        painter.drawText(QRectF(plot.left(), plot.bottom() + 4, plot.width(), 16),
                         Qt.AlignmentFlag.AlignLeft, f'{x0:.1f}')
        painter.drawText(QRectF(plot.left(), plot.bottom() + 4, plot.width(), 16),
                         Qt.AlignmentFlag.AlignRight, f'{x1:.1f}  {self._x_label}')

        for i, (name, ys) in enumerate(self._series):
            pen = QPen(QColor(PALETTE[i % len(PALETTE)]))
            pen.setWidthF(1.6)
            painter.setPen(pen)
            points = [to_px(x, y) for x, y in zip(self._x, ys)]
            for a, b in zip(points, points[1:]):
                painter.drawLine(a, b)
            painter.drawText(QPointF(plot.left() + 8 + 110 * i, top + 12), name)
        painter.end()
