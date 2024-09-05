"""
这部分代码的作用是将dicom格式的医学影像转换nii格式，方便后续处理！
"""

def main(file_dir):
    """
    功能：循环目录将dicom转换为nii
    输入：data总路径   
    """    
    for root, dirs, files in os.walk(file_dir): 
        for path in dirs:
            end_dirs = root +'/' + path 
            savepath ="A:/A_Data_of_hostpitals/A_Data_of_Cancer_hospital/Uterine_prognosis/Processed_img_seg/T2SAG/"   
            # print(end_dirs) 
            if 'T2SAG' in end_dirs:
                img_name = "IMG_pre_T2SAGMR_"+ str(end_dirs.split('/')[-2][4:]) +".nii" #获取病例编号以命名图像
                print(end_dirs)              
                #dicom文件序列可以通过ImageSeriesReader() 来构建一个序列执行器
                dicomsPath = end_dirs  
                reader = sitk.ImageSeriesReader()
                dicomName = reader.GetGDCMSeriesFileNames(dicomsPath)
                reader.SetFileNames(dicomName)
                sitkImage_dicom = reader.Execute()
                print('DICOM的层厚：',sitkImage_dicom.GetSpacing())
                # print("DICOM文件序列读取成功，Size为：{}".format(sitkImage_dicom.GetSize()))                
                # print("原点位置:{}".format(sitkImage_dicom.GetOrigin()))
                # print("尺寸：{}".format(sitkImage_dicom.GetSize()))
                # print("体素大小(x,y,z):{}".format(sitkImage_dicom.GetSpacing()) )
                # print("图像方向:{}".format(sitkImage_dicom.GetDirection()))
                # 成功读取DICOM序列，现在通过WriteImage()另存为Nifit格式文件。
                sitk.WriteImage(sitkImage_dicom,savepath + img_name)  
                # sitk.ResampleImageFilter()
        
main('./img')  
