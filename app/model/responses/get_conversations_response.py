from typing import List


class GetConversationsResponse:

    def __init__(self, conversations: List['ConversationInfo']):
        self.conversations = conversations

    class ConversationInfo:
        def __init__(self, conversation_id: str, conversation_name: str):
            self.conversation_id = conversation_id
            self.conversation_name = conversation_name

