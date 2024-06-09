from flask import Blueprint, jsonify, request, make_response

from app.service import FirebaseService
from app.core import authorize, EndpointValidators, ExecuteRequest
from app.respository import RedisRepository

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


@authorize
@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    """
    Deletes user from cache
    """
    uid = request.cookies.get('X-Uid', None)
    RedisRepository.delete_user(uid)

    return make_response("", 200)


@auth_bp.route('/authorized-hello-world', methods=['GET'])
@authorize
def authorized_welcome():
    return jsonify({'message': 'This is an authorized Hello World!'}), 200
