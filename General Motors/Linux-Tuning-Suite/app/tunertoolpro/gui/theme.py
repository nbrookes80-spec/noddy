"""Colour palette, stylesheet and icons. Icons come from the desktop theme's standard set, so no image files are needed."""

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QStyle

# Palette: midnight indigo base, hot-pink accent, electric cyan highlight. Every colour in the app
# comes from this dict; docs/DESIGN_TEMPLATE.md describes each token and how to change it.
PALETTE = {
    'window': '#0d0f24', 'base': '#171a38', 'alt': '#222650', 'text': '#f5f7ff', 'muted': '#aab1e0',
    'accent': '#ff2e7e', 'accent_hover': '#ff5c9a', 'accent2': '#ff9f1c', 'highlight': '#00e5ff',
    'good': '#2bff9a', 'warn': '#ffc247', 'bad': '#ff4d6d', 'border': '#3d4386',
}


def apply(app):
    """Set a dark palette and a stylesheet on the application. Safe to call once at start-up."""
    p = PALETTE
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor(p['window']))
    pal.setColor(QPalette.ColorRole.WindowText, QColor(p['text']))
    pal.setColor(QPalette.ColorRole.Base, QColor(p['base']))
    pal.setColor(QPalette.ColorRole.AlternateBase, QColor(p['alt']))
    pal.setColor(QPalette.ColorRole.Text, QColor(p['text']))
    pal.setColor(QPalette.ColorRole.Button, QColor(p['alt']))
    pal.setColor(QPalette.ColorRole.ButtonText, QColor(p['text']))
    pal.setColor(QPalette.ColorRole.Highlight, QColor(p['highlight']))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor('#0b0e11'))
    app.setPalette(pal)
    app.setStyleSheet(f"""
        QMainWindow, QWidget {{ background: {p['window']}; color: {p['text']}; }}
        QGroupBox {{ border: 1px solid {p['border']}; border-radius: 6px; margin-top: 14px; padding: 10px; }}
        QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 6px; color: {p['highlight']}; }}
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QPlainTextEdit, QTextEdit, QTableWidget, QListWidget {{
            background: {p['base']}; border: 1px solid {p['border']}; border-radius: 4px; padding: 3px;
            selection-background-color: {p['highlight']}; selection-color: #0b0e11; }}
        QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {p['accent']}, stop:1 {p['accent2']});
            color: white; border: none; border-radius: 6px; padding: 6px 14px; font-weight: 700; }}
        QPushButton:hover {{ background: {p['accent_hover']}; }}
        QPushButton:disabled {{ background: {p['alt']}; color: {p['muted']}; }}
        QPushButton[role="secondary"] {{ background: {p['alt']}; border: 1px solid {p['highlight']}; color: {p['highlight']}; }}
        QPushButton[role="secondary"]:hover {{ background: {p['border']}; }}
        QTabWidget::pane {{ border: 1px solid {p['border']}; border-radius: 4px; }}
        QTabBar::tab {{ background: {p['alt']}; color: {p['muted']}; padding: 7px 14px; margin-right: 2px;
            border-top-left-radius: 5px; border-top-right-radius: 5px; }}
        QTabBar::tab:selected {{ background: {p['accent']}; color: white; font-weight: 600; }}
        QTabBar::tab:hover:!selected {{ color: {p['text']}; }}
        QHeaderView::section {{ background: {p['alt']}; color: {p['highlight']}; border: none;
            border-bottom: 1px solid {p['border']}; padding: 4px; font-weight: 600; }}
        QTableWidget {{ gridline-color: {p['border']}; }}
        QStatusBar {{ background: {p['alt']}; color: {p['muted']}; }}
        QLabel[role="good"] {{ color: {p['good']}; font-weight: 600; }}
        QLabel[role="warn"] {{ color: {p['warn']}; font-weight: 600; }}
        QLabel[role="bad"] {{ color: {p['bad']}; font-weight: 600; }}
        QLabel[role="muted"] {{ color: {p['muted']}; }}
        QScrollBar:vertical {{ background: {p['base']}; width: 12px; }}
        QScrollBar::handle:vertical {{ background: {p['border']}; border-radius: 5px; min-height: 24px; }}
    """)


def icon(widget, name):
    """A standard icon for a button. name is one of the keys in ICONS."""
    style = widget.style()
    return style.standardIcon(ICONS.get(name, QStyle.StandardPixmap.SP_FileIcon))


ICONS = {
    'calculate': QStyle.StandardPixmap.SP_MediaPlay,
    'save': QStyle.StandardPixmap.SP_DialogSaveButton,
    'open': QStyle.StandardPixmap.SP_DialogOpenButton,
    'reload': QStyle.StandardPixmap.SP_BrowserReload,
    'export': QStyle.StandardPixmap.SP_DialogSaveButton,
    'ask': QStyle.StandardPixmap.SP_MessageBoxQuestion,
    'apply': QStyle.StandardPixmap.SP_DialogApplyButton,
    'reject': QStyle.StandardPixmap.SP_DialogCancelButton,
    'check': QStyle.StandardPixmap.SP_DialogYesButton,
    'warn': QStyle.StandardPixmap.SP_MessageBoxWarning,
    'info': QStyle.StandardPixmap.SP_MessageBoxInformation,
    'error': QStyle.StandardPixmap.SP_MessageBoxCritical,
    'help': QStyle.StandardPixmap.SP_DialogHelpButton,
    'key': QStyle.StandardPixmap.SP_DriveNetIcon,
}
