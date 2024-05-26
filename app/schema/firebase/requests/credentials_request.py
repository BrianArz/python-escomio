class FirebaseCredentialsRequest:
    email: str
    password: str

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
