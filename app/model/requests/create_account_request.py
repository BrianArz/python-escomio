class CreateAccountRequest:
    username: str
    email: str
    password: str
    escom_id: str

    def __init__(self, username: str, escom_id: str, email: str, password: str) -> None:
        self.username = username
        self.escom_id = escom_id
        self.email = email
        self.password = password
