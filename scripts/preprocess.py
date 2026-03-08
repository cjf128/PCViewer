from typing import Tuple

import numpy as np
import SimpleITK as sitk

from scripts.basic import read_dicom_series, resize_image
from scripts.pet2suv import pet_to_suv


def process_dicom_data(
    ct_folder: str,
    pet_folder: str,
) -> Tuple[sitk.Image, sitk.Image]:
    ct_img = read_dicom_series(ct_folder, "CT")
    pet_suv_img = pet_to_suv(pet_folder)
    pet_aligned = resize_image(pet_suv_img, ct_img, sitk.sitkLinear)
    return ct_img, pet_aligned


def process_nifti_data(
    pet_path: str,
    ct_path: str,
) -> Tuple[sitk.Image, sitk.Image]:
    ct_img = sitk.ReadImage(ct_path)
    ct_img = sitk.DICOMOrient(ct_img, "LPS")

    pet_img = sitk.ReadImage(pet_path)
    pet_img = sitk.DICOMOrient(pet_img, "LPS")

    pet_aligned = resize_image(pet_img, ct_img, sitk.sitkLinear)
    return ct_img, pet_aligned


def sitk_to_numpy(img: sitk.Image) -> Tuple[np.ndarray, Tuple[float, float, float]]:
    data = sitk.GetArrayFromImage(img)
    spacing = img.GetSpacing()
    return data, spacing
