from flask import current_app, jsonify

from app.core import ConversationBo
from app.schema import RasaAskRequest
from app.model import AddQuestionRequest, UpdateConversationNameRequest

from app.service.rasa_service import RasaService


class ChatBo:

    @classmethod
    def start_chat(cls, information: RasaAskRequest):
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
        try:
            response = ConversationBo.update_conversation_name(information.conversation_id, information.sender, information.new_name)

            if response:
                return jsonify({'message': 'Convsersación actualizada correctamente'}), 200

            else:
                return jsonify({'message': 'No se pudo actualizar la conversación'}), 400

        except Exception as e:
            current_app.logger.error(f"Rasa update conversation name failed: {str(e)}")
            return jsonify({'message': str(e)}), 500