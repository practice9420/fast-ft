#!/usr/bin/env python
# coding=utf-8

import os
from pathlib import Path

from flask import Flask, request, Response, render_template as rt

from .utils.get_folder_info import get_file_and_folder
from .utils.make_qrcode import get_inner_ip, open_browser, make_qrcode_
from .utils.health_examination import net_is_used

app = Flask(__name__)

# 项目根路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 上传路径
upload = os.path.join(BASE_DIR, 'upload/{}')

# 全局内网IP
global_inner_ip = 'test'


@app.route('/', methods=['GET'])
def index():
    return rt('./index_new.html', global_inner_ip=global_inner_ip)


@app.route('/file/upload', methods=['POST'])
def upload_part():  # 接收前端上传的一个分片
    task = request.form.get('task_id')  # 获取文件的唯一标识符
    chunk = request.form.get('chunk', 0)  # 获取该分片在所有分片中的序号
    filename = '%s%s' % (task, chunk)  # 构造该分片的唯一标识符

    upload_file = request.files['file']
    upload_file.save(upload.format(filename))  # 保存分片到本地
    return rt('./index.html')


@app.route('/file/merge', methods=['GET'])
def upload_success():  # 按序读出分片内容，并写入新文件
    target_filename = request.args.get('filename')  # 获取上传文件的文件名
    task = request.args.get('task_id')  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    path = upload.format(target_filename)
    with open(path, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = upload.format('{}{}'.format(task, chunk))
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break
            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间

    return rt('./index.html')


@app.route('/file/list', methods=['GET'])
def file_list():
    folder = request.args.get('folder', '')
    pre_folder = request.args.get('pre_folder')
    # 获取上传路劲以下子路径
    base_path = upload.replace('\\', '/').format('')
    if pre_folder:
        folder_list = pre_folder.replace(base_path, '').split('/')
        try:
            folder = folder_list[-2]
        except Exception as e:
            folder = ''
    path = upload.format(folder)
    if folder and not Path(path).exists():
        path = upload.format('')
    path = path.replace('\\', '/')
    # 获取文件目录
    files = get_file_and_folder(path)
    upload_path = upload.format('').replace('\\', '/')
    # files = map(lambda x: x if isinstance(x, 'unicode') else x.decode('utf-8'), files)  # 注意编码
    return rt('./list_new.html', files=files, path=path, folder=folder, upload_path=upload_path)


@app.route('/file/download/<filename>', methods=['GET'])
def file_download(filename):
    def send_chunk():  # 流式读取
        store_path = upload.format(filename)
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')


def main(**kwargs):
    host = kwargs.get('host') if kwargs.get('host') else '0.0.0.0'
    port = int(kwargs.get('port')) if kwargs.get('port') else 5000
    # 检查 上传目录是否存在 不存在就创建
    if not Path(upload.format('')).exists():
        os.mkdir(upload.format(''))
    if net_is_used(port):
        for i in range(3):
            port += 1
            if not net_is_used(port):
                break
    # 生成二维码
    inner_ip = get_inner_ip()
    global global_inner_ip
    global_inner_ip = inner_ip
    make_url = 'http://{}:{}'.format(inner_ip, port)
    save_path = os.path.join(BASE_DIR, 'static/images/qrcode/')
    make_qrcode_(make_url=make_url, save_path=save_path, qrcode_name='{}.png'.format(inner_ip))
    # 自动打开浏览器
    if kwargs.get('open_browser', True):
        open_url = 'http://{}:{}'.format(inner_ip, port)
        open_browser(open_url)
    app.run(debug=False, threaded=True, host=host, port=port)

# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
