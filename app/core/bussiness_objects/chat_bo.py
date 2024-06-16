from flask import current_app, jsonify

from app.schema import RasaAskRequest
from app.model import (AddQuestionRequest, UpdateConversationNameRequest, GetConversationMessagesRequest,
                       ConversationIdRequest, UpdateMessageGradeRequest, MessageIdRequest)

from app.service.rasa_service import RasaService


class ChatBo:

    @classmethod
    def start_chat(cls, information: RasaAskRequest):
        from app.core import ConversationBo
        try:
            rasa_response = RasaService.ask_question(information)

            response = ConversationBo.create_conversation(information.sender, information.message, rasa_response.text,
                                                          rasa_response.intent)
            return jsonify(response.__dict__), 200

        except Exception as e:
            current_app.logger.error(f"Rasa start chat failed: {str(e)}")
            return jsonify({'message': str(e)}), 500

    @classmethod
    def add_message_to_conversation(cls, information: AddQuestionRequest):
        from app.core import ConversationBo
        try:
            rasa_response = RasaService.ask_question(information)

            response = ConversationBo.add_message_to_conversation(information.conversation_id, information.sender,
                                                                  information.message, rasa_response.text,
                                                                  rasa_response.intent)
            return jsonify(response.__dict__), 200

        except Exception as e:
            current_app.logger.error(f"Rasa add question failed: {str(e)}")
            return jsonify({'message': str(e)}), 500

    @classmethod
    def update_conversation_name(cls, information: UpdateConversationNameRequest):
        from app.core import ConversationBo
        try:
            response = ConversationBo.update_conversation_name(information.conversation_id, information.sender, information.new_name)

            if response:
                return jsonify({'message': 'Convsersación actualizada correctamente'}), 200

            else:
                return jsonify({'message': 'No se pudo actualizar la conversación'}), 400

        except Exception as e:
            current_app.logger.error(f"Rasa update conversation name failed: {str(e)}")
            return jsonify({'message': str(e)}), 500

    @classmethod
    def delete_conversation(cls, information: ConversationIdRequest):
        from app.core import ConversationBo
        try:
            response = ConversationBo.delete_conversation(information.conversation_id, information.sender)

            if response:
                return jsonify({'message': 'Conversación eliminada correctamente'})

            else:
                return jsonify({'message': 'No se pudo eliminar la conversación'}), 400

        except Exception as e:
            current_app.logger.error(f"Rasa delete conversation failed: {str(e)}")
            return jsonify({'message': str(e)}), 500

    @classmethod
    def get_conversation_messages(cls, information: GetConversationMessagesRequest):
        from app.core import ConversationBo
        try:
            response = ConversationBo.get_conversation_messages(information.conversation_id, information.sender)

            if response:
                return jsonify(response.__dict__), 200

            else:
                return jsonify({'message': 'No se pudieron obtener los mensaje de la conversación'}), 400

        except Exception as e:
            current_app.logger.error(f"Rasa get conversation messages failed: {str(e)}")
            return jsonify({'message': str(e)}), 500

    @classmethod
    def update_message_grade(cls, information: UpdateMessageGradeRequest):
        from app.core import MessageBo
        try:
            response = MessageBo.update_message_grade(information.conversation_id, information.sender,
                                                      information.message_id, information.new_grade)

            if response:
                return jsonify({'message': 'Respuesta calificada exitosamente'}), 200

            else:
                return jsonify({'message': 'No se pudo calificar la respuesta'}), 400

        except Exception as e:
            current_app.logger.error(f"Rasa update message grade failed: {str(e)}")
            return jsonify({'message': str(e)}), 500

    @classmethod
    def suggest_training_by_chat(cls, information: MessageIdRequest):
        from app.core import SuggestionBo
        try:
            response = SuggestionBo.suggest_training_by_chat(information.conversation_id, information.sender, information.message_id)

            if response:
                return jsonify({'message': 'Sugerencia creada con éxito'}), 200

            else:
                return jsonify({'message': 'No se pudo crear la sugerencia'}), 400

        except Exception as e:
            current_app.logger.error(f"Rasa training suggestion failed: {str(e)}")
            return jsonify({'message': str(e)}), 500
