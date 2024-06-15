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
