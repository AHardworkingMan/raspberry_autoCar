# export CAFFE_ROOT=$PWD
# export PATH=$CAFFE_ROOT/build/tools:$PATH
# export PYTHONPATH=$CAFFE_ROOT/python:$PYTHONPATH
# export LD_LIBRARY_PATH=/home/hanxb/anaconda3/envs/caffe-ssd/lib:$LD_LIBRARY_PATH

C:/caffe_data/caffe-windows/scripts/build/tools/Release/caffe train \
  -solver lenet_solver_adam.prototxt \
  #-weights /home/hanxb/model_zoo/classification/caffe/resnet-18.caffemodel \
  -gpu 0