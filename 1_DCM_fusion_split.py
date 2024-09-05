""" 
混合在一起的dicom序列如何划分，根据dicom tag中的模态标签或者Acquisition Number标签
此外还可以参考博客：https://www.jianshu.com/p/a3d105064e78的做法
"""
import pydicom
end_dirs = 'C:/Users/yangyunfeng/Desktop/code/Z_dataset_fusion_split/fusion'
for root2, dirs2, files2 in os.walk(end_dirs):
    flag1 = pydicom.read_file(root2+"/"+files2[0] ,force=True).AcquisitionNumber
    flag2 = flag1+1  
    flag3 = flag2+1
    flag4 = flag3+1                
    for file in files2:
        if file.endswith("dcm"):
            end_dirs2 = root2+"/"+file
            # print(end_dirs2)
        dcm = pydicom.read_file(end_dirs2 ,force=True)                            
        dcm_AcquisitionNumber = dcm.AcquisitionNumber
        if dcm_AcquisitionNumber == flag1:
            # flag = flag1
            shutil.copy(end_dirs2,'C:/Users/yangyunfeng/Desktop/code/Z_dataset_fusion_split/Series_1')
        elif dcm_AcquisitionNumber == flag2:
            shutil.copy(end_dirs2,'C:/Users/yangyunfeng/Desktop/code/Z_dataset_fusion_split/Series_2')
        elif dcm_AcquisitionNumber == flag3:
            shutil.copy(end_dirs2,'C:/Users/yangyunfeng/Desktop/code/Z_dataset_fusion_split/Series_3')
        elif dcm_AcquisitionNumber == flag4:
            shutil.copy(end_dirs2,'C:/Users/yangyunfeng/Desktop/code/Z_dataset_fusion_split/Series_4')
    break
