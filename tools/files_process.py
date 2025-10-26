
import os
import shutil
from filecmp import dircmp


def is_file_good(file_path, min_size=1, prt=True):
    if not os.path.exists(file_path):
        if prt:
            print("<is_file_good> file not exist:", file_path)
        return -1
    if os.path.getsize(file_path) < 1000*min_size:
        # os.stat(in_path).st_size
        if prt:
            print(f"<is_file_good> file too small (<{1000*min_size}):", file_path)
        return -2
    return 0


def is_fold_exist(fold, create=True):
    if not os.path.exists(fold):
        if create:
            os.makedirs(fold)
        return False
    return True


def is_dir_exist(path, create=True):
    fold = os.path.dirname(path)
    if not os.path.exists(fold):
        if create:
            os.makedirs(fold)
        return False
    return True


def delete_file(file):
    if not os.path.isfile(file):
        print("not exist: {}".format(file))
        return -1
    else:
        try:
            os.remove(file)
            print("successful deleted: {}".format(file))
            return 0
        except Exception as e:
            print(e)
            return -2


def delete_0KB_file(root, type=['hdf', 'xml'], delete=True):
    flag = 0
    for fold, dirs, files in os.walk(root):
        for file in files:
            in_path = os.path.join(fold, file)  # fold可能是in_fold的子文件夹
            if in_path.split('.')[-1] in type and os.stat(in_path).st_size < 1000:
                print("!!! file < 1KB :", in_path)
                flag = 1
                if delete:
                    delete_file(in_path)
    return flag


def delete_fold(fold):
    if not os.path.exists(fold):
        print("文件夹不存在", fold)
        return -1
    shutil.rmtree(fold)
    print("successful deleted:", fold)


def move_file(in_file, out_fold):
    """ 将in_file移到out_fold中 """
    if not os.path.isfile(in_file):
        print("not exist: {}".format(in_file))
    else:
        in_name = in_file.split('\\')[-1]
        if os.path.exists(os.path.join(out_fold, in_name)):
            print("!!! file already there:  {}".format(in_name))

        else:
            shutil.move(in_file, out_fold)  # 系统无法将文件移到不同的磁盘驱动器
            print("successfully moved: {}".format(in_name))


def move_files(in_fold, out_fold, handle='out', file_type=None, delete=True):
    """
    将in_fold内类型为file_type的文件，移到out_fold中
    :param in_fold: 检索所有文件（包括子文件夹内的文件）
    :param out_fold: 仅检索单层，即该文件夹内直接包含的文件
    :param handle: 若两个文件夹内有同名文件，该如何处理。'in'指覆盖(删除out)，'out'指保留源文件(删除in)。
    :return:
    """
    if handle not in ['in', 'out']:
        print("!!! handle not specify")
        return -1

    for fold, dirs, files in os.walk(in_fold):
        for file in files:
            in_path = os.path.join(fold, file)  # fold可能是in_fold的子文件夹
            if file_type is not None:
                if file.split('.')[-1] != file_type:
                    print("skip: ", in_path)
                    continue
            out_path = os.path.join(out_fold, file)
            if os.path.exists(out_path):
                if handle == 'out':
                    os.remove(in_path)
                    print("keep the original:", in_path, '->', out_path)
                    continue
                if handle == 'in':
                    os.remove(out_path)
                    shutil.move(in_path, out_fold)  # 系统无法将文件移到不同的磁盘驱动器
                    print("cover:", in_path, '->', out_path)
                    continue
                print("!!! not handle:", in_path)
            else:
                shutil.move(in_path, out_fold)
                print("move:", in_path, '->', out_path)

    if delete:
        os.removedirs(in_fold)
    return 0


def copy_file(in_file, out_file):
    try:
        shutil.copyfile(in_file, out_file)  # 要求in_file是可写的
        return 0
    except Exception as e:
        print("文件复制失败", in_file)
        print(e)
        return -1


def copy_fold(in_fold, out_fold, delete=True):
    """ 将in_fold内部的所有文件，拷贝到out_fold内部。out_fold必须不存在。"""
    if os.path.exists(out_fold):
        print("<copy_fold> out_fold already exist", out_fold)
        if delete:
            delete_fold(out_fold)
            if os.path.exists(out_fold):
                print("<copy_fold> delete failed", out_fold)
                return -1
            else:
                shutil.copytree(in_fold, out_fold)
    else:
        shutil.copytree(in_fold, out_fold)
    print("<copy_fold> copy success", in_fold)
    return 0
