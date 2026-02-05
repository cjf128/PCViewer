import os
import shutil
import pydicom

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
    for dcm_file in os.listdir(folder_path):
        dcm_path = os.path.join(folder_path, dcm_file)
        try:
            dicom_data = pydicom.dcmread(dcm_path)
            modality = dicom_data.Modality
            if modality == 'PT':
                shutil.copy(dcm_path, dicom_PET_path)
            elif modality == 'CT':
                shutil.copy(dcm_path, dicom_CT_path)
        except Exception as e:
            continue
                