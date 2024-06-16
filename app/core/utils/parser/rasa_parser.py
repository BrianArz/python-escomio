import json
from flask import current_app

from app.schema import RasaQuestionResponse


class RasaParser:

    _grade_case_map = {
        0: "Sin calificar",
        1: "Satisfactoria",
        2: "No satisfactoria",
        3: "Sugerencia"
    }

    @classmethod
    def parse_test_question(cls, response: json) -> RasaQuestionResponse:
        try:
            texts = []
            intent = "No detectada"

            for message in response:
                if "text" in message:
                    texts.append(message["text"])
                if "custom" in message and "intent" in message["custom"]:
                    intent = message["custom"]["intent"]

            combined_text = "\n".join(texts) if texts else "De momento no me es posible responder esta pregunta. Por favor intenta con otra."

            return RasaQuestionResponse(intent, combined_text)

        except Exception as e:
            current_app.logger.error(f"Unable to parse response {e}")
            raise Exception(f"Unable to parse response {e}") from e

    @classmethod
    def parse_grade(cls, grade: int) -> str:
        return cls._grade_case_map.get(grade, "No se pudo obtener la calificación")
