class TestQuestion:
    sender: str
    message: str

    def __init__(self, sender: str, message: str) -> None:
        self.sender = sender
        self.message = message
