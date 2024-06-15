from app.model import MongoConversation, CreateConversationResponse
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
