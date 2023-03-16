from  process_function import get_dilation_mask,radiomics_feature_access,CT_transform_ww_wc

print('开始调整CT图像的窗宽窗位并规范化！')  
CT_transform_ww_wc(all_path='../DataSets_of_Intracerebral_Hemorrhage/Dicoms_labels/GoodOutcome/A_DataSet_for_access_pyradiomics')  
print('GoodOutcome数据集的CT图像的窗宽窗位和规范化完毕，开始处理PoorOutcome数据集！')                        
CT_transform_ww_wc(all_path='../DataSets_of_Intracerebral_Hemorrhage/Dicoms_labels/PoorOutcome/A_DataSet_for_access_pyradiomics') 

print('开始调整icc_computer数据集中的CT图像的窗宽窗位并规范化！')  
CT_transform_ww_wc(all_path='../DataSets_of_Intracerebral_Hemorrhage/icc_computer')  


print('开始进行训练集的病灶标签膨胀！')
get_dilation_mask('../DataSets_of_Intracerebral_Hemorrhage/Dicoms_labels/GoodOutcome/')   #调用标签膨胀函数
print('训练集处理完成，开始进行测试集的病灶标签膨胀！')
get_dilation_mask('../DataSets_of_Intracerebral_Hemorrhage/Dicoms_labels/PoorOutcome/')   
print('标签膨胀处理结束！')

#使用调整好窗宽和窗位并规范化好的数据，提取挑选出来的20例数据的特征，用来计算ICC
print('开始提取挑选处理的20例数据集的特征！首先是seg.nii')                        
radiomics_feature_access(all_path='../DataSets_of_Intracerebral_Hemorrhage/icc_computer',dataSetsName='ICC_Computer',mask_name='seg')   
print('开始提取挑选处理的20例数据集的特征！其次是seg2.nii')                        
radiomics_feature_access(all_path='../DataSets_of_Intracerebral_Hemorrhage/icc_computer',dataSetsName='ICC_Computer',mask_name='seg2')   


print('开始提取包含瘤周的GoodOutcome集组学特征！')  
radiomics_feature_access(all_path='../DataSets_of_Intracerebral_Hemorrhage/Dicoms_labels/GoodOutcome/A_DataSet_for_access_pyradiomics',dataSetsName='GoodOutcome',mask_name='dilation_seg')   #调用特征提取函数
print('GoodOutcome数据集的包含瘤周特征提取完毕，开始提取PoorOutcome数据集的包含瘤周特征！')                        
radiomics_feature_access(all_path='../DataSets_of_Intracerebral_Hemorrhage/Dicoms_labels/PoorOutcome/A_DataSet_for_access_pyradiomics',dataSetsName='PoorOutcome',mask_name='dilation_seg')   

print('开始提取精准标签的训练集组学特征！')  
radiomics_feature_access(all_path='../DataSets_of_Intracerebral_Hemorrhage/Dicoms_labels/GoodOutcome/A_DataSet_for_access_pyradiomics',dataSetsName='GoodOutcome',mask_name='seg')   #调用特征提取函数
print('GoodOutcome数据集的精准特征提取完毕，开始提取PoorOutcome数据集的精准标签特征！')                        
radiomics_feature_access(all_path='../DataSets_of_Intracerebral_Hemorrhage/Dicoms_labels/PoorOutcome/A_DataSet_for_access_pyradiomics',dataSetsName='PoorOutcome',mask_name='seg')    
