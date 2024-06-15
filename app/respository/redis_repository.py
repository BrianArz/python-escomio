from datetime import datetime
from redis_om import Migrator

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
        user.expire(3300)  # Saves registry in cache for 55 minutes (in case there's never a logout)

    @classmethod
    def clean_user_cache(cls):
        """
        Deletes all redis cached users instances
        """
        RedisUser.db().flushdb()

    @classmethod
    def delete_user(cls, pk):
        if pk is None:
            return
        RedisUser.delete(pk)

    @classmethod
    def get_user_by_id(cls, pk):
        return RedisUser.get(pk)


def initialize_database(connection):
    RedisUser.Meta.database = connection
    Migrator().run()
