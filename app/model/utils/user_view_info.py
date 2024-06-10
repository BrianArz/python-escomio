class UserViewInfo:
    def __init__(self, username: str, role: int):
        self.username = username
        self.role = role
        self.expires_in = None

    def set_expires_in(self, expires_in: str):
        self.expires_in = expires_in
