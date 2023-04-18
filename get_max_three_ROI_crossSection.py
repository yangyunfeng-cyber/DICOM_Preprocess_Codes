import os
import SimpleITK as sitk
import numpy as np
import cv2
from collections import Counter
from scipy import ndimage

def cal_ROI_counter(mask_img_arr): # 输入mask_img_arry，获取每个层面的不同label的面积值
    all_slice_lable_count = []
    for i in range(mask_img_arr.shape[0]):
        dc = dict(Counter(mask_img_arr[i,:,:].flatten()))
        del dc[0]
        all_slice_lable_count.append(dc)
    return all_slice_lable_count

def get_max_three_pieces(imagePath,maskPath):
    """ 
    功能：选取最大ROI截面及其前后两个截面的图像及其mask
    输入：nifity格式的影像和mask
    输出：最大ROI截面的z轴index
    """
    itk_IMG = sitk.ReadImage(imagePath)
    itk_MASK = sitk.ReadImage(maskPath)
    scan_IMG = sitk.GetArrayFromImage(itk_IMG)
    scan_MASK = sitk.GetArrayFromImage(itk_MASK)   

    #使用阈值法去除脑壳的高信号区，防止后续ROI外延将脑壳纳入
    # scan_IMG[scan_IMG >=1] = 0
    # scan_IMG[scan_IMG <=0.2] = 0

    #输入mask_arry，获取每个层面的不同label的面积值
    all_slice_lable_count = cal_ROI_counter(scan_MASK) 

    max_area = 0 # 预定义ROI的面积
    max_id = 1314 # 预定义ROI的index
    for i in range(len(all_slice_lable_count)):
        if all_slice_lable_count[i]:   
            temp_area = max(all_slice_lable_count[i].values())         
            if temp_area >= max_area:
                max_area = temp_area              
                max_id = i
        else:
            continue       

    #下面两行代码对mask进行膨胀，此处如果肿瘤在边缘处则容易将其它部分mask进去，如果要考虑这个问题需要对器官进行分割然后作为img 
    struct2 = ndimage.generate_binary_structure(3, 2)
    scan_MASK1 = ndimage.binary_dilation(scan_MASK, structure=struct2,iterations=1).astype(scan_MASK.dtype)
    
    scan_MASK2 = np.argwhere(scan_MASK1)
    (_, ystart0, xstart0), (_, ystop0, xstop0) = scan_MASK2.min(axis=0), scan_MASK2.max(axis=0) +1
    ROI_image_numpy = scan_IMG[max_id-1:max_id+2,ystart0:ystop0,xstart0:xstop0]
    ROI_mask = scan_MASK1[max_id-1:max_id+2,ystart0:ystop0,xstart0:xstop0]
    #将矩形框内的非病灶区域去除
    ROI_image_numpy[ROI_mask<1]=0
    image = sitk.GetImageFromArray(ROI_image_numpy)
    mask = sitk.GetImageFromArray(ROI_mask)
    return image,mask

def cut_max_three_ROI_IMG(file_dir,label_name):
    """
    功能：选取最大ROI截面及其前后两个截面的图像及其mask
    输入：data总路径
    输出：得到的三个截面图像及其mask
    """ 
    seg_dir_list = [] 
    img_dir_list = [] 
    for filename in os.listdir(file_dir):               
        file_path = file_dir +'/' + filename        
        if 'seg' in file_path:                    
            seg_dir_list.append(file_path)           
        elif 'ww_wc' in file_path:
            img_dir_list.append(file_path) 
    #获取排序后的img和seg列表   
    seg_dir_list.sort(key=lambda x:int((x.split('/')[-1].split('-')[0])))
    img_dir_list.sort(key=lambda x:int((x.split('/')[-1].split('-')[0]))) 

    for n in range(len(seg_dir_list)):
        print('正在处理第'+ str(n) +'个nii序列')
        seg_dir = seg_dir_list[n]
        vol_dir = img_dir_list[n]

        useful_image, useful_mask = get_max_three_pieces(vol_dir,seg_dir)

        for i in range(useful_image.GetSize()[-1]):
            image_slice = sitk.GetArrayFromImage(useful_image)[i,:,:]
            mask_slice = sitk.GetArrayFromImage(useful_mask)[i,:,:] 
            mask_slice[mask_slice>0] = 1    # 统一所有标签值为1    
            image_name = 'A:/A_Data_of_hostpitals/A_Data_of_Cancer_hospital/ICH/Dicoms_labels/C_dataSet_for2D/'+'image'+'_'+ str(n) +'_'+ str(i) +'_'+label_name+'.png'
            # mask_name = 'A:/A_Data_of_hostpitals/A_Data_of_Cancer_hospital/ICH/Dicoms_labels/GoodOutcome/C_dataSet_for2D/'+'mask'+ '_'+ str(n) +'_'+ str(i) +'label-1.png'        
            
            image_slice = cv2.resize(image_slice, (512,512)) 
           
            cv2.imwrite(image_name, (image_slice*255.0).astype('uint8')) 
            # cv2.imwrite(mask_name, (mask_slice*255.0).astype('uint8') ) 
 
PoorOutcom_path = 'A:/A_Data_of_hostpitals/A_Data_of_Cancer_hospital/ICH/Dicoms_labels/PoorOutcome/B_DataSet_for_deep_learning'
GoodOutcom_path = 'A:/A_Data_of_hostpitals/A_Data_of_Cancer_hospital/ICH/Dicoms_labels/GoodOutcome/B_DataSet_for_deep_learning'
cut_max_three_ROI_IMG(PoorOutcom_path,'label-0')  
cut_max_three_ROI_IMG(GoodOutcom_path,'label-1')  
