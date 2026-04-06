import sys
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QMessageBox,
    QPushButton,
)

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))


from ui.ShortcutDialog_ui import Ui_Dialog


class ShortcutDialog(QDialog, Ui_Dialog):
    """快捷键设置对话框"""

    shortcuts_changed = Signal(dict)  # 发送快捷键更改信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._main_window = parent

        # 快捷键编辑控件与 MainWindow action 的映射
        self._shortcuts_mapping = {
            "load_atn": self.load_Edit,
            "aim_atn": self.aim_edit,
            "paint_atn": self.paint_Edit,
            "add_atn": self.add_Edit,
            "move_atn": self.move_Edit,
            "eraser_atn": self.eraser_Edit,
            "save_atn": self.save_Edit,
            "win_atn": self.win_Edit,
            "sam_atn": self.SAM_Edit,
        }

        self.setWindowTitle("快捷键设置")
        self.setWindowModality(Qt.WindowModality.WindowModal)

        # 保存初始快捷键状态（打开对话框时的状态）
        self._initial_shortcuts = {}
        # 保存前一个有效状态（用于冲突时回滚）
        self._previous_valid_shortcuts = {}
        # 标志：是否正在恢复快捷键（禁用检查信号）
        self._restoring_shortcut = False

        # 从 MainWindow 加载当前快捷键
        self._load_shortcuts_from_mainwindow()

        # 保存加载后的初始状态
        self._save_initial_state()

        # 添加复原按钮
        self.reset_button = QPushButton("复原")
        self.reset_button.clicked.connect(self._reset_shortcuts)
        self.buttonBox.addButton(
            self.reset_button, QDialogButtonBox.ButtonRole.ResetRole
        )

        # 连接按钮信号
        self.buttonBox.accepted.connect(self._on_ok_clicked)
        self.buttonBox.rejected.connect(self._on_cancel_clicked)

        # 为每个快捷键编辑控件连接信号，实时检查冲突
        self._connect_shortcut_change_signals()

    def _load_shortcuts_from_mainwindow(self):
        """从 MainWindow 加载当前的快捷键设置"""
        if self._main_window is None:
            return

        for action_name, edit_widget in self._shortcuts_mapping.items():
            if hasattr(self._main_window, action_name):
                action = getattr(self._main_window, action_name)
                shortcut = action.shortcut()
                edit_widget.setKeySequence(shortcut)

    def _save_initial_state(self):
        """保存当前的快捷键状态作为初始状态"""
        for action_name, edit_widget in self._shortcuts_mapping.items():
            key_sequence = edit_widget.keySequence().toString()
            self._initial_shortcuts[action_name] = key_sequence
            self._previous_valid_shortcuts[action_name] = (
                key_sequence  # 同时保存为前一个有效状态
            )

    def _reset_shortcuts(self):
        """恢复快捷键到初始状态（打开对话框时的状态）"""
        self._restoring_shortcut = True
        for action_name, key_sequence in self._initial_shortcuts.items():
            edit_widget = self._shortcuts_mapping[action_name]
            edit_widget.setKeySequence(key_sequence)
        self._restoring_shortcut = False

        # 更新前一个有效状态
        self._previous_valid_shortcuts = self._initial_shortcuts.copy()

    def _connect_shortcut_change_signals(self):
        """为每个快捷键编辑控件连接信号"""
        for action_name, edit_widget in self._shortcuts_mapping.items():
            # 使用 lambda 捕获 action_name
            edit_widget.editingFinished.connect(
                lambda an=action_name: self._on_shortcut_edited(an)
            )

    def _on_shortcut_edited(self, action_name: str):
        """当某个快捷键编辑完成时的处理"""
        # 如果正在恢复快捷键，不再进行检查
        if self._restoring_shortcut:
            return

        # 收集所有快捷键设置
        shortcuts_dict = {}
        for an, edit_widget in self._shortcuts_mapping.items():
            key_sequence = edit_widget.keySequence().toString()
            shortcuts_dict[an] = key_sequence

        # 检查快捷键冲突
        is_valid, error_msg = self._check_shortcut_conflicts(shortcuts_dict)
        if not is_valid:
            QMessageBox.warning(
                self, "快捷键冲突", error_msg, QMessageBox.StandardButton.Ok
            )
            # 恢复引起冲突的快捷键到前一个有效状态
            self._restoring_shortcut = True
            edit_widget = self._shortcuts_mapping[action_name]
            edit_widget.setKeySequence(self._previous_valid_shortcuts[action_name])
            self._restoring_shortcut = False
        else:
            # 无冲突，保存当前状态为有效状态
            for an, key_sequence in shortcuts_dict.items():
                self._previous_valid_shortcuts[an] = key_sequence

    def _on_cancel_clicked(self):
        """取消按钮被点击时的处理 - 不应用任何更改"""
        self.reject()

    def _check_shortcut_conflicts(self, shortcuts_dict: dict) -> tuple[bool, str]:
        """
        检查快捷键冲突

        Args:
            shortcuts_dict: 快捷键设置字典

        Returns:
            (is_valid, error_message) - 元组，第一项为是否有效，第二项为错误信息
        """
        # 检查快捷键中的重复
        used_shortcuts = {}
        conflicts = []

        for action_name, key_sequence in shortcuts_dict.items():
            # 跳过空快捷键
            if not key_sequence or key_sequence.strip() == "":
                continue

            # 检查是否已使用
            if key_sequence in used_shortcuts:
                conflicts.append(
                    f"快捷键 '{key_sequence}' 被多次使用:\n"
                    f"  - {self._get_action_label(used_shortcuts[key_sequence])}\n"
                    f"  - {self._get_action_label(action_name)}"
                )
            else:
                used_shortcuts[key_sequence] = action_name

        if conflicts:
            error_msg = "检测到快捷键冲突！请修改:\n\n" + "\n\n".join(conflicts)
            return False, error_msg

        return True, ""

    def _get_action_label(self, action_name: str) -> str:
        """获取 action 的可读标签"""
        labels = {
            "load_atn": "导入数据",
            "aim_atn": "准心工具",
            "paint_atn": "标注工具",
            "add_atn": "导入标注",
            "move_atn": "移动工具",
            "eraser_atn": "擦除工具",
            "save_atn": "保存文件",
            "win_atn": "调窗工具",
            "sam_atn": "SAM工具",
        }
        return labels.get(action_name, action_name)

    def _on_ok_clicked(self):
        """确定按钮被点击时的处理"""
        shortcuts_dict = {}

        # 收集所有快捷键设置
        for action_name, edit_widget in self._shortcuts_mapping.items():
            key_sequence = edit_widget.keySequence().toString()
            shortcuts_dict[action_name] = key_sequence

        # 应用快捷键到 MainWindow
        if self._main_window is not None:
            for action_name, key_sequence in shortcuts_dict.items():
                if hasattr(self._main_window, action_name):
                    action = getattr(self._main_window, action_name)
                    action.setShortcut(key_sequence)

        # 发送信号
        self.shortcuts_changed.emit(shortcuts_dict)

        # 关闭对话框
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShortcutDialog(None)
    window.show()
    sys.exit(app.exec())
