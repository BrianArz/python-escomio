from .add_message_response import AddMessageResponse


class CreateConversationResponse(AddMessageResponse):
    conversation_id: str
    conversation_name: str
    response: str

    def __init__(self, message_id: str, conversation_id: str, conversation_name: str, response: str):
        super().__init__(message_id)
        self.conversation_id = conversation_id
        self.conversation_name = conversation_name
        self.response = response
