"""
这段代码是用来将MRI的灰度值归一化的
"""

def file_name(file_dir):
    """循环目录，将MR的灰度值归一化到[0，255]"""
    for root, dirs, files in os.walk(file_dir):     
        for path in dirs:
            end_dirs = root +'/' + path
            # 对image进行重采样
            if 'T2' in end_dirs:
                imageName = end_dirs +'/Pre_N4_resam113_MR.nii'                                 
                image= sitk.ReadImage(imageName)               
                resacleFilter = sitk.RescaleIntensityImageFilter()
                resacleFilter.SetOutputMaximum(255)
                resacleFilter.SetOutputMinimum(0)
                image = resacleFilter.Execute(image)
                sitk.WriteImage(image, end_dirs+'/Pre_N4_resam113_norm_MR.nii') 
                print(imageName)             

file_name('./BaiduNetdiskDownload')    

