#!/usr/bin/env python
# coding=utf-8
import os
import sys
from pathlib import Path

# 打包后添加当前目录到环境变量以便导入项目中的包
from settings import Config
from create_app import create_app, socket_server

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.make_qrcode import get_inner_ip, open_browser, make_qrcode_
from utils.health_examination import net_is_used
from utils.process_argv import process_argv

# 项目根路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 上传路径
upload = os.path.join(BASE_DIR, "upload/{}")


def main():
    kwargs = process_argv(sys.argv[1:])
    host = kwargs.get("host") if kwargs.get("host") else "0.0.0.0"
    port = int(kwargs.get("port")) if kwargs.get("port") else 5000
    # 检查 上传目录是否存在 不存在就创建
    if not Path(upload.format("")).exists():
        os.mkdir(upload.format(""))
    # 生成二维码
    inner_ip = get_inner_ip()
    Config.global_inner_ip = inner_ip
    if net_is_used(port, inner_ip):
        for i in range(10):
            port += 1
            if not net_is_used(port, inner_ip):
                break
    Config.global_port = port
    make_url = "http://{}:{}".format(inner_ip, port)
    save_path = os.path.join(BASE_DIR, "static/images/qrcode/")
    make_qrcode_(make_url=make_url, save_path=save_path, qrcode_name="{}.png".format(inner_ip))
    # 自动打开浏览器
    if kwargs.get("open_browser", False):
        open_url = "http://{}:{}".format(inner_ip, port)
        open_browser(open_url)
    app = create_app(debug=True)
    app.run(host=host, port=port)
    # socket_server.run(app, host=host, port=port)

# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------


if __name__ == "__main__" or "__main__" in sys.argv:
    main()
