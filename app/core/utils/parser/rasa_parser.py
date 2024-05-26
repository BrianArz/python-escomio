import json
from flask import current_app

from app.schema import RasaQuestionResponse


class RasaParser:

    @classmethod
    def parse_test_question(cls, response: json) -> RasaQuestionResponse:
        """
        Parses Rasa Test Question response
        """
        try:
            recipient_id = response.get('recipient_id')
            text = response.get('text')

            return RasaQuestionResponse(recipient_id, text)

        except Exception as e:
            current_app.logger.error(f"Unable to parse response {e}")
            raise Exception(f"Unable to parse response {e}") from e
