import shutil
import pydicom
from pathlib import Path

def sort_ima(folder_path: str, dicom_CT_path: str, dicom_PET_path: str) -> None:
    """
    sort_ima 的 Docstring
    
    :param folder_path: 患者文件夹，里面有CT和PET文件夹
    :type folder_path: str
    :param dicom_CT_path: 患者的最终存储CT的文件夹
    :type dicom_CT_path: str
    :param dicom_PET_path: 患者最终存储PET的文件夹
    :type dicom_PET_path: str
    """
    folder_path = Path(folder_path)
    for folder in folder_path.iterdir():
        ima_folder = folder
        if "WB" in folder.name and "CT" in folder.name:
            ima_files = [f for f in ima_folder.iterdir() if f.suffix == ".IMA"]
            dcm_files = [f for f in ima_folder.iterdir() if f.suffix == ".dcm"]
            if ima_files:
                for ima_file in ima_files:
                    ima_data = pydicom.dcmread(str(ima_file))
                    if ima_data.Modality == 'CT':
                        new_path = Path(dicom_CT_path) / (ima_file.stem + ".dcm")
                        ima_data.save_as(str(new_path))

            if dcm_files:
                for dcm_file in dcm_files:
                    dcm_data = pydicom.dcmread(str(dcm_file))

                    modality = dcm_data.Modality
                    if modality == 'CT':
                        shutil.copy(str(dcm_file), dicom_CT_path)

        if 'WB' in folder.name and 'PET' in folder.name:
            ima_files = [f for f in ima_folder.iterdir() if f.suffix == ".IMA"]
            dcm_files = [f for f in ima_folder.iterdir() if f.suffix == ".dcm"]

            if ima_files:
                for ima_file in ima_files:
                    ima_data = pydicom.dcmread(str(ima_file))
                    if ima_data.Modality == 'PT':
                        new_path = Path(dicom_PET_path) / (ima_file.stem + ".dcm")
                        ima_data.save_as(str(new_path))

            if dcm_files:
                for dcm_file in dcm_files:
                    dcm_data = pydicom.dcmread(str(dcm_file))
                    modality = dcm_data.Modality
                    if modality == 'PT':
                        shutil.copy(str(dcm_file), dicom_PET_path)
