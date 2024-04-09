import os
import pickle
from datetime import datetime

import cv2
import numpy as np

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
def file_load(path, file_suffix=''):
    image_files = [f for f in os.listdir(path) if f.endswith(file_suffix)]
    return image_files


def file_find(element, lst):
    if element in lst:
        return lst.index(element)

def dir_init(path):
    if not os.path.exists(path):
        os.makedirs(path)
class data_pickler():
    def __init__(self, temp_path='./temp/', data_path='./result/'):
        self.data_3d_list = []
        self.data_4d_list = []
        self.temp_path = temp_path
        dir_init(temp_path)
        dir_init(data_path)
        dir_init(temp_path + 'pic/')
        delete_files_in_folder(temp_path)
        delete_files_in_folder(temp_path + 'pic/')
        self.data_path = data_path

    def add_element(self, x, y, p):
        self.x, self.y = x, y
        matrix = np.array([[x, y, p]])
        self.data_3d_list.append(matrix)

    def add_line(self, view):
        matrix_3d = np.stack(self.data_3d_list)
        self.data_3d_list = []
        self.data_4d_list.append(matrix_3d)
        current_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(self.temp_path + current_time_str + 'view{}_array.matpkl'.format(view), 'wb') as file:
            pickle.dump(matrix_3d, file)
        print("{:=^50s}".format("view {}  finished").format(view))

    def keypoints_generate(self, fps):
        keypoints = np.stack(self.data_4d_list)
        nview = keypoints.shape[0]
        fps = str(fps)
        views_xywh = [[0, 0, 1280, 800], [1280, 0, 1280, 800], [2560, 0, 1280, 800], [0, 800, 1280, 800],
                      [1280, 800, 1280, 800], [2560, 800, 1280, 800], [0, 1600, 1280, 800], [1280, 1600, 1280, 800],
                      [2560, 1600, 1280, 800]][0:nview]
        info = {'nview': nview, 'fps': fps, 'shape': keypoints.shape}
        data = {'keypoints': keypoints, 'info': info, 'views_xywh': views_xywh}
        current_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(self.data_path + current_time_str + 'full_data.matpkl', 'wb') as file:
            pickle.dump(data, file)
        return data

    def pic_save(self, img_src, view, index):  # 图片保存临时地址，方便检查
        cv2.drawMarker(img_src, [self.x, self.y], color=(205, 0, 0), markerType=1, markerSize=30,
                       thickness=2)

        file_name = self.temp_path + 'pic/' + view + '_' + index
        cv2.imwrite(file_name, img_src)


if __name__ == '__main__':
    path = 'C:\\Users\\723\\Desktop\\images\\'
    views = file_load(path)
    print(views)
