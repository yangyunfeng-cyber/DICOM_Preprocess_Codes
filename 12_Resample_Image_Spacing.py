"""
用于对图像的spacing进行重采样，使数据保持统一！
"""

def file_name(file_dir):
    """循环目录，对MR进行重采样规范化"""
    for root, dirs, files in os.walk(file_dir):     
        for path in dirs:
            end_dirs = root +'/' + path
            # 对image进行重采样
            if 'T2' in end_dirs:
                imageName = end_dirs +'/Pre_N4_MR.nii'                                   
                print(imageName)   
                newSpacing = [1,1,3]  #可根据数据本身的特点来确定，尽量不过多改变数据
                newSpacing = np.array(newSpacing, float)           
                img = sitk.ReadImage(imageName)   
                newSize = np.array(img.GetSize())* np.array(img.GetSpacing()) / newSpacing 
                newSize = newSize.astype(np.int_)

                resample = sitk.ResampleImageFilter()
                resample.SetSize(newSize.tolist())
                resample.SetOutputSpacing(newSpacing)
                resample.SetInterpolator(sitk.sitkBSpline)
                resample.SetOutputDirection(img.GetDirection())
                resample.SetOutputOrigin(img.GetOrigin())      
                resample.SetTransform(sitk.Transform())
                resample.SetDefaultPixelValue(img.GetPixelIDValue())
  
                newimage = resample.Execute(img)
                sitk.WriteImage(newimage, end_dirs+'/Pre_N4_resam113_MR.nii')              

file_name('./MRI')   #总文件夹
