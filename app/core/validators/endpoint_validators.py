from flask import jsonify

from app.schema import RasaAskRequest, FirebaseCredentialsRequest
from app.model import CreateAccountRequest, AddQuestionRequest, UpdateConversationNameRequest, ConversationIdRequest, MessageIdRequest
from .input_validators import InputValidators
from ...model.requests.update_message_grade_request import UpdateMessageGradeRequest


class EndpointValidators:

    mongo_id_regex = r"^[a-fA-F0-9]{24}$"
    username_regex = r'^[a-zA-Z0-9_]+$'
    number_regex = r'^[0-9]*$'
    conversation_name_regex = r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]+$'

    @classmethod
    def validate_user_credentials(cls, request):
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return None, jsonify({'message': 'Credenciales faltantes'}), 400

        if not InputValidators.is_valid_email(email):
            return None, jsonify({'message': 'Correo electrónico inválido'}), 400

        if not InputValidators.is_valid_string(password, 8):
            return None, jsonify({'message': 'Contraseña inválida'}), 400

        return FirebaseCredentialsRequest(email, password), None, None

    @classmethod
    def validate_sign_up(cls, request):
        username = request.json.get('username')
        escom_id = request.json.get('escom_id')
        email = request.json.get('email')
        password = request.json.get('password')

        if not username or not escom_id or not email or not password:
            return None, jsonify({'message': 'Petición incompleta'}), 400

        if not InputValidators.is_valid_string(username, 8, 15, cls.username_regex):
            return None, jsonify({'message': 'Nombre de usuario inválido'}), 400

        if not InputValidators.is_valid_string(escom_id, 8, 15, cls.number_regex):
            return None, jsonify({'message': 'Número de boleta inválido'}), 400

        if not InputValidators.is_valid_email(email):
            return None, jsonify({'message': 'Correo electrónico inválido'}), 400

        if not InputValidators.is_valid_string(password, 8):
            return None, jsonify({'message': 'Contraseña inválida'}), 400

        return CreateAccountRequest(username, escom_id, email, password), None, None
    
    @classmethod
    def validate_rasa_question(cls, request):
        sender = request.cookies.get('X-Uid', None)
        message = request.json.get('question')

        if not sender or not message:
            return None, jsonify({'message': 'Información faltante'}), 400

        if not InputValidators.is_valid_string(sender, 5, 100):
            return None, jsonify({'message': 'Identificador inválido'}), 400

        if not InputValidators.is_valid_string(message, None, 300):
            return None, jsonify({'message': 'Pregunta inválida'}), 400

        return RasaAskRequest(sender, message), None, None

    @classmethod
    def validate_rasa_add_question(cls, request):
        sender = request.cookies.get('X-Uid', None)
        message = request.json.get('question')
        conversation_id = request.json.get('conversation_id')

        if not sender or not message or not conversation_id:
            return None, jsonify({'message': 'Información faltante'}), 400

        if not InputValidators.is_valid_string(sender, 5, 100):
            return None, jsonify({'message': 'Identificador inválido'}), 400

        if not InputValidators.is_valid_string(message, None, 300):
            return None, jsonify({'message': 'Pregunta inválida inválido'}), 400

        if not InputValidators.is_valid_string(conversation_id, 5, 24, cls.mongo_id_regex):
            return None, jsonify({'message': 'Identificador de conversación inválido'}), 400

        return AddQuestionRequest(sender, message, conversation_id), None, None

    @classmethod
    def validate_update_conversation_name(cls, request):
        sender = request.cookies.get('X-Uid', None)
        new_name = request.json.get('new_name')
        conversation_id = request.json.get('conversation_id')

        if not sender or not new_name or not conversation_id:
            return None, jsonify({'message': 'Información faltante'}), 400

        if not InputValidators.is_valid_string(sender, 5, 100):
            return None, jsonify({'message': 'Identificador inválido'}), 400

        if not InputValidators.is_valid_string(new_name, 1, 25, cls.conversation_name_regex):
            return None, jsonify({'message': 'Nombre de conversación inválido'}), 400

        if not InputValidators.is_valid_string(conversation_id, 5, 24, cls.mongo_id_regex):
            return None, jsonify({'message': 'Identificador de conversación inválido'}), 400

        return UpdateConversationNameRequest(sender, new_name, conversation_id), None, None

    @classmethod
    def validate_conversation_id_request(cls, request):
        sender = request.cookies.get('X-Uid', None)
        conversation_id = request.json.get('conversation_id')

        if not sender or not conversation_id:
            return None, jsonify({'message': 'Información faltante'}), 400

        if not InputValidators.is_valid_string(conversation_id, 5, 24, cls.mongo_id_regex):
            return None, jsonify({'message:' 'Identificador de conversación inválido'}), 400

        if not InputValidators.is_valid_string(sender, 5, 100):
            return None, jsonify({'message:': 'Identificador inválido'})

        return ConversationIdRequest(conversation_id, sender), None, None

    @classmethod
    def validate_message_id_request(cls, request):
        conversation_id_request, error_response, status_code = cls.validate_conversation_id_request(request)

        if error_response:
            return error_response, status_code

        message_id = request.json.get('message_id')

        if not InputValidators.is_valid_string(message_id, 5, 24, cls.mongo_id_regex):
            return None, jsonify({'message': 'Identificador de mensaje inválido'}), 400

        return MessageIdRequest(conversation_id_request.conversation_id, conversation_id_request.sender, message_id), None, None

    @classmethod
    def validate_update_message_grade(cls, request):
        message_id_request, error_response, status_code = cls.validate_message_id_request(request)

        if error_response:
            return error_response, status_code

        new_grade = request.json.get('new_grade')
        if not InputValidators.is_valid_string(new_grade, 1, 1, cls.number_regex):
            return None, jsonify({'message': 'Nueva calificación inválida'}), 400

        return UpdateMessageGradeRequest(message_id_request.conversation_id, message_id_request.sender, message_id_request.message_id, new_grade), None, None
