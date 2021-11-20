#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py.py    
@Contact :   https://2409256477@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/2/7 13:04   huangjh      1.0         None
"""
from flask import Flask
from flask_socketio import SocketIO

socket_server = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!58#'

    from transferFileViews import transfer
    app.register_blueprint(transfer)

    socket_server.init_app(app)
    return app
