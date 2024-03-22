# Packages
import json

# Local files
from app.schema import FirebaseError


def parse_error(error: str) -> FirebaseError:
    """
    Parses Firebase error string

    :param error: Error string
    :return: FirebaseError object
    """
    try:
        error_json = json.loads(error)

        error_code = error_json.get('error', {}).get('code')
        error_details = error_json.get('error', {}).get('errors')
        error_message = error_json.get('error', {}).get('message')

        return FirebaseError(error_code, error_details, error_message)

    except json.JSONDecodeError:
        pass
