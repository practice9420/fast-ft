#!/usr/bin/env python
# coding=utf-8
import json
import os
import sys
from pathlib import Path

from flask import Flask, request, Response, render_template as rt
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

# 打包后添加当前目录到环境变量以便导入项目中的包
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.get_folder_info import get_file_and_folder
from utils.get_ip import get_ip
from utils.make_qrcode import get_inner_ip, open_browser, make_qrcode_
from utils.health_examination import net_is_used
from utils.process_argv import process_argv

app = Flask(__name__)

# 项目根路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 上传路径
upload = os.path.join(BASE_DIR, 'upload/{}')

# 全局内网IP
global_inner_ip = '127.0.0.1'
global_port = 5000
user_socket_set = set()


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
    return rt('./index_new.html')


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

    return rt('./index_new.html')


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


@app.route('/webchat/', methods=['GET'])
def get_webchat():
    return rt('./webchat.html', ws_url=global_inner_ip, ws_port=global_port)


@app.route("/socket/")
def connection_socket():
    user_socket = request.environ.get("wsgi.websocket")
    ip = get_ip(request)
    if user_socket:
        user_socket_set.add(user_socket)
        for u_socket in user_socket_set:
            res_dict = {'chat_people': len(user_socket_set), 'is_update': True}
            try:
                u_socket.send(json.dumps(res_dict))
            except Exception:
                continue
        print('当前socket列表长度：{}； 接入客户端ip：{}。'.format(len(user_socket_set), ip))
    try:
        while True:
            req_json = user_socket.receive()
            if req_json is None:
                raise WebSocketError
            receive_dict = json.loads(req_json)
            msg = receive_dict.get('message')
            nick_name = receive_dict.get('nick_name')
            print('接受来自ip({})的信息：{}。'.format(ip, msg))
            for u_socket in user_socket_set:
                res_dict = {
                    'message': msg, 'ip': ip, 'nick_name': nick_name, 'chat_people': len(user_socket_set),
                    'is_mine': False if u_socket is not user_socket else True, 'is_update': False
                }
                try:
                    u_socket.send(json.dumps(res_dict))
                except Exception:
                    continue
    except WebSocketError as ex:
        user_socket_set.remove(user_socket)
        print('当前socket列表长度：{}； 断开客户端ip：{}；'.format(len(user_socket_set), ip))
        for u_socket in user_socket_set:
            res_dict = {'chat_people': len(user_socket_set), 'is_update': True}
            try:
                u_socket.send(json.dumps(res_dict))
            except Exception:
                continue
        return 'close'


def main():
    kwargs = process_argv(sys.argv[1:])
    host = kwargs.get('host') if kwargs.get('host') else '0.0.0.0'
    port = int(kwargs.get('port')) if kwargs.get('port') else 5000
    # 检查 上传目录是否存在 不存在就创建
    if not Path(upload.format('')).exists():
        os.mkdir(upload.format(''))
    # 生成二维码
    inner_ip = get_inner_ip()
    global global_inner_ip
    global_inner_ip = inner_ip
    if net_is_used(port):
        for i in range(10):
            port += 1
            if not net_is_used(port, inner_ip):
                break
    global global_port
    global_port = port
    make_url = 'http://{}:{}'.format(inner_ip, port)
    save_path = os.path.join(BASE_DIR, 'static/images/qrcode/')
    make_qrcode_(make_url=make_url, save_path=save_path, qrcode_name='{}.png'.format(inner_ip))
    # 自动打开浏览器
    if kwargs.get('open_browser', True):
        open_url = 'http://{}:{}'.format(inner_ip, port)
        open_browser(open_url)
    # 在APP外封装websocket
    http_server = WSGIServer((host, port), app, handler_class=WebSocketHandler)
    # 启动服务
    http_server.serve_forever()

# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------


if __name__ == '__main__' or '__main__' in sys.argv:
    main()
