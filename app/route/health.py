import json

from flask import current_app, Blueprint, jsonify

# Defining the blueprint
health_bp = Blueprint('health_bp', __name__)


@health_bp.route('/hello')
def hello():
    return jsonify('Hello World!'), 200


@health_bp.route('/get-environment')
def get_environment():
    return jsonify({'message': current_app.config['ENVIRONMENT']}), 200


@health_bp.route('/get-version')
def get_version():
    try:
        with open('version_info.txt', 'r') as file:
            version_info = file.read()
        return jsonify({'message': version_info})
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Could not read version information from file: {str(e)}'})
