# coding:utf-8
import xml
import xml.etree.ElementTree as ET
import os
import json
import cv2

"""
实现从xml文件中读取数据
"""
# 全局唯一标识
unique_id = 1


# 遍历所有的节点
def walkData(root_node, level, result_list):
    global unique_id
    temp_list = [unique_id, level, root_node.tag, root_node.attrib]
    result_list.append(temp_list)
    unique_id += 1

    # 遍历每个子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        walkData(child, level + 1, result_list)
    return


def getXmlData(file_name):
    level = 1  # 节点的深度从1开始
    result_list = []
    root = ET.parse(file_name).getroot()
    walkData(root, level, result_list)

    return result_list


type_dict = {'1': 'Epithelial', '2': 'Lymphocytes', '3': 'Macrophages', '4': 'Neutrophils',
             '5': 'Unknown', '6': 'Unknown', '7': 'Unknown', '8': 'Unknown', }

if __name__ == '__main__':

    root_dir = r'D:\lbq\dataset\gjj\dataset\05_Circle_selection\cells'
    for (dirpath, dirnames, filenames) in os.walk(root_dir):
        for src in filenames:
            if src[-3:] == 'xml':
                mm = []
                file_name = os.path.join(root_dir, src[:23], src)
                R = getXmlData(file_name)
                offset = []
                tplist = []
                tp_id = '0'
                for x in R:
                    if x[1] == 2:
                        tp_id = x[3]['Id']
                    if x[2] == 'Vertices':
                        offset.append('pause')
                        tplist.append(tp_id)
                    if len(x) == 4 and x[2] == 'Vertex':
                        tplist.append(tp_id)
                        x_new = x[-1]
                        offset.append([float(x_new['X']), float(x_new['Y'])])
                        # print(offset)
                        # train_path.write(str(offset) + '\n')
                        # pass
                    # train_path.close()

                mask_nums = offset.count('pause')
                begin_end = [i for i, x in enumerate(offset) if x == offset[0]]
                for j in range(mask_nums - 1):
                    begin, end = begin_end[j] + 1, begin_end[j + 1]
                    # print(begin, end)
                    model = {
                        "label": type_dict[tplist[begin]],
                        "points": offset[begin: end],
                        "group_id": 3,
                        "shape_type": "polygon",
                        "flags": {}
                    }
                    mm.append(model)

                # 原始数据
                dict1 = {
                    "version": "4.5.9",
                    "flags": {},
                    "shapes": mm,
                    "imagePath": 'Jpegs/' + src[:-4] + ".jpg",
                    "imageData": "3",
                    "imageHeight": 1000,
                    "imageWidth": 1000
                }
                # 将字典转换为JSON格式的字符串，并将转化后的结果写入文件
                json_path = r'D:\lbq\dataset\gjj\dataset\05_Circle_selection\annotations'
                filename = os.path.join(json_path, src[:-4] + '.json')
                with open(filename, 'w', encoding='UTF-8') as f:
                    json.dump(dict1, f, ensure_ascii=False)
            if src[-3:] == 'tif':
                file_name = os.path.join(root_dir, src[:23], src)
                print(file_name)
                image = cv2.imread(file_name, 1)
                dst_path = r'D:\lbq\dataset\gjj\dataset\05_Circle_selection\Jpegs'
                dst_name = os.path.join(dst_path, src[:-3] + 'jpg')
                cv2.imwrite(dst_name, image)
