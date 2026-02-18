from pathlib import Path

import SimpleITK as sitk

from scripts.pet2suv import pet_to_suv
from scripts.basic import Clamp_value, Clamp_ww_wl, read_dicom_series, resize_image_itk

def convert_dcm_to_nii_and_pet2suv(data_path: str) -> bool:
    data_path = Path(data_path)
    patient_id = data_path.name
    for folder in data_path.iterdir():
        if 'CT' in folder.name:
            dicom_path_CT = data_path / 'CT'
        
            ct_img = read_dicom_series(str(dicom_path_CT))
            ct_img = Clamp_ww_wl(ct_img, 400, 40)

            filename_final_CT: str = patient_id + "_0001.nii.gz"
            save_path_CT = data_path / filename_final_CT
            sitk.WriteImage(ct_img, str(save_path_CT))


        if 'PET' in folder.name:
            dicom_path_PET = data_path / 'PET'

            pet_suv_img = pet_to_suv(str(dicom_path_PET))

            suv_resampled = resize_image_itk(pet_suv_img, ct_img, sitk.sitkLinear)
            suv_image = Clamp_value(suv_resampled, 0.0, 20.0)

            filename_final_PET: str = patient_id + "_0000.nii.gz"
            save_path_PET = data_path / filename_final_PET
            sitk.WriteImage(suv_image, str(save_path_PET))

    return 1
