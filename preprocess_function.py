import os
from radiomics import featureextractor
import pandas as pd
import SimpleITK as sitk
from scipy import ndimage
import numpy as np

def get_dilation_mask(allSets_path):
    """
    功能：对精准标注的mask进行膨胀处理，使其包含瘤周区域
    输入：包含所有原图像与精准标注的mask的文件夹路径 ，文件夹分类应参考HCC_response中的样式来   
	"""
    Num = 0
    for root, dirs, _ in os.walk(allSets_path): 
        for path in dirs:
            end_dirs = root +'/' + path 
            if '201' in end_dirs: 
                maskpath = end_dirs + '/seg.nii' 
                itk_MASK = sitk.ReadImage(maskpath)
                MASK = sitk.GetArrayFromImage(itk_MASK) 
                #下面两行代码对mask进行膨胀，此处如果肿瘤在肝边缘处则容易将非肝脏部分mask进去，如果要考虑这个问题需要对肝脏进行分割然后作为img
                struct1 = ndimage.generate_binary_structure(3, 1)#膨胀方法1，对角膨胀
                struct2 = ndimage.generate_binary_structure(3, 2)#膨胀方法2，等距膨胀
                MASK_dilation = ndimage.binary_dilation(MASK, structure=struct2,iterations=5).astype(MASK.dtype)
                    
                MASK_index = np.argwhere(MASK)
                (zstart, _, _), (zstop, _, _) = MASK_index.min(axis=0), MASK_index.max(axis=0) +1
                MASK_dilation[0:zstart,:,:] =0
                MASK_dilation[zstop:-1,:,:] =0

                MASK_dilation = sitk.GetImageFromArray(MASK_dilation)
                MASK_dilation.SetDirection(itk_MASK.GetDirection())
                MASK_dilation.SetOrigin(itk_MASK.GetOrigin())
                MASK_dilation.SetSpacing(itk_MASK.GetSpacing())
                sitk.WriteImage(MASK_dilation, end_dirs+'/dilation_seg.nii')
                Num +=1
                if Num%20==0:
                    print(str(Num) , maskpath)
    print('数据集标签膨胀结束，共处理完'+ str(Num)+'个标签文件！')

def saved_preprocessed(savedImg,origin,direction,xyz_thickness,saved_name):
    newImg = sitk.GetImageFromArray(savedImg)
    newImg.SetOrigin(origin)
    newImg.SetDirection(direction)
    newImg.SetSpacing((xyz_thickness[0], xyz_thickness[1], xyz_thickness[2]))
    sitk.WriteImage(newImg, saved_name)
   
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

def CT_transform_ww_wc(all_path):
    """
    功能：根据设定的mask病灶部位的窗宽窗位对CT图像进行调窗，并规划化CT值到【0，1】
	"""
    Num = 0   
    # CT模态的提取参数设置  
    for root, dirs, _ in os.walk(all_path): 
        for path in dirs:
            end_dirs = root +'/' + path         
            if '201' in end_dirs:         
                imageName = end_dirs +'/IMG.nii'
                maskName = end_dirs+ '/seg.nii'  
                ct = sitk.ReadImage(imageName)
                origin = ct.GetOrigin()
                direction = ct.GetDirection()
                xyz_thickness = ct.GetSpacing()
                ct_array = sitk.GetArrayFromImage(ct)
                seg_array = sitk.GetArrayFromImage(sitk.ReadImage(maskName))
                seg_bg = seg_array == 0
                seg_tumor = seg_array == 1
                ct_bg = ct_array * seg_bg
                ct_tumor = ct_array * seg_tumor
                tumor_min = ct_tumor.min()
                tumor_max = ct_tumor.max() 

                #by tumor (recommended)
                tumor_wide = tumor_max - tumor_min
                tumor_center = (tumor_max + tumor_min) / 2
		#注意这个window_transform函数中的第二个，第三个参数是设置窗宽、窗位的具体值，可以按照自己意愿设置其它的值也可以，此处是根据肿瘤的体素值来设置最好的窗宽窗位
                tumor_wl = window_transform(ct_array, tumor_wide, tumor_center, normal=True) 
                saved_name = os.path.join(end_dirs, 'IMG_ww_wc.nii')
                saved_preprocessed(tumor_wl, origin, direction, xyz_thickness, saved_name)
                Num+=1 
                print(str(Num),imageName)

def radiomics_feature_access(all_path, dataSetsName,mask_name):
    """
    功能：根据设定的mask病灶标签对nifty影像进行影像组学特征提取，可以提取的类型包括：包含瘤周区域与不包含瘤周的所有模态的组学特征
    输入：包含所有nifty原图像，精准标注的mask，膨胀后的mask的文件夹路径 ；数据集的名称；标注文件的名称。tips：文件夹分类应参考HCC_response中的样式来   
	"""
    Num = 0   
    df = pd.DataFrame()
    # CT模态的提取参数设置
    paramPath = '/opt/data/private/C_Liver_Tumor/3D_radiomics_response/pyradiomics-master/examples/exampleSettings/exampleCT.yaml'
    for root, dirs, _ in os.walk(all_path): 
        for path in dirs:
            end_dirs = root +'/' + path           

            if '201' in end_dirs:         
                imageName = end_dirs +'/IMG_ww_wc.nii'
                maskName = end_dirs+ '/'+ mask_name+'.nii'   #此处应该考虑使用MASK.nii还是用mask_resample.nii，调整时注意
                
                extractor = featureextractor.RadiomicsFeatureExtractor(paramPath) 
                featureVector = extractor.execute(imageName,maskName)
                df_add = pd.DataFrame.from_dict(featureVector.values()).T
                df_add.columns = featureVector.keys()
                df= pd.concat([df,df_add])
                Num+=1 
                print(str(Num),imageName)
                print(maskName)                
            df.to_excel('../DataSets_of_Intracerebral_Hemorrhage' + '/excel_data/features_'+ dataSetsName+ '_'+mask_name+'.xlsx',index=False)  
