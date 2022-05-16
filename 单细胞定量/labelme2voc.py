#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import json
import os
import os.path as osp
import sys

import numpy as np
import PIL.Image

import labelme


def mkdir_os(path):
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    # parser = argparse.ArgumentParser(
    #     formatter_class=argparse.ArgumentDefaultsHelpFormatter
    # )
    # parser.add_argument('input_dir', help='input annotated directory', default='./labelme_json')
    # parser.add_argument('output_dir', help='output dataset directory', default='./voc_json')
    # parser.add_argument('--labels', help='labels file', default='labels.txt', required=True)
    # args = parser.parse_args()

    # if osp.exists(args.output_dir):
    #     print('Output directory already exists:', args.output_dir)
    #     sys.exit(1)
    input_dir = './annotations'
    output_dir = './voc_json'

    mkdir_os(output_dir)
    mkdir_os(osp.join(output_dir, 'JPEGImages'))
    mkdir_os(osp.join(output_dir, 'SegmentationClass'))
    mkdir_os(osp.join(output_dir, 'SegmentationClassPNG'))
    mkdir_os(osp.join(output_dir, 'SegmentationClassVisualization'))
    print('Creating dataset:', output_dir)

    class_names = ['single_cell']
    class_name_to_id = {'single_cell': 1}
    # for i, line in enumerate(open('labels.txt', encoding='UTF-8').readlines()):
    #     class_id = i - 1  # starts with -1
    #     class_name = line.strip()
    #     class_name_to_id[class_name] = class_id
    #     # if class_id == -1:
    #     #     print(class_name)
    #     #     assert class_name == '__ignore__'
    #     #     continue
    #     # elif class_id == 0:
    #     #     assert class_name == '_background_'
    #     class_names.append(class_name)
    class_names = tuple(class_names)
    print('class_names:', class_names)
    out_class_names_file = osp.join(output_dir, 'class_names.txt')
    with open(out_class_names_file, 'w') as f:
        f.writelines('\n'.join(class_names))
    print('Saved class_names:', out_class_names_file)

    colormap = labelme.utils.label_colormap(255)

    for label_file in glob.glob(osp.join(input_dir, '*.json')):
        print('Generating dataset from:', label_file)
        with open(label_file, encoding='UTF-8') as f:
            base = osp.splitext(osp.basename(label_file))[0]
            out_img_file = osp.join(
                output_dir, 'JPEGImages', base + '.jpg')
            out_lbl_file = osp.join(
                output_dir, 'SegmentationClassPNG', base + '.npy')
            # SegmentationClassPNG
            # SegmentationClass
            # out_lbl_file = osp.join(
            #     output_dir, 'SegmentationClass', base + '.png')
            out_png_file = osp.join(
                output_dir, 'SegmentationClass', base + '.png')
            out_viz_file = osp.join(
                output_dir,
                'SegmentationClassVisualization',
                base + '.jpg',
            )

            data = json.load(f)

            # img_file = osp.join(osp.dirname(label_file), data['imagePath'])
            img = np.asarray(PIL.Image.open('source/'+data['imagePath']))
            PIL.Image.fromarray(img).save(out_img_file)

            lbl = labelme.utils.shapes_to_label(
                img_shape=img.shape,
                shapes=data['shapes'],
                label_name_to_value=class_name_to_id,
            )
            labelme.utils.lblsave(out_png_file, lbl)

            np.save(out_lbl_file, lbl)

            viz = labelme.utils.draw_label(
                lbl, img, class_names, colormap=colormap)
            PIL.Image.fromarray(viz).save(out_viz_file)


if __name__ == '__main__':
    main()
