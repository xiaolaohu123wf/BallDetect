#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/25 10:58
# @Author  : xiaohuwang
# @File    : multi_cam_capture.py
# @Software: PyCharm

import cv2
import time
import os
import argparse
import threading
from urllib.parse import urlparse

import yaml
from utils.hkcam import HKCam


def yaml_read(yaml_path):
    f = open(yaml_path, encoding='utf-8')
    data = yaml.load(f.read(), Loader=yaml.FullLoader)
    # print(data.keys())  # 调试使用
    f.close()
    return data


def delete_files_in_folder(folder_path):
    # 获取文件夹内所有文件的列表
    file_list = os.listdir(folder_path)

    # 遍历文件列表并删除每个文件
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"已删除文件: {file_path}")
        except Exception as e:
            print(f"删除文件时出错: {e}")


def shot(pos, frame, output_path, count):
    # timestamp = str(timeit.default_timer() * 1000)
    filename = f"{output_path}/{pos}/{count}.jpg"
    print(filename)
    cv2.imwrite(filename, frame)
    print("snapshot saved into: " + filename)


def main(params, location, output_path, interval):
    # 1.打开海康摄像头,
    hk_cam = HKCam(params['ip'], params['name'], params['pwd'])

    # 2.删除历史记录
    delete_files_in_folder(f'{output_path}/' + location)

    # 3.创建窗口以显示实时画面
    cv2.namedWindow(location, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(location, 640, 480)
    if location == '1':
        cv2.moveWindow(location, 0, 0)  # 设置窗口位置为 (100, 100)
    elif location == '2':
        cv2.moveWindow(location, 640, 0)  # 设置窗口位置为 (100, 100)
    elif location == '3':
        cv2.moveWindow(location, 0, 480)  # 设置窗口位置为 (100, 100)
    else:
        cv2.moveWindow(location, 640, 480)  # 设置窗口位置为 (100, 100)

    start = time.perf_counter()
    count = 0

    # 4.循环读取帧并保存
    while True:
        n_stamp, frame_left = hk_cam.read()

        # 5.显示实时画面
        cv2.imshow(location, frame_left)
        now = time.perf_counter()
        # print(now - start)

        # 6.固定间隔拍照
        if now - start > interval:
            shot(location, frame_left, output_path, count)
            count += 1
            print("拍摄数量：" + str(count))
            start += interval

        # 7.检查是否按下了 'q' 键，如果是则中断循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 8.释放资源
    hk_cam.release()
    cv2.destroyAllWindows()


def dic_generate(rtsp_url):
    parsed_url = urlparse(rtsp_url)
    username = parsed_url.username
    password = parsed_url.password
    ip_address = parsed_url.hostname
    return {'ip': ip_address, 'name': username, 'pwd': password}


# 参数读取
config_camera_dict = yaml_read('./camera_config.yaml')  # 镜头设置文件，用yaml保存
config_camera = argparse.Namespace(**config_camera_dict)  # 转为namespace
config1 = dic_generate(config_camera.c200)
config2 = dic_generate(config_camera.c201)
config3 = dic_generate(config_camera.c202)
config4 = dic_generate(config_camera.c203)

output_path = config_camera.out_path
interval = config_camera.interval

# 运行主程序
if __name__ == '__main__':
    os.chdir(r'./utils/lib/win')

    thread1 = threading.Thread(target=main, args=(config1, '1', output_path, interval))
    thread2 = threading.Thread(target=main, args=(config2, '2', output_path, interval))
    thread3 = threading.Thread(target=main, args=(config3, '3', output_path, interval))
    thread4 = threading.Thread(target=main, args=(config4, '4', output_path, interval))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
