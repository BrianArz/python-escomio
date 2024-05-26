class FirebaseSignInResponse:
    expires_in: str
    refresh_token: str
    id_token: str
    uid: str

    def __init__(self, expires_in: str, refresh_token: str, id_token: str, uid: str) -> None:
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.uid = uid
