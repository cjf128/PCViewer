from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ThemeManager:
    @staticmethod
    def get_dark_palette():
        palette = QPalette()
        # 基础背景与窗口
        dark_gray = QColor(45, 45, 45)
        deep_black = QColor(30, 30, 30)

        palette.setColor(QPalette.ColorRole.Window, dark_gray)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, deep_black)
        palette.setColor(QPalette.ColorRole.AlternateBase, dark_gray)
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)

        # 按钮
        palette.setColor(QPalette.ColorRole.Button, dark_gray)
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)

        # 高亮（医学软件建议用柔和的蓝色）
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)

        # 禁用状态颜色（非常重要，防止禁用按钮看不清）
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.WindowText,
            Qt.GlobalColor.gray,
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, Qt.GlobalColor.gray
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.ButtonText,
            Qt.GlobalColor.gray,
        )

        return palette

    @staticmethod
    def get_light_palette():
        palette = QPalette()
        # 窗体背景使用浅灰色 (#F5F5F5)，避免纯白刺眼
        light_gray = QColor(245, 245, 245)

        palette.setColor(QPalette.ColorRole.Window, light_gray)
        palette.setColor(QPalette.ColorRole.WindowText, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(235, 235, 235))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Text, QColor(30, 30, 30))

        # 按钮
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(30, 30, 30))

        # 高亮
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)

        # 禁用状态颜色
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.WindowText,
            Qt.GlobalColor.lightGray,
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.Text,
            Qt.GlobalColor.lightGray,
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.ButtonText,
            Qt.GlobalColor.lightGray,
        )

        return palette

    @classmethod
    def set_theme(cls, mode="dark"):
        app = QApplication.instance()
        if not app:
            return

        # 强制使用 Fusion 风格，它是基于 Palette 绘图的
        app.setStyle("Fusion")

        if mode == "dark":
            app.setPalette(cls.get_dark_palette())
        else:
            app.setPalette(cls.get_light_palette())


# 假设上面的类在 theme_manager.py 中
# from theme_manager import ThemeManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NViewer - Medical Imaging")
        self.is_dark = True

        # 初始化主题
        ThemeManager.set_theme("dark")

        # 简单的切换按钮测试
        btn = QPushButton("切换亮/暗模式")
        btn.clicked.connect(self.toggle_theme)

        layout = QVBoxLayout()
        layout.addWidget(btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        mode = "dark" if self.is_dark else "light"
        ThemeManager.set_theme(mode)
        print(f"当前模式: {mode}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
