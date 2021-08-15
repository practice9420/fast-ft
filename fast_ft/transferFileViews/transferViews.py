import os
from pathlib import Path

from flask import render_template, request, Response

from settings import Config
from utils.get_folder_info import get_file_and_folder
from . import transfer

upload = os.path.join(Config.BASE_DIR, "upload/{}")


@transfer.route("/", methods=["GET"])
def index():
    return render_template("./index_new.html", global_inner_ip=Config.global_inner_ip)


@transfer.route("/file/upload", methods=["POST"])
def upload_parender_template():  # 接收前端上传的一个分片
    task = request.form.get("task_id")  # 获取文件的唯一标识符
    chunk = request.form.get("chunk", 0)  # 获取该分片在所有分片中的序号
    filename = "%s%s" % (task, chunk)  # 构造该分片的唯一标识符

    upload_file = request.files["file"]
    upload_file.save(upload.format(filename))  # 保存分片到本地
    return render_template("./index_new.html")


@transfer.route("/file/merge", methods=["GET"])
def upload_success():  # 按序读出分片内容，并写入新文件
    duplicate_temp = " - 副本"
    task = request.args.get("task_id")  # 获取文件的唯一标识符
    task_id = request.args.get("task_id", "default")[-5:]  # 任务随机id，Android端上传图片使用
    target_filename = request.args.get("filename", f"android_image_{task_id}.png")  # 获取上传文件的文件名
    chunk = 0  # 分片序号
    path = upload.format(target_filename)
    # 如果文件名存在，文件命名增加 - 副本 文字
    if os.path.isfile(path):
        for n in range(100):
            if n == 0:
                duplicate_str = duplicate_temp
            else:
                duplicate_str = f"{duplicate_temp}（{n}）"
            file_name_list = target_filename.split(".")
            new_filename = f"{file_name_list[0]}{duplicate_str}.{file_name_list[-1]}"
            path = upload.format(new_filename)
            if not os.path.isfile(path):
                break

    with open(path, "wb") as target_file:  # 创建新文件
        while True:
            try:
                filename = upload.format("{}{}".format(task, chunk))
                source_file = open(filename, "rb")  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break
            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间

    return render_template("./index_new.html")


@transfer.route("/file/list", methods=["GET"])
def file_list():
    folder = request.args.get("folder", "")
    pre_folder = request.args.get("pre_folder")
    # 获取上传路劲以下子路径
    base_path = upload.replace("\\", "/").format("")
    if pre_folder:
        folder_list = pre_folder.replace(base_path, "").split("/")
        try:
            folder = folder_list[-2]
        except Exception as e:
            folder = ""
    path = upload.format(folder)
    if folder and not Path(path).exists():
        path = upload.format("")
    path = path.replace("\\", "/")
    # 获取文件目录
    files = get_file_and_folder(path)
    upload_path = upload.format("").replace("\\", "/")
    return render_template("./list_new.html", files=files, path=path, folder=folder, upload_path=upload_path)


@transfer.route("/file/download/<filename>", methods=["GET"])
def file_download(filename):
    def send_chunk():  # 流式读取
        store_path = upload.format(filename)
        with open(store_path, "rb") as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type="application/octet-stream")


@transfer.route("/webchat/", methods=["GET"])
def get_webchat():
    return render_template("./webchat.html", ws_url=Config.global_inner_ip, ws_port=Config.global_port)


