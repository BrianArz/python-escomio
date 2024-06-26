from flask import current_app, jsonify
import requests
from requests.exceptions import HTTPError, ConnectionError

from app.core import RasaParser
from app.model import service_constants
from app.schema import RasaAskRequest, RasaQuestionResponse


class RasaService:

    @classmethod
    def __get_rasa_uri(cls):
        return f"{current_app.config['RASA_URI']}:{current_app.config['RASA_PORT']}"

    @classmethod
    def ask_question(cls, information: RasaAskRequest) -> RasaQuestionResponse:
        try:
            current_app.logger.info("Asking rasa...")

            response = requests.post(
                f"{cls.__get_rasa_uri()}/{service_constants.API_RASA_ASK}",
                json=information.__dict__
            )

            response.raise_for_status()
            response_json = response.json()

            question = RasaParser.parse_test_question(response_json)

            current_app.logger.info("Question successfully asked.")
            return question

        except ConnectionError as conn_ex:
            current_app.logger.error(f"Unable to connect to rasa service: {conn_ex}")
            raise conn_ex

        except HTTPError as http_ex:
            current_app.logger.error(f"A request error has occurred: {http_ex}")
            raise http_ex

        except Exception as ex:
            current_app.logger.error(f"Internal error: {ex}")
            raise ex
