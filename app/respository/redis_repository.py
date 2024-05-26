from datetime import datetime

from app.model import RedisUser


class RedisRepository:
    @classmethod
    def add_user(cls, id_token: str, uid: str, expiration_datetime: datetime):
        user = RedisUser(
            id_token=id_token,
            uid=uid,
            expiration_datetime=expiration_datetime
        )
        user.save()

    @classmethod
    def clean_user_cache(cls):
        """
        Deletes all redis cached users instances
        """
        RedisUser.db().flushdb()

    @classmethod
    def delete_user(cls, pk):
        RedisUser.delete(pk)

    @classmethod
    def get_user_by_id(cls, pk):
        return RedisUser.get(pk)
