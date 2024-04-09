#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/2 8:16
# @Author  : xiaohuwang
# @File    : HSVgenerater.py
# @Software: PyCharm


import cv2
import numpy as np

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, mode, img, roi

    drawing = False
    roi = cv2.selectROI('image', img, False)
    cv2.destroyWindow('image')
def get_major_color_hsv(image):

    # 将图像从BGR转换为RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 将图像从RGB转换为HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # 计算图像的直方图
    hist = cv2.calcHist([hsv_image], [0, 1], None, [180, 256], [0, 180, 0, 256])
    # 寻找直方图中的峰值
    _, _, _, max_loc = cv2.minMaxLoc(hist)
    # 获取最大峰值的色相和饱和度
    hue = max_loc[0]
    saturation = max_loc[1]

    # 根据要求输出lower和upper值
    lower = np.array([hue-10, saturation-50, 50])
    upper = np.array([hue+10, 255, 255])

    return lower, upper

image_path = 'C:\\Users\\723\\Desktop\\images\\1\\1011.jpg'  # 替换成你的图像路径
# 读取图像
img = cv2.imread(image_path)
# 创建窗口并绑定鼠标回调函数
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', draw_rectangle)
drawing = True
roi = None
while drawing:
    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == 27:  # 按ESC键退出
        break
if roi is not None:
    x, y, w, h = roi
    img = img[y:y+h, x:x+w]
    # img = roi

cv2.imshow('result', img)
lower, upper = get_major_color_hsv(img)
print("lower = np.array([{}, {}, {}])".format(lower[0], lower[1], lower[2]))
print("upper = np.array([{}, {}, {}])".format(upper[0], upper[1], upper[2]))
cv2.waitKey(0)
cv2.destroyAllWindows()