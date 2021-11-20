from flask import request
from flask_socketio import Namespace, emit
from urllib.parse import unquote

# from create_app import socket_server
from settings import Config
from utils.get_ip import get_ip
from utils.replace_special_chart import replace_special_chart

# from server import socket_server
from fast_ft import socket_server

user_socket_dict = Config.user_socket_dict


class MyCustomNamespace(Namespace):
    user_ip = ""

    def on_connect(self):
        sid = getattr(request, "sid")
        self.get_user_ip()
        if self.user_ip not in user_socket_dict.keys():
            user_socket_dict[self.user_ip] = {sid}
        else:
            user_socket_dict[self.user_ip].add(sid)
        res_dict = {"chat_people": len(user_socket_dict.keys()), "is_update": True}
        self.emit("response", res_dict)
        print("【客户端连接】".center(50, "#"))
        print("当前socket列表长度：{}；\n客户端ip：{}；\nsid:{}。".format(len(user_socket_dict.keys()), self.user_ip, sid))
        print()

    def on_disconnect(self):
        self.get_user_ip()
        sid = getattr(request, "sid")
        print("【客户端断开】".center(50, "#"))
        print("【断开】当前socket列表长度：{}；\n客户端ip：{}；\nsid:{}。".format(len(user_socket_dict.keys()), self.user_ip, sid))
        print()
        if self.user_ip in user_socket_dict.keys():
            user_socket_dict[self.user_ip].remove(sid)
            if not len(user_socket_dict[self.user_ip]):
                del user_socket_dict[self.user_ip]
        res_dict = {"chat_people": len(user_socket_dict.keys()), "is_update": True}
        self.emit("response", res_dict)

    def on_message(self, data):
        sid = getattr(request, "sid")
        msg = unquote(data.get("message"))
        nick_name = data.get("nick_name")
        self.get_user_ip()
        print("【客户端消息】".center(50, "#"))
        print("客户端ip：{}；\n客户端消息：{}。".format(self.user_ip, msg))
        print()
        msg = replace_special_chart(msg)
        res_dict = {
            "message": msg, "ip": self.user_ip, "nick_name": nick_name, "chat_people": len(user_socket_dict.keys()),
            "is_update": False
        }
        for user_ip, room_list in user_socket_dict.items():
            for room_id in room_list:
                if user_ip == self.user_ip:
                    res_dict["is_mine"] = True
                else:
                    res_dict["is_mine"] = False
                self.emit("message", res_dict, room_id)

    def get_user_ip(self):
        """ 获取用户ip """
        self.user_ip = get_ip(request)
        return


socket_server.on_namespace(MyCustomNamespace("/chat"))

