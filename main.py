#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/27 9:45
# @Author  : xiaohuwang
# @File    : main.py
# @Software: PyCharm

from utils.BallDetecter import ball_detecter
from utils.FileOperation import *

start_index = 0
stop_index = 2


def detail_show():
    n_view = 0
    current_pic = pics.index(pic) + 1
    total_pics = len(pics)
    print('视角{}，照片{}/{}，路径'.format(n_view, current_pic, total_pics) + str(path_view + pic))


if __name__ == '__main__':
    # 0. 路径生成
    path = 'C:\\Users\\723\\Desktop\\images\\'
    views = file_load(path)
    data_manger = data_pickler()
    for view in views:  # 逐个视角迭代
        path_view = path + view + '\\'
        pics = file_load(path + view + '\\')[start_index:stop_index]
        view_detail = view + ' {}--{}'.format(start_index, stop_index)

        for pic in pics:  # 逐张图片迭代
            # 1. 检测
            ball_manager = ball_detecter(path_view + pic)
            ball_manager.hough_circle()
            ball_manager.contour_circle()
            ball_manager.show_img()
            center_coordinate = ball_manager.circle_center

            # 2.单张图片数据处理
            if center_coordinate is None:  # 未检测到角点
                data_manger.add_element(0, 0, 0)
            else:  # 检测到角点
                data_manger.add_element(center_coordinate[0], center_coordinate[1], 1)
            detail_show()  # 详情显示
            data_manger.pic_save(ball_manager.img, view, pic)  # 结果缓存

        # 3. 单个视角数据处理
        data_manger.add_line(view_detail)  # 单视角存储

    # 4. 4d数组创建存储
    data = data_manger.keypoints_generate(10)  # 多视角存储
    print('任务完成，生成数据详情：', data['info'])
