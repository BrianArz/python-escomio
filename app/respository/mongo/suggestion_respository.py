from mongoengine import DoesNotExist

from app.model import MongoSuggestion


class MongoSuggestionRepository:

    @classmethod
    def save_suggestion(cls, suggestion: MongoSuggestion):
        suggestion.save()

    @classmethod
    def get_suggestions(cls):
        return MongoSuggestion.objects.all()

    @classmethod
    def get_suggestion_by_id(cls, suggestion_id: str):
        try:
            return MongoSuggestion.objects.get(id=suggestion_id)
        except DoesNotExist:
            return None
