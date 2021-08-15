import os


class Config(object):
    DEBUG = False
    TESTING = True
    global_inner_ip = "127.0.0.1"
    global_port = 5000
    user_socket_set = set()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

