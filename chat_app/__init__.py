import os

from celery import Celery
from flask import Flask
from flask_socketio import SocketIO

BROKER_URI = 'amqp://admin:admin@localhost:5672/local_vhost'


celery = Celery(__name__, broker=BROKER_URI)

socketio = SocketIO()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'chat_app.sqlite'),
    )
    app.config['CELERY_BROKER_URL'] = BROKER_URI
    app.config['CELERY_RESULT_BACKEND'] = BROKER_URI
    celery.conf.update(app.config)

    socketio.init_app(app, debug=True, message_queue=app.config['CELERY_BROKER_URL'])

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import chat
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint='sessions')

    return app
