from .conversation_id_request import ConversationIdRequest


class GetConversationMessagesRequest(ConversationIdRequest):

    def __init__(self, conversation_id: str, sender: str) -> None:
        super().__init__(conversation_id, sender)
