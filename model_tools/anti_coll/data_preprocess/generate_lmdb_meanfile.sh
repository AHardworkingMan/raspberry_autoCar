if [ $# -eq 2 ]; then
    echo "Start"
    echo "train_dataset : $1"
    echo "test_dataset : $2"
    echo "train_label : $1_label.txt"
    echo "test_label : $2_label.txt"
    ~/caffe/build/tools/convert_imageset -resize_height=224 -resize_width=224 -shuffle=true $1/ $1_label.txt $1_lmdb
    ~/caffe/build/tools/convert_imageset -resize_height=224 -resize_width=224 -shuffle=true $2/ $2_label.txt $2_lmdb
    ~/caffe/build/tools/compute_image_mean $1_lmdb  $1_mean.binaryproto
    ~/caffe/build/tools/compute_image_mean $2_lmdb  $2_mean.binaryproto
else
    echo "Input path as follow : ./train_dataset ./test_dataset"
fi
