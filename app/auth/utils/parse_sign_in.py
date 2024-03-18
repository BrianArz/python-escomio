# Packages
import json

# Local files
from ..models.sign_in_response import SignInResponse


def parse_sign_in(response: json) -> SignInResponse:
    """
    Parses Firebase SingIn response

    :param response: Firebase response
    :return: SignInResponse object
    """
    try:
        expires_in = response.get('expiresIn')
        refresh_token = response.get('refreshToken')

        return SignInResponse(expires_in, refresh_token)

    except json.JSONDecodeError:
        pass
