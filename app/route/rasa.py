from flask import Blueprint, jsonify, request

from app.core import authorize, EndpointValidators, ExecuteRequest
from app.service import RasaService

rasa_bp = Blueprint('rasa', __name__)


@rasa_bp.route('/ask-question', methods=['POST'])
@authorize
def test_question():
    information, error_response, status_code = EndpointValidators.validate_rasa_question(request)

    if error_response:
        return error_response, status_code

    return ExecuteRequest.execute(RasaService.ask_question, information)


