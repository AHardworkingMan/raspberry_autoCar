1.data_augmentation.py
    功能：数据增强（增强方式为：随机改变亮度、随机改变饱和度、随机改变对比度、随机改变锐度、蒙板局部光照、模糊化、左右翻转）
    用例：python data_augmentation.py path_to_dataImage/ path_to_sunlightImage/

2.split_train_test.py
    功能：将整个数据集按比例分割为训练集和测试集（比例可设定），并且生成对应的list.txt和label.txt文件
    用例：python split_train_test.py ./all_img

3.generate_lmdb_meanfile.sh
    功能：生成lmdb文件和对应的meanfile文件
    用例：./generate_lmdb_meanfile.sh ./train_dir ./test_dir