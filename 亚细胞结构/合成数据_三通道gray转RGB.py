import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from PIL import Image
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
# import tensorflow as tf
import cv2


dataframe = pd.read_csv('./human-protein-atlas-image-classification/train.csv')
# print(dataframe.head(5))
INPUT_SHAPE = (512, 512, 3)
BATCH_SIZE = 16
path_to_train = './human-protein-atlas-image-classification/train/'
dataframe["complete_path"] = path_to_train + dataframe["Id"]
# print(dataframe.head(5))

# for i in range(3):
#     for j in range(4):
#         idx = random.randint(0, dataframe.shape[0])
#         row = dataframe.iloc[idx, :]
#         path = row.complete_path
for path in dataframe["complete_path"]:
    red = np.array(Image.open(path + '_red.png'))
    green = np.array(Image.open(path + '_green.png'))
    blue = np.array(Image.open(path + '_blue.png'))
    im = np.stack((
        red,
        green,
        blue), -1)

    dst = Image.fromarray(im)
    pic_name = path.split("/")[-1]
    dst.save('./human-protein-atlas-image-classification/rgb/' + pic_name + '_dst.png')




# import cv2
# import numpy as np
# import os
#
#
# path = r'C:\Users\RTX3090\Pictures\gjj\dataset\4_Subcell\human-protein-atlas-image-classification\train\000a6c98-bb9b-11e8-b2b9-ac1f6b6435d0'
#
# red = np.array(cv2.imread(path + '_red.png'))
# green = np.array(cv2.imread(path + '_green.png'))
# blue = np.array(cv2.imread(path + '_blue.png'))
# im = np.stack((
#     red,
#     green,
#     blue), -1)
# # 转换成int8类型
# img = np.int8(im)
# cv2.imshow("fill_color", img)
# cv2.waitKey(0)
#
#
# # path = 'D:/lbq/dataset/multi_stained/train/HEPG2-01/Plate1/'
# #
# # for filename in os.listdir(path):
# #     image = cv2.imread(path + filename)
# #     B, G, R = cv2.split(image)  # 分离出图片的 BGR 颜色通道
# #     zeros = np.zeros(image.shape[:2], dtype="uint8")  # 创建与 imgae 大小相同的零矩阵
# #     if filename[-5] == '1':
# #         dst = cv2.merge([B, zeros, zeros])
# #         cv2.imwrite(path + filename[:-4] + '.jpg', dst)
# #     elif filename[-5] == '2':
# #         dst = cv2.merge([zeros, G, zeros])
# #         cv2.imwrite(path + filename[:-4] + '.jpg', dst)
# #     elif filename[-5] == '3':
# #         dst = cv2.merge([zeros, zeros, R])
# #         cv2.imwrite(path + filename[:-4] + '.jpg', dst)
# #     elif filename[-5] == '4':
# #         dst = cv2.merge([B, G, zeros])
# #         cv2.imwrite(path + filename[:-4] + '.jpg', dst)
# #     elif filename[-5] == '5':
# #         dst = cv2.merge([zeros, G, R])
# #         cv2.imwrite(path + filename[:-4] + '.jpg', dst)
# #     elif filename[-5] == '6':
# #         dst = cv2.merge([B, zeros, R])
# #         cv2.imwrite(path + filename[:-4] + '.jpg', dst)
#
# # path = 'D:/lbq/dataset/multi_stained/train/HEPG2-01/p1_rgb/'
# # image1 = cv2.imread(path + 'B02_s1_w1.jpg')
# # image2 = cv2.imread(path + 'B02_s1_w2.jpg')
# # image3 = cv2.imread(path + 'B02_s1_w3.jpg')
# # image4 = cv2.imread(path + 'B02_s1_w4.jpg')
# # image5 = cv2.imread(path + 'B02_s1_w5.jpg')
# # image6 = cv2.imread(path + 'B02_s1_w6.jpg')
# # add1 = cv2.add(image1, image2, image3)
# # add2 = cv2.add(image4, image5, image6)
# # add = cv2.add(add1,add2)
# # cv2.imshow('dst',add)
# # cv2.waitKey(0)
#
#
