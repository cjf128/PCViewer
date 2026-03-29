import sys

# 导入系统模块，用于判断是否为主程序入口
from pathlib import Path

# 判断是否为直接运行程序，如果是则添加父目录到Python路径
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入PySide6核心模块：Qt命名空间（包含枚举常量）、信号机制
from PySide6.QtCore import Qt, Signal

# 导入PySide6 GUI模块：标准项（用于树形列表）、标准项模型
from PySide6.QtGui import QStandardItem, QStandardItemModel

# 导入PySide6 widgets模块：应用程序、输入对话框、菜单、消息框、基础窗口部件
from PySide6.QtWidgets import QApplication, QInputDialog, QMenu, QMessageBox, QWidget

# 导入配置管理模块，用于保存和加载配置文件
from app.configs import ConfigManager

# 导入UI生成的界面类
from ui.FileDock_ui import Ui_Form


class FileDocker(QWidget, Ui_Form):
    """文件管理器窗口部件，用于显示和管理已导入的医学影像文件列表"""

    # 定义信号，用于向主窗口传递文件名（患者名称）
    # 当用户双击文件或重命名文件时发出，接收者为MainWindow再传给ImageViewer显示
    file_name = Signal(str)

    def __init__(self, parent, main_window):
        """
        初始化文件管理器

        参数:
            parent: 父窗口部件
            main_window: 主窗口引用，用于访问配置和调用主窗口方法
        """
        super().__init__(parent)  # 调用父类QWidget的构造函数
        self.main_window = main_window  # 保存主窗口引用，以便后续访问配置和数据
        self.setupUi(self)  # 由Qt Designer生成的UI文件提供，初始化界面控件
        self.config()  # 初始化配置，包括设置模型和连接信号

    def config(self) -> None:
        """
        初始化文件管理器的配置
        设置TreeView的模型、信号连接和初始文件列表加载
        """
        # 创建标准项模型，用于存储文件列表数据（类似于表格模型）
        self.model = QStandardItemModel()
        # 设置模型的水平表头标签，即列名
        self.model.setHorizontalHeaderLabels(["数据名称"])
        # 将模型设置到TreeView（树形视图）控件上
        self.treeView.setModel(self.model)

        # ========== 设置TreeView的显示属性 ==========
        # 设置不显示展开/折叠图标（因为是单层列表，不需要树形结构）
        self.treeView.setRootIsDecorated(False)
        # 设置最后一列自动拉伸以填满可用空间
        self.treeView.header().setStretchLastSection(True)

        # ========== 连接信号与槽函数 ==========
        # 连接双击信号：当用户双击列表项时触发on_item_double_clicked
        self.treeView.doubleClicked.connect(self.on_item_double_clicked)
        # 设置右键菜单策略为自定义菜单
        self.treeView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # 连接右键菜单请求信号：当用户右键点击时触发on_context_menu
        self.treeView.customContextMenuRequested.connect(self.on_context_menu)

        # 初始化加载文件列表
        self.load_file_list()

    def load_file_list(self):
        """
        加载已导入的文件列表（增量更新模式）

        对比当前模型中的数据ID和配置中的数据ID，找出需要添加和需要删除的项
        只更新变化的项，避免每次都清空重载导致闪烁或性能问题

        返回:
            无
        """
        # 检查主窗口和配置是否存在，不存在则直接返回
        if not self.main_window or not hasattr(self.main_window, "_config"):
            return

        # 从主窗口的配置中获取数据字典
        # 格式: {"1": {"pet": "path", "ct": "path", "type": "DICOM", "name": "case1"}, ...}
        data = self.main_window._config.data
        # 如果数据为空，直接返回（避免后续遍历空字典）
        if not data:
            return

        # ========== 第一步：获取当前模型中已有的数据ID集合 ==========
        # 用于与配置中的数据对比，找出差异
        existing_ids = set()  # 创建空集合，存储当前模型中所有数据的ID
        # 遍历模型中的所有行（每个行对应一个文件项）
        for row in range(self.model.rowCount()):
            # 获取指定行第0列的项
            item = self.model.item(row, 0)
            if item:
                # 从项的UserRole中获取data_id，并转换为字符串统一格式
                existing_ids.add(str(item.data(Qt.ItemDataRole.UserRole)))

        # ========== 第二步：计算需要添加和需要删除的ID ==========
        # 将配置中所有key转换为字符串集合
        new_ids = set(str(k) for k in data.keys())
        # 集合差运算：新ID中有但模型中没有的 = 需要新增的
        ids_to_add = new_ids - existing_ids
        # 集合差运算：模型中有但新ID中没有的 = 需要删除的
        ids_to_remove = existing_ids - new_ids

        # ========== 第三步：删除已不存在的项 ==========
        # 遍历需要删除的ID
        for data_id in ids_to_remove:
            # 在模型中查找对应ID的项并删除
            for row in range(self.model.rowCount()):
                item = self.model.item(row, 0)
                # 比较时都转为字符串，确保类型一致
                if item and str(item.data(Qt.ItemDataRole.UserRole)) == data_id:
                    self.model.removeRow(row)  # 删除该行
                    break  # 删除后跳出内层循环，继续处理下一个ID

        # ========== 第四步：收集当前模型中已有的名称，用于重名检测 ==========
        # 创建集合存储现有名称，避免新增项与现有项重名
        used_names = set(
            self.model.item(row, 0).text() for row in range(self.model.rowCount())
        )

        # ========== 第五步：添加新增的数据项 ==========
        # 对新增ID进行排序，确保按数字顺序添加（如1,2,3而不是随机顺序）
        for data_id in sorted(
            ids_to_add, key=lambda x: int(x) if x.isdigit() else float("inf")
        ):
            # 获取数据项信息，处理字符串和整数key两种情况
            info = data.get(data_id) or (
                data.get(int(data_id)) if data_id.isdigit() else None
            )
            if not info:  # 如果获取不到信息，跳过该项
                continue

            # ========== 获取文件显示名称 ==========
            # 优先使用配置中存储的名称
            raw_name = info.get("name")
            # 如果没有存储名称，则从PET文件路径中提取文件名
            if not raw_name:
                pet_path = info.get("pet", "")  # 获取PET文件路径
                if pet_path:
                    # 提取文件名（含后缀）
                    raw_name = Path(pet_path).name
                else:
                    # 既没有名称也没有路径，使用默认名称"数据_ID"
                    raw_name = f"数据_{data_id}"

            # 去除文件后缀（如.nii.gz），只保留基础名称
            # 例如 "case_001.nii.gz" -> "case_001"
            base_name = raw_name.split(".")[0]

            # ========== 处理重名情况 ==========
            # 如果基础名称已存在，自动添加后缀(_1, _2, ...)
            final_name = base_name
            counter = 1
            while final_name in used_names:
                final_name = f"{base_name}_{counter}"
                counter += 1

            # 将确定不重复的名称加入集合，供后续检查
            used_names.add(final_name)

            # 更新配置中该数据的名称
            self.main_window._config.data[data_id]["name"] = final_name

            # 创建配置管理器并保存更新后的配置到yaml文件
            config_manager = ConfigManager()
            config_manager.save(self.main_window._config)

            # ========== 创建模型项并添加到模型 ==========
            # 创建标准项，设置显示文本
            row = [QStandardItem(final_name)]
            # 将data_id存储在UserRole中，便于后续通过data()获取
            row[0].setData(data_id, Qt.ItemDataRole.UserRole)
            # 将行添加到模型
            self.model.appendRow(row)

        # ========== 第六步：调整列宽适应内容 ==========
        # 根据内容自动调整第0列宽度
        self.treeView.resizeColumnToContents(0)

    def on_item_double_clicked(self, index):
        """
        处理双击文件列表项的事件

        功能：
        1. 获取被双击项对应的data_id
        2. 从配置中获取原始文件名（去除后缀）
        3. 调用MainWindow的reload_data重新加载数据
        4. 发出file_name信号更新viewer显示的患者名称

        参数:
            index: 双击的项的模型索引
        """
        # 根据索引获取对应的模型项
        item = self.model.itemFromIndex(index)
        # 从项的UserRole中获取数据ID
        data_id = item.data(Qt.ItemDataRole.UserRole)

        # 初始化文件名为空字符串
        name = ""
        # 如果data_id有效且主窗口配置存在
        if data_id and self.main_window and hasattr(self.main_window, "_config"):
            # 检查该ID是否在配置数据中
            if data_id in self.main_window._config.data:
                # 从配置中获取原始名称，备选为当前显示文本
                raw_name = self.main_window._config.data[data_id].get(
                    "name", item.text()
                )
                # 去除后缀
                name = raw_name.split(".")[0]

        # 如果data_id有效且主窗口有reload_data方法，调用重新加载数据
        if data_id and self.main_window and hasattr(self.main_window, "reload_data"):
            self.main_window.reload_data(data_id)

        # 发出file_name信号，通知viewer更新显示的患者名称
        self.file_name.emit(name)

    def on_context_menu(self, position):
        """
        处理右键菜单请求

        当用户在文件列表上右键点击时，显示包含"重命名"和"删除"选项的菜单

        参数:
            position: 右键点击的位置（相对于TreeView）
        """
        # 获取点击位置对应的模型索引
        index = self.treeView.indexAt(position)
        # 如果点击位置没有对应的有效项，直接返回
        if not index.isValid():
            return

        # 创建右键菜单
        menu = QMenu()
        # 添加"重命名"菜单项
        rename_action = menu.addAction("重命名")
        # 添加"删除"菜单项
        delete_action = menu.addAction("删除")

        # 连接菜单项的触发信号到对应处理函数
        # 注意：使用lambda传递index，确保点击时使用正确的索引
        rename_action.triggered.connect(lambda: self.rename_data(index))
        delete_action.triggered.connect(lambda: self.delete_data(index))

        # 在全局坐标位置显示菜单（需要将TreeView局部坐标转换为全局坐标）
        menu.exec(self.treeView.mapToGlobal(position))

    def rename_data(self, index):
        """
        重命名数据处理函数

        弹出输入对话框让用户输入新名称
        保存到配置并更新显示，同时通知viewer更新

        参数:
            index: 要重命名的项的模型索引
        """
        # 获取对应的模型项
        item = self.model.itemFromIndex(index)
        # 获取存储的data_id
        data_id = item.data(Qt.ItemDataRole.UserRole)

        # 如果data_id有效且主窗口配置存在
        if data_id and self.main_window and hasattr(self.main_window, "_config"):
            # 弹出输入对话框，title为"重命名"，提示文本，初始值为当前显示名称
            new_name, ok = QInputDialog.getText(
                self, "重命名", "请输入新的名称:", text=item.text()
            )

            # 如果用户点击确定且输入了非空名称
            if ok and new_name:
                # 检查data_id是否仍在配置中（可能在并发操作中被删除）
                if data_id in self.main_window._config.data:
                    # 更新配置中该数据的名称
                    self.main_window._config.data[data_id]["name"] = new_name

                    # 创建配置管理器并保存更新后的配置到yaml文件
                    config_manager = ConfigManager()
                    config_manager.save(self.main_window._config)

                    # 直接更新模型中该项的显示文本（避免重新加载整个列表）
                    item.setText(new_name)

            # 发出file_name信号，通知viewer更新显示的患者名称
            # 注意：即使重命名取消（ok为False），只要用户输入了内容也发出信号
            self.file_name.emit(new_name)

    def delete_data(self, index):
        """
        删除数据处理函数

        1. 弹出确认对话框
        2. 从配置中删除数据
        3. 重新排序剩余数据的ID（保持ID连续）
        4. 保存配置并重新加载列表

        参数:
            index: 要删除的项的模型索引
        """
        # 获取对应的模型项
        item = self.model.itemFromIndex(index)
        # 获取存储的data_id
        data_id = item.data(Qt.ItemDataRole.UserRole)

        # 如果data_id有效且主窗口配置存在
        if data_id and self.main_window and hasattr(self.main_window, "_config"):
            # 检查当前是否有选中的数据，如果有则不能删除
            current_id = getattr(self.main_window, "current_data_id", "")
            if current_id and str(current_id) == str(data_id):
                QMessageBox.warning(
                    self,
                    "无法删除",
                    "该数据正在使用中，无法删除",
                    QMessageBox.StandardButton.Ok,
                )
                return

            # 弹出确认对话框，询问是否确定删除
            reply = QMessageBox.question(
                self,
                "确认删除",
                f"确定要删除数据 {item.text()} 吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            # 如果用户点击"是"
            if reply == QMessageBox.StandardButton.Yes:
                # 检查data_id是否仍在配置中
                if data_id in self.main_window._config.data:
                    # 从配置中删除该数据项
                    del self.main_window._config.data[data_id]

                    # ========== 重新排序ID ==========
                    # 获取剩余所有ID并按数字排序
                    sorted_ids = sorted(
                        self.main_window._config.data.keys(),
                        key=lambda x: int(x) if str(x).isdigit() else float("inf"),
                    )
                    # 创建新字典，用连续数字作为新ID
                    new_data = {}
                    for new_id, old_id in enumerate(sorted_ids, start=1):
                        new_data[str(new_id)] = self.main_window._config.data[old_id]
                    # 替换配置中的数据字典
                    self.main_window._config.data = new_data

                    # ========== 保存配置 ==========
                    from app.configs import ConfigManager

                    config_manager = ConfigManager()
                    config_manager.save(self.main_window._config)

                    # ========== 重新加载文件列表 ==========
                    # 清空模型现有内容
                    self.model.clear()
                    # 重新设置表头
                    self.model.setHorizontalHeaderLabels(["数据名称"])

                    # 用于存储已使用的名称，检测重名
                    used_names = set()
                    # 遍历重新编号后的数据，重新创建所有列表项
                    for new_id, info in new_data.items():
                        # 获取原始名称
                        raw_name = info.get("name")
                        # 如果没有存储名称，从文件路径提取
                        if not raw_name:
                            pet_path = info.get("pet", "")
                            if pet_path:
                                raw_name = Path(pet_path).name
                            else:
                                raw_name = f"数据_{new_id}"

                        # 去除后缀
                        base_name = raw_name.split(".")[0]

                        # 处理重名
                        final_name = base_name
                        counter = 1
                        while final_name in used_names:
                            final_name = f"{base_name}_{counter}"
                            counter += 1
                        used_names.add(final_name)

                        # 创建并添加模型项
                        row = [QStandardItem(final_name)]
                        row[0].setData(new_id, Qt.ItemDataRole.UserRole)
                        self.model.appendRow(row)

                    # 调整列宽
                    self.treeView.resizeColumnToContents(0)

    def select_item_by_id(self, data_id):
        """
        根据data_id选中对应的列表项

        用于在导入或加载数据后，选中FileDocker中当前正在使用的数据项

        参数:
            data_id: 要选中的数据的ID（字符串或整数）
        """
        # 遍历模型中的所有行，查找匹配的data_id
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item:
                # 比较data_id，确保类型一致
                item_id = str(item.data(Qt.ItemDataRole.UserRole))
                if item_id == str(data_id):
                    # 获取该行的模型索引
                    index = self.model.indexFromItem(item)
                    # 获取TreeView的选择模型
                    selection_model = self.treeView.selectionModel()
                    # 先清除所有选中项，再选中当前项
                    selection_model.clearSelection()
                    # 选中该行
                    selection_model.select(index, selection_model.SelectionFlag.Select)
                    selection_model.setCurrentIndex(
                        index, selection_model.SelectionFlag.NoUpdate
                    )
                    break


# 主程序入口，用于独立测试FileDocker组件
if __name__ == "__main__":
    # 创建应用程序实例（PySide6需要）
    app = QApplication(sys.argv)
    # 创建FileDocker窗口实例（parent为None，main_window为None，仅用于测试）
    window = FileDocker(None, None)
    # 显示窗口
    window.show()
    # 启动事件循环
    sys.exit(app.exec())
