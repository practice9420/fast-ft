#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   get_folder_info.py    
@Contact :   https://2409256477@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/2/6 10:20   huangjh      1.0         None
"""
import datetime
import os
import time


def get_file_and_folder(target_path):
    """
    获取文件夹下文件 文件夹信息
    :param target_path: 目标路径
    :return:
    """
    files = os.listdir(target_path)
    result_list = list()
    for f in files:
        file_path = os.path.join(target_path, f)
        # 获取时间
        file_update = os.stat(target_path).st_mtime
        file_update = time_format(file_update)
        file_create = os.stat(target_path).st_ctime
        file_create = time_format(file_create)
        file_dict = {'crete_date': file_create, 'update_date': file_update}
        # 判断文件/文件夹
        if os.path.isdir(file_path):
            file_dict.update({'name': f, 'is_folder': True})
        elif os.path.isfile(file_path):
            file_size = os.path.getsize(os.path.join(target_path, f))
            file_size = size_format(file_size)
            file_dict.update({'name': f, 'size': file_size, 'is_folder': False})
        else:
            continue
        result_list.append(file_dict)
    return result_list


def time_format(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
    """
    获取固定格式时间戳
    :param timestamp:
    :param format_str:
    :return:
    """
    date_array = datetime.datetime.fromtimestamp(timestamp)
    format_date = date_array.strftime(format_str)
    return format_date


def size_format(size):
    """
    文件大小格式化
    :param size: byte
    :return:
    """
    if size < 1000:
        return '%i' % size + 'size'
    elif 1000 <= size < 1000000:
        return '%.1f' % float(size/1000) + 'KB'
    elif 1000000 <= size < 1000000000:
        return '%.1f' % float(size/1000000) + 'MB'
    elif 1000000000 <= size < 1000000000000:
        return '%.1f' % float(size/1000000000) + 'GB'
    elif 1000000000000 <= size:
        return '%.1f' % float(size/1000000000000) + 'TB'


if __name__ == '__main__':
    path_ = 'C:\\program1\\fast-ft\\fast_ft\\upload\\'
    result = get_file_and_folder(path_)
    print(result)
