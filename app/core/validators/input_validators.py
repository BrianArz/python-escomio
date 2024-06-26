import re


class InputValidators:

    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
        if re.match(email_regex, email):
            return True
        return False

    @staticmethod
    def is_valid_string(s: str, min_length: int = None, max_length: int = None, regex: str = None) -> bool:
        if min_length is not None and len(s) < min_length:
            return False
        if max_length is not None and len(s) > max_length:
            return False
        if regex is not None and not re.match(regex, s):
            return False
        return True
