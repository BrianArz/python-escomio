from typing import List

from app.model import MongoMessage


class GetConversationMessagesResponse:
    conversation_id: str
    messages: List[MongoMessage]

    def __init__(self, conversation_id: str, messages: List[MongoMessage]):
        self.conversation_id = conversation_id
        self.messages = messages
