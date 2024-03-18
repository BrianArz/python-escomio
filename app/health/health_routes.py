from flask import current_app, Blueprint, jsonify

# Defining the blueprint
health_bp = Blueprint('health_bp', __name__)


@health_bp.route('/hello')
def hello():
    return jsonify('Hello'), 200


@health_bp.route('/get-environment')
def get_environment():
    return jsonify({'Environment': current_app.config['ENVIRONMENT']}), 200
