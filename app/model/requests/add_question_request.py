from app.service.rasa_service import RasaAskRequest


class AddQuestionRequest(RasaAskRequest):
    conversation_id: str

    def __init__(self, sender: str, message: str, conversation_id: str):
        super().__init__(sender, message)
        self.conversation_id = conversation_id

