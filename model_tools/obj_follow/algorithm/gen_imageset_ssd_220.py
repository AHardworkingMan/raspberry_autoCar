import sys,os 
import random 
import glob
import cv2
if __name__ == '__main__':
    caffe_root=sys.argv[1:][0]
    dataset_dir=sys.argv[1:][1]
    if dataset_dir[-1]=='/':
        dataset_dir[:-1]
    #trainval_percent = 0.66
    #train_percent = 0.5
    trainval_percent = 0.70
    train_percent = 0.65
    xmlfilepath = os.path.join(dataset_dir,'Annotations')
    txtsavepath = os.path.join(dataset_dir,'ImageSets/Main')
    total_xml = os.listdir(xmlfilepath) 
    num=len(total_xml) 
    list=range(num) 
    tv=int(num*trainval_percent) 
    tr=int(tv*train_percent) 
    trainval= random.sample(list,tv)
    train=random.sample(trainval,tr)
    ftrainval = open(os.path.join(dataset_dir,'ImageSets/Main/trainval.txt'), 'w')
    ftest = open(os.path.join(dataset_dir,'ImageSets/Main/test.txt'), 'w')
    ftrain = open(os.path.join(dataset_dir,'ImageSets/Main/train.txt'), 'w')
    fval = open(os.path.join(dataset_dir,'ImageSets/Main/val.txt'), 'w')
    for i in list: 
        name=total_xml[i][:-4]+'\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)
    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest .close()
    print('*'*20,'generate ImageSets done')

    dataset_name=dataset_dir.split("/")[-1]
    gen_root_dir=os.path.join(dataset_dir,'lmdb')
    if os.path.exists(gen_root_dir):
        os.system('rm -rf {}'.format(gen_root_dir))
    os.system('mkdir -p {}'.format(gen_root_dir))
    with open(os.path.join(dataset_dir,'ImageSets/Main/trainval.txt')) as ftv:
        with open(os.path.join(gen_root_dir,'trainval.txt'),'w') as ftvw:
            for idx,l1 in enumerate(ftv.readlines()):
                l=l1.replace('\n','')
                print(l)
                #ftvw.write("{} {} {}\n".format(idx+1,'{}/JPEGImages/{}.xml'.format(dataset_name,l),'{}/Annotations/{}.xml'.format(dataset_name,l)))
                ftvw.write("{} {}\n".format('{}/JPEGImages/{}.jpg'.format(dataset_name,l),'{}/Annotations/{}.xml'.format(dataset_name,l)))

    with open(os.path.join(dataset_dir,'ImageSets/Main/test.txt')) as ftv:
        with open(os.path.join(gen_root_dir,'test.txt'),'w') as ftvw:
            for idx,l1 in enumerate(ftv.readlines()):
                l=l1.replace('\n','')
                #ftvw.write("{} {} {}\n".format(idx+1,'{}/JPEGImages/{}.xml'.format(dataset_name,l),'{}/Annotations/{}.xml'.format(dataset_name,l)))
                ftvw.write("{} {}\n".format('{}/JPEGImages/{}.jpg'.format(dataset_name,l),'{}/Annotations/{}.xml'.format(dataset_name,l)))


    with open(os.path.join(gen_root_dir,'test_name_size.txt'),'w') as ftvw:
        imgs = glob.glob(os.path.join(dataset_dir,'JPEGImages/*.jpg'))
        for img in imgs:
            name=os.path.basename(img)[:-(len(img.split(".")[-1])+1)]
            i=cv2.imread(img,1)
            ftvw.write("{} {} {}\n".format(name,i.shape[0],i.shape[1]))


    redo=1
    root_dir=caffe_root
    data_root_dir=os.path.dirname(dataset_dir) if dataset_dir[-1] != '/' else os.path.dirname(dataset_dir[:-1])
    print("#"*100,data_root_dir)
    dataset_name="VOC0712"
    mapfile=os.path.join(dataset_dir,'labelmap_voc.prototxt')
    anno_type="detection"
    db="lmdb_result"
    min_dim=0
    max_dim=0
    width=220
    height=220
    dataset_db=os.path.join(data_root_dir,dataset_name,db,dataset_name)
    os.system('rm -rf {}'.format(dataset_db))

    extra_cmd="--encode-type=jpg --encoded"
    if redo==1:
      extra_cmd="{} --redo".format(extra_cmd)

    for subset in ['test', 'trainval']:
        subset_f=os.path.join(gen_root_dir,"{}.txt".format(subset))
        cmd_params={'root_dir':root_dir,
                'anno_type':anno_type,
                'mapfile':mapfile,
                'min_dim':min_dim,
                'max_dim':max_dim,
                'resized_width':width,
                'resized_height':height,
                'extra_cmd':extra_cmd,
                'data_root_dir':data_root_dir,
                'subset_f':subset_f,
                'gen_root_dir':gen_root_dir,
                'dataset_db':os.path.join(dataset_db,subset)
                }
        cmd='''python {root_dir}/scripts/create_annoset.py --anno-type={anno_type} --label-map-file={mapfile} --min-dim={min_dim} --max-dim={max_dim} --resize-width={resized_width} --resize-height={resized_height} --check-label {extra_cmd} {data_root_dir} {subset_f} {dataset_db} {gen_root_dir}'''.format(**cmd_params)
        print(cmd)
        os.system(cmd)

    print('*'*20,'generate lmdb done')
