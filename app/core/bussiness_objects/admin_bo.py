from flask import current_app, jsonify


class AdminBo:

    @classmethod
    def get_users(cls, user_id: str):
        from app.core import UserBo
        try:
            response = UserBo.get_users(user_id)
            return response

        except Exception as e:
            current_app.logger.error(f"Admin get users failed: {str(e)}")
            return jsonify({'message': str(e)}), 500

    @classmethod
    def get_messages(cls, user_id: str):
        from app.core import MessageBo
        try:
            response = MessageBo.get_messages(user_id)
            return response

        except Exception as e:
            current_app.logger.error(f"Admin get messages failed: {str(e)}")
            return jsonify({'message': str(e)}), 500

    @classmethod
    def get_suggestions(cls, user_id: str):
        from app.core import SuggestionBo
        try:
            response = SuggestionBo.get_suggestions(user_id)
            return response

        except Exception as e:
            current_app.logger.error(f"Admin get suggestions failed: {str(e)}")
            return jsonify({'message': str(e)}), 500
