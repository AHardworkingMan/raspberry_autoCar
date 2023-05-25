# !/bin/bash
# default sh is dash in ubuntu, so use 'bash ssd_detect.sh' to start the script in ubuntu
root_dir='/home/nanjing_01/project/caffe/test/data/auto_car/auto_car_220_220'
#model=${root_dir}/models/VGGNet/VOC0712/SSD_220x220/VGG_VOC0712_SSD_220x220_iter_28000.caffemodel
model=${root_dir}/models/VGGNet/VOC0712/SSD_220x220/VGG_VOC0712_SSD_220x220_iter_176000.caffemodel
test_img_dir=${root_dir}/JPEGImages
python ssd_detect_imgs.py --gpu_id=0 --labelmap_file=${root_dir}/labelmap_voc.prototxt --model_def=${root_dir}/models/VGGNet/VOC0712/SSD_220x220/deploy.prototxt --image_resize=220 --model_weights=${model} --image_file=${test_img_dir}
