from redis_om import HashModel, Field
from datetime import datetime


class RedisUser(HashModel):
    id_token: str
    uid: str = Field(primary_key=True)
    expiration_datetime: datetime

    class Meta:
        database = None
