# Packages
import json
from flask import jsonify, current_app
from requests.exceptions import HTTPError
import pyrebase
import firebase_admin
from firebase_admin import credentials

from app.core import FirebaseParser
from app.schema import FirebaseCredentialsRequest


class FirebaseService:
    @classmethod
    def init_app(cls, app):
        cls.app = app
        cls.firebase_app = cls._init_firebase()
        cls.firebase_admin = cls._init_firebase_admin()

    @staticmethod
    def _init_firebase():
        """
        Initializes pyrebase application with configuration file
        """
        try:
            with open('instance/firebase_config.json', 'r') as config_file:
                config = json.load(config_file)

            return pyrebase.initialize_app(config)

        except json.JSONDecodeError as json_ex:
            current_app.logger.error(f"Invalid JSON configuration for Firebase: {json_ex}")
            raise ValueError("Invalid JSON configuration for Firebase.") from json_ex

    @staticmethod
    def _init_firebase_admin():
        """
        Initializes firebase sdk admin app
        """
        try:
            cred = credentials.Certificate("instance/firebase_admin_key.json")
            return firebase_admin.initialize_app(cred)

        except FileNotFoundError as file_ex:
            current_app.logger.error(f"Firebase admin credential file not found: {file_ex}")
            raise FileNotFoundError("Firebase admin credentials file not found.")

    @staticmethod
    def get_firebase_auth():
        """
        Gets firebase sdk admin auth application
        """
        if hasattr(FirebaseService, 'firebase_app'):
            return FirebaseService.firebase_app.auth()

        else:
            current_app.logger.error("Unable to get firebase auth app")
            raise Exception("Unable to get firebase auth app")

    @classmethod
    def sign_in(cls, creds: FirebaseCredentialsRequest):
        try:
            firebase_auth = cls.get_firebase_auth()

            response = firebase_auth.sign_in_with_email_and_password(creds.email, creds.password)
            fb_response = FirebaseParser.parse_sign_in(response)

            return jsonify(fb_response.__dict__), 200

        except HTTPError as http_ex:
            current_app.logger.error(f"Firebase API sign-in error response has occurred {http_ex}")

            error_response = FirebaseParser.parse_error(http_ex.strerror)
            if error_response is None:
                return jsonify({"message": "Internal Server Error"}), 500

            return jsonify({"message": error_response.message}), 500

        except Exception as ex:
            current_app.logger.error(f"Unable to sign in to firebase {ex}")
            return jsonify({"message": "Unable to sign in to firebase"}), 500

    @classmethod
    def sign_up(cls, creds: FirebaseCredentialsRequest):
        try:
            firebase_auth = cls.get_firebase_auth()

            response = firebase_auth.create_user_with_email_and_password(creds.email, creds.password)
            fb_response = FirebaseParser.parse_sign_in(response)

            return jsonify(fb_response.__dict__), 200

        except HTTPError as http_error:
            current_app.logger.error(f"Firebase API sign-up error response has occurred {http_error}")

            error_response = FirebaseParser.parse_error(http_error.strerror)
            if error_response is None:
                return jsonify({"message": "Internal Server Error"}), 500

            return jsonify({"message": error_response.message}), 500

        except Exception as ex:
            current_app.logger.error(f"Unable to sign up to firebase {ex}")
            return jsonify({"message": "Unable to sign up to firebase"}), 500
