from pathlib import Path
import numpy as np
from PySide6.QtCore import QThread, Signal
from path import BASE_PATH
from scripts.preprocess import convert_dcm_to_nii_and_pet2suv
from scripts.logger import log_info, log_debug, log_error
import vtk
from vtkmodules.util import numpy_support


class WorkerThread(QThread):
    """用于执行耗时任务的线程类"""
    finished = Signal()

    def __init__(self, dicom_path):
        super().__init__()
        self._is_running = True
        self.dicom_path = str(Path(dicom_path).resolve())

    def run(self):
        """执行耗时任务"""
        log_info(f"开始处理DICOM数据: {self.dicom_path}")
        try:
            d2n = convert_dcm_to_nii_and_pet2suv(self.dicom_path)
            if d2n:
                log_info(f"DICOM数据处理完成: {self.dicom_path}")
                self.finished.emit()
            else:
                log_error(f"DICOM数据处理失败: {self.dicom_path}")
        except Exception as e:
            log_error(f"处理DICOM数据时发生错误: {e}")

class SamThread(QThread):
    finished = Signal(np.ndarray)

    def __init__(self, predictor, input_box):
        super().__init__()
        self.predictor = predictor
        self.input_box = input_box

    def run(self):
        log_debug(f"开始SAM预测, 输入框: {self.input_box}")
        try:
            box = self.input_box.copy()

            if box[0] > box[2]:
                box[0], box[2] = box[2], box[0]
            if box[1] > box[3]:
                box[1], box[3] = box[3], box[1]

            box_coords = ((int(box[0]), int(box[1])), (int(box[2]), int(box[3])))
            label_id = 0

            masks = self.predictor.set_box(box_coords, label_id)
            mask = masks[label_id].astype(np.uint8)

            log_debug(f"SAM预测完成, mask形状: {mask.shape}")
            self.finished.emit(mask)
        except Exception as e:
            log_error(f"SAM预测时发生错误: {e}")

class ModelLoader(QThread):
    finished = Signal(object)

    def __init__(self):
        super().__init__()

    def run(self):
        log_info("开始加载SAM2模型")
        try:
            from sam2 import SAM2Image

            encoder_path = BASE_PATH / "models" / "sam2.1_hiera_base_plus_encoder.onnx"
            decoder_path = BASE_PATH / "models" / "sam2.1_hiera_base_plus_decoder.onnx"
            
            log_debug(f"编码器路径: {encoder_path}")
            log_debug(f"解码器路径: {decoder_path}")
            
            self.predictor = SAM2Image(str(encoder_path), str(decoder_path))
            
            log_info("SAM2模型加载完成")
            self.finished.emit(self.predictor)
        except Exception as e:
            log_error(f"加载SAM2模型时发生错误: {e}")

class BuiltThread(QThread):
    actor_ready = Signal(object)

    def __init__(self, data, spacing):
        super().__init__()
        self.data = data
        self.spacing = spacing

    def run(self):
        log_debug(f"开始3D重建, 数据形状: {self.data.shape}")
        try:
            image_data = np.ascontiguousarray(self.data)

            vtk_data = vtk.vtkImageData()
            d, h, w = image_data.shape
            vtk_data.SetDimensions(w, h, d)
            vtk_data.SetSpacing(self.spacing)

            vtk_arr = numpy_support.numpy_to_vtk(image_data.ravel(), deep=True, array_type=vtk.VTK_UNSIGNED_SHORT)
            vtk_data.GetPointData().SetScalars(vtk_arr)

            dmc = vtk.vtkDiscreteMarchingCubes()
            dmc.SetInputData(vtk_data)
            dmc.GenerateValues(2, 1, 2)
            dmc.Update()

            smoother = vtk.vtkWindowedSincPolyDataFilter()
            smoother.SetInputConnection(dmc.GetOutputPort())
            smoother.SetNumberOfIterations(20)
            smoother.Update()

            lut = vtk.vtkLookupTable()
            lut.SetNumberOfTableValues(3)
            lut.Build()
            lut.SetTableValue(0, 0.0, 0.0, 0.0, 0.0)
            lut.SetTableValue(1, 0.0, 0.0, 1.0, 1.0)
            lut.SetTableValue(2, 0.0, 1.0, 0.0, 1.0)
            lut.SetRange(0, 2)

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(smoother.GetOutputPort())
            mapper.SetLookupTable(lut)
            mapper.SetScalarRange(0, 2)
            mapper.ScalarVisibilityOn()

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            actor.GetProperty().SetInterpolationToGouraud()
            actor.GetProperty().SetAmbient(0.2)
            actor.GetProperty().SetDiffuse(0.8)

            log_debug("3D重建完成")
            self.actor_ready.emit(actor)
        except Exception as e:
            log_error(f"3D重建时发生错误: {e}")
