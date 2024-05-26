# Packages
from typing import List


class ErrorElement:
    domain: str
    message: str
    reason: str

    def __init__(self, domain: str, message: str, reason: str) -> None:
        self.domain = domain
        self.message = message
        self.reason = reason


class FirebaseErrorResponse:
    code: int
    errors: List[ErrorElement]
    message: str

    def __init__(self, code: int, errors: List[ErrorElement], message: str) -> None:
        self.code = code
        self.errors = errors
        self.message = message
