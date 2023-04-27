#组学特征的意义，详见：https://blog.csdn.net/weixin_46428351/article/details/123592586
#采用的yaml文件，这是我自己修改后用于提取CT的特征的文件，见主文件夹中的CT_my.yaml

# 影像组学批量特征提取
import os
from radiomics import featureextractor
import pandas as pd
import SimpleITK as sitk
import numpy as np

def radiomics_feature_access(all_path):
    """
    功能：根据设定的mask病灶标签对nifty影像进行影像组学特征提取
    输入：包含所有nifty原图像，精准标注的mask 
	"""    
    df = pd.DataFrame()
    img_name_list=[]
    # 提取参数设置，#这个yaml文件里，我更改了提取的轴位，因为我的数据是在sagittal轴位上标注的
    paramPath = 'C:/Users/yangyunfeng/Desktop/code/CT_my.yaml' 
    path_list = os.listdir(all_path)
    path_list.sort(key=lambda x:int(x.split('-')[0]))   #对输出的路径进行排序，然后作为输入
    for img_name in path_list:
        if img_name.split('-')[1][0:3]=="IMG":  
            print(img_name)
            img_name_list.append(img_name)
            imageName = all_path +'/'+img_name
            maskName = imageName.replace('IMG_processed','seg')   
            # print(maskName)  
            extractor = featureextractor.RadiomicsFeatureExtractor(paramPath)            
            featureVector = extractor.execute(imageName,maskName)
            df_add = pd.DataFrame.from_dict(featureVector.values()).T
            df_add.columns = featureVector.keys()
            df= pd.concat([df,df_add])             
            df.to_excel('A:/A_Data_of_hostpitals/A_Data_of_Cancer_hospital/ICH/A_Processed_data/B_ChangSha_test/radiomics_features_CT.xlsx')  
    
    features_df = pd.read_excel("A:/A_Data_of_hostpitals/A_Data_of_Cancer_hospital/ICH/A_Processed_data/B_ChangSha_test/radiomics_features_CT.xlsx") 
    features_df.insert(loc=0, column='Name', value=img_name_list) #在特征表中第一列位置插入图像名字列
    num2 = 0
    unuseful_features = []
    for feature in features_df.columns:
        if 'diagnostics' in feature:       
            unuseful_features.append(feature)
            num2 +=1
    print('共去除了'+str(num2)+'个无用的版本信息特征')  
    features_df.drop(columns=unuseful_features, inplace=True)       
    print('去除版本信息后提取得到的病例个数:{}，放射组学特征个数：{}'.format(features_df.shape[0],features_df.shape[1]))  
    features_df.to_excel("A:/A_Data_of_hostpitals/A_Data_of_Cancer_hospital/ICH/A_Processed_data/B_ChangSha_test/radiomics_features_CT.xlsx",index=False)
radiomics_feature_access('A:/A_Data_of_hostpitals/A_Data_of_Cancer_hospital/ICH/A_Processed_data/B_ChangSha_test/IMG_Seg')
