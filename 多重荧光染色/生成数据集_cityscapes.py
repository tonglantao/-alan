'''

注意调色板，
cityscapes的r，g，b值与index相同
voc的的r，g，b值随意

'''

import numpy as np  # linear algebra
# import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from PIL import Image
import matplotlib.pyplot as plt
import os
# from sklearn.model_selection import train_test_split
# import tensorflow as tf
import cv2

path = r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\0_source'
bcell_path = os.path.join(r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\cityscapes\B细胞\leftImg8bit')
virus_path = os.path.join(r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\cityscapes\巨噬细胞\leftImg8bit')
nucle_path = os.path.join(r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\cityscapes\细胞核\leftImg8bit')

bcell_seg = os.path.join(
    r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\cityscapes\B细胞\gtFine')
nucle_seg = os.path.join(
    r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\cityscapes\细胞核\gtFine')
virus_seg = os.path.join(
    r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\cityscapes\巨噬细胞\gtFine')

for root, dirs, files in os.walk(path):
    for dir in dirs:
        sub_dir = os.path.join(path, dir)
        virus_img = []
        virus_seg_img = []

        for filename in os.listdir(sub_dir):
            src = filename.find('original') > 0
            seg = filename.find('segment') > 0
            # src_red = []
            if seg:
                src_red = filename.find('CD14') > 0 or filename.find('CD163') > 0
                src_green = filename.find('DAPI') > 0
                src_blue = filename.find('Pax5') > 0
                src_path = os.path.join(sub_dir, filename)
                src_img = Image.open(src_path)
                src_single = np.array(src_img)
                if src_red:
                    virus_seg_img.append(src_single)
                if src_green:
                    img_tr = Image.fromarray(src_single)
                    bmp_P_web = img_tr.convert('P')
                    web_palette = bmp_P_web.getpalette()  # <---
                    data = np.array(bmp_P_web)
                    # second part
                    bmp = Image.fromarray(data)
                    bmp.putpalette([
                        0, 0, 0,  # black background
                        1, 1, 1,  # index 1 is red
                        # 255, 255, 0,  # index 2 is yellow
                        # 255, 0, 255,  # index 3 is orange
                    ])
                    bmp.save(bcell_seg + '/' + dir + '_gtFine_labelIds.png')
                if src_blue:
                    img_tr = Image.fromarray(src_single)
                    bmp_P_web = img_tr.convert('P',  colors=3)
                    web_palette = bmp_P_web.getpalette()  # <---
                    data = np.array(bmp_P_web)
                    # second part
                    bmp = Image.fromarray(data)
                    bmp.putpalette([
                        0, 0, 0,  # index 0 is black background
                        1, 1, 1,  # index 1 is blue
                        # 255, 0, 0,  # index 2 is red
                    ])
                    bmp.save(nucle_seg + '/' + dir + '_gtFine_labelIds.png')

            if src:
                # src_path = os.path.join(sub_dir, filename)
                # src_single = np.array(Image.open(src_path))
                # src_img.append(src_single)
                src_red = filename.find('CD14') > 0 or filename.find('CD163') > 0
                src_green = filename.find('DAPI') > 0
                src_blue = filename.find('Pax5') > 0
                src_path = os.path.join(sub_dir, filename)
                src_single = np.array(Image.open(src_path))
                if src_red:
                    virus_img.append(src_single)
                if src_green:
                    zeros = np.zeros(src_single.shape, dtype="uint8")
                    bcell_im = np.stack((
                        zeros,
                        src_single,
                        zeros), -1)
                    bcell_dst = Image.fromarray(bcell_im)
                    bcell_dst.save(bcell_path + '/' + dir + '_leftImg8bit.png')
                if src_blue:
                    zeros = np.zeros(src_single.shape, dtype="uint8")
                    nuclei_im = np.stack((
                        zeros,
                        zeros,
                        src_single), -1)
                    nucle_dst = Image.fromarray(nuclei_im)
                    nucle_dst.save(nucle_path + '/' + dir + '_leftImg8bit.png')

        virus_np = virus_img[0] + virus_img[1]
        zeros = np.zeros(virus_np.shape, dtype="uint8")
        virus_ds2 = np.stack((
            virus_np,
            zeros,
            zeros), -1)
        virus_dst = Image.fromarray(virus_ds2)
        virus_dst.save(virus_path + '/' + dir + '_leftImg8bit.png')

        img_tr = Image.fromarray(virus_seg_img[0] + virus_seg_img[1])
        bmp_P_web = img_tr.convert('P')
        web_palette = bmp_P_web.getpalette()  # <---
        data = np.array(bmp_P_web)
        # second part
        bmp = Image.fromarray(data)
        bmp.putpalette([
            0, 0, 0,  # black background
            0, 0, 0,  # index 1 is red
            0, 0, 0,  # index 2 is yellow
            3, 3, 3,  # index 3 is orange
        ])
        bmp.save(virus_seg + '/' + dir + '_gtFine_labelIds.png')

        # dst.show()
        # cv2.waitKey(0)

        # im = np.stack((
        #     src_img[0] + src_img[1],
        #     src_img[2],
        #     src_img[3]), -1)
        # dst = Image.fromarray(im)
        # dst_path = os.path.join(r'D:\lbq\dataset\0_gjj\dataset\07_MultipleFluorescence\漫性大B细胞淋巴瘤\2_合成图')
        # dst.save(dst_path +'/'+ dir + '.png')

# path1 = 'specimen_01_tile_01_02_channel_'
# path2 = '_type_original_mode_gs.png'
#
# red1 = np.array(Image.open(path1 + 'CD14' + path2))
# red2 = np.array(Image.open(path1 + 'CD163' + path2))
# green = np.array(Image.open(path1 + 'DAPI' + path2))
# blue = np.array(Image.open(path1 + 'Pax5' + path2))
# im = np.stack((
#     red1 + red2,
#     green,
#     blue), -1)
# dst = Image.fromarray(im)
# # dst.save('dst.png')
#
# path3 = '_type_segment_mode_bw.png'
# r1 = np.array(Image.open(path1 + 'CD14' + path3))
# r2 = np.array(Image.open(path1 + 'CD163' + path3))
# g = np.array(Image.open(path1 + 'DAPI' + path3))
# b = np.array(Image.open(path1 + 'Pax5' + path3))
#
# # seg = np.stack((
# #     red_s1+red_s2,
# #     green_s,
# #     blue_s), -1)
# # 转换成int8类型
# img_tr = Image.fromarray(r1 + r2)
# bmp_P_web = img_tr.convert('P')
# web_palette = bmp_P_web.getpalette()  # <---
# print(web_palette)
# data = np.array(bmp_P_web)
# # second part
# bmp = Image.fromarray(data)
# bmp.putpalette([
#     0, 0, 0,  # black background
#     255, 0, 255,  # index 1 is red
#     255, 255, 0,  # index 2 is yellow
#     255, 0, 0,  # index 3 is orange
# ])
# bmp.save('1.png')
# #
# image = Image.open(path1 + 'Pax5' + path3)
# palettedata = [0, 0, 0, 102, 102, 102, 176, 176, 176, 255, 255, 255]
# palimage = Image.new('P', (16, 16))
# palimage.putpalette(palettedata * 64)
# newimage = image.quantize(palette=palimage)
# newimage.save('131.png')


# bmp_P_web = bmp.convert('P', palette=Image.LIBIMAGEQUANT)
# web_palette = bmp_P_web.getpalette()  # <---
# data = np.array(bmp_P_web)
# # second part
# bmp = Image.fromarray(data)
# bmp.putpalette([
#     0, 0, 0,  # black background
#     255, 0, 0,  # index 1 is red
#     255, 255, 0,  # index 2 is yellow
#     255, 153, 255,  # index 3 is orange
# ])
# bmp.save('bmp_tr.png')


# dataframe = pd.read_csv('./human-protein-atlas-image-classification/train.csv')
# # print(dataframe.head(5))
# INPUT_SHAPE = (512, 512, 3)
# BATCH_SIZE = 16
# path_to_train = './human-protein-atlas-image-classification/train/'
# dataframe["complete_path"] = path_to_train + dataframe["Id"]
# # print(dataframe.head(5))
#
# # for i in range(3):
# #     for j in range(4):
# #         idx = random.randint(0, dataframe.shape[0])
# #         row = dataframe.iloc[idx, :]
# #         path = row.complete_path
# for path in dataframe["complete_path"]:
#     red = np.array(Image.open(path + '_red.png'))
#     green = np.array(Image.open(path + '_green.png'))
#     blue = np.array(Image.open(path + '_blue.png'))
#     im = np.stack((
#         red,
#         green,
#         blue), -1)
#
#     dst = Image.fromarray(im)
#     pic_name = path.split("/")[-1]
#     dst.save('./human-protein-atlas-image-classification/rgb/' + pic_name + '_dst.png')


# import cv2
# import numpy as np
# import os
#
#
# path = r'D:\lbq\dataset\0_gjj\dataset\4_Subcell\human-protein-atlas-image-classification\train\000a6c98-bb9b-11e8-b2b9-ac1f6b6435d0'
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
