import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication, QWidget, QTreeView, QMenu, QMessageBox, QInputDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from ui.FileDock_ui import Ui_Form


class FileDocker(QWidget, Ui_Form):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi(self)
        self.config()

    def config(self) -> None:
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['数据名称'])
        self.treeView.setModel(self.model)
        
        # 设置TreeView属性，去除空白列
        self.treeView.setRootIsDecorated(False)  # 不显示展开/折叠图标
        self.treeView.header().setStretchLastSection(True)  # 自动拉伸最后一列
        
        # 连接双击信号
        self.treeView.doubleClicked.connect(self.on_item_double_clicked)
        # 连接右键菜单信号
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.on_context_menu)
        
        # 加载文件列表
        self.load_file_list()
    
    def load_file_list(self):
        """加载已导入的文件列表"""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['数据名称'])
        
        if self.main_window and hasattr(self.main_window, '_config'):
            data = self.main_window._config.data
            for data_id, info in data.items():
                # 优先使用配置中存储的名称
                data_name = info.get('name')
                
                # 如果没有存储名称，则从PET文件路径中提取
                if not data_name:
                    pet_path = info.get('pet', '')
                    if pet_path:
                        data_name = Path(pet_path).name
                        # 移除文件扩展名
                        data_name = '.'.join(data_name.split('.')[:-1])
                    else:
                        data_name = f"数据 {data_id}"
                
                # 只添加数据名称列
                row = [QStandardItem(data_name)]
                # 存储数据ID作为item的data，方便双击时获取
                row[0].setData(data_id, Qt.UserRole)
                self.model.appendRow(row)
        
        # 调整列宽以适应内容
        self.treeView.resizeColumnToContents(0)
    
    def on_item_double_clicked(self, index):
        """双击文件列表项重新导入"""
        # 获取双击的item
        item = self.model.itemFromIndex(index)
        # 从item的data中获取数据ID
        data_id = item.data(Qt.UserRole)
        
        if data_id and self.main_window and hasattr(self.main_window, 'reload_data'):
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
        
        if data_id and self.main_window and hasattr(self.main_window, '_config'):
            # 弹出输入对话框，让用户输入新的名称
            new_name, ok = QInputDialog.getText(
                self, "重命名", f"请输入新的名称:",
                text=item.text()
            )
            
            if ok and new_name:
                # 更新配置中的数据名称
                if data_id in self.main_window._config.data:
                    self.main_window._config.data[data_id]['name'] = new_name
                    
                    # 保存配置
                    from app.configs import ConfigManager
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
        
        if data_id and self.main_window and hasattr(self.main_window, '_config'):
            # 显示确认对话框
            reply = QMessageBox.question(
                self, "确认删除", f"确定要删除数据 {item.text()} 吗？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
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
