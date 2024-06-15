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
