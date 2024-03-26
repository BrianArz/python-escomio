class TestQuestionResponse:
    recipient_id: str
    text: str

    def __init__(self, recipient_id: str, text: str) -> None:
        self.recipient_id = recipient_id
        self.text = text
