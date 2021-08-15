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

    # socket_server.init_app(app)
    return app
