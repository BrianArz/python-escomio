from flask import Blueprint, jsonify

# Defining the blueprint
health_bp = Blueprint('health_bp', __name__)


@health_bp.route('/hello')
def hello():
    return jsonify('Hello')
