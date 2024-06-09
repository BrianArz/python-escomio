from flask import jsonify

from app.schema import RasaAskRequest, FirebaseCredentialsRequest
from app.model import CreateAccountRequest
from .input_validators import InputValidators


class EndpointValidators:

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

        username_regex = r'^[a-zA-Z0-9_]+$'
        if not InputValidators.is_valid_string(username, 8, 15, username_regex):
            return None, jsonify({'message': 'Nombre de usuario inválido'}), 400

        escom_id_regex = r'^[0-9]*$'
        if not InputValidators.is_valid_string(escom_id, 8, 15, escom_id_regex):
            return None, jsonify({'message': 'Número de boleta inválido'}), 400

        if not InputValidators.is_valid_email(email):
            return None, jsonify({'message': 'Correo electrónico inválido'}), 400

        if not InputValidators.is_valid_string(password, 8):
            return None, jsonify({'message': 'Contraseña inválida'}), 400

        return CreateAccountRequest(username, escom_id, email, password), None, None

    @classmethod
    def validate_rasa_question(cls, request):
        sender = request.json.get('sender')
        message = request.json.get('message')
        if not sender or not message:
            return None, jsonify({'message': 'Missing Information'}), 400
        return RasaAskRequest(sender, message), None, None
