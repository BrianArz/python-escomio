from functools import wraps
from flask import request, jsonify, current_app, make_response

from app.respository import RedisRepository


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        """ This function obtains auth data sent through cookies from the client, if something fails we just assume
        the request is not valid and does not come from a trustfully source """

        try:
            access_token = request.cookies.get('X-Access-Token', None)
            uid = request.cookies.get('X-Uid', None)

            if access_token is None or uid is None:
                return make_response(jsonify({'message': 'Unauthorized request'})), 401

            redis_user = RedisRepository.get_user_by_id(uid)

            if redis_user is None or redis_user.id_token != access_token:
                return make_response(jsonify({'message': 'Unauthorized request'})), 401

        except Exception as ex:
            current_app.logger.error(f"Unable to obtain auth cookies information: {ex}")
            return make_response(jsonify({'message': 'Unauthorized request'})), 401

        return f(*args, **kwargs)

    return decorated_function
