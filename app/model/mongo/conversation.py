from mongoengine import Document, ReferenceField, ListField, StringField

from .message import MongoMessage


class MongoConversation(Document):
    user = ReferenceField('MongoUser', required=True)
    name = StringField(required=True)
    messages = ListField(ReferenceField(MongoMessage))

    meta = {'collection': 'conversations'}
