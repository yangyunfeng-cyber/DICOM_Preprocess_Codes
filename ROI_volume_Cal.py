def ROI_volume_Cal_nii(maskName):  
    """
    功能：对ROI的占位体积进行计算
    输入：真实ROI的路径
    输出：ROI的占位体积
    """
    sitkImage = sitk.ReadImage(maskName) 
    maskArr = sitk.GetArrayFromImage(sitkImage)  #order:z,y,x
    counts = np.sum(maskArr !=0)    #标签中包含的体素的个数
    spacing = sitkImage.GetSpacing()  #order:x,y,z  每个体素的间隔  
    unitVol = np.prod(spacing)#单个体素的单位体积 
    roiVol = unitVol * counts  #计算label肿瘤病灶的体积，单位是立方毫米
    return roiVol
