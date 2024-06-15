from mongoengine import Document, StringField, IntField, DateTimeField, ReferenceField
from datetime import datetime, timezone


class MongoMessage(Document):
    asked_question = StringField(required=True)
    question_answer = StringField(required=True)
    intent = StringField(required=True)
    grade = IntField(default=0)
    creation_datetime = DateTimeField(default=datetime.now(timezone.utc))
    conversation_id = ReferenceField('MongoConversation', required=True)

    meta = {'collection': 'messages'}

