from app.model import MongoUser
from mongoengine import DoesNotExist


class MongoUserRepository:

    @classmethod
    def save_user(cls, user: MongoUser):
        user.save()

    @classmethod
    def get_user_by_uid(cls, firebase_uid: str):
        try:
            user = MongoUser.objects.get(firebase_uid=firebase_uid)
            return user
        except DoesNotExist:
            return None

    @classmethod
    def get_all_users(cls):
        return MongoUser.objects.all()

    @classmethod
    def to_json(cls, user: MongoUser):
        return {
            "username": user.username,
            "escom_id": user.escom_id,
            "firebase_uid": user.firebase_uid,
            "role": "Estudiante" if user.role == 1 else "Administrador",
            "is_active": "Activo" if user.active else "Deshabilitado"
        }

    @classmethod
    def all_users_to_json(cls):
        users = cls.get_all_users()
        return [cls.to_json(user) for user in users]
