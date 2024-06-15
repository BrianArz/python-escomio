import json
from flask import current_app

from app.schema import RasaQuestionResponse


class RasaParser:

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
