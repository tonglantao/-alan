from PIL import Image
import os
import numpy as np
import glob

# 原图
Path_1 = r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\cityscapes\巨噬细胞\leftImg8bit\train'
# 标签
Path_2 = r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\cityscapes\巨噬细胞\gtFine\train'
# 验证效果
Path_3 = r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\2_数据集验证'

source_imgs = glob.glob(os.path.join(Path_1, "*.png"))
label_imgs = glob.glob(os.path.join(Path_2, "*.png"))

for img_path in zip(source_imgs, label_imgs):
    # print(img_path[0], img_path[1])
    base_name = os.path.basename(img_path[0])
    source = np.array(Image.open(img_path[0]))
    label = np.array(Image.open(img_path[1]).convert('RGB'))  # 最大值为1

    height = label.shape[0]  # 将tuple中的元素取出，赋值给height，width，channels
    width = label.shape[1]
    channels = label.shape[2]

    for channel in range(channels):  # 遍历每个通道（三个通道分别是RGB）
        if channel == 0:
            for row in range(height):  # 遍历每一行
                for col in range(width):  # 遍历每一列
                    if label[row][col][channel] > 0:
                        source[row][col][channel + 1] = int(source[row][col][channel] / 3)
    # print(np.shape(label) == np.shape(source))

    dst = source + label * 10
    dst_name = os.path.join(Path_3, base_name)
    img_tr = Image.fromarray(dst)
    img_tr.save(dst_name)
