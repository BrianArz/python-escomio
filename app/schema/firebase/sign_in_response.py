class SignInResponse:
    expires_in: str
    refresh_token: str

    def __init__(self, expires_in: str, refresh_token: str) -> None:
        self.expires_in = expires_in
        self.refresh_token = refresh_token
