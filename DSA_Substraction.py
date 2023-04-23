import SimpleITK as sitk

def window_transform(ct_array, windowWidth, windowCenter, normal=False):
    """
   return: trucated image according to window center and window width
   and normalized to [0,1]
    """
    minWindow = float(windowCenter) - 0.5*float(windowWidth)
    newimg = (ct_array - minWindow) / float(windowWidth)
    newimg[newimg < 0] = 0
    newimg[newimg > 1] = 1
    if not normal:
        newimg = (newimg * 255).astype('uint8')
    return newimg

dicomsPath = 'C:/Users/yangyunfeng/Desktop/Files_Store_Workspace/jianying/new'
reader = sitk.ImageSeriesReader()
dicomName = reader.GetGDCMSeriesFileNames(dicomsPath)
reader.SetFileNames(dicomName)
sitkImage_dicom = reader.Execute()
dicom_array = sitk.GetArrayFromImage(sitkImage_dicom)
print(dicom_array.shape)
#去除外层冗余维度
dicom_array_new = dicom_array.squeeze()
min = dicom_array_new.min()
max = dicom_array_new.max() 
windows_wide = max - min
windows_center = (max + min) / 2
dicom_array_ww_wc = window_transform(dicom_array_new,windows_wide,windows_center,True)
sitkImage = sitk.GetImageFromArray(dicom_array_ww_wc)
print(dicom_array_new.shape)           
sitk.WriteImage(sitkImage, 'C:/Users/yangyunfeng/Desktop/Files_Store_Workspace/jianying/new/IMG_ww_wc.nii') 
#对dsa影像进行减影操作，循环减去最后一帧的值
for index in range(dicom_array_ww_wc.shape[0]):
    dicom_array_ww_wc[index] = dicom_array_ww_wc[index]-dicom_array_ww_wc[dicom_array_ww_wc.shape[0]-1]
sitkImage_substract = sitk.GetImageFromArray(dicom_array_ww_wc)
sitk.WriteImage(sitkImage_substract, 'C:/Users/yangyunfeng/Desktop/Files_Store_Workspace/jianying/new/IMG_ww_wc_substract.nii') 
