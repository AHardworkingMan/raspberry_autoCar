import os
import subprocess
import sys

def create_env():
    all_list = os.listdir('.')
    if test_dir_path.split('/')[1] in all_list or train_dir_path.split('/')[1] in all_list:
        print('Please delete dir: ' + test_dir_path,train_dir_path)
        return 0
    elif test_list.split('/')[1] in all_list or train_list.split('/')[1] in all_list:
        print('Please delete txt: ' + test_list,train_list)
        return 0

    elif test_label.split('/')[1] in all_list or train_label.split('/')[1] in all_list:
        print('Please delete txt: ' + test_label,train_label) 
        return 0

    else:
        mk_train_dir = ['mkdir', train_dir_path]
        mk_test_dir = ['mkdir', test_dir_path]
        subprocess.run(mk_train_dir)
        subprocess.run(mk_test_dir)
        return 1


def parting_all_img(all_img_path,train_scale,test_scale):
    all_img_list = os.listdir(all_img_path)
    for index in range(0, len(all_img_list)):
        if index%(train_scale + test_scale) < test_scale:
            move = ['mv', all_img_path + '/' + all_img_list[index], test_dir_path]
        else:
            move = ['mv', all_img_path + '/' + all_img_list[index], train_dir_path]
        subprocess.run(move)

def generate_list():
    train_img_list = os.listdir(train_dir_path)
    with open(train_list, 'a+') as train_list_f:
        for index in range(0, len(train_img_list)):
            train_list_f.write(train_img_list[index] + '\n')
    train_list_f.close()

    test_img_list = os.listdir(test_dir_path)
    with open(test_list, 'a+') as test_list_f:
        for index in range(0, len(test_img_list)):
            test_list_f.write(test_img_list[index] + '\n')
    test_list_f.close()

def generate_label():
    with open(train_label, 'a+') as train_label_f:
        for train_img in os.listdir(train_dir_path):
            if train_img.split('_')[1] == 'danger':
                train_label_f.write(train_img + ' ' + '0' + '\n')
            elif train_img.split('_')[1] == 'safe':
                train_label_f.write(train_img + ' ' + '1' + '\n')
    train_label_f.close()
    
    with open(test_label, 'a+') as test_label_f:
        for test_img in os.listdir(test_dir_path):
            if test_img.split('_')[1] == 'danger':
                test_label_f.write(test_img + ' ' + '0' + '\n')
            elif test_img.split('_')[1] == 'safe':
                test_label_f.write(test_img + ' ' + '1' + '\n')
    test_label_f.close()


if __name__ == '__main__' :
    
    IMG_PATH = sys.argv[1]
    if list(IMG_PATH).count('/') > 1:
        print('makesure input path as : ./all_img')
    else :
        train_dir_path = IMG_PATH + '_train'
        test_dir_path = IMG_PATH + '_test'
        train_list = train_dir_path + '_list.txt'
        test_list = test_dir_path + '_list.txt'
        train_label = train_dir_path + '_label.txt'
        test_label = test_dir_path + '_label.txt'
    
        if(create_env()):
            parting_all_img(IMG_PATH,9,1) # change train/test at here (xxx,train proportion, test proportion)
            generate_list()
            generate_label()
