#!/usr/bin/env sh
#set -e
#2>&1 > caffe_log.txt

#nohup ../build/tools/caffe train --solver=/home/nanjing_01/project/deepdetect/templates/caffe/resnet_18/resnet_18_solver.prototxt --gpu 0,1,2,3 --weights=/home/nanjing_01/temp/ResNet-18-Caffemodel-on-ImageNet/resnet-18.caffemodel 2>&1 &
#tail -f nohup.out

#../build/tools/caffe train --solver=/home/nanjing_01/project/deepdetect/templates/caffe/resnet_18/resnet_18_solver.prototxt --gpu 0,1,2,3

#finetune
#../build/tools/caffe train --solver=/home/nanjing_01/project/deepdetect/templates/caffe/resnet_18/resnet_18_solver.prototxt --gpu 0,1,2,3 --weights=/home/nanjing_01/temp/ResNet-18-Caffemodel-on-ImageNet/resnet-18.caffemodel

~/caffe/build/tools/caffe train --solver=./Resnet18_class_solver.prototxt  --gpu 0,1 --weights=./Resnet18_table_weights/fine_tuning_weight.caffemodel 2>&1 | tee ./caffe_log.txt

#resume
#../build/tools/caffe train --solver=/home/nanjing_01/project/deepdetect/templates/caffe/resnet_18/resnet_18_solver.prototxt --gpu 0,1,2,3 --snapshot=/home/nanjing_01/project/caffe/test/data/imagenet/snapshot/snapshot_iter_596.caffemodel
