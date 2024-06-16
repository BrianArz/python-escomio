from .conversation_id_request import ConversationIdRequest


class MessageIdRequest(ConversationIdRequest):
    message_id: str

    def __init__(self, conversation_id: str, sender: str, message_id: str):
        super().__init__(conversation_id, sender)
        self.message_id = message_id
