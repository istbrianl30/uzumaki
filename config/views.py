from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QTextBrowser, QLineEdit, QLabel, QToolBar, QPushButton, QFileDialog, QStatusBar
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QAction, QIcon
from models import Card
from storage import load_all_cards, save_card, update_card_file
from utils import generate_id, get_cards_dir
from renderer import md_to_html
from editor import CardEditor
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self, app_name: str = "Uzumaki"):
        super().__init__()
        self.setWindowTitle(app_name)
        self.resize(1080, 720)

        self.cards_dir = get_cards_dir()
        self.items: list[tuple[Path, Card]] = []
        self.filtered_indices: list[int] = []
        self.selected_index: int | None = None

        self._build_ui()
        self._load_cards()

    def _build_ui(self):
        # Toolbar superior
        toolbar = QToolBar("Acciones")
        toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(toolbar)

        new_action = QAction("Nuevo", self)
        edit_action = QAction("Editar", self)
        export_action = QAction("Exportar .py", self)
        import_action = QAction("Importar .py", self)
        open_folder_action = QAction("Abrir carpeta", self)

        toolbar.addAction(new_action)
        toolbar.addAction(edit_action)
        toolbar.addSeparator()
        toolbar.addAction(export_action)
        toolbar.addAction(import_action)
        toolbar.addSeparator()
        toolbar.addAction(open_folder_action)

        new_action.triggered.connect(self._new_card)
        edit_action.triggered.connect(self._edit_card)
        export_action.triggered.connect(self._export_card)
        import_action.triggered.connect(self._import_card)
        open_folder_action.triggered.connect(self._open_folder)

        # Área central
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        left = QVBoxLayout()
        layout.addLayout(left, 1)

        # Búsqueda
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Buscar por título, contenido o etiqueta...")
        left.addWidget(self.search_edit)

        self.hint_lbl = QLabel("Consejo: usa #etiqueta para filtrar por etiqueta exacta.")
        self.hint_lbl.setProperty("hint", True)
        left.addWidget(self.hint_lbl)

        # Lista de fichas
        self.list_widget = QListWidget()
        left.addWidget(self.list_widget, 1)

        # Vista previa
        right = QVBoxLayout()
        layout.addLayout(right, 2)
        self.preview = QTextBrowser()
        self.preview.setOpenExternalLinks(True)
        right.addWidget(self.preview, 1)

        # Botones de acción rápida
        quick = QHBoxLayout()
        self.btn_new = QPushButton("Nueva ficha")
        self.btn_new.setProperty("accent", True)
        self.btn_edit = QPushButton("Editar")
        self.btn_export = QPushButton("Exportar")
        self.btn_import = QPushButton("Importar")
        quick.addWidget(self.btn_new)
        quick.addWidget(self.btn_edit)
        quick.addWidget(self.btn_export)
        quick.addWidget(self.btn_import)
        right.addLayout(quick)

        self.btn_new.clicked.connect(self._new_card)
        self.btn_edit.clicked.connect(self._edit_card)
        self.btn_export.clicked.connect(self._export_card)
        self.btn_import.clicked.connect(self._import_card)

        # Conexiones
        self.list_widget.currentRowChanged.connect(self._on_select)
        self.search_edit.textChanged.connect(self._on_search_text_changed)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Búsqueda con debounce para fluidez
        self._search_timer = QTimer()
        self._search_timer.setInterval(150)
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._apply_filter)

    def _load_cards(self):
        self.items = load_all_cards(self.cards_dir)
        self._apply_filter()
        self.status.showMessage(f"{len(self.items)} fichas cargadas", 2000)

    def _apply_filter(self):
        query = self.search_edit.text().strip().lower()
        tag_filter = None
        if query.startswith("#") and " " not in query:
            tag_filter = query[1:]

        self.list_widget.clear()
        self.filtered_indices = []
        for idx, (path, card) in enumerate(self.items):
            haystack = f"{card.title}\n{card.content}\n{' '.join(card.tags)}".lower()
            if tag_filter is not None:
                if tag_filter in [t.lower() for t in card.tags]:
                    self._add_item(idx, card)
            else:
                if all(q in haystack for q in query.split()):
                    self._add_item(idx, card)

        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)
        else:
            self.preview.setHtml("<h2>Sin resultados</h2><p>Intenta otra búsqueda.</p>")

    def _add_item(self, idx: int, card: Card):
        item = QListWidgetItem(f"{card.title}    —    {', '.join(card.tags)}")
        self.list_widget.addItem(item)
        self.filtered_indices.append(idx)

    def _on_search_text_changed(self, _):
        self._search_timer.start()

    def _on_select(self, row: int):
        if row < 0 or row >= len(self.filtered_indices):
            self.selected_index = None
            self.preview.setHtml("<p>Selecciona una ficha para ver la vista previa.</p>")
            return
        self.selected_index = self.filtered_indices[row]
        _, card = self.items[self.selected_index]
        html = md_to_html(card.content)
        # Inyecta título simple
        self.preview.setHtml(f"<h2>{card.title}</h2>" + html)

    def _new_card(self):
        from utils import generate_id
        dlg = CardEditor(self)
        if dlg.exec():
            title, content, tags = dlg.get_card_data()
            if not title:
                title = "(Sin título)"
            card = Card(id=generate_id(), title=title, content=content, tags=tags)
            path = save_card(card, self.cards_dir)
            self.items.insert(0, (path, card))
            self._apply_filter()
            self.status.showMessage("Ficha creada", 2000)

    def _edit_card(self):
        if self.selected_index is None:
            self.status.showMessage("Selecciona una ficha para editar", 2000)
            return
        path, card = self.items[self.selected_index]
        dlg = CardEditor(self, card)
        if dlg.exec():
            title, content, tags = dlg.get_card_data()
            card.title = title or card.title
            card.content = content
            card.tags = tags
            card.update_timestamp()
            update_card_file(path, card)
            self._apply_filter()
            self.status.showMessage("Ficha actualizada", 2000)

    def _export_card(self):
        if self.selected_index is None:
            self.status.showMessage("Selecciona una ficha para exportar", 2000)
            return
        path, card = self.items[self.selected_index]
        dest, _ = QFileDialog.getSaveFileName(self, "Exportar ficha como .py", f"{card.title}.py", "Python (*.py)")
        if dest:
            try:
                # Simplemente copia el archivo fuente de la ficha
                Path(dest).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
                self.status.showMessage("Ficha exportada", 2000)
            except Exception as e:
                self.status.showMessage(f"Error al exportar: {e}", 4000)

    def _import_card(self):
        src, _ = QFileDialog.getOpenFileName(self, "Importar ficha .py", str(self.cards_dir), "Python (*.py)")
        if not src:
            return
        try:
            src_path = Path(src)
            # Valida cargando y luego guarda con nuevo nombre (no sobrescribe)
            from storage import load_card_from_py, save_card
            card = load_card_from_py(src_path)
            # Mantén su ID y timestamps para portabilidad auténtica
            dest = save_card(card, self.cards_dir)
            self.items.insert(0, (dest, card))
            self._apply_filter()
            self.status.showMessage("Ficha importada", 2000)
        except Exception as e:
            self.status.showMessage(f"Error al importar: {e}", 4000)

    def _open_folder(self):
        # Abre la carpeta de fichas en el explorador
        folder = str(self.cards_dir)
        from PySide6.QtGui import QDesktopServices
        from PySide6.QtCore import QUrl
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder))
        
        