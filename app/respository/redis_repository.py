from app.model import RedisUser


class RedisRepository:
    @classmethod
    def add_user(cls, user: RedisUser):
        if user is None:
            raise ValueError("User cannot be None")
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
