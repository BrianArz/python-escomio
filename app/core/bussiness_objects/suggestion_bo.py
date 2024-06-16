from datetime import datetime, timezone

from app.respository import MongoUserRepository, MongoConversationRepository, MongoMessageRepository, MongoSuggestionRepository
from app.model import MongoUser, MongoSuggestion


class SuggestionBo:

    @staticmethod
    def create_suggestion(suggested_by: MongoUser, suggested_by_user_role: int, suggested_question: str, status: int, description: str = ''):
        suggestion = MongoSuggestion(
            suggested_by=suggested_by,
            suggested_by_user_role=suggested_by_user_role,
            suggested_question=suggested_question,
            status=status,
            description=description,
            creation_datetime=datetime.now(timezone.utc)
        )
        MongoSuggestionRepository.save_suggestion(suggestion)
        return suggestion

    @staticmethod
    def suggest_training_by_chat(conversation_id: str, user_id: str, message_id: str):

        user = MongoUserRepository.get_user_by_uid(user_id)
        if not user:
            raise ValueError('Usuario no encontrado')

        conversation = MongoConversationRepository.get_conversation_by_id_and_user(conversation_id, user)
        if not conversation:
            raise ValueError('Conversación no encontrada')

        message = MongoMessageRepository.get_message_by_id(message_id)
        if not message or message not in conversation.messages:
            raise ValueError('Mensaje no encontrado')

        SuggestionBo.create_suggestion(user, user.role, message.asked_question, 0)
        message.grade = 3
        MongoMessageRepository.save_message(message)

        return True
