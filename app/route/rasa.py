from flask import Blueprint, make_response, request

from app.core import authorize, EndpointValidators, ChatBo

rasa_bp = Blueprint('rasa', __name__)


@rasa_bp.route('/create-conversation', methods=['POST'])
@authorize
def create_conversation():
    information, error_response, status_code = EndpointValidators.validate_rasa_question(request)

    if error_response:
        return error_response, status_code

    response = ChatBo.start_chat(information)
    return make_response(response)


@rasa_bp.route('/add-message-to-conversation', methods=['PUT'])
@authorize
def add_message_to_conversation():
    information, error_response, status_code = EndpointValidators.validate_rasa_add_question(request)

    if error_response:
        return error_response, status_code

    response = ChatBo.add_message_to_conversation(information)
    return make_response(response)


@rasa_bp.route('/update-conversation-name', methods=['PUT'])
@authorize
def update_conversation_name():
    information, error_response, status_code = EndpointValidators.validate_update_conversation_name(request)

    if error_response:
        return error_response, status_code

    response = ChatBo.update_conversation_name(information)
    return make_response(response)


@rasa_bp.route('/delete-conversation', methods=['DELETE'])
@authorize
def delete_conversation():
    information, error_response, status_code = EndpointValidators.validate_conversation_id_request(request)

    if error_response:
        return error_response, status_code

    response = ChatBo.delete_conversation(information)
    return make_response(response)


@rasa_bp.route('/get-conversation_messages', methods=['GET'])
def get_conversation_messages():
    information, error_response, status_code = EndpointValidators.validate_conversation_id_request(request)

    if error_response:
        return error_response, status_code

    response = ChatBo.get_conversation_messages(information)
    return make_response(response)


@rasa_bp.route('/update-message-grade', methods=['PUT'])
def update_message_grade():
    information, error_response, status_code = EndpointValidators.validate_update_message_grade(request)

    if error_response:
        return error_response, status_code

    response = ChatBo.update_message_grade(information)
    return make_response(response)
