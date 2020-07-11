from flask import Flask, render_template
from app.views import config_blueprint
from app.config import config
from app.extensions import config_extensions

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    config_blueprint(app)
    config_extensions(app)
    return app
