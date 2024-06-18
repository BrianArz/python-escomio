from datetime import datetime, timezone
from flask import jsonify

from app.model import MongoMessage
from app.respository import MongoMessageRepository, MongoUserRepository, MongoConversationRepository
from app.core import RasaParser


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
    def update_message_grade(conversation_id: str, user_id: str, message_id: str, new_grade: int):

        user = MongoUserRepository.get_user_by_uid(user_id)
        if not user:
            raise ValueError("User not found")

        conversation = MongoConversationRepository.get_conversation_by_id_and_user(conversation_id, user)
        if not conversation:
            raise ValueError("Conversación no encontrada")

        message = MongoMessageRepository.get_message_by_id(message_id)
        if not message or message not in conversation.messages:
            raise ValueError("Mensaje no encontrado")

        message.grade = new_grade
        MongoMessageRepository.save_message(message)

        return True

    @staticmethod
    def serialize_message(message: MongoMessage):
        return {
            "asked_question": message.asked_question,
            "question_answer": message.question_answer,
            "grade": RasaParser.parse_grade(message.grade),
            "creation_datetime": message.creation_datetime.isoformat(),
            "conversation_id": str(message.conversation_id.id),
            "message_id": str(message.id),
        }

    @staticmethod
    def get_messages(user_id: str):
        user = MongoUserRepository.get_user_by_uid(user_id)
        if user is None:
            return jsonify({'message': 'Usuario no identificado'}), 400

        if user.role != 0:
            return jsonify({'message': 'Usuario no tiene los permisos necesarios'}), 400

        response = MongoMessageRepository.all_messages_to_json()
        return jsonify(response), 200
