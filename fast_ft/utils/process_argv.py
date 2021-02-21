#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   process_argv.py    
@Contact :   https://2409256477@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/2/21 21:10   huangjh      1.0         None
"""


def process_argv(argv_list):
    """
    处理参数列表
    :param argv_list:
    :return:
    """
    type_dict = {'host': str, 'port': int, 'open_browser': eval}
    result_dict = dict()
    for arg in argv_list:
        key_value = arg.split('=')
        get_type = type_dict.get(key_value[0], str)
        result_dict[key_value[0]] = get_type(key_value[-1])
    return result_dict
