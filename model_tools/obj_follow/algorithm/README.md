# caffe训练脚本相关说明
* ## caffe源码下载地址和安装
### git clone https://github.com/weiliu89/caffe.git
* ## 脚本代码相关说明
    ### ssd_pascal_220_220.py用于训练ssd模型
    ### ssd_detect_220.sh和ssd_detect_imgs.py用于模型测试
    ### gen_imageset_ssd_220.py 用于生成训练用的PASCAL VOC格式文件
    ### prototxt 训练用网络模型，包括测试、验证、部署、和训练
* ## 其它说明
    ### 将caffe源码下载后按照caffe里的编译流程编译完成，将脚本代码和caffe源码结合，将自己的数据集加入到caffe训练路径后可以使用prototxt直接训练。也可以直接用ssd\_pascal\_220_\220.py生成训练用网络模型。
