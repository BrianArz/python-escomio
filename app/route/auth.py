from flask import Blueprint, jsonify, request, make_response

from app.service import FirebaseService
from app.core import authorize, EndpointValidators, ExecuteRequest
from app.respository import RedisRepository

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign-in', methods=['POST'])
def login():

    credentials, error_response, status_code = EndpointValidators.validate_user_credentials(request)
    if error_response:
        return error_response, status_code

    return ExecuteRequest.execute(FirebaseService.sign_in, credentials)


@auth_bp.route('/sign-up', methods=['POST'])
def sign_up():

    try:
        sign_up_data, error_response, status_code = EndpointValidators.validate_sign_up(request)
        if error_response:
            return error_response, status_code

        return ExecuteRequest.execute(FirebaseService.sign_up, sign_up_data)

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@auth_bp.route('/logout', methods=['DELETE'])
@authorize
def logout():

    uid = request.cookies.get('X-Uid', None)    
    RedisRepository.delete_user(uid)

    return make_response("", 200)


@auth_bp.route('/refresh_token', methods=['PATCH'])
@authorize
def refresh_token():

    try:
        token = request.cookies.get('X-Refresh-Token', None)

        if token is None:
            return make_response(jsonify({'message': 'Token de actualización inválido'})), 400

        return ExecuteRequest.execute(FirebaseService.refresh_token, token)

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@auth_bp.route('/authorized-hello-world', methods=['GET'])
@authorize
def authorized_welcome():

    return jsonify({'message': 'This is an authorized Hello World!'}), 200
