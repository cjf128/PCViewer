import SimpleITK as sitk

def read_dicom_series(directory: str, modality: str=None) -> sitk.Image:
    """
    directory: DICOM 序列所在文件夹
    return: dicom读取后的sitk的图像
    """
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(directory)
    reader.SetFileNames(dicom_names)
    img = reader.Execute()

    if modality and modality.lower()== "ct":
        stats_filter = sitk.StatisticsImageFilter()
        stats_filter.Execute(img)
        min_pixel = stats_filter.GetMinimum()

        if min_pixel >= 0:
            img = img - 1024.0
    
    return img

def Clamp_ww_wl(image: sitk.Image, ww: float, wl: float) -> sitk.Image:
    """
    image: 输入sitk读取的图像
    ww: 窗宽
    wl: 窗位
    return: 截断过后的sitk图像    
    """
    up = wl + ww / 2
    low = wl - ww / 2
    return sitk.Clamp(sitk.Cast(image, sitk.sitkFloat32), sitk.sitkFloat32, low, up)

def Clamp_value(image: sitk.Image, low: float, up: float) -> sitk.Image:
    """
    image: 输入sitk读取的图像
    up: 上限
    low: 下限
    return: 截断过后的sitk图像    
    """
    return sitk.Clamp(sitk.Cast(image, sitk.sitkFloat32), sitk.sitkFloat32, low, up)

def resize_image_itk(ori_img: sitk.Image, target_img: sitk.Image, resamplemethod=sitk.sitkLinear) -> sitk.Image:
    """
    用itk方法将原始图像resample到与目标图像一致
    :param ori_img: 原始需要对齐的itk图像
    :param target_img: 要对齐的目标itk图像
    :param resamplemethod: itk插值方法: sitk.sitkLinear-线性  sitk.sitkNearestNeighbor-最近邻
    :return:img_res_itk: 重采样好的itk图像
    """
    target_Size = target_img.GetSize()      # 目标图像大小  [x,y,z]
    target_Spacing = target_img.GetSpacing()   # 目标的体素块尺寸    [x,y,z]
    target_origin = target_img.GetOrigin()      # 目标的起点 [x,y,z]
    target_direction = target_img.GetDirection()  # 目标的方向 [冠,矢,横]=[z,y,x]

    # itk的方法进行resample
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(target_img)  # 需要重新采样的目标图像

    # 设置目标图像的信息
    resampler.SetSize(target_Size)		# 目标图像大小
    resampler.SetOutputOrigin(target_origin)
    resampler.SetOutputDirection(target_direction)
    resampler.SetOutputSpacing(target_Spacing)
    
    # 根据需要重采样图像的情况设置不同的dype
    if resamplemethod == sitk.sitkNearestNeighbor:
        resampler.SetOutputPixelType(sitk.sitkUInt8)   # 近邻插值用于mask的，保存uint8
    else:
        resampler.SetOutputPixelType(sitk.sitkFloat32)  # 线性插值用于PET/CT/MRI之类的，保存float32
    resampler.SetTransform(sitk.Transform(3, sitk.sitkIdentity))    
    resampler.SetInterpolator(resamplemethod)
    itk_img_resampled = resampler.Execute(ori_img)  # 得到重新采样后的图像
    itk_img_resampled.CopyInformation(target_img)
    return itk_img_resampled
