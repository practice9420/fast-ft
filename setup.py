#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   setup.py    
@Contact :   https://2409256477@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/2/6 21:37   huangjh      1.0         None
"""
import setuptools

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

install_requires = ['click', 'Flask', 'itsdangerous', 'Jinja2', 'MarkupSafe', 'Pillow', 'qrcode',
                    'six', 'Werkzeug', 'gevent-websocket']

setuptools.setup(
    name="fast-ft",
    version="0.1.2",
    author="Uncle supported wall",
    author_email="2409256477@qq.com",
    description="A simple file transfer tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/practice9420/fast-ft",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'fast-ft = fast_ft.server:main',
        ]
    }
)
