import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from theming import apply_dark_theme
from views import MainWindow

APP_NAME = "Uzumaki"

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    # configurar icono de la aplicación (ruta relativa al proyecto)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    icon_path = os.path.join(project_root, "IMG", "uzumaki_azul_con_letras-Photoroom.png")

    # fallback si la imagen está en un subdirectorio IMG/IMG (según su ejemplo)
    if not os.path.exists(icon_path):
        alt = os.path.join(project_root, "IMG", "IMG", "uzumaki_azul_con_letras-Photoroom.png")
        if os.path.exists(alt):
            icon_path = alt

    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    apply_dark_theme(app)
    window = MainWindow(app_name=APP_NAME)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
