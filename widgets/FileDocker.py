import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QInputDialog, QMenu, QMessageBox, QWidget

from ui.FileDock_ui import Ui_Form
from app.configs import ConfigManager


class FileDocker(QWidget, Ui_Form):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi(self)
        self.config()

    def config(self) -> None:
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["数据名称"])
        self.treeView.setModel(self.model)

        # 设置TreeView属性，去除空白列
        self.treeView.setRootIsDecorated(False)  # 不显示展开/折叠图标
        self.treeView.header().setStretchLastSection(True)  # 自动拉伸最后一列

        # 连接双击信号
        self.treeView.doubleClicked.connect(self.on_item_double_clicked)
        # 连接右键菜单信号
        self.treeView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.on_context_menu)

        # 加载文件列表
        self.load_file_list()

    def load_file_list(self):
        """加载已导入的文件列表"""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["数据名称"])

        if self.main_window and hasattr(self.main_window, "_config"):
            data = self.main_window._config.data

            # 记录本轮已添加的名称，用于排重
            used_names = set()

            for data_id, info in data.items():
                # 1. 确定基础 data_name
                # 优先使用配置中存储的名称
                raw_name = info.get("name")

                # 如果没有存储名称，则从 PET 文件路径中提取
                if not raw_name:
                    pet_path = info.get("pet", "")
                    if pet_path:
                        raw_name = Path(pet_path).name
                    else:
                        raw_name = f"数据_{data_id}"

                # 2. 取以 "." 分隔的第一个字符串
                # 例如 "case_001.nii.gz" -> "case_001"
                base_name = raw_name.split(".")[0]

                # 3. 检查重名并自动添加后缀 (_1, _2, ...)
                final_name = base_name
                counter = 1
                while final_name in used_names:
                    final_name = f"{base_name}_{counter}"
                    counter += 1

                # 将确定不重复的名称加入集合
                used_names.add(final_name)

                # 4. 添加到模型
                row = [QStandardItem(final_name)]
                # 存储数据 ID，注意此处使用 Qt.ItemDataRole.UserRole 以符合 Qt 6 规范
                row[0].setData(data_id, Qt.ItemDataRole.UserRole)
                self.model.appendRow(row)

        # 调整列宽以适应内容
        self.treeView.resizeColumnToContents(0)

    def on_item_double_clicked(self, index):
        """双击文件列表项重新导入"""
        # 获取双击的item
        item = self.model.itemFromIndex(index)
        # 从item的data中获取数据ID
        data_id = item.data(Qt.UserRole)

        if data_id and self.main_window and hasattr(self.main_window, "reload_data"):
            # 调用MainWindow的reload_data方法重新导入
            self.main_window.reload_data(data_id)

    def on_context_menu(self, position):
        """右键菜单"""
        # 获取当前选中的项
        index = self.treeView.indexAt(position)
        if not index.isValid():
            return

        # 创建右键菜单
        menu = QMenu()
        rename_action = menu.addAction("重命名")
        delete_action = menu.addAction("删除")

        # 连接菜单项的触发信号
        rename_action.triggered.connect(lambda: self.rename_data(index))
        delete_action.triggered.connect(lambda: self.delete_data(index))

        # 显示菜单
        menu.exec(self.treeView.mapToGlobal(position))

    def rename_data(self, index):
        """重命名数据"""
        # 获取选中的item
        item = self.model.itemFromIndex(index)
        # 从item的data中获取数据ID
        data_id = item.data(Qt.UserRole)

        if data_id and self.main_window and hasattr(self.main_window, "_config"):
            # 弹出输入对话框，让用户输入新的名称
            new_name, ok = QInputDialog.getText(
                self, "重命名", "请输入新的名称:", text=item.text()
            )

            if ok and new_name:
                # 更新配置中的数据名称
                if data_id in self.main_window._config.data:
                    self.main_window._config.data[data_id]["name"] = new_name

                    config_manager = ConfigManager()
                    config_manager.save(self.main_window._config)

                    # 更新文件列表
                    self.load_file_list()

    def delete_data(self, index):
        """删除数据"""
        # 获取选中的item
        item = self.model.itemFromIndex(index)
        # 从item的data中获取数据ID
        data_id = item.data(Qt.UserRole)

        if data_id and self.main_window and hasattr(self.main_window, "_config"):
            # 显示确认对话框
            reply = QMessageBox.question(
                self,
                "确认删除",
                f"确定要删除数据 {item.text()} 吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                # 从配置中删除数据
                if data_id in self.main_window._config.data:
                    del self.main_window._config.data[data_id]

                    # 保存配置
                    from app.configs import ConfigManager

                    config_manager = ConfigManager()
                    config_manager.save(self.main_window._config)

                    # 更新文件列表
                    self.load_file_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileDocker(None, None)
    window.show()
    sys.exit(app.exec())
