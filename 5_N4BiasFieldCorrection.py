"""
医学图像，尤其是磁共振成像（MRI）图像，常常受到偏置场的影响，这种偏置场是由于磁场不均匀或其他因素导致的强度变化。偏置场会导致图像在不同区域的强度不均匀，从而影响图像的质量和后续的分析结果。
N4 偏置场校正算法是 N3 偏置场校正算法的改进版本，它通过估计和校正图像的偏置场来减少这种不均匀性。该算法是一种非参数的自适应方法，基于图像的统计特性来实现校正。
"""

def file_name(file_dir):
    """循环目录，对MRI进行N4偏置场校正"""
    N=0
    for root, dirs, files in os.walk(file_dir):             
        for path in dirs:
            end_dirs = root +'/' + path          
            if 'T1' in end_dirs:
                imageName = end_dirs +'/Pre_MR.nii'   
                print(imageName)                               
                input_image = sitk.ReadImage(imageName)  
                mask_image = sitk.OtsuThreshold(input_image, 0, 1, 200)
                input_image = sitk.Cast(input_image, sitk.sitkFloat32)
                corrector = sitk.N4BiasFieldCorrectionImageFilter()
                output_image = corrector.Execute(input_image, mask_image)
                output_image = sitk.Cast(output_image, sitk.sitkInt16)
                sitk.WriteImage(output_image, end_dirs+'/Pre_N4_MR.nii')
                N=N+1
                print('已完成个数：', N)                        

file_name('A:/BaiduNetdiskDownload')    
