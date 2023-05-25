# =============
# output file content:
# image_name.jpg 100,80
# =============


import os
import json
import numpy as np
import pandas as pd
np.random.seed(1)


DATASET_PATH = "E:/rasp_model/imgs/img"
OUTPUT_PATH = "E:/rasp_model/imgs/road_line"
TRAIN_LIST_NAME = "train_filelist.txt"
VAL_LIST_NAME = "val_filelist.txt"




def get_orordinate(filename):
    # append coordinates after filename
    json_filename = os.path.join(DATASET_PATH, filename.replace(".jpg", ".json"))
    with open(json_filename, "r") as f_json:
        anno = json.loads(f_json.read())
    return anno[0:2]


train_list = []
val_list = []

for (dirpath, dirnames, filenames) in os.walk(DATASET_PATH):
    filenames = [filename for filename in filenames if filename.endswith(".jpg")]
    total_file_number = len(filenames)

    # train / val

    num_train = int(total_file_number * 0.9)
    num_validation = total_file_number - num_train

    index_train = np.random.choice(total_file_number, size=num_train, replace=False)
    index_validation = np.setdiff1d(list(range(total_file_number)), index_train)

    train_set = [filenames[index] for index in index_train]
    validation_set = [filenames[index] for index in index_validation]

    train_list += train_set
    val_list +=validation_set


# with open(TRAIN_LIST_NAME, "w") as f:
#     for filename in train_list:
#         anno = get_orordinate(filename)
#         anno_str = ",".join([str(i) for i in anno])
#         line_to_write = filename + " " + anno_str + "\n"
#         f.write(line_to_write)
# with open(VAL_LIST_NAME, "w") as f:
#     for filename in val_list:
#         anno = get_orordinate(filename)
#         anno_str = ",".join([str(i) for i in anno])
#         line_to_write = filename + " " + anno_str + "\n"
#         f.write(line_to_write)

with open("{}/{}".format(OUTPUT_PATH, TRAIN_LIST_NAME), "w") as f:
    for filename in train_list:
        f.write(filename + "\n")
with open("{}/{}".format(OUTPUT_PATH, VAL_LIST_NAME), "w") as f:
    for filename in val_list:
        f.write(filename + "\n")
