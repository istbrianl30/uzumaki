from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton
from PySide6.QtCore import Qt
from models import Card

class CardEditor(QDialog):
    def __init__(self, parent=None, card: Card | None = None):
        super().__init__(parent)
        self.setWindowTitle("Uzumaki — Editor de ficha")
        self.setMinimumSize(560, 480)
        self._card = card

        layout = QVBoxLayout(self)

        row1 = QHBoxLayout()
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Título")
        row1.addWidget(QLabel("Título:"))
        row1.addWidget(self.title_edit)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Etiquetas separadas por comas (ej. ciencia, notas)")
        row2.addWidget(QLabel("Etiquetas:"))
        row2.addWidget(self.tags_edit)
        layout.addLayout(row2)

        layout.addWidget(QLabel("Contenido (formato ligero tipo Markdown):"))
        self.content_edit = QPlainTextEdit()
        self.content_edit.setPlaceholderText("# Encabezado\n\n- Lista 1\n- Lista 2\n\n**negritas** y *cursivas*")
        layout.addWidget(self.content_edit, 1)

        btns = QHBoxLayout()
        btns.addStretch(1)
        self.cancel_btn = QPushButton("Cancelar")
        self.save_btn = QPushButton("Guardar")
        self.save_btn.setProperty("accent", True)
        btns.addWidget(self.cancel_btn)
        btns.addWidget(self.save_btn)
        layout.addLayout(btns)

        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.accept)

        if card:
            self.title_edit.setText(card.title)
            self.content_edit.setPlainText(card.content)
            self.tags_edit.setText(", ".join(card.tags))

    def get_card_data(self) -> tuple[str, str, list[str]]:
        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText()
        tags = [t.strip() for t in self.tags_edit.text().split(",") if t.strip()]
        return title, content, tags
