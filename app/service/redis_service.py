import redis
from flask import current_app


class RedisService:

    redis_connection = None

    @classmethod
    def init_app(cls, app):
        """
        Initialize Redis connection using the application config
        """
        cls.app = app
        cls.redis_connection = cls.get_redis_connection()

    @staticmethod
    def create_redis_connection():
        """
        Creates and returns a Redis connection instance.
        """
        try:
            redis_url = current_app.config.get('REDIS_URL', 'redis://localhost:6379')
            return redis.Redis.from_url(redis_url)

        except Exception as e:
            current_app.logger.error(f"Error creating redis connection: {e}")
            raise Exception(f"Error connecting to Redis: {e}") from e

    @classmethod
    def get_redis_connection(cls):
        """
        Returns the Redis connection instance. Initializes it if not already initialized.
        """
        if cls.redis_connection is None:

            try:
                cls.redis_connection = cls.create_redis_connection()
            except Exception as e:

                current_app.logger.error(f"Failed to obtain redis connection: {e}")
                raise Exception(f"Redis connection is not available: {e}") from e

        return cls.redis_connection
