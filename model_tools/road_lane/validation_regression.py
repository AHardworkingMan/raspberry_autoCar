# https://www.cnblogs.com/frombeijingwithlove/p/5314042.html
# https://nbviewer.jupyter.org/github/BVLC/caffe/blob/master/examples/00-classification.ipynb

import sys
import numpy as np
import caffe
import os
import cv2 as cv
import h5py


deploy_file = 'E:/rasp_model/code/Algorithm-Lane_Detection/algorithm\ResNet-18-Caffemodel-on-ImageNet/deploy.prototxt'
caffe_model = 'E:/rasp_model/code/Algorithm-Lane_Detection/algorithm\ResNet-18-Caffemodel-on-ImageNet/output_iter_4200.caffemodel'
# caffe_model = '/home/hanxb/output/classification/caffe/resnet-18-reg/resnet-18-reg_iter_5000.caffemodel'

test_image_list = "E:/rasp_model/imgs/road_line/val_filelist.txt"
test_image_path = "E:/rasp_model/imgs/img/"
output_list = "E:/rasp_model/imgs/road_line/test_result.txt"


OUTPUT_PATH = "E:/rasp_model/imgs/road_line"
TRAIN_HDF5 = "train.h5"
TEST_HDF5 = "test.h5"

image_size = (224, 224)
# if use average mean values
# mean_value = [128, 128, 128]
# if mean is substracted during generating hdf5
# mean_value = [125.30891, 94.282852, 95.152946]
# if mean is not substracted during generating hdf5
mean_value = [0, 0, 0]

caffe.set_mode_gpu()
net = caffe.Net(deploy_file, caffe_model, caffe.TEST)
net.blobs['data'].reshape(1, 3, *image_size)



transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
# HWC -> CHW
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.array(mean_value))
transformer.set_raw_scale('data', 255)
# RGB-->BGR
transformer.set_channel_swap('data', (2,1,0))


# read from file with caffe.io
def read_by_caffe():
    total_loss = 0.0
    count = 0
    with open(test_image_list, 'r') as f_test, open(output_list, "w") as f_out:
        for line in f_test.readlines():
            count += 1
            test_filename = line[:-1]
            test_filename = os.path.join(test_image_path, test_filename)
            image = caffe.io.load_image(test_filename, True)
            transformed_image = transformer.preprocess('data', image)
            # print("image ", image)
            # print("transformed_image, ", transformed_image)
            # print(transformed_image.shape)
            # print(image.shape)
            net.blobs['data'].data[...] = transformed_image

            output = net.forward()
            score = output['fc2'][0]
            x = score[0]
            y = score[1]
            f_out.write(test_filename + " : " + np.array2string(score, precision=6, separator=',')[1:-1] + "\n")

            json_filename = test_filename.replace(".jpg", ".json")
            with open(json_filename, "r") as json_f:
                label = json_f.read()
                label = label[1:-2]
                label = [int(i) for i in label.split(",")]
                label = [label[0]/1280.0, label[1]/720.0]
            loss = sum([(score[0] - label[0]) ** 2, (score[1] - label[1]) ** 2]) / (2*2)
            total_loss += loss
            mean_loss = total_loss / count
            print (test_filename)
            print (score)
            print (label)
            print("loss = ", loss)
            print("mean_loss = ", mean_loss)

            # img = cv.imread(test_filename, 1)
            # cv.circle(img, (int(x/100.0*224), int(y/100.0*224)), 1, (0,255,0), -1)
            # cv.imshow("", img)
            # cv.waitKey()


# read from file with opencv
def read_by_opencv():
    total_loss = 0.0
    count = 0
    with open(test_image_list, 'r') as f_test:
        for line in f_test.readlines():
            count += 1
            test_filename = line[:-1]
            test_filename = os.path.join(test_image_path, test_filename)
            image = cv.imread(test_filename, 1)
            transformed_image = cv.resize(image, (224, 224))
            # 1. standard transform
            # RGB2BGR
            transformed_image = cv.cvtColor(transformed_image, cv.COLOR_BGR2RGB)
            # HWC -> CHW, (224,224,3) -> (3,224,224)
            transformed_image = transformed_image.transpose(2, 0, 1)

            # 2. another wrong way
            # transformed_image = transformed_image.reshape((3,224,224))

            net.blobs['data'].data[...] = transformed_image

            output = net.forward()
            score = output['fc2'][0]
            x = score[0]
            y = score[1]

            json_filename = test_filename.replace(".jpg", ".json")
            with open(json_filename, "r") as json_f:
                label = json_f.read()
                label = label[1:-2]
                label = [int(i) for i in label.split(",")]
                label = [label[0]/1280.0, label[1]/720.0]
            loss = sum([(score[0] - label[0]) ** 2, (score[1] - label[1]) ** 2]) / (2*2)
            total_loss += loss
            mean_loss = total_loss / count
            # print (image)
            # print (transformed_image)
            # print (test_filename)
            print (score)
            print (label)
            print("loss = ", loss)
            print("mean_loss = ", mean_loss)

            # img = cv.imread(test_filename, 1)
            # cv.circle(img, (int(x*1280), int(y*720)), 10, (0,255,0), -1)
            # cv.circle(img, (int(label[0]*1280), int(label[1]*720)), 10, (255,0,0), -1)
            # cv.imshow("", img)
            # cv.waitKey()



# read from hdf5
def read_by_hdf5():
    filename = os.path.join(OUTPUT_PATH, TEST_HDF5)
    f = h5py.File(filename, 'r')

    print("Keys: %s" % f.keys())
    label_group = f["label"]
    data_group = f["data"]
    labels = list(f["label"])
    data = list(f["data"])

    total_loss = 0.0
    count = 0
    for i in range(len(labels)):
        count += 1
        img = data[i]
        label = labels[i]

        net.blobs['data'].data[...] = img
        output = net.forward()
        score = output['fc2'][0]
        # print(img)
        # print(img.shape)
        print(score)
        print(label)

        loss = sum([(score[0] - label[0]) ** 2, (score[1] - label[1]) ** 2]) / (2*2)
        total_loss += loss
        mean_loss = total_loss / count
        print("loss = ", loss)
        print("mean_loss = ", mean_loss)

def main():
    # read_by_caffe()
    read_by_opencv()
    # read_by_hdf5()

if __name__ == '__main__':
    main()
