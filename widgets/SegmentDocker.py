import sys
import yaml
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem, QColorDialog, QAbstractItemView
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from ui.SegmentDock_ui import Ui_Form


class SegmentDocker(QWidget, Ui_Form):
    # 定义一个信号，用于通知MainWindow更新color_label
    label_selected = Signal(int)
    
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.setupUi(self)
        self.init_connectAction()
        self.init_labels()

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
        self.pushButton.clicked.connect(self.add_label)
        self.pushButton_2.clicked.connect(self.delete_label)
        self.tableWidget.cellChanged.connect(self.update_label)
        self.tableWidget.cellDoubleClicked.connect(self.change_color)
        # 当选择行变化时，发送信号
        self.tableWidget.itemSelectionChanged.connect(self.on_label_selected)

    def init_labels(self):
        """初始化标签表格"""
        # 从MainWindow的配置中加载标签
        labels = self.main_window._config.label
        
        # 清空表格
        self.tableWidget.setRowCount(0)
        
        # 按标签ID排序
        sorted_labels = sorted(labels.items(), key=lambda x: int(x[0]))
        
        # 填充表格
        for idx, (label_id, label_info) in enumerate(sorted_labels):
            self.tableWidget.insertRow(idx)
            
            # 名称列
            name_item = QTableWidgetItem(label_info['name'])
            self.tableWidget.setItem(idx, 0, name_item)
            
            # 颜色列
            color_item = QTableWidgetItem()
            color = QColor(label_info['color'])
            color_item.setBackground(color)
            # 不显示颜色文本
            color_item.setText('')
            self.tableWidget.setItem(idx, 1, color_item)
        
        # 设置选择行为为整行选择
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置选择模式为单选
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置列宽，固定列宽
        self.tableWidget.setColumnWidth(0, 100)  # Name列固定宽度250
        self.tableWidget.setColumnWidth(1, 150)  # Label列固定宽度150

    def add_label(self):
        """添加新标签"""
        # 打开颜色选择对话框
        color_dialog = QColorDialog()
        color_dialog.setWindowTitle("选择标签颜色")
        
        if color_dialog.exec() == QColorDialog.Accepted:
            new_color = color_dialog.currentColor().name()
            
            # 从MainWindow的配置中获取标签
            labels = self.main_window._config.label
            
            # 生成新标签ID
            label_ids = [int(id) for id in labels.keys()]
            new_id = str(max(label_ids) + 1) if label_ids else '1'
            
            # 添加新标签
            labels[new_id] = {'name': f'Label {new_id}', 'color': new_color}
            
            # 更新表格
            self.init_labels()

    def delete_label(self):
        """删除选中标签"""
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            # 从MainWindow的配置中获取标签
            labels = self.main_window._config.label
            
            # 获取要删除的标签ID
            # 按标签ID排序
            sorted_labels = sorted(labels.items(), key=lambda x: int(x[0]))
            if selected_row < len(sorted_labels):
                label_id = int(sorted_labels[selected_row][0])
                # 删除标签
                del labels[str(label_id)]
                
                # 更新MainWindow的seg数组，将所有使用该标签ID的体素设置为0
                if hasattr(self.main_window, 'seg') and self.main_window.seg.size > 0:
                    self.main_window.seg[self.main_window.seg == label_id] = 0
                
                # 更新表格
                self.init_labels()
                # 刷新图像
                if hasattr(self.main_window, 'update_image'):
                    self.main_window.update_image()

    def update_label(self, row, column):
        """更新标签信息"""
        if column == 0:  # 只处理名称列的修改
            # 从MainWindow的配置中获取标签
            labels = self.main_window._config.label
            
            # 获取标签ID
            label_ids = list(labels.keys())
            if row < len(label_ids):
                label_id = label_ids[row]
                # 更新名称
                labels[label_id]['name'] = self.tableWidget.item(row, 0).text()

    def change_color(self, row, column):
        """修改标签颜色"""
        if column == 1:  # 只处理颜色列的双击
            # 打开颜色选择对话框
            color_dialog = QColorDialog()
            # 从MainWindow的配置中获取当前颜色
            labels = self.main_window._config.label
            label_ids = list(labels.keys())
            if row < len(label_ids):
                label_id = label_ids[row]
                current_color = labels[label_id]['color']
                color_dialog.setCurrentColor(QColor(current_color))
                
                if color_dialog.exec() == QColorDialog.Accepted:
                    new_color = color_dialog.currentColor().name()
                    
                    # 更新表格
                    color_item = self.tableWidget.item(row, 1)
                    color_item.setBackground(QColor(new_color))
                    # 不显示颜色文本
                    color_item.setText('')
                    
                    # 更新配置
                    labels[label_id]['color'] = new_color
    
    def on_label_selected(self):
        """当选择标签时，发送信号给MainWindow"""
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            # 获取标签ID（按表格显示顺序）
            labels = self.main_window._config.label
            # 按标签ID排序
            sorted_labels = sorted(labels.items(), key=lambda x: int(x[0]))
            if row < len(sorted_labels):
                label_id = int(sorted_labels[row][0])
                # 发送信号
                self.label_selected.emit(label_id)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SegmentDocker(None, None)
    window.show()
    sys.exit(app.exec())
