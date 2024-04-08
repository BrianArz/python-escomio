import json
import os
from flask import Blueprint, jsonify

# Defining the blueprint
health_bp = Blueprint('health_bp', __name__)


# Check the FLASK_ENV environment variable
flask_env = os.getenv('FLASK_ENV', 'development')  # Default to 'development' if not set


@health_bp.route('/hello')
def hello():
    return jsonify('Hello World!'), 200


@health_bp.route('/get-environment')
def get_environment():
    return jsonify({'message': flask_env}), 200


@health_bp.route('/get-version')
def get_version():
    try:
        with open('version_info.txt', 'r') as file:
            version_info = file.read()
        return jsonify({'message': version_info})
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Could not read version information from file: {str(e)}'})
