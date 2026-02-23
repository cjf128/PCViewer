import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication, QWidget

from ui.SegmentDock_ui import Ui_Form


class SegmentDocker(QWidget, Ui_Form):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi(self)
        self.init_connectAction()

    def init_connectAction(self):
        """初始化信号与槽连接"""
        self.sldAlphaSeg.valueChanged.connect(
            lambda v: self.boxAlphaSeg.setValue(v / 100)
        )
        self.boxAlphaSeg.valueChanged.connect(
            lambda v: self.sldAlphaSeg.setValue(int(v * 100))
        )
        self.boxAlphaSeg.valueChanged.connect(
            lambda v: self.main_window.update_property_and_refresh("seg_alpha", v)
        )
        self.boxPaint.valueChanged.connect(
            lambda v: self.main_window.update_property_and_refresh("radius", v)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SegmentDocker(None, None)
    window.show()
    sys.exit(app.exec())
