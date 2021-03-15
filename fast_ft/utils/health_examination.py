#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   health_examination.py    
@Contact :   https://2409256477@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/2/7 13:15   huangjh      1.0         None
"""
import socket


def net_is_used(port, ip='127.0.0.1'):
    """
    查看端口是否占用
    :param port: 端口
    :param ip:
    :return: boolean False 表示没有占用 True 表示已被占用
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(2)
        return True
    except Exception as e:
        print('bind host: http://{}:{}'.format(ip, port))
        return False


if __name__ == '__main__':
    # False 表示没有占用
    is_ok = net_is_used(5000)
    print(is_ok)
