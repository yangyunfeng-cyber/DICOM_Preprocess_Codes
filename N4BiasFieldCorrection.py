def file_name(file_dir):
    """循环目录，对MR进行N4偏置场校正"""
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

file_name('A:/BaiduNetdiskDownload/tu xiang-zhao')    
