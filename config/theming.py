from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

def apply_dark_theme(app):
    # Paleta oscura limpia y con buen contraste
    palette = QPalette()
    base = QColor(28, 28, 33)
    alt_base = QColor(38, 38, 45)
    text = QColor(230, 230, 235)
    subtle = QColor(160, 160, 170)
    primary = QColor(90, 136, 255)     # azul acento
    highlight = QColor(60, 90, 200)

    palette.setColor(QPalette.Window, base)
    palette.setColor(QPalette.WindowText, text)
    palette.setColor(QPalette.Base, alt_base)
    palette.setColor(QPalette.AlternateBase, base)
    palette.setColor(QPalette.ToolTipBase, alt_base)
    palette.setColor(QPalette.ToolTipText, text)
    palette.setColor(QPalette.Text, text)
    palette.setColor(QPalette.Button, alt_base)
    palette.setColor(QPalette.ButtonText, text)
    palette.setColor(QPalette.BrightText, QColor(Qt.red))
    palette.setColor(QPalette.Highlight, primary)
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.PlaceholderText, subtle)

    app.setStyle("Fusion")
    app.setPalette(palette)
    app.setStyleSheet("""
        QLineEdit, QTextEdit, QPlainTextEdit, QListWidget, QTreeWidget, QTextBrowser {
            border: 1px solid #3e3e46; border-radius: 6px; padding: 6px;
            selection-background-color: #5a88ff;
        }
        QPushButton {
            background-color: #2f2f37; border: 1px solid #494950; border-radius: 8px; padding: 8px 12px;
        }
        QPushButton:hover { background-color: #3a3a43; }
        QPushButton:pressed { background-color: #32323a; }
        QPushButton[accent="true"] { background-color: #5a88ff; color: white; border: none; }
        QToolBar { border: none; spacing: 6px; }
        QStatusBar { border-top: 1px solid #3e3e46; }
        QListWidget::item { padding: 8px; }
        QListWidget::item:selected { background: #3d4f7d; color: white; }
        QLabel[hint="true"] { color: #a0a0aa; }
        QScrollBar:vertical { width: 10px; background: #2c2c32; }
        QScrollBar::handle:vertical { background: #4a4a52; border-radius: 5px; min-height: 30px; }
        QScrollBar::add-line, QScrollBar::sub-line { background: none; height: 0px; }
    """)
# Aplica un tema oscuro con buen contraste y colores agradables