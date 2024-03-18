from flask import Flask
from .auth import auth_routes as auth
from .health import health_routes as health


def create_app(config_name):
    flask_app = Flask(__name__, instance_relative_config=True)

    # App configuration
    flask_app.config.from_pyfile('config.py', silent=True)

    # Blueprints registry
    flask_app.register_blueprint(auth.auth_bp, url_prefix='/auth')
    flask_app.register_blueprint(health.health_bp, url_prefix='/health')

    return flask_app
