from flask import Flask

from .config import Config
from .object import db, ma, mg
from .view import apiv1_bp


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_mapping(config)
    db.init_app(app)
    mg.init_app(app, db)
    ma.init_app(app)
    app.register_blueprint(apiv1_bp)
    return app
