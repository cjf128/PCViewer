import shutil
import pydicom
from pathlib import Path

def sort_dcm(folder_path: str, dicom_CT_path: str, dicom_PET_path: str) -> None:
    """
    sort_dcm 的 Docstring
    
    :param folder_path: 患者文件夹，里面有CT和PET文件夹
    :type folder_path: str
    :param dicom_CT_path: 患者的最终存储CT的文件夹
    :type dicom_CT_path: str
    :param dicom_PET_path: 患者最终存储PET的文件夹
    :type dicom_PET_path: str
    """
    folder_path = Path(folder_path)
    for dcm_file in folder_path.iterdir():
        try:
            dicom_data = pydicom.dcmread(str(dcm_file))
            modality = dicom_data.Modality
            if modality == 'PT':
                shutil.copy(str(dcm_file), dicom_PET_path)
            elif modality == 'CT':
                shutil.copy(str(dcm_file), dicom_CT_path)
        except Exception as e:
            continue
