from mongoengine import DoesNotExist

from app.model import MongoMessage


class MongoMessageRepository:

    @classmethod
    def save_message(cls, message: MongoMessage):
        message.save()

    @classmethod
    def get_messages(cls):
        return MongoMessage.objects.all()

    @classmethod
    def get_message_by_id(cls, message_id: str):
        try:
            return MongoMessage.objects.get(id=message_id)
        except DoesNotExist:
            return None

    @classmethod
    def get_messages_by_conversation_id(cls, conversation_id: str):
        return MongoMessage.objects(conversacion_id=conversation_id)

    @classmethod
    def to_json(cls, message: MongoMessage):
        grade_map = {
            0: "Sin calificar",
            1: "Satisfactoria",
            2: "No satisfactoria",
            3: "Sugerencia"
        }
        return {
            "asked_question": message.asked_question,
            "question_answer": message.question_answer,
            "intent": message.intent,
            "grade": grade_map.get(message.grade, "Sin calificar"),
            "creation_datetime": message.creation_datetime.isoformat(),
            "conversation_id": str(message.conversation_id.id)
        }

    @classmethod
    def all_messages_to_json(cls):
        messages = cls.get_messages()
        return [cls.to_json(message) for message in messages]

    @classmethod
    def messages_by_conversation_id_to_json(cls, conversation_id: str):
        messages = cls.get_messages_by_conversation_id(conversation_id)
        return [cls.to_json(message) for message in messages]
