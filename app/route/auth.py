# Packages
from flask import current_app, Blueprint, jsonify
from requests.exceptions import HTTPError


# Auth files
from app.core import parse_error, parse_sign_in
from app.service import firebase_service

# Defines the blueprint
auth_bp = Blueprint('auth', __name__)

# Initilizes firebase app
firebase_app = firebase_service.init_firebase()
firebase_auth = firebase_app.auth()


@auth_bp.route('/sign-in-with-email-and-password', methods=['GET'])
def login():
    """
    Signs into FirebaseAuth with user credentials

    TODO: Get email and password from HTTP Request
    :parameter:

    :return:
    """

    try:
        response = parse_sign_in(
            firebase_auth.sign_in_with_email_and_password(
                current_app.config['EXAMPLE_EMAIL'], current_app.config['EXAMPLE_PASSWORD']
            )
        )
        return jsonify(response.__dict__), 200

    except HTTPError as error:
        error_data = parse_error(error.strerror)

        if error_data is None:
            return jsonify({'Internal server error': error.strerror}), 500

        return jsonify({'message': error_data.message}), 400
