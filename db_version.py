# coding=utf-8
import os


def read(file_path):  # 读version.txt文件，并返回版本号
    with open(file_path) as files:
        v = files.read()
    return v


def write(path, v):  # 向version.txt写版本号
    file_path = path + r'\version.txt'
    with open(file_path, 'w') as files:
        files.write(v)


def create(file_path):  # 创建version.txt文件
    start_version = 1.0  # 自动创建的dashboard工程起始编号

    with open(file_path, 'w') as files:
        files.write(str(start_version))
    return str(start_version)


def change(change_version):  # 将强制更改dashboard的版本编号为该变量值，而不是在之前的基础上进行递增
    # with open(file_path, 'w') as files:
    #     files.write(str(change_version))
    v = str(change_version)
    return v


def add_version(file_path, tolerance):  # 为dashboard的版本号进行更新
    old_v = read(file_path)
    new_v = str(float(old_v) + float(tolerance))
    return new_v


def calculate(path, change_version):
    project_path = path + r'\version.txt'
    FileIsExist = os.path.exists(project_path)  # version.exe文件存在标志位
    ChangeIsZero = change_version != 0  # 变更版本标志位
    Key = FileIsExist * 2 + ChangeIsZero
    if Key == 0:
        version = create(project_path)
    elif Key == 1:
        version = change_version(project_path, change_version)
    elif Key == 2:
        version = add_version(project_path, 0.1)
    else:
        if read(project_path) >= str(change_version):
            version = add_version(project_path, 0.1)
        else:
            version = change(change_version)
    return version
