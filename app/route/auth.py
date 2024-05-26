from flask import Blueprint, jsonify, request

from app.service import FirebaseService
from app.core import authorize, EndpointValidators, ExecuteRequest

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign-in', methods=['POST'])
def login():
    """
    Signs into FirebaseAuth with user credentials
    """
    credentials, error_response, status_code = EndpointValidators.validate_user_credentials(request)
    if error_response:
        return error_response, status_code

    return ExecuteRequest.execute(FirebaseService.sign_in, credentials)


@auth_bp.route('/sign-up', methods=['POST'])
def sign_up():
    """
    Creates a new user in FirebaseAuth with email and password
    """
    credentials, error_response, status_code = EndpointValidators.validate_user_credentials(request)
    if error_response:
        return error_response, status_code

    return ExecuteRequest.execute(FirebaseService.sign_up, credentials)


@auth_bp.route('/authorized-hello-world', methods=['GET'])
@authorize
def authorized_welcome():
    return jsonify({'message': 'This is an authorized Hello World!'}), 200
