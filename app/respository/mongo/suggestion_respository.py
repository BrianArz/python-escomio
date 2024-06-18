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

    @classmethod
    def to_json(cls, suggestion: MongoSuggestion):
        role_map = {
            1: "Estudiante",
            2: "Administrador"
        }
        status_map = {
            0: "Pendiente",
            1: "Aprobada",
            2: "Rechazada"
        }
        return {
            "suggested_by": str(suggestion.suggested_by.id),
            "suggested_by_user_role": role_map.get(suggestion.suggested_by_user_role, "Desconocido"),
            "suggested_question": suggestion.suggested_question,
            "status": status_map.get(suggestion.status, "Desconocido"),
            "creation_datetime": suggestion.creation_datetime.isoformat(),
        }

    @classmethod
    def all_suggestions_to_json(cls):
        suggestions = cls.get_suggestions()
        return [cls.to_json(suggestion) for suggestion in suggestions]
