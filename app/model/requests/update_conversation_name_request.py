class UpdateConversationNameRequest:
    sender: str
    new_name: str
    conversation_id: str

    def __init__(self, sender, new_name, conversation_id):
        self.sender = sender
        self.new_name = new_name
        self.conversation_id = conversation_id
