# -*-coding:gb2312-*-
import argparse, os, glob, json, base64, io, math
from PIL import Image, ImageDraw

'''
LABEL_MAP = [
    0, 0, 0, 128, 0, 0, 0, 128, 0, 128, 128, 0, 0, 0, 128, 128, 0, 128, 0, 128, 128, 128, 128, 128, 64, 0, 0, 192, 0, 0,
    64, 128, 0, 192, 128, 0, 64, 0, 128, 192, 0, 128, 64, 128, 128, 192, 128, 128, 0, 64, 0, 128, 64, 0, 0, 192, 0, 128,
    192, 0, 0, 64, 128, 128, 64, 128, 0, 192, 128, 128, 192, 128, 64, 64, 0, 192, 64, 0, 64, 192, 0, 192, 192, 0, 64,
    64, 128, 192, 64, 128, 64, 192, 128, 192, 192, 128, 0, 0, 64, 128, 0, 64, 0, 128, 64, 128, 128, 64, 0, 0, 192, 128,
    0, 192, 0, 128, 192, 128, 128, 192, 64, 0, 64, 192, 0, 64, 64, 128, 64, 192, 128, 64, 64, 0, 192, 192, 0, 192, 64,
    128, 192, 192, 128, 192, 0, 64, 64, 128, 64, 64, 0, 192, 64, 128, 192, 64, 0, 64, 192, 128, 64, 192, 0, 192, 192,
    128, 192, 192, 64, 64, 64, 192, 64, 64, 64, 192, 64, 192, 192, 64, 64, 64, 192, 192, 64, 192, 64, 192, 192, 192,
    192, 192, 32, 0, 0, 160, 0, 0, 32, 128, 0, 160, 128, 0, 32, 0, 128, 160, 0, 128, 32, 128, 128, 160, 128, 128, 96, 0,
    0, 224, 0, 0, 96, 128, 0, 224, 128, 0, 96, 0, 128, 224, 0, 128, 96, 128, 128, 224, 128, 128, 32, 64, 0, 160, 64, 0,
    32, 192, 0, 160, 192, 0, 32, 64, 128, 160, 64, 128, 32, 192, 128, 160, 192, 128, 96, 64, 0, 224, 64, 0, 96, 192, 0,
    224, 192, 0, 96, 64, 128, 224, 64, 128, 96, 192, 128, 224, 192, 128, 32, 0, 64, 160, 0, 64, 32, 128, 64, 160, 128,
    64, 32, 0, 192, 160, 0, 192, 32, 128, 192, 160, 128, 192, 96, 0, 64, 224, 0, 64, 96, 128, 64, 224, 128, 64, 96, 0,
    192, 224, 0, 192, 96, 128, 192, 224, 128, 192, 32, 64, 64, 160, 64, 64, 32, 192, 64, 160, 192, 64, 32, 64, 192, 160,
    64, 192, 32, 192, 192, 160, 192, 192, 96, 64, 64, 224, 64, 64, 96, 192, 64, 224, 192, 64, 96, 64, 192, 224, 64, 192,
    96, 192, 192, 224, 192, 192, 0, 32, 0, 128, 32, 0, 0, 160, 0, 128, 160, 0, 0, 32, 128, 128, 32, 128, 0, 160, 128,
    128, 160, 128, 64, 32, 0, 192, 32, 0, 64, 160, 0, 192, 160, 0, 64, 32, 128, 192, 32, 128, 64, 160, 128, 192, 160,
    128, 0, 96, 0, 128, 96, 0, 0, 224, 0, 128, 224, 0, 0, 96, 128, 128, 96, 128, 0, 224, 128, 128, 224, 128, 64, 96, 0,
    192, 96, 0, 64, 224, 0, 192, 224, 0, 64, 96, 128, 192, 96, 128, 64, 224, 128, 192, 224, 128, 0, 32, 64, 128, 32, 64,
    0, 160, 64, 128, 160, 64, 0, 32, 192, 128, 32, 192, 0, 160, 192, 128, 160, 192, 64, 32, 64, 192, 32, 64, 64, 160,
    64, 192, 160, 64, 64, 32, 192, 192, 32, 192, 64, 160, 192, 192, 160, 192, 0, 96, 64, 128, 96, 64, 0, 224, 64, 128,
    224, 64, 0, 96, 192, 128, 96, 192, 0, 224, 192, 128, 224, 192, 64, 96, 64, 192, 96, 64, 64, 224, 64, 192, 224, 64,
    64, 96, 192, 192, 96, 192, 64, 224, 192, 192, 224, 192, 32, 32, 0, 160, 32, 0, 32, 160, 0, 160, 160, 0, 32, 32, 128,
    160, 32, 128, 32, 160, 128, 160, 160, 128, 96, 32, 0, 224, 32, 0, 96, 160, 0, 224, 160, 0, 96, 32, 128, 224, 32,
    128, 96, 160, 128, 224, 160, 128, 32, 96, 0, 160, 96, 0, 32, 224, 0, 160, 224, 0, 32, 96, 128, 160, 96, 128, 32,
    224, 128, 160, 224, 128, 96, 96, 0, 224, 96, 0, 96, 224, 0, 224, 224, 0, 96, 96, 128, 224, 96, 128, 96, 224, 128,
    224, 224, 128, 32, 32, 64, 160, 32, 64, 32, 160, 64, 160, 160, 64, 32, 32, 192, 160, 32, 192, 32, 160, 192, 160,
    160, 192, 96, 32, 64, 224, 32, 64, 96, 160, 64, 224, 160, 64, 96, 32, 192, 224, 32, 192, 96, 160, 192, 224, 160,
    192, 32, 96, 64, 160, 96, 64, 32, 224, 64, 160, 224, 64, 32, 96, 192, 160, 96, 192, 32, 224, 192, 160, 224, 192, 96,
    96, 64, 224, 96, 64, 96, 224, 64, 224, 224, 64, 96, 96, 192, 224, 96, 192, 96, 224, 192, 224, 224, 192
]
'''

PALETTE = [[128, 64, 128], [244, 35, 232], [70, 70, 70], [102, 102, 156],
           [190, 153, 153], [153, 153, 153], [250, 170, 30], [220, 220, 0],
           [107, 142, 35], [152, 251, 152], [70, 130, 180], [220, 20, 60],
           [255, 0, 0], [0, 0, 142], [0, 0, 70], [0, 60, 100],
           [0, 80, 100], [0, 0, 230], [119, 11, 32]]

LABEL_MAP = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11,
             11, 11, 12,
             12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21,
             21, 21, 22,
             22, 22, 23, 23, 23, 24, 24, 24, 25, 25, 25, 26, 26, 26, 27, 27, 27, 28, 28, 28, 29, 29, 29, 30, 30, 30, 31,
             31, 31, 32,
             32, 32, 33, 33, 33, 34, 34, 34, 35, 35, 35, 36, 36, 36, 37, 37, 37, 38, 38, 38, 39, 39, 39, 40, 40, 40, 41,
             41, 41, 42,
             42, 42, 43, 43, 43, 44, 44, 44, 45, 45, 45, 46, 46, 46, 47, 47, 47, 48, 48, 48, 49, 49, 49, 50, 50, 50, 51,
             51, 51, 52,
             52, 52, 53, 53, 53, 54, 54, 54, 55, 55, 55, 56, 56, 56, 57, 57, 57, 58, 58, 58, 59, 59, 59, 60, 60, 60, 61,
             61, 61, 62,
             62, 62, 63, 63, 63, 64, 64, 64, 65, 65, 65, 66, 66, 66, 67, 67, 67, 68, 68, 68, 69, 69, 69, 70, 70, 70, 71,
             71, 71, 72,
             72, 72, 73, 73, 73, 74, 74, 74, 75, 75, 75, 76, 76, 76, 77, 77, 77, 78, 78, 78, 79, 79, 79, 80, 80, 80, 81,
             81, 81, 82,
             82, 82, 83, 83, 83, 84, 84, 84, 85, 85, 85, 86, 86, 86, 87, 87, 87, 88, 88, 88, 89, 89, 89, 90, 90, 90, 91,
             91, 91, 92,
             92, 92, 93, 93, 93, 94, 94, 94, 95, 95, 95, 96, 96, 96, 97, 97, 97, 98, 98, 98, 99, 99, 99, 100, 100, 100,
             101, 101,
             101, 102, 102, 102, 103, 103, 103, 104, 104, 104, 105, 105, 105, 106, 106, 106, 107, 107, 107, 108, 108,
             108, 109, 109,
             109, 110, 110, 110, 111, 111, 111, 112, 112, 112, 113, 113, 113, 114, 114, 114, 115, 115, 115, 116, 116,
             116, 117, 117,
             117, 118, 118, 118, 119, 119, 119, 120, 120, 120, 121, 121, 121, 122, 122, 122, 123, 123, 123, 124, 124,
             124, 125, 125,
             125, 126, 126, 126, 127, 127, 127, 128, 128, 128, 129, 129, 129, 130, 130, 130, 131, 131, 131, 132, 132,
             132, 133, 133,
             133, 134, 134, 134, 135, 135, 135, 136, 136, 136, 137, 137, 137, 138, 138, 138, 139, 139, 139, 140, 140,
             140, 141, 141,
             141, 142, 142, 142, 143, 143, 143, 144, 144, 144, 145, 145, 145, 146, 146, 146, 147, 147, 147, 148, 148,
             148, 149, 149,
             149, 150, 150, 150, 151, 151, 151, 152, 152, 152, 153, 153, 153, 154, 154, 154, 155, 155, 155, 156, 156,
             156, 157, 157,
             157, 158, 158, 158, 159, 159, 159, 160, 160, 160, 161, 161, 161, 162, 162, 162, 163, 163, 163, 164, 164,
             164, 165, 165,
             165, 166, 166, 166, 167, 167, 167, 168, 168, 168, 169, 169, 169, 170, 170, 170, 171, 171, 171, 172, 172,
             172, 173, 173,
             173, 174, 174, 174, 175, 175, 175, 176, 176, 176, 177, 177, 177, 178, 178, 178, 179, 179, 179, 180, 180,
             180, 181, 181,
             181, 182, 182, 182, 183, 183, 183, 184, 184, 184, 185, 185, 185, 186, 186, 186, 187, 187, 187, 188, 188,
             188, 189, 189,
             189, 190, 190, 190, 191, 191, 191, 192, 192, 192, 193, 193, 193, 194, 194, 194, 195, 195, 195, 196, 196,
             196, 197, 197,
             197, 198, 198, 198, 199, 199, 199, 200, 200, 200, 201, 201, 201, 202, 202, 202, 203, 203, 203, 204, 204,
             204, 205, 205,
             205, 206, 206, 206, 207, 207, 207, 208, 208, 208, 209, 209, 209, 210, 210, 210, 211, 211, 211, 212, 212,
             212, 213, 213,
             213, 214, 214, 214, 215, 215, 215, 216, 216, 216, 217, 217, 217, 218, 218, 218, 219, 219, 219, 220, 220,
             220, 221, 221,
             221, 222, 222, 222, 223, 223, 223, 224, 224, 224, 225, 225, 225, 226, 226, 226, 227, 227, 227, 228, 228,
             228, 229, 229,
             229, 230, 230, 230, 231, 231, 231, 232, 232, 232, 233, 233, 233, 234, 234, 234, 235, 235, 235, 236, 236,
             236, 237, 237,
             237, 238, 238, 238, 239, 239, 239, 240, 240, 240, 241, 241, 241, 242, 242, 242, 243, 243, 243, 244, 244,
             244, 245, 245,
             245, 246, 246, 246, 247, 247, 247, 248, 248, 248, 249, 249, 249, 250, 250, 250, 251, 251, 251, 252, 252,
             252, 253, 253,
             253, 254, 254, 254, 255, 255, 255]

IMAGE_SETS_DIR_NAME = 'ImageSets'
SEGMENTATION_DIR_NAME = 'Segmentation'
JPEG_IMAGES_DIR_NAME = "leftImg8bit"
SEGMENTATION_CLASS_DIR_NAME = 'gtFine_labelIds'
SEGMENTATION_CLASS_RAW_DIR_NAME = 'gtFine_color'
SEGMENTATION_CLASS_VISUALIZATION_DIR_NAME = 'SegmentationClassVisualization'
LABELS_TEXT_FILE_NAME = 'labels.txt'
TRAINVAL_TXT_FILE_NAME = "trainval.txt"
TRAIN_TXT_FILE_NAME = "train.txt"
VAL_TXT_FILE_NAME = "val.txt"
BORDER_WIDTH = 4
BORDER_COLOR = 255


class ShapeTypes:
    CIRCLE = "circle"
    POLYGON = "polygon"
    RECTANGLE = 'rectangle'


def check_to_mkdir(p):
    if not os.path.exists(p):
        os.mkdir(p)


def get_image_sets_dir(base_output_dir):
    return os.path.join(base_output_dir, IMAGE_SETS_DIR_NAME)


def get_segmentation_dir(base_output_dir):
    return os.path.join(base_output_dir, IMAGE_SETS_DIR_NAME, SEGMENTATION_DIR_NAME)


def get_jpeg_images_dir(base_output_dir):
    return os.path.join(base_output_dir, JPEG_IMAGES_DIR_NAME)


def get_segmentation_class_dir(base_output_dir):
    return os.path.join(base_output_dir, SEGMENTATION_CLASS_DIR_NAME)


def get_segmentation_class_raw_dir(base_output_dir):
    return os.path.join(base_output_dir, SEGMENTATION_CLASS_RAW_DIR_NAME)


def get_segmentation_class_visualization_dir(base_output_dir):
    return os.path.join(base_output_dir, SEGMENTATION_CLASS_VISUALIZATION_DIR_NAME)


def get_labels_text_file(base_output_dir):
    return os.path.join(base_output_dir, LABELS_TEXT_FILE_NAME)


def get_trainval_text_file(base_output_dir):
    return os.path.join(get_segmentation_dir(base_output_dir), TRAINVAL_TXT_FILE_NAME)


def get_train_text_file(base_output_dir):
    return os.path.join(get_segmentation_dir(base_output_dir), TRAIN_TXT_FILE_NAME)


def get_val_text_file(base_output_dir):
    return os.path.join(get_segmentation_dir(base_output_dir), VAL_TXT_FILE_NAME)


def check_to_make_output_dirs(output_dir):
    check_to_mkdir(output_dir)
    check_to_mkdir(get_image_sets_dir(output_dir))
    check_to_mkdir(get_segmentation_dir(output_dir))
    check_to_mkdir(get_jpeg_images_dir(output_dir))
    check_to_mkdir(get_segmentation_class_dir(output_dir))
    check_to_mkdir(get_segmentation_class_raw_dir(output_dir))
    check_to_mkdir(get_segmentation_class_visualization_dir(output_dir))


def translate_points(points):
    new_arr = []
    for p in points:
        new_arr.append((p[0], p[1]))
    return new_arr


labels = ["_background_"]


def get_label_color(label):
    if label in labels:
        color_index = labels.index(label)
    else:
        labels.append(label)
        color_index = len(labels) - 1
    return color_index


def get_rgb_by_p_index(color_index):
    start = color_index * 3
    return LABEL_MAP[start], LABEL_MAP[start + 1], LABEL_MAP[start + 2]


def draw_polygon(seg_class_img, shape, draw_border, seg_class_visualization_img=None, seg_class_raw_img=None):
    seg_class_img_draw = ImageDraw.Draw(seg_class_img)
    points = translate_points(shape['points'])
    fill_color = get_label_color(shape['label'])

    seg_class_raw_img_draw = None
    if seg_class_raw_img:
        seg_class_raw_img_draw = ImageDraw.Draw(seg_class_raw_img)

    if len(points):
        seg_class_img_draw.polygon(points, fill=fill_color)
        if seg_class_raw_img_draw:
            seg_class_raw_img_draw.polygon(points, fill=fill_color)

        # close the path
        points.append((points[0][0], points[0][1]))
        # draw border, 需不需要像cityscapes那样画mask的边缘
        if draw_border:
            seg_class_img_draw.line(points, fill=BORDER_COLOR, width=BORDER_WIDTH, joint="curve")
            if seg_class_raw_img_draw:
                seg_class_raw_img_draw.line(points, fill=BORDER_COLOR, width=BORDER_WIDTH, joint="curve")

        # draw visualization_img
        if seg_class_visualization_img:
            seg_class_visualization_img_draw = ImageDraw.Draw(seg_class_visualization_img)
            seg_class_visualization_img_draw.line(
                points, fill=get_rgb_by_p_index(fill_color),
                width=BORDER_WIDTH,
                joint="curve"
            )
        pass


def draw_circle(seg_class_img, shape, seg_class_visualization_img=None, seg_class_raw_img=None):
    draw = ImageDraw.Draw(seg_class_img)
    points = shape['points']
    center_x = points[0][0]
    center_y = points[0][1]
    dx = center_x - points[1][0]
    dy = center_y - points[1][1]
    cr = math.sqrt(dx * dx + dy * dy)
    fill_color = get_label_color(shape['label'])
    draw.ellipse(
        xy=[(center_x - cr, center_y - cr), (center_x + cr, center_y + cr)],
        fill=fill_color, outline=BORDER_COLOR,
        width=BORDER_WIDTH
    )
    if seg_class_raw_img:
        seg_class_raw_img_draw = ImageDraw.Draw(seg_class_raw_img)
        seg_class_raw_img_draw.ellipse(
            xy=[(center_x - cr, center_y - cr), (center_x + cr, center_y + cr)],
            fill=fill_color, outline=BORDER_COLOR,
            width=BORDER_WIDTH
        )
    if seg_class_visualization_img:
        seg_class_visualization_img_draw = ImageDraw.Draw(seg_class_visualization_img)
        seg_class_visualization_img_draw.ellipse(
            xy=[(center_x - cr, center_y - cr), (center_x + cr, center_y + cr)],
            fill=None, outline=get_rgb_by_p_index(fill_color),
            width=BORDER_WIDTH
        )
        pass
    pass


def draw_rectangle(seg_class_img, shape, seg_class_visualization_img, seg_class_raw_img):
    seg_class_img_draw = ImageDraw.Draw(seg_class_img)
    seg_class_visualization_img_draw = ImageDraw.Draw(seg_class_visualization_img)
    seg_class_raw_img_draw = ImageDraw.Draw(seg_class_raw_img)
    points = translate_points(shape['points'])
    fill_color = get_label_color(shape['label'])
    seg_class_img_draw.rectangle(points, fill=fill_color, outline=BORDER_COLOR, width=BORDER_WIDTH)
    seg_class_raw_img_draw.rectangle(points, fill=fill_color, outline=BORDER_COLOR, width=BORDER_WIDTH)
    seg_class_visualization_img_draw.rectangle(
        points, fill=None, outline=get_rgb_by_p_index(fill_color),
        width=BORDER_WIDTH
    )
    pass


def gen_train_and_val_from_trainval(trainval_text_file_path):
    base_dir_path = os.path.dirname(trainval_text_file_path)
    fp = open(trainval_text_file_path, 'r')
    lines = fp.readlines()
    fp.close()

    # train.txt
    split_index = int(len(lines) * 0.95)
    fp = open(os.path.join(base_dir_path, TRAIN_TXT_FILE_NAME), 'w')
    fp.write("".join(lines[0:split_index]))
    fp.close()

    # var.txt
    fp = open(os.path.join(base_dir_path, VAL_TXT_FILE_NAME), 'w')
    fp.write("".join(lines[split_index:]))
    fp.close()


def gen_voc_dataset(labelme_dataset_input_dir, voc_dataset_output_dir, draw_border):
    labelme_files = glob.glob(os.path.join(labelme_dataset_input_dir, "*.json"))
    trainval_txt_fp = open(get_trainval_text_file(voc_dataset_output_dir), 'w')
    for p in labelme_files:
        print(f"Transferring {p}")
        filename, ext = os.path.splitext(os.path.basename(p))
        f = open(p, encoding='UTF-8')
        fo = json.load(f)
        f.close()

        # load image data
        # image_data_base64 = fo['imageData']
        # image_data = base64.decodebytes(image_data_base64.encode("utf-8"))
        # image_data_io = io.BytesIO(image_data)
        src_img = Image.open('annotations/' + fo['imagePath'])

        # writing JPEGImages
        src_img = src_img.convert('RGB')
        src_img.save(os.path.join(get_jpeg_images_dir(voc_dataset_output_dir), f"{filename}_leftImg8bit.png"), "png")

        # draw shapes
        seg_class_img = Image.new(mode='P', size=src_img.size, color=0)
        seg_class_img.putpalette(LABEL_MAP)
        seg_class_raw_img = Image.new(mode='P', size=src_img.size)
        seg_class_visualization_img = Image.new(mode="RGBA", size=src_img.size)
        seg_class_visualization_img.paste(src_img)
        shapes = fo['shapes']
        for s in shapes:
            shape_type = s['shape_type']
            if shape_type == ShapeTypes.POLYGON:
                draw_polygon(
                    seg_class_img, s, draw_border,seg_class_visualization_img=seg_class_visualization_img,
                    seg_class_raw_img=seg_class_raw_img
                )
            elif shape_type == ShapeTypes.CIRCLE:
                draw_circle(
                    seg_class_img, s, seg_class_visualization_img=seg_class_visualization_img,
                    seg_class_raw_img=seg_class_raw_img
                )
            elif shape_type == ShapeTypes.RECTANGLE:
                draw_rectangle(
                    seg_class_img, s, seg_class_visualization_img=seg_class_visualization_img,
                    seg_class_raw_img=seg_class_raw_img
                )
            else:
                raise NotImplementedError(f"Unsupported shape type {shape_type}")

        # writing SegmentationClass and SegmentationClassRaw
        seg_class_img.save(
            os.path.join(get_segmentation_class_dir(voc_dataset_output_dir), f"{filename}_gtFine_labelIds.png"), "PNG")
        # 这个应该画成color图
        seg_class_raw_img.save(
            os.path.join(get_segmentation_class_raw_dir(voc_dataset_output_dir), f"{filename}_gtFine_color.png"),
            "PNG"
        )
        seg_class_visualization_img.save(
            os.path.join(get_segmentation_class_visualization_dir(voc_dataset_output_dir), f"{filename}.png"),
            "PNG"
        )

        # close the image io
        # image_data_io.close()

        # write text files
        trainval_txt_fp.write(filename + "\n")
        pass

    trainval_txt_fp.close()
    # create train.txt, var.txt
    gen_train_and_val_from_trainval(get_trainval_text_file(voc_dataset_output_dir))

    # create labels.txt
    fp = open(get_labels_text_file(voc_dataset_output_dir), 'w')
    fp.write("\n".join(labels))
    fp.close()
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_dir", help="input labelme annotated directory")
    parser.add_argument("output_dir", help="output voc dataset directory")
    parser.add_argument("draw_border", default=False, help="是否画边缘")
    args = parser.parse_args()
    check_to_make_output_dirs(args.output_dir)
    gen_voc_dataset(args.input_dir, args.output_dir, args.draw_border)
    pass
