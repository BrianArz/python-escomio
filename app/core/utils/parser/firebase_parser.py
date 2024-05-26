import json
from flask import current_app

from app.schema import FirebaseSignInResponse, FirebaseErrorResponse


class FirebaseParser:
    @classmethod
    def parse_sign_in(cls, response: json) -> FirebaseSignInResponse:
        """
        Parses Firebase SingIn response
        """
        try:
            expires_in = response.get('expiresIn')
            refresh_token = response.get('refreshToken')
            id_token = response.get('idToken')

            return FirebaseSignInResponse(expires_in, refresh_token, id_token)

        except Exception as e:
            current_app.logger.error(f"Unable to parse response {e}")
            raise Exception(f"Unable to parse response {e}") from e

    @classmethod
    def parse_error(cls, error: str) -> FirebaseErrorResponse:
        """
        Parses Firebase error string
        """
        try:
            error_json = json.loads(error)

            error_code = error_json.get('error', {}).get('code')
            error_details = error_json.get('error', {}).get('errors')
            error_message = error_json.get('error', {}).get('message')

            return FirebaseErrorResponse(error_code, error_details, error_message)

        except Exception as e:
            current_app.logger.error(f"Unable to parse error response {e}")
            return FirebaseErrorResponse(500, [], "Unable to parse error response")
