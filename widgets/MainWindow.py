import shutil
import sys
import warnings
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

import cv2
import numpy as np
import pypinyin as pin
import SimpleITK as sitk
import vtk
from PySide6.QtCore import Qt
from PySide6.QtGui import QActionGroup, QImage, QPixmap, QUndoCommand, QUndoStack
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QDialog,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QVBoxLayout,
)
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from app.configs import AppConfig
from app.mode import LOADMode, VIEWERMode, VIEWMode
from path import CACHE_PATH, SEGMENTATION_PATH
from scripts.logger import log_debug, log_error, log_info, log_warning
from ui.MainWindow_ui import Ui_MainWindow
from widgets.LoadDialog import LoadDialog
from widgets.WorkerThread import (
    BuiltThread,
    DicomWorker,
    ModelLoader,
    NiftiWorker,
    SamThread,
)

warnings.filterwarnings("ignore")


class SegChangeCommand(QUndoCommand):
    def __init__(self, parent, layer, old_slice, new_slice, description="修改标签"):
        super().__init__(description)
        self.parent = parent
        self.layer = layer
        # 只保存当前层的 2D 切片，降低内存与拷贝开销
        self.old_slice = old_slice.copy() if old_slice is not None else None
        self.new_slice = new_slice.copy()

    def redo(self):
        """重做：将数据设为新值，并更新 UI"""
        self.parent.seg[:, :, self.layer] = self.new_slice
        self.parent.update_all()

    def undo(self):
        """撤销：恢复为旧值，并更新 UI"""
        if self.old_slice is not None:
            self.parent.seg[:, :, self.layer] = self.old_slice
            self.parent.update_all()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._config = config

        self.resize(config.width, config.height)

        self.patient_id: str = ""

        # 图像透明度参数
        self.ct_alpha: float = 0.5
        self.pet_alpha: float = 0.5
        self.seg_alpha: float = 0.5

        # 窗宽窗位参数
        self.ct_ww: float = 400.0
        self.ct_wl: float = 50.0
        self.pet_ww: float = 2.5
        self.pet_wl: float = 5.0

        # 标注与图层参数
        self.color_label: int = 1
        self.layer: int = 0
        self.num: int = -1

        # 坐标参数
        self.y_star: int = 0
        self.y_end: int = 0
        self.x_star: int = 0
        self.x_end: int = 0

        self.radius: int = 5

        # 图像数据
        self.ct = []
        self.pet = []
        self.seg = []
        # 撤销前快照（当前层）
        self._seg_before_edit = None

        # 状态标志
        self.load_mode = LOADMode.UNLOAD
        self.view_mode = VIEWMode.CROSS

        # 路径参数
        self.cache_path: Path = CACHE_PATH
        self.seg_path: Path = SEGMENTATION_PATH
        self.data_path: Path = ""
        self.seg_file: Path = ""

        self.SamPredictor = None
        self.undo_stack = QUndoStack(self)
        self.undo_stack.setUndoLimit(10)

        self.model_loader = ModelLoader()
        self.model_loader.finished.connect(self.on_model_loaded)
        self.model_loader.start()

        self.setWindowTitle("鼻咽癌PET/CT图像全身病灶检测软件")

        self.init_ui()
        self.init_connectAction()

    def init_ui(self):
        self.view_3d = QVTKRenderWindowInteractor()
        self.view_layout = QVBoxLayout()
        self.view_layout.addWidget(self.view_3d)
        self.view_frame.setLayout(self.view_layout)

        self.atn_group = QActionGroup(self)
        self.atn_group.setExclusive(True)
        self.atn_group.addAction(self.aim_atn)
        self.atn_group.addAction(self.move_atn)
        self.atn_group.addAction(self.win_atn)
        self.atn_group.addAction(self.paint_atn)
        self.atn_group.addAction(self.sam_atn)
        self.atn_group.addAction(self.eraser_atn)

        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)
        self.btn_group.addButton(self.btnH)
        self.btn_group.addButton(self.btnS)
        self.btn_group.addButton(self.btnG)
        self.btn_group.addButton(self.btn3D)

        self.undo_action = self.undo_stack.createUndoAction(self, "撤销")
        self.undo_action.setShortcut("Ctrl+Z")
        self.redo_action = self.undo_stack.createRedoAction(self, "重做")
        self.redo_action.setShortcut("Ctrl+Y")
        self.addAction(self.undo_action)
        self.addAction(self.redo_action)

        self.dialog = QDialog(self)
        self.dialog.setWindowModality(Qt.WindowModal)  # 设置为模态对话框
        self.dialog.setFixedSize(300, 100)

        layout = QVBoxLayout()
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 0)  # 设置为循环进度条
        progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(progress_bar)
        self.dialog.setLayout(layout)

        self.statusbar = QMainWindow.statusBar(self)
        self.statusbar.setStyleSheet("background-color: #1A89FF;")

    def init_connectAction(self):
        """初始化信号与槽连接"""
        self.sldAlphaCt.valueChanged.connect(
            lambda v: self.boxAlphaCt.setValue(v / 100)
        )
        self.boxAlphaCt.valueChanged.connect(
            lambda v: self.sldAlphaCt.setValue(int(v * 100))
        )
        self.sldAlphaPet.valueChanged.connect(
            lambda v: self.boxAlphaPet.setValue(v / 100)
        )
        self.boxAlphaPet.valueChanged.connect(
            lambda v: self.sldAlphaPet.setValue(int(v * 100))
        )
        self.sldPET_ww.valueChanged.connect(lambda v: self.boxPET_ww.setValue(v / 100))
        self.boxPET_ww.valueChanged.connect(
            lambda v: self.sldPET_ww.setValue(int(v * 100))
        )
        self.sldPET_wl.valueChanged.connect(lambda v: self.boxPET_wl.setValue(v / 100))
        self.boxPET_wl.valueChanged.connect(
            lambda v: self.sldPET_wl.setValue(int(v * 100))
        )
        self.sldAlphaSeg.valueChanged.connect(
            lambda v: self.boxAlphaSeg.setValue(v / 100)
        )
        self.boxAlphaSeg.valueChanged.connect(
            lambda v: self.sldAlphaSeg.setValue(int(v * 100))
        )

        self.load_atn.triggered.connect(self.load_slot)
        self.loadseg_atn.triggered.connect(self.load_Seg_slot)
        self.save_atn.triggered.connect(self.save_slot)
        self.run_atn.triggered.connect(self.run_slot)
        self.redo_atn.triggered.connect(self.redo_slot)
        self.setting_atn.triggered.connect(self.setting_slot)

        self.aim_atn.triggered.connect(self.aim_slot)
        self.sam_atn.triggered.connect(self.sam_slot)
        self.paint_atn.triggered.connect(self.paint_slot)
        self.move_atn.triggered.connect(self.move_slot)
        self.win_atn.triggered.connect(self.win_slot)
        self.eraser_atn.triggered.connect(self.eraser_slot)

        self.actionopen.triggered.connect(self.load_slot)
        self.actionsegload.triggered.connect(self.load_Seg_slot)
        self.actionsave.triggered.connect(self.save_slot)
        self.actionexit.triggered.connect(self.close)
        self.actiontool.triggered.connect(self.setting_slot)
        self.actioncrossline.triggered.connect(self.crossline_slot)

        self.actionfile.triggered.connect(self.toggle_toolBar_file)
        self.actionpaint.triggered.connect(self.toggle_toolBar_draw)
        self.actionrun.triggered.connect(self.toggle_toolBar_run)

        self.boxCT_ww.valueChanged.connect(
            lambda v: self.update_property_and_refresh("ct_ww", v)
        )
        self.boxCT_wl.valueChanged.connect(
            lambda v: self.update_property_and_refresh("ct_wl", v)
        )
        self.boxPET_ww.valueChanged.connect(
            lambda v: self.update_property_and_refresh("pet_ww", v)
        )
        self.boxPET_wl.valueChanged.connect(
            lambda v: self.update_property_and_refresh("pet_wl", v)
        )
        self.boxAlphaCt.valueChanged.connect(lambda: self.set_alpha("CT"))
        self.boxAlphaPet.valueChanged.connect(lambda: self.set_alpha("PET"))
        self.boxAlphaSeg.valueChanged.connect(
            lambda v: self.update_property_and_refresh("seg_alpha", v)
        )
        self.boxPaint.valueChanged.connect(
            lambda v: self.update_property_and_refresh("radius", v)
        )
        self.boxLayer.valueChanged.connect(
            lambda v: self.update_property_and_refresh("layer", v)
        )

        self.boxCT.clicked.connect(self.update_all)
        self.boxPET.clicked.connect(self.update_all)
        self.boxSeg.clicked.connect(self.update_all)

        self.btnH.clicked.connect(lambda: self.change_slot(VIEWMode.CROSS))
        self.btnS.clicked.connect(lambda: self.change_slot(VIEWMode.SAGITTAL))
        self.btnG.clicked.connect(lambda: self.change_slot(VIEWMode.CORONAL))
        self.btn3D.clicked.connect(self.view_3d_built)

        self.btnCa.clicked.connect(self.screen_shot)
        self.btnReset.clicked.connect(self.reset_slot)

        self.cboxMode.currentIndexChanged.connect(self.on_cbox_mode_changed)

        self.viewer.Sam_Signal.connect(self.operation)
        self.viewer.Mode_Signal.connect(self.checkmode)

    def transpose(self, mode):
        if mode == "trans":
            if self.view_mode == VIEWMode.CROSS:
                return [1, 2, 0]
            if self.view_mode == VIEWMode.SAGITTAL:
                return [0, 1, 2]
            if self.view_mode == VIEWMode.CORONAL:
                return [0, 2, 1]
        elif mode == "save":
            if self.view_mode == VIEWMode.CROSS:
                return [2, 0, 1]
            if self.view_mode == VIEWMode.SAGITTAL:
                return [0, 1, 2]
            if self.view_mode == VIEWMode.CORONAL:
                return [0, 2, 1]

    def on_model_loaded(self, predictor):
        self.SamPredictor = predictor
        log_info("SAM模型已加载到主窗口")

    def setting_slot(self):
        if self.dockWidget_2.isVisible():
            self.dockWidget_2.hide()
        else:
            self.dockWidget_2.show()

    def toggle_toolBar_file(self):
        self.toolBar_file.setVisible(not self.toolBar_file.isVisible())

    def toggle_toolBar_draw(self):
        self.toolBar_draw.setVisible(not self.toolBar_draw.isVisible())

    def toggle_toolBar_run(self):
        self.toolBar_run.setVisible(not self.toolBar_run.isVisible())

    def screen_shot(self):
        if self.load_mode != LOADMode.UNLOAD:
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Screenshot_{timestamp}.png"
            save_path = QFileDialog.getSaveFileName(
                self, "保存图片", filename, "PNG (*.png)"
            )[0]

            viewport = self.viewer.viewport()
            pixmap = viewport.grab()
            if save_path:
                pixmap.save(save_path)
                self.statusbar.showMessage("图片已保存：" + save_path)

    def change_slot(self, mode):
        if self.load_mode != LOADMode.UNLOAD:
            self.stackedWidget.setCurrentIndex(0)

            save = self.transpose("save")
            self.pet = np.transpose(self.pet, axes=save)
            self.ct = np.transpose(self.ct, axes=save)
            self.seg = np.transpose(self.seg, axes=save)

            self.view_mode = mode
            self.viewer.view_mode = mode

            trans = self.transpose("trans")
            self.pet = np.transpose(self.pet, axes=trans)
            self.ct = np.transpose(self.ct, axes=trans)
            self.seg = np.transpose(self.seg, axes=trans)

            self.load_mode = LOADMode.CHANGE
            self.setting()

    def on_cbox_mode_changed(self, index):
        """改变病灶标注类型"""
        self.color_label = index + 1

    def set_alpha(self, state):
        if state == "CT":
            self.ct_alpha = self.boxAlphaCt.value()
            self.boxAlphaPet.setValue(1 - self.ct_alpha)
            self.pet_alpha = 1 - self.ct_alpha
        elif state == "PET":
            self.pet_alpha = self.boxAlphaPet.value()
            self.boxAlphaCt.setValue(1 - self.pet_alpha)
            self.ct_alpha = 1 - self.pet_alpha
        self.update_image()

    def reset_slot(self):
        """复位处理"""
        if self.load_mode != LOADMode.UNLOAD:
            self.viewer.fitInView(self.viewer.pixmap_item, Qt.KeepAspectRatio)

    def redo_slot(self):
        """重做-清空标注"""
        if self.load_mode != LOADMode.UNLOAD:
            reply = QMessageBox.question(
                self,
                "确认",
                "是否确认清空所有标注？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.seg = np.zeros_like(self.ct)
                self.viewer.input_box = []
                self.update_image()

    def load_Seg_slot(self):
        if self.load_mode == LOADMode.UNLOAD:
            log_warning("请先输入原始数据")
            QMessageBox.warning(self, "警告！", "请先输入原始数据！", QMessageBox.Ok)
            return
        else:
            seg_file, _ = QFileDialog.getOpenFileName(
                self, "选择文件", "", "NIfTI Files (*.nii *.nii.gz)"
            )
            if seg_file:
                log_info(f"加载分割文件: {seg_file}")
                name = Path(seg_file).stem.split(".")[0]
                new_path = Path(self.seg_path) / (name + ".nii.gz")
                shutil.copy2(seg_file, str(new_path))
                self.seg_file = seg_file

                seg = sitk.ReadImage(str(new_path))
                seg_data = sitk.GetArrayFromImage(seg)
                trans = self.transpose("trans")
                seg_data = np.transpose(seg_data, axes=trans)
                if seg_data.shape == self.pet.shape:
                    self.seg = seg_data
                    self.update_image()
                    log_info(f"分割文件加载成功: {seg_file}")
                else:
                    log_error(
                        f"分割文件形状不匹配: {seg_data.shape} vs {self.pet.shape}"
                    )
                    QMessageBox.warning(
                        self,
                        "警告！",
                        "输入标签与原始数据不符，请检查标注是否正确！",
                        QMessageBox.Ok,
                    )
                    return
            else:
                return

    def load_slot(self):
        """导入数据对话框"""
        log_info("打开数据加载对话框")
        cache_path = Path(self.cache_path)
        if cache_path.exists():
            for file_path in cache_path.iterdir():
                if file_path.is_dir():
                    shutil.rmtree(str(file_path))
                else:
                    file_path.unlink()

        load_dialog = LoadDialog(self)
        load_dialog.FilesSelected.connect(self.on_files_selected)
        load_dialog.show()

    def on_files_selected(self, pet_file: str, ct_file: str, file_type: str):
        """处理文件选择"""
        log_info(f"选择文件 - PET: {pet_file}, CT: {ct_file}, 类型: {file_type}")

        self.dialog.setWindowTitle("导入中")
        self.dialog.show()

        pet_path = Path(pet_file)
        patient_id = pet_path.parent.name
        patient_id = pin.slug(patient_id)
        if "-" in patient_id:
            patient_id = patient_id.replace("-", "")
        if "_" in patient_id:
            patient_id = patient_id.replace("_", "")
        if len(patient_id) >= 4 and patient_id[:4].isdigit():
            patient_id = patient_id[4:]

        self.patient_id = patient_id

        data_folder = Path(self.cache_path) / self.patient_id
        data_folder.mkdir(parents=True, exist_ok=True)
        self.data_path = str(data_folder)

        if file_type == "NIfTI":
            self._load_nifti_files(pet_file, ct_file)
        else:
            self._load_dicom_files(pet_file, ct_file, data_folder)

    def _load_dicom_files(self, pet_file: str, ct_file: str, data_folder: Path):
        """处理DICOM/IMA文件"""
        self.worker_thread = DicomWorker(pet_file, ct_file, data_folder)
        self.worker_thread.finished.connect(self.dialog.close)
        self.worker_thread.finished.connect(self.on_data_loaded)
        self.worker_thread.start()

    def _load_nifti_files(self, pet_file: str, ct_file: str):
        """处理NIfTI文件"""
        self.worker_thread = NiftiWorker(pet_file, ct_file)
        self.worker_thread.finished.connect(self.dialog.close)
        self.worker_thread.finished.connect(self.on_data_loaded)
        self.worker_thread.start()

    def on_data_loaded(self, ct_data: np.ndarray, pet_data: np.ndarray, spacing: tuple):
        """数据加载完成后的处理"""
        self.load_mode = LOADMode.RELOAD

        trans = self.transpose("trans")
        self.ct = np.transpose(ct_data, axes=trans)
        self.pet = np.transpose(pet_data, axes=trans)
        self.seg = np.zeros_like(self.pet)
        self.viewer.spacing = spacing

        self.undo_stack.clear()

        self.setting()

    def setting(self):
        """导入数据后初始化层数"""
        self.seg_file = ""
        self.viewer.show_crosshair = True
        self.viewer.position[0] = self.viewer.width() // 2
        self.viewer.position[1] = self.viewer.height() // 2

        self.stackedWidget.setCurrentIndex(0)

        if self.load_mode != LOADMode.CHANGE:
            self.boxAlphaCt.setValue(self.ct_alpha)
            self.boxCT_wl.setValue(self.ct_wl)
            self.boxCT_ww.setValue(self.ct_ww)

            self.boxAlphaPet.setValue(self.pet_alpha)
            self.boxPaint.setValue(self.radius)

            pet_max = np.max(self.pet)
            self.pet_ww = pet_max
            self.pet_wl = pet_max / 2
            self.boxPET_wl.setValue(self.pet_wl)
            self.boxPET_ww.setValue(self.pet_ww)

            self.boxAlphaSeg.setValue(self.seg_alpha)

            self.aim_atn.setChecked(True)
            self.aim_slot()

        self.sldLayer.setMaximum(self.ct.shape[2] - 1)
        self.boxLayer.setMaximum(self.ct.shape[2] - 1)
        self.layer = self.ct.shape[2] // 2
        self.boxLayer.setValue(self.layer)

        self.update_image()

    def run_slot(self):
        """运行预测"""
        pass

    def save_slot(self):
        """保存设置"""
        if np.any(self.seg):
            file_, ok = QFileDialog.getSaveFileName(
                self, "文件保存", "C:\\Users\\", "NFiTI(*.nii.gz)"
            )

            if file_ != "":
                log_info(f"保存分割文件: {file_}")
                image = np.copy(self.seg)
                save = self.transpose("save")
                image = np.transpose(image, axes=save)
                image = sitk.GetImageFromArray(image)
                self.statusBar().showMessage("已保存文件：" + file_)
                sitk.WriteImage(image, file_)
        elif self.seg_file:
            log_info(f"保存分割文件: {self.seg_file}")
            image = np.copy(self.seg)
            save = self.transpose("save")
            image = np.transpose(image, axes=save)
            image = sitk.GetImageFromArray(image)
            self.statusBar().showMessage("已保存文件：" + self.seg_file)
            sitk.WriteImage(image, self.seg_file)
        else:
            log_warning("无可保存分割图像")
            QMessageBox.warning(self, "警告", "无可保存分割图像！", QMessageBox.Ok)

    def crossline_slot(self):
        self.viewer.cross_show = not self.viewer.cross_show

    def checkmode(self):
        self.aim_slot()
        self.sam_slot()
        self.paint_slot()
        self.eraser_slot()
        self.move_slot()
        self.win_slot()

    def aim_slot(self):
        """目标工具-设置按键冲突，调整图像状态"""
        if self.aim_atn.isChecked() and self.load_mode != LOADMode.UNLOAD:
            self.viewer.mode = VIEWERMode.AIM
            self.update_all()

    def sam_slot(self):
        """使用SAM画框-设置按键冲突，调整图像状态"""
        if self.sam_atn.isChecked() and self.load_mode != LOADMode.UNLOAD:
            self.viewer.mode = VIEWERMode.SAM
            self.update_all()

    def paint_slot(self):
        """画笔工具-设置按键冲突，调整图像状态"""
        if self.paint_atn.isChecked() and self.load_mode != LOADMode.UNLOAD:
            self.viewer.mode = VIEWERMode.PAINT
            self.update_all()

    def eraser_slot(self):
        """擦除工具-设置按键冲突，调整图像状态"""
        if self.eraser_atn.isChecked() and self.load_mode != LOADMode.UNLOAD:
            self.viewer.mode = VIEWERMode.ERASER
            self.update_all()

    def move_slot(self):
        """图像移动工具-设置按键冲突，调整图像状态"""
        if self.move_atn.isChecked() and self.load_mode != LOADMode.UNLOAD:
            self.viewer.mode = VIEWERMode.MOVE
            self.update_all()

    def win_slot(self):
        """调窗工具-设置按键冲突，调整图像状态"""
        if self.win_atn.isChecked() and self.load_mode != LOADMode.UNLOAD:
            self.viewer.mode = VIEWERMode.WIN
            self.update_all()

    def update_all(self):
        """更新-以防按键冲突后仍有残留项"""
        if self.load_mode != LOADMode.UNLOAD:
            self.viewer.input_box = None
            self.update_image()
            if self.stackedWidget.currentIndex() == 1:
                self.view_3d_built()

    def operation(self, input_box):
        log_debug(f"SAM操作开始, 输入框: {input_box}")
        try:
            ct_slice = self.ct[:, :, self.layer]
            ct_slice = self.normalize(ct_slice, self.ct_ww, self.ct_wl)
            ct_slice = np.stack([ct_slice] * 3, axis=-1)

            pet_slice = self.pet[:, :, self.layer]
            pet_slice = self.normalize(pet_slice, self.pet_ww, self.pet_wl)
            pet_slice = cv2.applyColorMap(pet_slice, cv2.COLORMAP_HOT)

            current_slice = cv2.addWeighted(
                ct_slice, self.ct_alpha, pet_slice, self.pet_alpha, 0
            )

            if self.layer != self.num:
                self.SamPredictor.set_image(current_slice)
                self.num = self.layer

            # 在 SAM 修改前先缓存当前层的切片，供撤销使用
            old_slice = self.seg[:, :, self.layer].copy()
            current_layer = self.layer  # 保存当前层索引，避免lambda捕获问题

            # 使用闭包正确捕获old_slice和layer值
            def on_sam_finished(mask):
                # SAM返回mask后，更新seg
                self.seg[:, :, current_layer] = np.where(
                    mask > 0, self.color_label, self.seg[:, :, current_layer]
                )
                # 检查变化并提交撤销命令
                new_slice = self.seg[:, :, current_layer]
                if not np.array_equal(old_slice, new_slice):
                    self.commit_seg_change(
                        current_layer, old_slice, new_slice, "SAM分割"
                    )
                self.update_all()
                self.checkmode()

            self.SamThread = SamThread(self.SamPredictor, input_box)
            self.SamThread.finished.connect(on_sam_finished)
            self.SamThread.start()
        except Exception as e:
            log_error(f"SAM操作失败: {e}")
            import traceback

            traceback.print_exc()
            return

    def normalize(self, slice, ww, wl):
        window_upper = wl + ww / 2
        window_lower = wl - ww / 2

        slice = np.clip(slice, window_lower, window_upper)
        slice = (slice - window_lower) / (window_upper - window_lower) * 255
        slice = slice.astype(np.uint8)
        return slice

    def update_image(self):
        """图像更新"""
        if self.load_mode != LOADMode.UNLOAD:
            img = self.prepare_image()
            self.viewer.load_image(img, self.radius)

        if self.load_mode == LOADMode.CHANGE or self.load_mode == LOADMode.RELOAD:
            self.viewer.fitInView(self.viewer.pixmap_item, Qt.KeepAspectRatio)
            self.viewer.scene.setSceneRect(self.viewer.pixmap_item.sceneBoundingRect())
            self.load_mode = LOADMode.LOADED

    def update_property_and_refresh(self, attr_name, value):
        old_value = getattr(self, attr_name, None)
        setattr(self, attr_name, value)
        # 如果切换了层，清理编辑缓存
        if attr_name == "layer" and old_value is not None and old_value != value:
            self._seg_before_edit = None
        if self.load_mode != LOADMode.UNLOAD:
            self.update_image()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "退出提示",
            "确定退出?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self._config.width = self.width()
            self._config.height = self.height()

            log_info("应用程序关闭，清理缓存")
            clear_path = [Path(self.cache_path), Path(self.seg_path)]
            for directory_path in clear_path:
                if directory_path.exists():
                    for file_path in directory_path.iterdir():
                        if file_path.is_file() or file_path.is_symlink():
                            file_path.unlink()
                        elif file_path.is_dir():
                            shutil.rmtree(str(file_path))
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        """鼠标按下事件重写，用于拖拽和绘图"""
        super().mousePressEvent(event)
        if self.load_mode != LOADMode.UNLOAD:
            if event.button() == Qt.RightButton:
                self.update_all()

            elif event.button() == Qt.LeftButton:
                if self.paint_atn.isChecked() or self.eraser_atn.isChecked():
                    # 在开始绘制前，缓存当前层的切片，作为撤销的 old_slice
                    if self._seg_before_edit is None:
                        self._seg_before_edit = self.seg[:, :, self.layer].copy()

                    point = self.viewer.point  # 获取 QPoint 对象
                    x = point.x()  # 获取 x 坐标
                    y = point.y()  # 获取 y 坐标

                    arr = np.array(self.seg[:, :, self.layer], dtype=np.uint8)
                    rows, cols = arr.shape

                    for i in range(
                        max(x - self.radius, 0), min(x + self.radius + 1, cols)
                    ):
                        for j in range(
                            max(y - self.radius, 0), min(y + self.radius + 1, rows)
                        ):
                            distance_squared = (i - x) ** 2 + (j - y) ** 2
                            if distance_squared <= self.radius**2:
                                arr[j, i] = self.viewer.draw_state * self.color_label

                    self.seg[:, :, self.layer] = arr
                    self.update_all()

        event.accept()

    def mouseMoveEvent(self, event):
        """鼠标移动重写，用于移动和绘图"""
        super().mouseMoveEvent(event)
        if self.load_mode != LOADMode.UNLOAD and event.buttons() & Qt.LeftButton:
            if self.win_atn.isChecked() and self.viewer.underMouse():
                delta = self.viewer.delta

                self.ct_ww = np.clip(self.ct_ww, 1, 2000)
                self.ct_wl = np.clip(self.ct_wl, -1000, 1000)

                self.ct_ww += int(delta.x())
                self.ct_wl += int(delta.y())
                self.boxCT_ww.setValue(self.ct_ww)
                self.boxCT_wl.setValue(self.ct_wl)

            elif self.paint_atn.isChecked() or self.eraser_atn.isChecked():
                point = self.viewer.point  # 获取 QPoint 对象
                x = point.x()  # 获取 x 坐标
                y = point.y()  # 获取 y 坐标

                arr = np.array(self.seg[:, :, self.layer], dtype=np.uint8)
                rows, cols = arr.shape

                for i in range(max(x - self.radius, 0), min(x + self.radius, cols)):
                    for j in range(max(y - self.radius, 0), min(y + self.radius, rows)):
                        distance_squared = (i - x) ** 2 + (j - y) ** 2
                        if distance_squared <= self.radius**2:
                            arr[j, i] = self.viewer.draw_state * self.color_label

                self.seg[:, :, self.layer] = arr
                self.update_all()

        event.accept()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.paint_atn.isChecked() or self.eraser_atn.isChecked():
            # 鼠标抬起时，将修改前后的当前层切片压入撤销栈
            if self._seg_before_edit is not None:
                new_slice = self.seg[:, :, self.layer]
                # 只有当切片确实发生变化时才记录撤销命令
                if not np.array_equal(self._seg_before_edit, new_slice):
                    self.commit_seg_change(
                        self.layer, self._seg_before_edit, new_slice, "绘制"
                    )
                self._seg_before_edit = None

        event.accept()

    def wheelEvent(self, event):
        super().wheelEvent(event)
        """鼠标滚动重写，用于切换层数，放缩"""
        angle = event.angleDelta()

        if event.modifiers() == Qt.ControlModifier:
            if self.paint_atn.isChecked() or self.eraser_atn.isChecked():
                if angle.y() > 0 and self.radius < 30:
                    self.radius += 1
                    self.boxPaint.setValue(self.radius)
                elif angle.y() < 0 and self.radius > 1:
                    self.radius -= 1
                    self.boxPaint.setValue(self.radius)

        elif self.load_mode != LOADMode.UNLOAD:
            old_layer = self.layer
            if angle.y() > 0 and self.layer < self.ct.shape[2] - 1:
                self.layer += 1
                self.sldLayer.setValue(self.layer)
            elif angle.y() < 0 < self.layer:
                self.layer -= 1
                self.sldLayer.setValue(self.layer)

            # 切换层时，清理之前层的编辑缓存
            if old_layer != self.layer:
                self._seg_before_edit = None

        self.update_all()

        event.accept()

    def prepare_image(self):
        """更新显示图像"""
        ct = np.array(self.ct[:, :, self.layer])
        ct = self.normalize(ct, self.ct_ww, self.ct_wl)

        pet = np.array(self.pet[:, :, self.layer])
        pet = self.normalize(pet, self.pet_ww, self.pet_wl)

        new_ct = np.stack([ct] * 3, axis=-1)
        new_pet = cv2.applyColorMap(pet, cv2.COLORMAP_HOT)
        seg = np.array(self.seg[:, :, self.layer], dtype=np.uint8)

        overlay = np.zeros_like(new_ct)
        overlay[seg == 1] = [255, 0, 0]
        overlay[seg == 2] = [0, 255, 0]

        ct_alpha = self.ct_alpha if self.boxCT.isChecked() else 0
        pet_alpha = self.pet_alpha if self.boxPET.isChecked() else 0
        seg_alpha = self.seg_alpha if self.boxSeg.isChecked() else 0
        new_im = cv2.addWeighted(new_ct, ct_alpha, new_pet, pet_alpha, 0)
        mask = seg > 0
        mask = np.stack([mask] * 3, axis=-1)
        new_im = np.where(
            mask, cv2.addWeighted(new_im, 1 - seg_alpha, overlay, seg_alpha, 0), new_im
        )

        height, width, channels = new_im.shape
        bytes_per_line = channels * width
        pre_image = QImage(
            new_im.data, width, height, bytes_per_line, QImage.Format_BGR888
        )
        pre_image = QPixmap.fromImage(pre_image)

        return pre_image

    def view_3d_built(self):
        self.stackedWidget.setCurrentIndex(1)

        if not hasattr(self, "renderer"):
            self.renderer = vtk.vtkRenderer()
            self.view_3d.GetRenderWindow().AddRenderer(self.renderer)
            self.iren = self.view_3d.GetRenderWindow().GetInteractor()
            self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        self.renderer.RemoveAllViewProps()

        if self.load_mode != LOADMode.UNLOAD and np.any(self.seg):
            seg = self.seg.copy()
            save = self.transpose("save")
            seg = np.transpose(seg, axes=save)
            data = np.ascontiguousarray(seg)

            def add_vtk_actor(actor):
                self.renderer.AddActor(actor)
                self.renderer.ResetCamera()
                self.view_3d.GetRenderWindow().Render()

            # 启动 VTK 处理线程
            self.Built_Thread = BuiltThread(data, self.viewer.spacing)
            self.Built_Thread.actor_ready.connect(add_vtk_actor)
            self.Built_Thread.start()
        else:
            self.renderer.ResetCamera()
            self.renderer.SetBackground(0, 0, 0)
            self.view_3d.GetRenderWindow().Render()

    def commit_seg_change(self, layer, old_slice, new_slice, description="编辑"):
        """当某一层 seg 发生变化时，调用此函数记录撤销命令"""
        if old_slice is None or new_slice is None:
            return

        command = SegChangeCommand(self, layer, old_slice, new_slice, description)
        self.undo_stack.push(command)


if __name__ == "__main__":
    from app.configs import ConfigManager
    app = QApplication(sys.argv)
    config_manager = ConfigManager()
    config = config_manager.load()
    MainWindow = MainWindow(config)
    MainWindow.show()
    sys.exit(app.exec())
