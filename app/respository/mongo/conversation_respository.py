from mongoengine import DoesNotExist

from app.model import MongoConversation, MongoUser, MongoMessage


class MongoConversationRepository:

    @classmethod
    def save_conversation(cls, conversation: MongoConversation):
        conversation.save()

    @classmethod
    def get_conversations_by_user(cls, user: MongoUser):
        try:
            conversations = MongoConversation.objects(user=user)
            return conversations
        except DoesNotExist:
            return []

    @classmethod
    def get_conversation_by_id(cls, conversation_id: str):
        try:
            conversation = MongoConversation.objects.get(id=conversation_id)
            return conversation
        except DoesNotExist:
            return None

    @classmethod
    def get_conversation_by_id_and_user(cls, conversation_id: str, user: MongoUser):
        try:
            conversation = MongoConversation.objects.get(id=conversation_id, user=user)
            return conversation
        except DoesNotExist:
            return None

    @classmethod
    def delete_conversation_by_user(cls, conversation_id: str, user: MongoUser):
        try:
            conversation = cls.get_conversation_by_id_and_user(conversation_id, user)

            if conversation is None:
                return False

            MongoMessage.objects(conversation_id=conversation_id).delete()
            conversation.delete()
            return True

        except DoesNotExist:
            return False

    @classmethod
    def get_conversation_messages_by_user(cls, conversation_id: str, user: MongoUser):
        try:
            conversation = cls.get_conversation_by_id_and_user(conversation_id, user)
            if conversation is None:
                return []

            messages = MongoMessage.objects(conversation_id=conversation_id)
            return messages

        except DoesNotExist:
            return []
