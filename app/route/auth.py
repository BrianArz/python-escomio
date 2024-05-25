# Packages
from flask import Blueprint, jsonify, request
from requests.exceptions import HTTPError

# Local files
from app.core import parse_error, parse_sign_in
from app.service import FirebaseService
from app.core import authorize

# Defines the blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign-in', methods=['POST'])
def login():
    """
    Signs into FirebaseAuth with user credentials

    :parameter: User email and password
    :return: SignInResponse object
    """

    # Get firebase app instance
    firebase_auth = FirebaseService.get_firebase_auth()

    # Get email and password from HTTP Request
    email = request.json.get('email')
    password = request.json.get('password')

    # Validates empty request body
    if email is None or password is None:
        return jsonify({'message': 'Missing Credentials'}), 400

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

    # Get firebase app instance
    firebase_auth = FirebaseService.get_firebase_auth()

    # Get email and password from HTTP Request
    email = request.json.get('email')
    password = request.json.get('password')

    # Validates empty request body
    if email is None or password is None:
        return jsonify({'message': 'Missing Credentials'}), 400

    try:
        response = parse_sign_in(
            firebase_auth.create_user_with_email_and_password(
                email, password
            )
        )

        return jsonify(response.__dict__), 200

    except HTTPError as error:
        error_data = parse_error(error.strerror)

        if error_data is None:
            return jsonify({'Internal server error': error.strerror}), 500

        return jsonify({'message': error_data.message}), 400


@auth_bp.route('/authorized-hello-world', methods=['GET'])
@authorize
def authorized_welcome():
    return jsonify({'message': 'This is an authorized Hello World!'}), 200
