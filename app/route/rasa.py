# Packages
from flask import Blueprint, jsonify, request
import requests


# Local files
from app.core import authorize
from app.core import parse_test_question
import app.config as config


# Defines the blueprint
rasa_bp = Blueprint('rasa', __name__)


@rasa_bp.route('/test-question', methods=['POST'])
@authorize
def test_question():
    """
    Asks simple question to rasa server

    :parameter: User name and user question
    :return: Rasa server response
    """

    # Get sender and message from HTTP Request
    sender = request.json.get('sender')
    message = request.json.get('message')

    # Validates empty request body
    if sender is None or message is None:
        return jsonify({'message': 'Missing Information'}), 400

    api_url = f"{config.RASA_URI}:{config.RASA_PORT}/{config.TEST_QUESTION}"

    try:
        response = requests.post(api_url, json={'sender': sender, 'message': message})
        response_json = response.json()

        # Returns first response of request
        question = parse_test_question(response_json[0])

        return jsonify(question.__dict__), 200

    except Exception as error:
        return jsonify({'Internal server error': error}), 500
