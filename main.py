import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from utils import resource_path
from widgets.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("icons", "logo.ico")))
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
