import shutil
from pathlib import Path
from typing import Tuple

import numpy as np
import vtk
import SimpleITK as sitk
from PySide6.QtCore import QThread, Signal
from vtkmodules.util import numpy_support

from path import MODELS_PATH
from scripts.logger import log_debug, log_error, log_info
from scripts.preprocess import process_dicom_data, process_nifti_data, sitk_to_numpy
from scripts.sort_dicom import sort_dicom_series


class DicomWorker(QThread):
    finished = Signal(np.ndarray, np.ndarray, tuple, dict)

    def __init__(self, pet_file: str, ct_file: str, cache_folder: Path):
        super().__init__()
        self.pet_file = pet_file
        self.ct_file = ct_file
        self.cache_folder = cache_folder

    def run(self):
        ct_folder = self.cache_folder / "CT"
        pet_folder = self.cache_folder / "PET"
        ct_folder.mkdir(exist_ok=True)
        pet_folder.mkdir(exist_ok=True)

        success_ct, msg_ct = sort_dicom_series(
            self.ct_file, str(ct_folder), str(pet_folder)
        )
        log_info(f"CT处理结果: {msg_ct}")

        success_pet, msg_pet = sort_dicom_series(
            self.pet_file, str(ct_folder), str(pet_folder)
        )
        log_info(f"PET处理结果: {msg_pet}")

        if not success_ct or not success_pet:
            log_error("DICOM文件处理失败")
            return

        log_info("开始处理DICOM数据")
        try:
            ct_img, pet_img = process_dicom_data(str(ct_folder), str(pet_folder))
            ct_data, spacing = sitk_to_numpy(ct_img)
            pet_data, _ = sitk_to_numpy(pet_img)

            # 提取患者信息
            patient_info = {}
            # 从DICOM文件中提取患者信息
            try:
                # 获取CT文件夹中的第一个DICOM文件
                ct_files = list(ct_folder.glob('*.dcm'))
                if ct_files:
                    ct_file = str(ct_files[0])
                    img = sitk.ReadImage(ct_file)
                    # 提取DICOM标签
                    if '0010|0010' in img.GetMetaDataKeys():
                        patient_info['患者名'] = img.GetMetaData('0010|0010')
                    if '0010|0020' in img.GetMetaDataKeys():
                        patient_info['患者ID'] = img.GetMetaData('0010|0020')
                    if '0010|0030' in img.GetMetaDataKeys():
                        patient_info['出生日期'] = img.GetMetaData('0010|0030')
                    if '0010|0040' in img.GetMetaDataKeys():
                        patient_info['性别'] = img.GetMetaData('0010|0040')
                    if '0010|1030' in img.GetMetaDataKeys():
                        patient_info['体重'] = img.GetMetaData('0010|1030')
            except Exception as e:
                log_error(f"提取DICOM患者信息时发生错误: {e}")

            shutil.rmtree(str(ct_folder))
            shutil.rmtree(str(pet_folder))

            log_info(
                f"DICOM数据处理完成, CT形状: {ct_data.shape}, PET形状: {pet_data.shape}"
            )
            self.finished.emit(ct_data, pet_data, spacing, patient_info)
        except Exception as e:
            log_error(f"处理DICOM数据时发生错误: {e}")


class NiftiWorker(QThread):
    finished = Signal(np.ndarray, np.ndarray, tuple, dict)

    def __init__(self, pet_path: str, ct_path: str):
        super().__init__()
        self.pet_path = pet_path
        self.ct_path = ct_path

    def run(self):
        log_info("开始处理NIfTI数据")
        try:
            ct_img, pet_img = process_nifti_data(self.pet_path, self.ct_path)
            ct_data, spacing = sitk_to_numpy(ct_img)
            pet_data, _ = sitk_to_numpy(pet_img)

            # 提取患者信息
            patient_info = {}
            # 从NIfTI文件中提取患者信息
            try:
                # 读取CT文件获取元数据
                ct_img = sitk.ReadImage(self.ct_path)
                # 提取NIfTI头信息
                if ct_img.HasMetaDataKey('PatientName'):
                    patient_info['患者名'] = ct_img.GetMetaData('PatientName')
                if ct_img.HasMetaDataKey('PatientID'):
                    patient_info['患者ID'] = ct_img.GetMetaData('PatientID')
                if ct_img.HasMetaDataKey('PatientBirthDate'):
                    patient_info['出生日期'] = ct_img.GetMetaData('PatientBirthDate')
                if ct_img.HasMetaDataKey('PatientSex'):
                    patient_info['性别'] = ct_img.GetMetaData('PatientSex')
                if ct_img.HasMetaDataKey('PatientWeight'):
                    patient_info['体重'] = ct_img.GetMetaData('PatientWeight')
            except Exception as e:
                log_error(f"提取NIfTI患者信息时发生错误: {e}")

            log_info(
                f"NIfTI数据处理完成, CT形状: {ct_data.shape}, PET形状: {pet_data.shape}"
            )
            self.finished.emit(ct_data, pet_data, spacing, patient_info)
        except Exception as e:
            log_error(f"处理NIfTI数据时发生错误: {e}")


class SamThread(QThread):
    finished = Signal(np.ndarray)

    def __init__(self, predictor, input_box: np.ndarray):
        super().__init__()
        self.predictor = predictor
        self.input_box = input_box

    def _normalize_box(self) -> Tuple[int, int, int, int]:
        box = self.input_box.copy()
        if box[0] > box[2]:
            box[0], box[2] = box[2], box[0]
        if box[1] > box[3]:
            box[1], box[3] = box[3], box[1]
        return int(box[0]), int(box[1]), int(box[2]), int(box[3])

    def run(self):
        log_debug(f"开始SAM预测, 输入框: {self.input_box}")
        try:
            x1, y1, x2, y2 = self._normalize_box()
            masks = self.predictor.set_box(((x1, y1), (x2, y2)), label_id=0)
            mask = masks[0].astype(np.uint8)

            log_debug(f"SAM预测完成, mask形状: {mask.shape}")
            self.finished.emit(mask)
        except Exception as e:
            log_error(f"SAM预测时发生错误: {e}")


class ModelLoader(QThread):
    finished = Signal(object)

    _ENCODER_MODEL = "checkpoints/sam2.1_hiera_base_plus_encoder.onnx"
    _DECODER_MODEL = "checkpoints/sam2.1_hiera_base_plus_decoder.onnx"

    def run(self):
        log_info("开始加载SAM2模型")
        try:
            from models.sam2 import SAM2Image

            encoder_path = MODELS_PATH / self._ENCODER_MODEL
            decoder_path = MODELS_PATH / self._DECODER_MODEL

            log_debug(f"编码器路径: {encoder_path}")
            log_debug(f"解码器路径: {decoder_path}")

            predictor = SAM2Image(str(encoder_path), str(decoder_path))
            log_info("SAM2模型加载完成")
            self.finished.emit(predictor)
        except Exception as e:
            log_error(f"加载SAM2模型时发生错误: {e}")


class BuiltThread(QThread):
    actor_ready = Signal(object)

    def __init__(self, data: np.ndarray, spacing: Tuple[float, float, float]):
        super().__init__()
        self.data = data
        self.spacing = spacing

    def _create_lookup_table(self) -> vtk.vtkLookupTable:
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(3)
        lut.Build()
        lut.SetTableValue(0, 0.0, 0.0, 0.0, 0.0)
        lut.SetTableValue(1, 0.0, 0.0, 1.0, 1.0)
        lut.SetTableValue(2, 0.0, 1.0, 0.0, 1.0)
        lut.SetRange(0, 2)
        return lut

    def run(self):
        log_debug(f"开始3D重建, 数据形状: {self.data.shape}")
        try:
            image_data = np.ascontiguousarray(self.data)

            vtk_data = vtk.vtkImageData()
            d, h, w = image_data.shape
            vtk_data.SetDimensions(w, h, d)
            vtk_data.SetSpacing(self.spacing)

            vtk_arr = numpy_support.numpy_to_vtk(
                image_data.ravel(), deep=True, array_type=vtk.VTK_UNSIGNED_SHORT
            )
            vtk_data.GetPointData().SetScalars(vtk_arr)

            dmc = vtk.vtkDiscreteMarchingCubes()
            dmc.SetInputData(vtk_data)
            dmc.GenerateValues(2, 1, 2)
            dmc.Update()

            smoother = vtk.vtkWindowedSincPolyDataFilter()
            smoother.SetInputConnection(dmc.GetOutputPort())
            smoother.SetNumberOfIterations(20)
            smoother.Update()

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(smoother.GetOutputPort())
            mapper.SetLookupTable(self._create_lookup_table())
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
