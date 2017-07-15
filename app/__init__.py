from flask import Flask
from flask_socketio import SocketIO
from flask_session import Session
from flask_cors import CORS


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
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "supports_credentials": True
        }
    })

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
