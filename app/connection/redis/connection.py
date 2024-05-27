from redis_om import get_redis_connection
from flask import current_app


class RedisConnection:
    _redis_connection = None

    @classmethod
    def init_connection(cls):
        current_app.logger.info("Initializing redis connection...")

        if cls._redis_connection is None:
            redis_uri = current_app.config.get('REDIS_URI', 'localhost')
            redis_port = current_app.config.get('REDIS_PORT', 6379)
            redis_url = f'{redis_uri}:{redis_port}'
            cls._redis_connection = get_redis_connection(url=redis_url)
        return cls._redis_connection

    @classmethod
    def get_connection(cls):
        if cls._redis_connection is None:
            cls.init_connection()
        return cls._redis_connection
