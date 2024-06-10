from mongoengine import Document, StringField, IntField, BooleanField


class MongoUser(Document):
    username = StringField(required=True, max_length=15)
    escom_id = StringField(required=True, unique=True)
    firebase_uid = StringField(required=True, unique=True)
    role = IntField(required=True)
    active = BooleanField(required=True, default=True)

    meta = {'collection': 'users'}
