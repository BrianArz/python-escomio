import urllib.parse

from mongoengine import connect
from pymongo.errors import ServerSelectionTimeoutError
from flask import current_app


class MongoDbConnection:
    _mongo_connection = None

    @classmethod
    def init_connection(cls):

        current_app.logger.info("Initializing MongoDb connection...")

        if cls._mongo_connection is None:
            mongo_uri = current_app.config.get('MONGO_URI')
            mongo_port = current_app.config.get('MONGO_PORT')
            mongo_database = current_app.config.get('MONGO_DATABASE')
            mongo_user = current_app.config.get('MONGO_USER')
            mongo_password = current_app.config.get('MONGO_PASSWORD')
            mongo_source = current_app.config.get('MONGO_SOURCE')

            cls._mongo_connection = connect(
                db=mongo_database,
                host=f'mongodb://{urllib.parse.quote_plus(mongo_user)}:{urllib.parse.quote_plus(mongo_password)}@{mongo_uri}:{mongo_port}/{mongo_database}?authSource={mongo_source}',
            )

        try:
            cls._mongo_connection.list_database_names()
        except ServerSelectionTimeoutError as e:
            current_app.logger.error(f"Unable to connect to MongoDB")
            raise Exception("MongoDB is unavailable") from e

        return cls._mongo_connection

    @classmethod
    def get_connection(cls):
        if cls._mongo_connection is None:
            cls.init_connection()
        return cls._mongo_connection
