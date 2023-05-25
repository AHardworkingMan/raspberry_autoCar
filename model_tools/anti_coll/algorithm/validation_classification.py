# coding: utf-8
import sys
sys.path.append('/home/jlm/caffe/python')
import numpy as np
import caffe
import os

deploy = 'E:/rasp_model/code/Algorithm-collision_anti-drop/algorithm/Resnet18_classification/Resnet18_class_deploy.prototxt'
caffe_model = 'E:/rasp_model/code/Algorithm-collision_anti-drop/algorithm/Resnet18_classification/2+2_table_nj_iter_50000.caffemodel'

labels_filename = 'E:/rasp_model/imgs/Resnet18_class/label_class.txt' 
test_image_list = "E:/rasp_model/imgs/img/Table_anti-collision_data_83080_test_list.txt"
test_image_dir = 'E:/rasp_model/imgs/img/Resnet18_class/Table_data/Table_anti-collision_data_83080_test'

result_path = 'E:/rasp_model/imgs/Resnet18_class/test_result/83080_test.txt'

mean_value = [108,105,121]
image_size = (224, 224)

sum = 0.0
correct = 0

caffe.set_mode_gpu()
net = caffe.Net(deploy,caffe_model,caffe.TEST)
net.blobs['data'].reshape(1, 3, *image_size)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})  
transformer.set_transpose('data', (2,0,1))   
transformer.set_mean('data', np.array(mean_value))
transformer.set_raw_scale('data', 255)   
transformer.set_channel_swap('data', (2,1,0))

with open(test_image_list, 'r') as f_test, open(result_path, "a+") as f_out:
   for line in f_test.readlines():
      filename = line[:-1]
      filename_save = filename
      filename = os.path.join(test_image_dir, filename)
      # print (filename)
      image = caffe.io.load_image(filename, True)
      transformed_image = transformer.preprocess('data', image)
      # print(transformed_image.shape)
      # print(image.shape)
      net.blobs['data'].data[...] = transformed_image

      output = net.forward()

      labels = np.loadtxt(labels_filename, str, delimiter='\t') 
      prob= net.blobs['prob'].data[0].flatten()   #取出最后一层（prob）属于某个类别的概率值  data[0].flatten()
      order=prob.argsort()[1]  #从小到大排列，2分类网络:[0][1]

      # print (filename_save + ':' + labels[order])
      print (('{:<55}'.format(filename_save)) + ' is ' + labels[order])
      print ('------------------------------------------------')
      f_out.writelines(filename_save + ' ' + labels[order] + '\n')



with open(result_path,'r') as f:
   for fn in f.readlines():
      file = fn[:-1]
      file_correct = file.split('_')[1]
      file_result = file.split(' ')[1]
      sum += 1
      if file_correct == 'danger' and file_result == 'danger':
            correct += 1
      if file_correct == 'safe' and file_result == 'safe':
            correct += 1

print('test sum :', sum, '\n')
print('accuracy for algorithm:', correct / sum , '\n')

with open(result_path, 'a+') as f:
   f.write('test sum :' + str(sum) + '\n')
   f.write('accuracy for algorithm:' + str(correct / sum) +  '\n')
