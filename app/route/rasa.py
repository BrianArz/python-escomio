# Packages
from flask import Blueprint, jsonify
import requests

# Local files
from app.core import authorize
from app.core import parse_test_question
import app.config as config
from app.schema.rasa.test_question import TestQuestion

# Defines the blueprint
rasa_bp = Blueprint('rasa', __name__)

test_question = TestQuestion('Sender1', 'cual es tu funcion?')


@rasa_bp.route('/test-question', methods=['GET'])
#@authorize
def test_question():
    """
    Asks simple question to rasa server

    :return: Rasa server response
    """

    api_url = f"{config.RASA_URI}:{config.RASA_PORT}/{config.TEST_QUESTION}"

    try:
        response = requests.post(api_url, json=test_question.__dict__)
        response_json = response.json()

        first_response = response_json[0]

        parsed_response = parse_test_question(first_response)
        print(parsed_response.__dict__)

    except Exception as error:
        return jsonify({'Internal server error': error}), 500
