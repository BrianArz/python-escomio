from flask import current_app, jsonify
import requests
from requests.exceptions import HTTPError, ConnectionError

from app.core import RasaParser
from app.model import service_constants
from app.schema import RasaAskRequest


class RasaService:

    @classmethod
    def __get_rasa_uri(cls):
        """
        Private method to construct the Rasa URI from the Flask app config.
        """
        return f"{current_app.config['RASA_URI']}:{current_app.config['RASA_PORT']}"

    @classmethod
    def ask_question(cls, information: RasaAskRequest):
        """
        Handles asking a question to the Rasa service and returns a JSON response.
        """
        try:
            response = requests.post(
                f"{cls.__get_rasa_uri()}/{service_constants.API_RASA_ASK}",
                json=information.__dict__
            )

            response.raise_for_status()
            response_json = response.json()

            question = RasaParser.parse_test_question(response_json[0])
            return jsonify(question.__dict__), 200

        except ConnectionError as conn_ex:
            current_app.logger.error(f"Unable to connect to rasa service: {conn_ex}")
            return jsonify({"message": "Unable to connect to rasa service"}), 500

        except HTTPError as http_ex:
            current_app.logger.error(f"A request error has occurred: {http_ex}")
            return jsonify({"message": "A request error has occurred"}), http_ex.response.status_code

        except Exception as ex:
            current_app.logger.error(f"Internal error: {ex}")
            return jsonify({"message": "Internal server error"}), 500
