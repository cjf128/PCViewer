import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication, QWidget, QButtonGroup

from app.mode import SAMMode
from ui.DLDock_ui import Ui_Form


class DLDocker(QWidget, Ui_Form):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi(self)
        
        # 创建互斥按钮组
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.button_group.addButton(self.pushButton)
        self.button_group.addButton(self.pushButton_2)
        self.button_group.addButton(self.pushButton_3)
        
        # 连接按钮点击事件
        self.pushButton.clicked.connect(self.on_add_button_clicked)
        self.pushButton_2.clicked.connect(self.on_box_button_clicked)
        self.pushButton_3.clicked.connect(self.on_sub_button_clicked)
        
        self.current_mode = SAMMode.BOX
    
    def on_box_button_clicked(self):
        """Box模式"""
        self.current_mode = SAMMode.BOX
    
    def on_add_button_clicked(self):
        """Add模式"""
        self.current_mode = SAMMode.ADD
    
    def on_sub_button_clicked(self):
        """Sub模式"""
        self.current_mode = SAMMode.SUB


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DLDocker(None, None)
    window.show()
    sys.exit(app.exec())
