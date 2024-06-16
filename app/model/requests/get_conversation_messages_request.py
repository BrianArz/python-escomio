from .delete_conversation_request import DeleteConversationRequest


class GetConversationMessagesRequest(DeleteConversationRequest):

    def __init__(self, conversation_id: str, sender: str) -> None:
        super().__init__(conversation_id, sender)
