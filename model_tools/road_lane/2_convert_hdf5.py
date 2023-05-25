# ==========
# https://www.cnblogs.com/yjbjingcha/p/8322127.html
# HDF5Data does not transform data.
# So minus mean should be performed in data pre-process.
#
# https://blog.csdn.net/mzpmzk/article/details/89247739
# 2G in one file
# ==========

from __future__ import division

import json
import h5py
import sys
import caffe
import os
import cv2
import time
import math
import numpy as np


IMAGE_PATH = "E:/rasp_model/imgs/img"
TRAIN_LIST = "train_filelist.txt"
TEST_LIST = "val_filelist.txt"
OUTPUT_PATH = "E:/rasp_model/imgs/road_line"
TRAIN_HDF5 = "train.h5"
TEST_HDF5 = "test.h5"
NUM_POINT = 1
VARIABLE_LEN = NUM_POINT * 2

is_output_normalized = True
is_input_normalized = True

global B_mean_value, G_mean_value, R_mean_value

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def shuffle_in_unison_scary(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)

# By yaojt
def generate_mean(imgs):
    print("image number to generate mean:", len(imgs))
    global B_mean_value, G_mean_value, R_mean_value
    imgs = imgs.astype(np.float32)
    # print(imgs.shape)
    B_mean = []
    G_mean = []
    R_mean = []
    for i, img in enumerate(imgs):
       w, h, c = img.shape
       bgr = img.mean(1).mean(1)
       B_mean.append(bgr[0])
       G_mean.append(bgr[1])
       R_mean.append(bgr[2])
    B_mean_value = np.asarray(B_mean).mean()
    G_mean_value = np.asarray(G_mean).mean()
    R_mean_value = np.asarray(R_mean).mean()
    # return B_mean_value, G_mean_value, R_mean_value

def generate_mean_fixed():
    global B_mean_value, G_mean_value, R_mean_value
    B_mean_value = 104
    G_mean_value = 117
    R_mean_value = 123


def generate_mean_matrix():
    mean_matrix = np.zeros((3, 224, 224), np.float)
    for i in range(3):
        for j in range(224):
            for k in range(224):
                if i == 0:
                    mean_matrix[i, j, k] = B_mean_value
                if i == 1:
                    mean_matrix[i, j, k] = G_mean_value
                if i == 2:
                    mean_matrix[i, j, k] = R_mean_value
    return mean_matrix


# Wrong here!
# def process_images(imgs):
#     mean_matrix = generate_mean_matrix()
#     imgs = imgs.astype(np.float)
#     for i, img in enumerate(imgs):
#         print("img before: ", img)
#         img = img - mean_matrix
#         print("img after: ", img)
#     print(imgs)
#     print("BGR", B_mean_value, G_mean_value, R_mean_value)
#     return imgs

def process_images(imgs):
    mean_matrix = generate_mean_matrix()
    imgs = imgs.astype(np.float)
    for i in range(len(imgs)):
        imgs[i] = imgs[i] - mean_matrix
    # print(imgs)
    print("BGR", B_mean_value, G_mean_value, R_mean_value)
    return imgs


def generate_trainval_test_list(data_path):
    if not os.path.exists(data_path):
        print(data_path)
        print('The path of data is not exists !!!!!!')
        sys.exit()
    files = os.listdir(data_path)
    if len(files) == 0:
        print('The data is empty !!!!!')
        sys.exit()
    with open("{}/{}".format(OUTPUT_PATH, TRAIN_LIST), "r") as f:
        files_json_train = f.readlines()
        files_json_train = [i.strip().replace(".jpg", ".json") for i in files_json_train]
    with open("{}/{}".format(OUTPUT_PATH, TEST_LIST), "r") as f:
        files_json_test = f.readlines()
        files_json_test = [i.strip().replace(".jpg", ".json") for i in files_json_test]
    return files_json_test, files_json_train


def create_hdf5(data_path, files_json, InBBox, InImg, HDF5_file_name, flags):
    for file_json in files_json:
        file_name = file_json.split('.')[0]
        full_file_name = '%s%s'%(file_name,'.jpg')
        full_file_dir = '%s/%s'%(data_path,full_file_name)
        Img = cv2.imread(full_file_dir)
        h , w, c = Img.shape

        with open("%s/%s"%(data_path, file_json), "r") as json_file:
            load_dict = json.load(json_file)
        landmark = np.zeros(VARIABLE_LEN)
        length = len(load_dict[0:VARIABLE_LEN])
        for i in range(0, length, 2):
            landmark[i] = load_dict[i] / w
            landmark[i + 1] = load_dict[i + 1] / h

        # print(landmark)
        InBBox.append(landmark.reshape(VARIABLE_LEN))
        Img = cv2.resize(Img,(224,224))

        # A wrong method to change HWC to CHW
        # InImg.append(Img.reshape((3,224,224)))

        # image read by OpenCV is BGR, but BGR2RGB is optional, model can be trained with BGR image also.
        # transformed_image = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)

        # Use BGR directly
        transformed_image = Img
        # a correct method to change HWC to CHW, HWC for CPU, CHW for GPU
        transformed_image = transformed_image.transpose(2, 0, 1)
        InImg.append(transformed_image)

    InImg, InBBox = np.asarray(InImg), np.asarray(InBBox)
    # if flags == 'train':
    #     generate_mean(InImg)
    # generate_mean(InImg)
    generate_mean_fixed()
    InImg = process_images(InImg)
    shuffle_in_unison_scary(InImg, InBBox)
    with h5py.File(HDF5_file_name, 'w') as h5:
        h5['data'] = InImg.astype(np.float32)
        h5['label'] = InBBox.astype(np.float32)
        h5.close()
    print("Saved to ", HDF5_file_name)

def generate_trainvl_hdf5(data_path, files_json_train, hdf5_test, flags="train"):
    InBBox_test = []
    InImg_test = []
    create_hdf5(data_path, files_json_train, InBBox_test, InImg_test, hdf5_test, flags)
    with open('{}/{}_h5.txt'.format(OUTPUT_PATH, 'train'), 'w') as f:
        f.write(hdf5_test)

def generate_test_hdf5(data_path, files_json_test, hdf5_train, flags="test"):
    InBBox_train = []
    InImg_train = []
    create_hdf5(data_path,files_json_test, InBBox_train, InImg_train, hdf5_train, flags)
    with open('{}/{}_h5.txt'.format(OUTPUT_PATH, 'test'), 'w') as f:
        f.write(hdf5_train)


def main():
    data_path = IMAGE_PATH
    test_data_list, train_data_list = generate_trainval_test_list(data_path)

    hdf5_train = os.path.join(OUTPUT_PATH, TRAIN_HDF5)
    generate_trainvl_hdf5(data_path, train_data_list, hdf5_train)
    hdf5_test = os.path.join(OUTPUT_PATH, TEST_HDF5)
    generate_test_hdf5(data_path, test_data_list, hdf5_test)

    # with open("train_list.txt", "w") as f:
    #     for f_name in train_data_list:
    #         f_name = f_name.replace(".json", ".jpg")
    #         f.write(f_name + "\n")

    # with open("test_list.txt", "w") as f:
    #     for f_name in test_data_list:
    #         f_name = f_name.replace(".json", ".jpg")
    #         f.write(f_name + "\n")


if __name__ == '__main__':
    main()
