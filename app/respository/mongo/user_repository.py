from app.model import MongoUser


class MongoUserRepository:

    @classmethod
    def save_user(cls, username: str, escom_id: int, firebase_uid: str, role: int):
        user = MongoUser(
            username=username,
            escom_id=escom_id,
            firebase_uid=firebase_uid,
            role=role,
            active=True,
        )
        user.save()
