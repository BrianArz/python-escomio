from app.model import MongoUser


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
