import os
import json
import random
from glob import glob
from datetime import datetime
import sys

from labelme_utils import progress_bar, get_coord_from_shape


def make_category(_id, name):
    return {
        'supercategory': 'object',
        'id': _id,
        'name': name
    }


def make_image(_id, file_name, height, width):
    return {
        'license': random.choice(list(range(1, 8))),
        'coco_url': '',
        'flickr_url': '',
        'date_captured': '',

        'id': _id,
        'file_name': file_name,
        'height': height,
        'width': width
    }


def make_annotation(category_id, image_id, _id, points):
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    left_offset = min(xs)
    top_offset = min(ys)
    bbox_width = max(xs) - min(xs)
    bbox_height = max(ys) - min(ys)
    segmentation = [[]]
    for point in points:
        segmentation[0].extend(point)
    return {
        'segmentation': segmentation,
        'iscrowd': 0,

        'category_id': category_id,
        'image_id': image_id,
        'id': _id,
        'bbox': [left_offset, top_offset, bbox_width, bbox_height],
        'area': bbox_width * bbox_height
    }


def default_info():
    return {'contributor': 'Seizet DL',
            'date_created': datetime.now().strftime('%Y/%m/%d'),
            'description': 'Seizet DL Dataset',
            'url': 'http://seizet.com/index.aspx',
            'version': '1.0',
            'year': datetime.now().strftime('%Y')}


def fake_licenses():
    return [{'id': 1,
             'name': 'Attribution-NonCommercial-ShareAlike License',
             'url': 'http://creativecommons.org/licenses/by-nc-sa/2.0/'},
            {'id': 2,
             'name': 'Attribution-NonCommercial License',
             'url': 'http://creativecommons.org/licenses/by-nc/2.0/'},
            {'id': 3,
             'name': 'Attribution-NonCommercial-NoDerivs License',
             'url': 'http://creativecommons.org/licenses/by-nc-nd/2.0/'},
            {'id': 4,
             'name': 'Attribution License',
             'url': 'http://creativecommons.org/licenses/by/2.0/'},
            {'id': 5,
             'name': 'Attribution-ShareAlike License',
             'url': 'http://creativecommons.org/licenses/by-sa/2.0/'},
            {'id': 6,
             'name': 'Attribution-NoDerivs License',
             'url': 'http://creativecommons.org/licenses/by-nd/2.0/'},
            {'id': 7,
             'name': 'No known copyright restrictions',
             'url': 'http://flickr.com/commons/usage/'},
            {'id': 8,
             'name': 'United States Government Work',
             'url': 'http://www.usa.gov/copyright.shtml'}]



def main():
    print('Labelme Convert to COCO')
    label_list = []
    category_list = []
    with open('classes.txt', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f.readlines()):
            category_id = i + 1
            category_name = line.strip()
            label_list.append(category_name)
            category_list.append(make_category(category_id, category_name))

    image_list = []
    annotation_list = []

    total_json_file_path_list = []

    current_dir_abspath = os.path.abspath(os.path.dirname(__file__))

    dir_path_list = [os.path.join(current_dir_abspath, path) for path in os.listdir(current_dir_abspath) if
                     os.path.isdir(path)]
    for dir_path in dir_path_list:
        json_file_path_list = glob(os.path.join(dir_path, '*.json'))
        if json_file_path_list:

            total_json_file_path_list.extend(json_file_path_list)

    # 打印进度条需要提供总步数
    total_steps = len(total_json_file_path_list)

    for ii, json_file_path in enumerate(total_json_file_path_list):
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_obj = json.load(f)

        image_id = len(image_list) + 1
        file_name = json_file_path.split('\\')[-2] + '\\' + json_obj['imagePath']
        height = json_obj['imageHeight']
        width = json_obj['imageWidth']
        image_list.append(make_image(image_id, file_name, height, width))

        for shape in json_obj['shapes']:
            category_name = shape['label']
            category_id = label_list.index(category_name) + 1
            points = shape['points']

            annotation_id = len(annotation_list) + 1
            annotation_list.append(make_annotation(category_id,
                                                   image_id,
                                                   annotation_id,
                                                   points))

        progress_bar(total_steps)

    annotation_content = {
        'info': default_info(),
        'licenses': fake_licenses(),
        'categories': category_list,
        'images': image_list,
        'annotations': annotation_list
    }
    with open('annotation.json', 'w') as f:
        json.dump(annotation_content, f)

    # print('', flush=False)
    # input("press any key to exit ...")


if __name__ == '__main__':
    main()
