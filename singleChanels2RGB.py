import os

from PIL import Image
import numpy as np

# 加载灰度图像
# root_path = './Test_Yi_Yuan/PCNSL'
# root_path = './Train_Er_Yuan/GBM'
root_path = './Train_Er_Yuan_maxROI/PCNSL'

for img in os.listdir(root_path):
    img_path = root_path+'/'+img
    gray_image = Image.open(img_path)

    # 将灰度图像转换为Numpy数组
    gray_array = np.array(gray_image)
    print(gray_array.shape)

    # 复制数组，扩展为3通道
    rgb_array = np.repeat(gray_array[:, :, np.newaxis], 3, axis=2)
    print(rgb_array.shape)

    # 将Numpy数组转换回PIL图像并保存
    rgb_image = Image.fromarray(rgb_array)
    rgb_image.save(img_path)


# import os
# def batch_rename_images(directory):
#     # 遍历指定目录下的所有文件
#     for filename in os.listdir(directory):
#         if  filename.endswith('.png'):
#             # 构建新的文件名
#             new_filename = "PCNSL-" + filename

#             # 生成旧文件的路径和新文件的路径
#             old_filepath = os.path.join(directory, filename)
#             new_filepath = os.path.join(directory, new_filename)

#             # 重命名文件
#             os.rename(old_filepath, new_filepath)
#             print(f'Renamed {filename} to {new_filename}')


# # 指定目录
# directory = './Train_Er_Yuan_maxROI/PCNSL'

# # 执行批量更改图像名称
# batch_rename_images(directory)
