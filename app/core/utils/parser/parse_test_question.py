import json

from app.schema.rasa.test_question_response import TestQuestionResponse


def parse_test_question(response: json) -> TestQuestionResponse:
    """
    Parses Rasa Test Question response

    :param response: Rasa response
    :return: TestQuestionResponse object
    """
    try:
        recipient_id = response.get('recipient_id')
        text = response.get('text')

        return TestQuestionResponse(recipient_id, text)

    except json.JSONDecodeError:
        pass
