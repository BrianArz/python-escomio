from mongoengine import Document, ReferenceField, IntField, StringField, DateTimeField
from datetime import datetime, timezone


class MongoSuggestion(Document):
    suggested_by = ReferenceField('MongoUser', required=True)
    suggested_by_user_role = IntField(required=True)
    suggested_question = StringField(required=True)
    status = IntField(required=True, default=0)
    creation_datetime = DateTimeField(default=datetime.now(timezone.utc))
    description = StringField(default='')

    meta = {'collection': 'suggestions'}
