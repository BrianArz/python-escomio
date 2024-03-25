# Packages
import json

# Local files
from app.schema import SignInResponse


def parse_sign_in(response: json) -> SignInResponse:
    """
    Parses Firebase SingIn response

    :param response: Firebase response
    :return: SignInResponse object
    """
    try:
        expires_in = response.get('expiresIn')
        refresh_token = response.get('refreshToken')
        id_token = response.get('idToken')

        return SignInResponse(expires_in, refresh_token, id_token)

    except json.JSONDecodeError:
        pass
