#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   get_ip.py    
@Contact :   https://2409256477@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/3/6 17:55   huangjh      1.0         None
"""


def get_ip(request):
    """
    获取请求ip
    :param request:
    :return:
    """
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']
