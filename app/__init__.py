from flask import Flask
from flask_socketio import SocketIO
from flask.ext.session import Session


socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config.update({
        'SESSION_TYPE': 'filesystem',
        'SECRET_KEY': '!6gjr39dkjn344_7#'
    })

    Session(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
