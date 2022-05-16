import time
import math


step = 0
tic = time.time()


def progress_bar(total_steps):
    global step
    global tic
    step += 1
    used_time = time.time() - tic
    avg_time = used_time / step
    eta = (total_steps - step) * avg_time
    if step == total_steps:
        do = 60
    else:
        do = int(60 * step / total_steps)
    undo = 60 - do

    print('{}/{} [{}{}] - eta: {:.2f}s - {:.2f}s/step'.format(
        step, total_steps, '=' * do, ' ' * undo, eta, avg_time), end='\r')


def get_coord_from_shape(shape):
    if len(shape['points']) != 2:
        raise ValueError('标注错误，发现标注点不为两个点（circle标注应该仅包含圆心点和圆周点）')
    center_point = [int(value) for value in shape['points'][0]]
    circle_point = [int(value) for value in shape['points'][1]]
    radius = int(math.sqrt(pow(center_point[0] - circle_point[0], 2) +
                           pow(center_point[1] - circle_point[1], 2)))

    x_min = center_point[0] - radius
    y_min = center_point[1] - radius
    x_max = center_point[0] + radius
    y_max = center_point[1] + radius
    return x_min, y_min, x_max, y_max
