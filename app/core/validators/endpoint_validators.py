from flask import jsonify

from app.schema import RasaAskRequest, FirebaseCredentialsRequest


class EndpointValidators:

    @classmethod
    def validate_user_credentials(cls, request):
        """
        Validates the presence of email and password in the request.
        """
        email = request.json.get('email')
        password = request.json.get('password')
        if not email or not password:
            return None, jsonify({'message': 'Missing Credentials'}), 400
        return FirebaseCredentialsRequest(email, password), None, None

    @classmethod
    def validate_rasa_question(cls, request):
        """
        Validates the presence of sender and message in the request.
        """
        sender = request.json.get('sender')
        message = request.json.get('message')
        if not sender or not message:
            return None, jsonify({'message': 'Missing Information'}), 400
        return RasaAskRequest(sender, message), None, None
