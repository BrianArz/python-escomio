# Packages
from flask import Flask
from flask_cors import CORS
import os

# Local files
from app.route import health_bp, auth_bp, rasa_bp
from .service.firebase import firebase_service

firebase_app = None
firebase_admin = None


def create_firebase_app():
    global firebase_app
    if firebase_app is None:
        firebase_app = firebase_service.init_firebase()
    return firebase_app


def create_firebase_admin():
    global firebase_admin
    if firebase_admin is None:
        firebase_admin = firebase_service.init_firebase_admin()


def create_app():
    flask_app = Flask(__name__, instance_relative_config=True)

    # This allows access from any origin. To restrict to certain domain replace "*" with url
    CORS(flask_app)
    flask_app.config['CORS_HEADERS'] = 'Content-Type'

    # Get environment, if not defined 'development' will be default
    environment = os.getenv('FLASK_ENV', 'development')

    # App configuration
    if environment == 'production':
        flask_app.config.from_pyfile('production_config.py', silent=True)
    else:
        flask_app.config.from_pyfile('development_config.py', silent=True)

    # Blueprints registry
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')
    flask_app.register_blueprint(health_bp, url_prefix='/health')
    flask_app.register_blueprint(rasa_bp, url_prefix='/rasa')

    # Initializes firebase application
    create_firebase_app()

    # Initializes firebase admin app
    create_firebase_admin()

    return flask_app
