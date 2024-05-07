from flask import Flask, current_app
from flask_cors import CORS
from redis_om import get_redis_connection
import os

# Local files
from app.route import health_bp, auth_bp, rasa_bp
from .service.firebase import firebase_service

# Global variables
firebase_app = None
firebase_admin = None
redis_connection = None


def create_firebase_app():
    """
    Creates Pyrebase app for singleton import
    :return: pyrebase app instance
    """
    global firebase_app
    if firebase_app is None:
        firebase_app = firebase_service.init_firebase()
    return firebase_app


def create_firebase_admin():
    """
    Initializes firebase admin application
    """
    global firebase_admin
    if firebase_admin is None:
        firebase_admin = firebase_service.init_firebase_admin()


def get_redis():
    """
    Redis connection configuration
    """
    global redis_connection
    if redis_connection is None:
        redis_url = current_app.config.get('REDIS_URL')
        redis_connection = get_redis_connection(url=redis_url)
    return redis_connection


def create_app():
    flask_app = Flask(__name__, instance_relative_config=True)

    # This allows access from any origin. To restrict to certain domain replace "*" with url
    CORS(flask_app)
    flask_app.config['CORS_HEADERS'] = 'Content-Type'

    # Get environment, if not defined 'development' will be default
    environment = os.getenv('FLASK_ENV', 'development')

    # App configuration
    if environment == 'development':
        flask_app.config.from_pyfile('development_config.py', silent=True)
    elif environment == 'docker':
        flask_app.config.from_pyfile('docker_config.py', silent=True)
    else:
        flask_app.config.from_pyfile('production_config.py', silent=True)

    # Blueprints registry
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')
    flask_app.register_blueprint(health_bp, url_prefix='/health')
    flask_app.register_blueprint(rasa_bp, url_prefix='/rasa')

    # Initializes firebase application
    create_firebase_app()

    # Initializes firebase admin app
    create_firebase_admin()

    # Initializes redis
    with flask_app.app_context():
        get_redis()

    return flask_app
