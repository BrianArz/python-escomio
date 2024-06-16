from datetime import datetime, timezone

from app.model import MongoMessage
from app.respository import MongoMessageRepository


class MessageBo:

    @staticmethod
    def create_message(asked_question: str, question_answer: str, intent: str, conversation_id: str) -> MongoMessage:
        message = MongoMessage(
            asked_question=asked_question,
            question_answer=question_answer,
            intent=intent,
            grade=0,
            creation_datetime=datetime.now(timezone.utc),
            conversation_id=conversation_id
        )
        MongoMessageRepository.save_message(message)
        return message

    @staticmethod
    def update_grade(message_id: str, new_grade: int):
        message = MongoMessageRepository.get_message_by_id(message_id)

        if not message:
            raise ValueError("Message not found")

        message.grade = new_grade
        MongoMessageRepository.save_message(message)
        return True

    @staticmethod
    def serialize_message(message: MongoMessage):
        return {
            "asked_question": message.asked_question,
            "question_answer": message.question_answer,
            "grade": message.grade,
            "creation_datetime": message.creation_datetime.isoformat(),
            "conversation_id": str(message.conversation_id.id)
        }
