import pydicom
import numpy as np
import SimpleITK as sitk 

def dicom_hhmmss(t: str) -> float:
    """
    t: DICOM的时间格式
    将DICOM时间格式转换为总秒数，支持HHMMSS.FFFFFF格式
    """
    t = str(t)
    if '.' in t:
        t = t.split('.')[0]
    if len(t) == 5:
        t = '0' + t

    try:
        h_t = float(t[0:2])
        m_t = float(t[2:4])
        s_t = float(t[4:6])
        return h_t * 3600 + m_t * 60 + s_t
    except (ValueError, IndexError):
        return 0.0

def extract_dicom_metadata(dicom_file_path: str) -> tuple[list, sitk.Image]:
    """
    dicom_file_path: pet的文件夹路径，文件夹下是dcm序列文件
    提取 PET DICOM 序列的元数据并返回图像对象。
    """
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dicom_file_path)
    reader.SetFileNames(dicom_names)
    pet_sitk = reader.Execute()

    ds = pydicom.dcmread(dicom_names[0])
    try:
        radio_info = ds.RadiopharmaceuticalInformationSequence[0]
    except (AttributeError, IndexError):
        raise ValueError(f"DICOM file {dicom_names[0]} lacks Radiopharmaceutical Information")

    # 提取所有关键字段
    metadata = {
        'PatientWeight': float(getattr(ds, 'PatientWeight', 70.0)),
        'StudyTime': getattr(ds, 'AcquisitionTime', ds.StudyTime),
        'RadiopharmaceuticalStartTime': getattr(radio_info, 'RadiopharmaceuticalStartTime', ""),
        'RadionuclideTotalDose': float(radio_info.RadionuclideTotalDose),
        'RadionuclideHalfLife': float(radio_info.RadionuclideHalfLife),
        'RescaleSlope': float(getattr(ds, 'RescaleSlope', 1.0)),
        'RescaleIntercept': float(getattr(ds, 'RescaleIntercept', 0.0))
    }
    
    return metadata, pet_sitk

def pet_to_suv(dicom_file_path: str, patient_id: str | None = "Unknown", norm: bool = False) -> sitk.Image:
    """
    将 PET 图像转换为 SUV 图像。
    
    参数:
    - meta: 包含 DICOM 关键信息的字典 (如体重、注射剂量、衰减校正时间)
    - PET: SimpleITK Image 对象
    - norm: 是否将结果归一化到 [0, 1] 或进行标准化
    """
    meta, PET = extract_dicom_metadata(dicom_file_path)

    # 统一使用字典获取参数，防止索引错位
    ST = meta['StudyTime']
    RST = meta['RadiopharmaceuticalStartTime']
    PW = float(meta['PatientWeight'])
    RTD = float(meta['RadionuclideTotalDose'])
    RHL = float(meta['RadionuclideHalfLife'])
    RS = float(meta['RescaleSlope'])
    RI = float(meta['RescaleIntercept'])

    # 1. 计算衰减时间
    time_acq = dicom_hhmmss(ST)
    time_inj = dicom_hhmmss(RST)
    decay_time = time_acq - time_inj
    if decay_time < 0:
        decay_time += 24 * 3600

    # 2. 衰减剂量
    decay_dose = RTD * pow(2, -decay_time / RHL)

    # 3. SUV 因子 (g/ml)
    # 注意：如果 RTD 单位是 Bq，PW 是 kg，1000*PW 换算成 g，结果是合理的
    SUVbwScaleFactor = (1000.0 * PW) / decay_dose

    # --- DEBUG 打印 ---
    if patient_id != "Unknown":
        print(f"\n[DEBUG - {patient_id}]")
        print(f"  > 体重: {PW} kg, 总剂量: {RTD} Bq")
        print(f"  > 采集时间: {ST}, 注射时间: {RST}, 衰减秒数: {decay_time}s")
        print(f"  > 半衰期: {RHL}s, 衰减后剂量: {decay_dose:.2f} Bq")
        print(f"  > RescaleSlope: {RS}, RescaleIntercept: {RI}")
        print(f"  > *** SUV Scale Factor ***: {SUVbwScaleFactor:.8f}")
        print(f"  > 原始像素 Max: {np.max(PET):.2f}, Min: {np.min(PET):.2f}")
    # ------------------

    if norm:
        # 重要：如果图像看起来异常，可能是 RS/RI 已经被 sitk 应用过了
        PET_SUV = (PET * RS + RI) * SUVbwScaleFactor
    else:
        PET_SUV = PET * SUVbwScaleFactor

    return PET_SUV
