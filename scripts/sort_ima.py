import os
import shutil
import pydicom

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
    for folder in os.listdir(folder_path):
        ima_folder = os.path.join(folder_path, folder)
        if "WB" in folder and "CT" in folder:
            ima_files = [f for f in os.listdir(ima_folder) if f.endswith(".IMA")]
            dcm_files = [f for f in os.listdir(ima_folder) if f.endswith(".dcm")]
            if ima_files:
                for ima_file in ima_files:
                    ima_path = os.path.join(ima_folder, ima_file)
                    ima_data = pydicom.dcmread(ima_path)
                    if ima_data.Modality == 'CT':
                        ima_path = os.path.join(dicom_CT_path, ima_file.replace(".IMA", ".dcm"))
                        ima_data.save_as(ima_path)

            if dcm_files:
                for dcm_file in dcm_files:
                    dcm_path = os.path.join(ima_folder, dcm_file)
                    dcm_data = pydicom.dcmread(dcm_path)

                    modality = dcm_data.Modality
                    if modality == 'CT':
                        shutil.copy(dcm_path, dicom_CT_path)

        if 'WB' in folder and 'PET' in folder:
            ima_files = [f for f in os.listdir(ima_folder) if f.endswith(".IMA")]
            dcm_files = [f for f in os.listdir(ima_folder) if f.endswith(".dcm")]

            if ima_files:
                for ima_file in ima_files:
                    ima_path = os.path.join(ima_folder, ima_file)
                    ima_data = pydicom.dcmread(ima_path)
                    if ima_data.Modality == 'PT':
                        ima_path = os.path.join(dicom_PET_path, ima_file.replace(".IMA", ".dcm"))
                        ima_data.save_as(ima_path)

            if dcm_files:
                for dcm_file in dcm_files:
                    dcm_path = os.path.join(ima_folder, dcm_file)
                    dcm_data = pydicom.dcmread(dcm_path)
                    modality = dcm_data.Modality
                    if modality == 'PT':
                        shutil.copy(dcm_path, dicom_PET_path)