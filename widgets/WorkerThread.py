import os
import numpy as np
from PySide6.QtCore import QThread, Signal
import torch
from utils import resource_path
from scripts.preprocess import convert_dcm_to_nii_and_pet2suv
import vtk
from vtkmodules.util import numpy_support


class WorkerThread(QThread):
    """用于执行耗时任务的线程类"""
    finished = Signal()

    def __init__(self, dicom_path):
        super().__init__()
        self._is_running = True
        self.dicom_path = os.path.abspath(dicom_path)

    def run(self):
        """执行耗时任务"""
        d2n = convert_dcm_to_nii_and_pet2suv(self.dicom_path)
        if d2n:
            self.finished.emit()

class SamThread(QThread):
    finished = Signal(np.ndarray)

    def __init__(self, predictor, input_box):
        super().__init__()
        self.predictor = predictor
        self.input_box = input_box

    def run(self):
        box = self.input_box.copy()

        if box[0] > box[2]:
            box[0], box[2] = box[2], box[0]
        if box[1] > box[3]:
            box[1], box[3] = box[3], box[1]

        masks, _, _ = self.predictor.predict(
            box=box,
            multimask_output=False
        )

        mask = masks[0].astype(np.uint8)
        self.finished.emit(mask)

class ModelLoader(QThread):
    finished = Signal(object)

    def __init__(self):
        super().__init__()

    def run(self):
        from mobile_sam import sam_model_registry, SamPredictor

        sam_checkpoint = resource_path("checkpoints\\SAM", "mobile_sam.pt")
        device = "cuda" if torch.cuda.is_available() else "cpu"  # 设备类型
        sam = sam_model_registry["vit_t"](checkpoint=sam_checkpoint)
        sam.to(device=device)
        self.predictor = SamPredictor(sam)

        self.finished.emit(self.predictor)

class BuiltThread(QThread):
    actor_ready = Signal(object)  # 信号：每生成一个 Actor 就发给主界面渲染

    def __init__(self, data, spacing):
        super().__init__()
        self.data = data
        self.spacing = spacing

    def run(self):
        # --- 1. 数据转换与轴向对齐 ---
        # 医学 NIfTI 数据索引通常为 (z, y, x)，VTK 需要 (x, y, z) 布局
        # 我们需要确保数据在内存中是连续的
        image_data = np.ascontiguousarray(self.data)

        vtk_data = vtk.vtkImageData()
        # 注意：VTK 的 Dimensions 顺序是 (width, height, depth)
        d, h, w = image_data.shape
        vtk_data.SetDimensions(w, h, d)
        # 严格设置 Spacing，保证物理尺寸正确
        vtk_data.SetSpacing(self.spacing)

        # 将 Numpy 数组转为 VTK 标量数据
        vtk_arr = numpy_support.numpy_to_vtk(image_data.ravel(), deep=True, array_type=vtk.VTK_UNSIGNED_SHORT)
        vtk_data.GetPointData().SetScalars(vtk_arr)

        # --- 2. 离散马奇立方体重建 ---
        dmc = vtk.vtkDiscreteMarchingCubes()
        dmc.SetInputData(vtk_data)
        dmc.GenerateValues(2, 1, 2)  # 参数：(标签数量, 起始值, 结束值)
        dmc.Update()

        # --- 3. 网格平滑 (可选，保持解剖结构平滑) ---
        smoother = vtk.vtkWindowedSincPolyDataFilter()
        smoother.SetInputConnection(dmc.GetOutputPort())
        smoother.SetNumberOfIterations(20)  # 迭代次数，越多越平滑
        smoother.Update()

        # --- 4. 颜色映射表 (LUT) ---
        # 这里精确设置：标签1 -> 蓝色, 标签2 -> 绿色
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(3)  # 0(背景), 1, 2
        lut.Build()
        lut.SetTableValue(0, 0.0, 0.0, 0.0, 0.0)  # 标签0：透明黑色
        lut.SetTableValue(1, 0.0, 0.0, 1.0, 1.0)  # 标签1：纯蓝色 (R, G, B, A)
        lut.SetTableValue(2, 0.0, 1.0, 0.0, 1.0)  # 标签2：纯绿色 (R, G, B, A)
        lut.SetRange(0, 2)

        # --- 5. 渲染配置 ---
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(smoother.GetOutputPort())
        mapper.SetLookupTable(lut)
        mapper.SetScalarRange(0, 2)
        mapper.ScalarVisibilityOn()  # 开启标量着色

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # 设置材质属性，让颜色看起来更真实
        actor.GetProperty().SetInterpolationToGouraud()  # 高洛德插值，增加光泽感
        actor.GetProperty().SetAmbient(0.2)  # 环境光
        actor.GetProperty().SetDiffuse(0.8)  # 漫反射

        self.actor_ready.emit(actor)
