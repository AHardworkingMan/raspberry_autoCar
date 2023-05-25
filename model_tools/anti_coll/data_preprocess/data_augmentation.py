# -*- coding:utf-8 -*-
from PIL import Image, ImageEnhance, ImageOps, ImageFile, ImageFilter
import numpy as np
import random
import threading, os, time
import logging
import sys

def randomSaturation(save_path, data_name, image):
    random_factor = np.random.randint(5, 16) / 10.0  # 随机因子
    # print(random_factor)
    saturation_image = ImageEnhance.Color(image).enhance(random_factor)  # 调整图像的饱和度
    # saturation_image.show()
    saturation_image.save(save_path + data_name.split('.')[0] + '_Satu.jpg')

def randomBrightness(save_path, data_name, image):
    random_factor = np.random.randint(5, 16) / 10.0  # 随机因子
    # print(random_factor)
    brightness_image = ImageEnhance.Brightness(image).enhance(random_factor)  # 调整图像的亮度
    # brightness_image.show()
    brightness_image.save(save_path + data_name.split('.')[0] + '_Brig.jpg')

def randomContrast(save_path, data_name, image):
    random_factor = np.random.randint(5, 16) / 10.0  # 随机因子
    # print(random_factor)
    contrast_image = ImageEnhance.Contrast(image).enhance(random_factor)  # 调整图像对比度
    # contrast_image.show()
    contrast_image.save(save_path + data_name.split('.')[0] + '_Cont.jpg')


def randomSharpness(save_path, data_name, image):
    random_factor = np.random.randint(10, 51) / 10.0  # 随机因子
    # print(random_factor) 
    sharpness_image = ImageEnhance.Sharpness(image).enhance(random_factor)  # 调整图像锐度
    # sharpness_image.show()
    sharpness_image.save(save_path + data_name.split('.')[0] + '_Sharp.jpg')


def flipLeft2Right(save_path, data_name, image):
    flip_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    # flip_image.show()
    flip_image.save(save_path + data_name.split('.')[0] + '_Flip.jpg')

def blurImage(path, data_name, image):
    filter_image = image.filter(ImageFilter.BLUR)
    # filter_image.show()
    filter_image.save(path + data_name.split('.')[0] + '_Blur.jpg')


def blendImage(save_path, data_name, data_image, light_image):
    random_factor = (np.random.randint(0, 41) / 10) /10.0  # 随机因子
    new_img = Image.blend(data_image, light_image, random_factor)
    # new_img.show()
    new_img.save(save_path + data_name.split('.')[0] + '_Blend.jpg')

# def traversal(root_dir):
    # for root,dirs,files in os.walk(root_dir):
        # for file in files:
            # if file.split('.')[1] == 'jpg' :
                # print(file)
                # image = getImage(file)
        # for dir in dirs:
            # traversal(dir)

def getImage(path):
    image = Image.open(path)
    return image

def ResizeImage(path, light_image, light_name):
    resize_light = light_image.resize((1280,720),Image.ANTIALIAS)
    resize_light.show()
    resize_light.save(path + light_name)
 
if __name__ == '__main__' :
    data_path = sys.argv[1]
    light_path = sys.argv[2]
    light_list = os.listdir(light_path)
    for data_name in os.listdir(data_path):
        if data_name.split('.')[1] == 'jpg' :
            data_image = getImage(data_path + data_name)
            light_random_index = np.random.randint(0, len(light_list))   
            light_image = getImage(light_path + light_list[light_random_index])
            blendImage(data_path, data_name, data_image, light_image)
            randomBrightness(data_path, data_name, data_image)
            randomSaturation(data_path, data_name, data_image)
            randomSharpness(data_path, data_name, data_image)
            randomContrast(data_path, data_name, data_image)
            flipLeft2Right(data_path, data_name, data_image)
            blurImage(data_path, data_name, data_image)