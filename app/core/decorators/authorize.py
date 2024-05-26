from functools import wraps
from flask import request, jsonify

from firebase_admin import auth


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        bearer_token = request.headers.get('Authorization', None)
        if bearer_token is None:
            return jsonify({'message': 'Unauthorized'}), 401

        # noinspection PyBroadException
        try:
            token = bearer_token.replace('Bearer ', '')
            decoded_token = auth.verify_id_token(token, clock_skew_seconds=0)
            request.user = decoded_token

        except Exception as e:
            return jsonify({'message': 'Unauthorized'}), 401

        return f(*args, **kwargs)

    return decorated_function
