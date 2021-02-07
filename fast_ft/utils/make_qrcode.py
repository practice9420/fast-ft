import os
from pathlib import Path

import qrcode
import socket
import webbrowser
import time


def get_inner_ip():
    """
    获取本机内网ip
    :return:
    """
    return socket.gethostbyname(socket.gethostname())


def open_browser(open_url='http://www.baidu.com'):
    """
    在浏览器中打开指定url
    :return:
    """
    webbrowser.open_new(open_url)


def make_qrcode_(make_url='http://101.200.206.164/', save_path='./', qrcode_name='test.png'):
    """
    生成二维码
    :param make_url: 需要生成的url地址
    :param save_path: 保存路径
    :param qrcode_name: 保存图面名称
    :return:
    """
    # img_path = qrcode.make(make_url)
    # with open(os.path.join(save_path, qrcode_name), 'wb') as f:
    #     img_path.save(f)
    qrcode_img = os.path.join(save_path, qrcode_name)
    if Path(qrcode_img).exists():
        return

    # 删除其他二维码
    files = os.listdir(save_path)
    for f in files:
        os.remove(os.path.join(save_path, f))

    # 高级用法
    qr = qrcode.QRCode(
        # 二维码矩阵尺寸
        version=1,
        # 二维码容错率
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        # 二维码中每个Box的像素值
        box_size=10,
        # 二维码与图片边界的距离,默认为4
        border=0,
    )
    qr.add_data(make_url)
    qr.make(fit=True)

    img1 = qr.make_image()
    img1.save(os.path.join(save_path, qrcode_name))


if __name__ == '__main__':
    # make_qrcode()
    # print(get_inner_ip())
    url = 'http://' + get_inner_ip() + ':8002'
    open_browser(open_url=url)
