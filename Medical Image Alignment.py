import SimpleITK as sitk
import os

def register_images(fixed_image_path, moving_image_path):
    # 读取固定图像和移动图像
    fixed_image = sitk.ReadImage(fixed_image_path, sitk.sitkFloat32)
    moving_image = sitk.ReadImage(moving_image_path, sitk.sitkFloat32)    
    # 创建配准对象
    registration = sitk.ImageRegistrationMethod()    
    # 设置相似度度量标准（可根据需求选择其他度量标准）
    registration.SetMetricAsMattesMutualInformation()    
    # 设置优化方法（可根据需求选择其他优化方法）
    registration.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100, estimateLearningRate=registration.Once)    
    # 设置插值器（可根据需求选择其他插值器）
    registration.SetInterpolator(sitk.sitkLinear)    
    # 设置采样策略
    registration.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    registration.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    registration.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()    
    # 执行配准
    transform = registration.Execute(fixed_image, moving_image)    
    # 应用变换到移动图像
    registered_image = sitk.Resample(moving_image, fixed_image, transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())    
    return registered_image


file_dir = 'A:/A_Data_of_hostpitals/A_Data_of_Cancer_hospital/brain_cancer/A_processed_data' 
fixed_image_path_all = []
moving_image_path_T1_all = []
moving_image_path_T2_all = []
for root, dirs, files in os.walk(file_dir):     
        for path in dirs:
            end_dirs = root +'/' + path        
            if 'T' in end_dirs:
                if '+' in end_dirs:                 
                    fixed_image_path_all.append(end_dirs.replace('\\','/') +'/'+'Pre_N4_resam113_MR.nii') 
                elif 'T1' in end_dirs:
                    moving_image_path_T1_all.append(end_dirs.replace('\\','/') +'/'+'Pre_N4_resam113_MR.nii')
                elif 'T2' in end_dirs:
                    moving_image_path_T2_all.append(end_dirs.replace('\\','/') +'/'+'Pre_N4_resam113_MR.nii')                       
 
for n in range(len(fixed_image_path_all)):
    fixed_image_path= fixed_image_path_all[n]
    moving_image_path_T1 = moving_image_path_T1_all[n]
    moving_image_path_T2 = moving_image_path_T2_all[n]  
    
    registered_image_T1 = register_images(fixed_image_path, moving_image_path_T1)
    registered_image_T2 = register_images(fixed_image_path, moving_image_path_T2)
    # # 保存配准后的图像
    sitk.WriteImage(registered_image_T1, moving_image_path_T1.replace('Pre_N4_resam113_MR.nii','registered_image.nii'))
    sitk.WriteImage(registered_image_T2, moving_image_path_T2.replace('Pre_N4_resam113_MR.nii','registered_image.nii'))
    print(n)
    print(moving_image_path_T1.replace('Pre_N4_resam113_MR.nii','registered_image.nii'))

