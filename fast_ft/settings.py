import os


class Config(object):
    DEBUG = False
    TESTING = True
    global_inner_ip = "127.0.0.1"
    global_port = 5000
    user_socket_dict = dict()
    socket_server = None
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gjr39dkjn344_!58#'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

