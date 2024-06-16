from .message_id_request import MessageIdRequest


class UpdateMessageGradeRequest(MessageIdRequest):
    new_grade: int

    def __init__(self, conversation_id: str, sender: str, message_id: str, new_grade) -> None:
        super().__init__(conversation_id, sender, message_id)
        self.new_grade = new_grade

