import os
import csv
import numpy as np
from tools.files_process import is_dir_exist


def read_csv(csv_path, header_exist=True):
    if not os.path.exists(csv_path):
        print("文件不存在:", csv_path)
        return [], [], -1

    with open(csv_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        # 'utf-8-sig' 解决 “出现\ufeff”：文本保存时包含了BOM（Byte Order Mark，字节顺序标记）
        rows = csv.reader(csvfile)
        count = 0
        header = []
        content = []
        for row in rows:
            count += 1
            if header_exist and count == 1:
                header = row
            else:
                content.append(np.array(row))
        if count < 1:
            print("空文件:", csv_path)
            return [], [], -1
    return header, np.array(content), count


def write_csv(csv_path, header, rows):
    is_dir_exist(csv_path)
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
    return 0


def append_csv(csv_path, rows):
    if os.path.exists(csv_path):
        with open(csv_path, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in rows:
                writer.writerow(row)
        return 0
    else:
        print("!!! {} 不存在".format(csv_path))
        return -1

