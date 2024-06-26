from app.model import MongoConversation, CreateConversationResponse, GetConversationMessagesResponse, GetConversationsResponse
from app.respository import MongoUserRepository, MongoConversationRepository
from app.core import MessageBo


class ConversationBo:

    @staticmethod
    def create_conversation(uid: str, asked_question: str, question_answer: str, intent: str):

        user = MongoUserRepository.get_user_by_uid(uid)
        if not user:
            raise ValueError("Usuario no encontrado")

        conversation_name = asked_question
        if len(conversation_name) > 22:
            conversation_name = conversation_name[:22]
        conversation_name = conversation_name + "..."

        conversation = MongoConversation(
            user=user,
            name=conversation_name
        )
        MongoConversationRepository.save_conversation(conversation)

        message = MessageBo.create_message(asked_question, question_answer, intent, conversation.id)
        conversation.messages.append(message)
        MongoConversationRepository.save_conversation(conversation)

        return CreateConversationResponse(str(message.id), str(conversation.id), conversation.name, question_answer)

    @staticmethod
    def add_message_to_conversation(conversation_id: str, user_id: str, asked_question: str, question_answer: str, intent: str):

        user = MongoUserRepository.get_user_by_uid(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        conversation = MongoConversationRepository.get_conversation_by_id_and_user(conversation_id, user)
        if not conversation:
            raise ValueError("Conversación no encontrada")

        message = MessageBo.create_message(asked_question, question_answer, intent, conversation.id)
        conversation.messages.append(message)
        MongoConversationRepository.save_conversation(conversation)

        return CreateConversationResponse(str(message.id), str(conversation.id), conversation.name, question_answer)

    @staticmethod
    def update_conversation_name(conversation_id: str, user_id: str, new_name: str):

        user = MongoUserRepository.get_user_by_uid(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        conversation = MongoConversationRepository.get_conversation_by_id_and_user(conversation_id, user)
        if not conversation:
            raise ValueError("Conversación no encontrada")

        conversation.name = new_name
        MongoConversationRepository.save_conversation(conversation)

        return True

    @staticmethod
    def delete_conversation(conversation_id: str, user_id: str):

        user = MongoUserRepository.get_user_by_uid(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        response = MongoConversationRepository.delete_conversation_by_user(conversation_id, user)
        if not response:
            raise ValueError("No se pudo eliminar la conversación")

        return response

    @staticmethod
    def get_conversation_messages(conversation_id: str, user_id: str):

        user = MongoUserRepository.get_user_by_uid(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        response = MongoConversationRepository.get_conversation_messages_by_user(conversation_id, user)
        if not response:
            raise ValueError("No se pudieron obtener los mensajes de la conversación")

        serialized_messages = [MessageBo.serialize_message(message) for message in response]

        return GetConversationMessagesResponse(conversation_id, serialized_messages)

    @staticmethod
    def serialize_conversation(conversation: MongoConversation):
        return {
            "name": conversation.name,
            "id": str(conversation.id)
        }

    @staticmethod
    def get_user_conversations(user_id: str):

        user = MongoUserRepository.get_user_by_uid(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        response = MongoConversationRepository.get_conversations_by_user(user)
        if not response:
            return []

        serialized_conversations = [ConversationBo.serialize_conversation(conversation) for conversation in response]

        return GetConversationsResponse(serialized_conversations)
