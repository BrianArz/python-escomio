class RasaQuestionResponse:
    text: str
    intent: str

    def __init__(self, intent: str, text: str) -> None:
        self.intent = intent
        self.text = text
