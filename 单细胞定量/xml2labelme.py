import json


def resolveJson(path):
    file = open(path, "rb")
    fileJson = json.load(file)
    annotations = fileJson["annotations"]
    images = fileJson["images"]
    # type = fileJson["type"]
    # name = fileJson["name"]
    # time = fileJson["time"]

    return images, annotations


path = "source.json"
img, ann = resolveJson(path)
for item in img:
    idi = item['id']
    img_seg = []
    for col in ann:
        one_seg = []
        ida = col['image_id']
        if idi == ida:
            line_seg = col['segmentation'][0]
            segs = len(line_seg)
            for i in range(0, segs, 2):
                one_seg.append([line_seg[i], line_seg[i + 1]])
                model = {
                    "label": "single_cell",
                    "points": one_seg,
                    "group_id": 3,
                    "shape_type": "polygon",
                    "flags": {}
                }
                img_seg.append(model)



    dict1 = {
        "version": "4.5.9",
        "flags": {},
        "shapes": img_seg,
        "imagePath": item['file_name'],
        "imageData": "3",
        "imageHeight": item['height'],
        "imageWidth": item['width']
    }
    # 将字典转换为JSON格式的字符串，并将转化后的结果写入文件
    filename = item['file_name'][:-4] + '.json'
    with open('./labelme/' + filename, 'w', encoding='UTF-8') as f:
        json.dump(dict1, f, ensure_ascii=False)

# # coding:utf-8
# import xml
# import xml.etree.ElementTree as ET
# import os
# import json
#
# """
# 实现从xml文件中读取数据
# """
# # 全局唯一标识
# unique_id = 1
#
#
# # 遍历所有的节点
# def walkData(root_node, level, result_list):
#     global unique_id
#     temp_list = [unique_id, level, root_node.tag, root_node.attrib]
#     result_list.append(temp_list)
#     unique_id += 1
#
#     # 遍历每个子节点
#     children_node = root_node.getchildren()
#     if len(children_node) == 0:
#         return
#     for child in children_node:
#         walkData(child, level + 1, result_list)
#     return
#
#
# def getXmlData(file_name):
#     level = 1  # 节点的深度从1开始
#     result_list = []
#     root = ET.parse(file_name).getroot()
#     walkData(root, level, result_list)
#
#     return result_list
#
#
# if __name__ == '__main__':
#
#     root_dir = r'C:\Users\RTX3090\Pictures\gjj\dataset\03_single\MoNuSeg\xml'
#     rootdir = os.path.join(root_dir)
#     for (dirpath, dirnames, filenames) in os.walk(rootdir):
#         for src in filenames:
#             mm = []
#             file_name = os.path.join(root_dir, src)
#             R = getXmlData(file_name)
#             offset = []
#             for x in R:
#                 print(x)
#             #     if x[2] == 'Vertices':
#             #         offset.append('pause')
#             #     if len(x) == 4 and x[2] == 'Vertex':
#             #         x_new = x[-1]
#             #
#             #         offset.append([float(x_new['X']), float(x_new['Y'])])
#             #         # print(offset)
#             #         # train_path.write(str(offset) + '\n')
#             #         # pass
#             #     # train_path.close()
#             #
#             # mask_nums = offset.count('pause')
#             # begin_end = [i for i, x in enumerate(offset) if x == offset[0]]
#             # for j in range(mask_nums - 1):
#             #     begin, end = begin_end[j] + 1, begin_end[j + 1]
#             #     # print(begin, end)
#             #     model = {
#             #         "label": "tissue",
#             #         "points": offset[begin: end],
#             #         "group_id": 3,
#             #         "shape_type": "polygon",
#             #         "flags": {}
#             #     }
#             #     mm.append(model)
#             #
#             # # 原始数据
#             # dict1 = {
#             #     "version": "4.5.9",
#             #     "flags": {},
#             #     "shapes": mm,
#             #     "imagePath": 'Jpegs/' + src[:-4] + ".jpg",
#             #     "imageData": "3",
#             #     "imageHeight": 1000,
#             #     "imageWidth": 1000
#             # }
#             # # 将字典转换为JSON格式的字符串，并将转化后的结果写入文件
#             # filename = file_name[:-4] + '.json'
#             # with open(filename, 'w', encoding='UTF-8') as f:
#             #     json.dump(dict1, f, ensure_ascii=False)
