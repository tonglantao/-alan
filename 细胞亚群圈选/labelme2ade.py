#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import json
import os
import os.path as osp
import sys

import cv2
import numpy as np
import PIL.Image

import labelme


# from labelme.utils.draw import label_colormap

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
    output_dir = './ade_json'

    mkdir_os(output_dir)
    mkdir_os(osp.join(output_dir, 'JPEGImages'))
    mkdir_os(osp.join(output_dir, 'SegmentationClass'))
    mkdir_os(osp.join(output_dir, 'SegmentationClassPNG'))
    mkdir_os(osp.join(output_dir, 'SegmentationClassVisualization'))
    print('Creating dataset:', output_dir)

    class_names = ['Epithelial', 'Lymphocytes', 'Macrophages', 'Neutrophils', 'Unknown']
    class_name_to_id = {'Epithelial': '1', 'Lymphocytes': 2, 'Macrophages': 3, 'Neutrophils': 4, 'Unknown': 5}
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
            img = np.asarray(PIL.Image.open(data['imagePath']))
            PIL.Image.fromarray(img).save(out_img_file)

            lbl = labelme.utils.shapes_to_label(
                img_shape=img.shape,
                shapes=data['shapes'],
                label_name_to_value=class_name_to_id,
            )
            lblsave_ade(out_png_file, lbl)

            np.save(out_lbl_file, lbl)

            viz = labelme.utils.draw_label(
                lbl, img, class_names, colormap=colormap)
            PIL.Image.fromarray(viz).save(out_viz_file)


def label_colormap(N=256):
    def bitget(byteval, idx):
        return ((byteval & (1 << idx)) != 0)

    cmap = np.zeros((N, 3))
    for i in range(0, N):
        id = i
        r, g, b = 0, 0, 0
        for j in range(0, 8):
            r = np.bitwise_or(r, (bitget(id, 0) << 7 - j))
            g = np.bitwise_or(g, (bitget(id, 1) << 7 - j))
            b = np.bitwise_or(b, (bitget(id, 2) << 7 - j))
            id = (id >> 3)
        cmap[i, 0] = r
        cmap[i, 1] = g
        cmap[i, 2] = b
    # 我认为添加的一段，自己设置不同类别的rgb值
    cmap[0, :] = [0, 0, 0]  # 背景的rgb值
    cmap[1, :] = [1, 1, 1]  # 上皮细胞的rgb
    cmap[2, :] = [2, 2, 2]  # 淋巴细胞的rgb
    cmap[3, :] = [3, 3, 3]  # 巨噬细胞的rgb
    cmap[4, :] = [4, 4, 4]  # 中性粒细胞的rgb
    cmap[5, :] = [5, 5, 5]  # 中性粒细胞的rgb
    cmap = cmap.astype(np.float32) / 255
    return cmap


def lblsave_ade(filename, lbl):
    if osp.splitext(filename)[1] != '.png':
        filename += '.png'
    # Assume label ranses [-1, 254] for int32,
    # and [0, 255] for uint8 as VOC.
    if lbl.min() >= -1 and lbl.max() < 255:
        lbl_pil = PIL.Image.fromarray(lbl.astype(np.uint8), mode='P')
        colormap = label_colormap(255)
        lbl_pil.putpalette((colormap * 255).astype(np.uint8).flatten())
        lbl_pil.save(filename)
    else:
        raise ValueError(
            '[%s] Cannot save the pixel-wise class label as PNG. '
            'Please consider using the .npy format.' % filename
        )


if __name__ == '__main__':
    main()
