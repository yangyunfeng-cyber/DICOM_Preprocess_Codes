""""
这部分代码是本人根据DSA(数字血管造影图像）的减影原理写的，琢磨了一下，基本功能都实现了,效果一般但能将减影后的图像进行保存（Radiant软件也能进行减影操作，但是软件里面无法保存减影后的图像）
目前没有在网上看到有DSA减影的开源代码，这可能是头一份。
"""
import SimpleITK as sitk
import os

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

def main(file_dir):
    """
    功能：DSA减影及窗宽窗位调整
    输入：data总路径   
    """    
    for root, dirs, files in os.walk(file_dir): 
        for path in dirs:
            end_dirs = root +'/' + path               
            if 'SE' in end_dirs:
                for dicomName in os.listdir(end_dirs):
                    if dicomName.endswith('nii'):
                        continue
                    else:
                        dicomPath = end_dirs +'/'+dicomName  

                        sitk_dicom = sitk.ReadImage(dicomPath)
                        dicom_array = sitk.GetArrayFromImage(sitk_dicom)
                        print(dicomPath)
                        # print(dicom_array.shape)  
                        #下面这6行代码是按照整体的CT值来确定窗宽窗位，但是好像根据radiant推荐的窗宽窗位对DSA减影效果显示比较好，故注释掉                
                        # min = dicom_array.min()
                        # max = dicom_array.max() 
                        # windows_wide = max - min
                        # windows_center = (max + min) / 2
                        # print('cent',windows_center)
                        # print('wide',windows_wide)

                        dicom_array_ww_wc = window_transform(dicom_array,640,508,True)
                        # dicom_array_ww_wc = dicom_array

                        # sitkImage = sitk.GetImageFromArray(dicom_array_ww_wc)                            
                        # sitk.WriteImage(sitkImage, dicomPath.replace(dicomName,dicomName+'_ww_wc.nii')) 
                        # 对dsa影像进行减影操作，循环减去最后一帧的值
                        for index in range(dicom_array_ww_wc.shape[0]):
                            dicom_array_ww_wc[index] = dicom_array_ww_wc[index]-dicom_array_ww_wc[-1]                      
                        sitkImage_substract = sitk.GetImageFromArray(dicom_array_ww_wc)
                        sitk.WriteImage(sitkImage_substract, dicomPath.replace(dicomName,dicomName+'_substraction.nii')) 

main('A:/A_Data_of_hostpitals/B_Data_of_RuiJin_Hospital/Five_TAE_data-0423')
