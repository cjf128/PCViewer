import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication, QWidget

from ui.SamDock_ui import Ui_Form


class SamDocker(QWidget, Ui_Form):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SamDocker(None, None)
    window.show()
    sys.exit(app.exec())
