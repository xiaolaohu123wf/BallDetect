#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/19 14:02
# @Author  : xiaohuwang
# @File    : cs.py
# @Software: PyCharm

import numpy as np
import cv2
from scipy.spatial import KDTree


class ball_detecter():
    '''
    小球检测对象，检测出备选坐标存储在self.ball_center_coordinates变量中，用户鼠标点击后，按照最近邻原则匹配真实小球坐标。
    主要有以下方法：
    hough_circle 霍夫圆检测小球中心
    contour_circle 轮廓阈值检测小球中心
    mouse_callback 鼠标点击事件
    show_img 图像显示
    find_nearest_point 最近点搜索
    '''

    def __init__(self, image_path, lower=[35, 61, 50], upper=[55, 255, 255]):
        self.circle_center = None
        self.ball_center_coordinates = np.empty((0, 2), int)
        img = cv2.imread(image_path)
        # 颜色阈值
        lower = np.array(lower)
        upper = np.array(upper)
        imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(imgHsv, lower, upper)
        self.img = img

    def hough_circle(self, img_src=None):  # 霍夫圆检测
        if img_src == None:
            img_src = self.img
        b, g, r = cv2.split(img_src)
        r = np.int16(r)
        b = np.int16(b)
        img_gray = r - b
        img_gray = (img_gray + abs(img_gray)) / 2
        img_gray = np.uint8(img_gray)
        img_convert = cv2.medianBlur(img_gray, 3)
        img_convert = cv2.GaussianBlur(img_convert, (17, 19), 0)
        circles = cv2.HoughCircles(img_convert, cv2.HOUGH_GRADIENT, 1, 200,
                                   param1=10, param2=15, minRadius=10, maxRadius=70)
        try:
            circles = np.uint16(np.around(circles))
        except:
            pass
        else:
            for i in circles[0, :]:
                cv2.circle(img_src, (i[0], i[1]), i[2], (255, 100, 0), 1)
                cv2.circle(img_src, (i[0], i[1]), 2, (0, 0, 255), 2)
                self.add_coordinate(i[0], i[1])  # x,y

    def contour_circle(self, img_src=None):  # 轮廓检测
        if img_src == None:
            img_src = self.img
        contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 300:
                x, y, w, h = cv2.boundingRect(cnt)
                target_pos_x = int(x + w / 2)
                target_pos_y = int(y + h / 2)
                # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.circle(img_src, (target_pos_x, target_pos_y), 20, (255, 100, 0), 1)
                cv2.circle(img_src, (target_pos_x, target_pos_y), 2, (0, 255, 0), 2)
                self.add_coordinate(target_pos_x, target_pos_y)  # x,y

    def add_coordinate(self, x, y):  # 坐标列表增加
        new_coordinate = np.array([[x, y]])
        self.ball_center_coordinates = np.concatenate((self.ball_center_coordinates, new_coordinate), axis=0)

    def mouse_callback(self, event, x_click, y_click, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            x_center, y_center = self.find_nearest_point([x_click, y_click])
            cv2.drawMarker(self.img, [x_click, y_click], (0, 255, 0), markerType=2, markerSize=10, thickness=1)
            np.random.randint(0, 255)
            color_tuple = (
                int(np.random.randint(0, 255)), int(np.random.randint(0, 255)), int(np.random.randint(0, 255)))
            cv2.drawMarker(self.img, [x_center, y_center], color_tuple, markerType=3, markerSize=15, thickness=3)
            self.circle_center = [x_center, y_center]
        if event == cv2.EVENT_RBUTTONDOWN:
            cv2.drawMarker(self.img, [x_click, y_click], (255, 255, 255), markerType=7, markerSize=15, thickness=3)
            self.circle_center = [x_click, y_click]
        cv2.rectangle(self.img, (2, 25), (350, 60), (255, 255, 255), -1)
        cv2.putText(self.img, 'cevter_coording:' + str(self.circle_center), (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (0, 0, 255), 2)

    def show_img(self):
        cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('Image', self.mouse_callback)
        while True:
            cv2.imshow('Image', self.img)
            key = cv2.waitKey(30)
            if key == 27:  # ESC
                print('用户退出')
                break
            elif key == 32:
                print('记录成功' + str(self.circle_center))
                return self.circle_center

    def find_nearest_point(self, point_coordinate):
        tree = KDTree(self.ball_center_coordinates, leafsize=10)
        dist, idx = tree.query(point_coordinate)
        nearest_point = self.ball_center_coordinates[idx]
        return nearest_point


if __name__ == '__main__':
    cs_ball_manager = ball_detecter('../old/60.jpg')  # 测试使用
    cs_ball_manager.hough_circle()
    cs_ball_manager.contour_circle()
    cs_ball_manager.show_img()
    ball_coordinate = cs_ball_manager.circle_center
    print('ball_coordinate:', ball_coordinate)
