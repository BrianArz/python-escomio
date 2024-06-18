from flask import jsonify

from app.model import MongoUser
from app.respository import MongoUserRepository


class UserBo:
    @staticmethod
    def create_user(username: str, escom_id: str, firebase_uid: str, role: int) -> MongoUser:
        return MongoUser(
            username=username,
            escom_id=escom_id,
            firebase_uid=firebase_uid,
            role=role,
            active=True,
        )

    @staticmethod
    def get_users(user_id: str):
        user = MongoUserRepository.get_user_by_uid(user_id)
        if user is None:
            return jsonify({'message': 'Usuario no identificado'}), 400

        if user.role != 0:
            return jsonify({'message': 'Usuario no tiene los permisos necesarios'}), 400

        response = MongoUserRepository.all_users_to_json()
        return jsonify(response), 200
