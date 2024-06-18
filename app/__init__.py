import os

from flask import Flask
from flask_cors import CORS

# Local files
from app.route import health_bp, auth_bp, rasa_bp, admin_bp
from app.service import FirebaseService
from app.connection import RedisConnection, MongoDbConnection
from app.respository import initialize_database
from app.logger import configure_logging

# Global variables
firebase_app = None
firebase_admin = None
redis_connection = None


def create_app():

    # Initializes the Flask application
    app = Flask(__name__, instance_relative_config=True)

    try:
        # This allows access from any localhost domain and subdomain.
        CORS(app, supports_credentials=True, origins=["http://localhost:4200"], methods=["GET", "POST", "PUT", "DELETE", "PATCH"])

        @app.after_request
        def after_request(response):
            if response.headers.get('Access-Control-Allow-Headers'):
                return response
            else:
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, XCSRF-Token')
            return response

        # Configuration loading
        environment = os.getenv('FLASK_ENV', 'development')
        app.config.from_pyfile(f'{environment}_config.py', silent=True)

        # Blueprints registry
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(health_bp, url_prefix='/health')
        app.register_blueprint(rasa_bp, url_prefix='/rasa')
        app.register_blueprint(admin_bp, url_prefix='/admin')

        # Activates all level logging
        configure_logging(app)

        with app.app_context():
            # Initializes firebase services
            FirebaseService.init_app(app)
            # Initializes redis connection
            initialize_database(RedisConnection.init_connection())
            # Initializes mongo connection
            MongoDbConnection.init_connection()

        return app

    except Exception as e:
        app.logger.error(f"Unable to create flask application: {e}")
        raise Exception("Flask services are unavailable") from e
