from flask import current_app, jsonify


class ExecuteRequest:

    @classmethod
    def execute(cls, service_method, request_object):
        try:
            response = service_method(request_object)
            return response
        except Exception as e:
            current_app.logger.error(f"{service_method.__name__} endpoint failed")
            return jsonify({'message': str(e)}), 500
