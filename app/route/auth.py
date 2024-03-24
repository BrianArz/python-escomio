# Packages
from flask import Blueprint, jsonify, request
from requests.exceptions import HTTPError

# Auth files
from app.core import parse_error, parse_sign_in
from app.service import firebase_service

# Defines the blueprint
auth_bp = Blueprint('auth', __name__)

# Initilizes firebase app
firebase_app = firebase_service.init_firebase()
firebase_auth = firebase_app.auth()


@auth_bp.route('/sign-in-with-email-and-password', methods=['POST'])
def login():
    """
    Signs into FirebaseAuth with user credentials

    :parameter: User email and password
    :return: SignInResponse object
    """
    # Get email and password from HTTP Request
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        response = parse_sign_in(
            firebase_auth.sign_in_with_email_and_password(
                email, password
            )
        )
        return jsonify(response.__dict__), 200

    except HTTPError as error:
        error_data = parse_error(error.strerror)

        if error_data is None:
            return jsonify({'Internal server error': error.strerror}), 500

        return jsonify({'message': error_data.message}), 400


@auth_bp.route('/sign-up', methods=['POST'])
def sign_up():
    """
    Creates a new user in FirebaseAuth with email and password

    :parameter: User email and password
    :return: SignInResponse object
    """
    # Get email and password from HTTP Request
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        user = firebase_auth.create_user_with_email_and_password(email, password)
        # If successful, let's also sign in the user and return the token and expires
        response = parse_sign_in(firebase_auth.sign_in_with_email_and_password(email, password))
        return jsonify(response.__dict__), 200

    except HTTPError as error:
        error_data = parse_error(error.strerror)

        if error_data is None:
            return jsonify({'Internal server error': error.strerror}), 500

        return jsonify({'message': error_data.message}), 400
