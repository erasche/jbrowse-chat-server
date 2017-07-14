from flask import Flask
from flask_socketio import SocketIO
from flask.ext.session import Session


socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = '!6gjr39dkjn344_7#'
    app.config.update({
        'SESSION_TYPE': 'filesystem'
    })

    Session(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
