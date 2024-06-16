class DeleteConversationRequest:
    conversation_id: str
    sender: str

    def __init__(self, conversation_id: str, sender: str):
        self.conversation_id = conversation_id
        self.sender = sender
