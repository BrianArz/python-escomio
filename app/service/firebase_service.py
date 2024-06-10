import json
import pyrebase

from datetime import datetime, timedelta, timezone
from flask import jsonify, current_app, make_response, Response
from requests.exceptions import HTTPError

from app.core import FirebaseParser
from app.schema import FirebaseCredentialsRequest, FirebaseSignInResponse
from app.respository import RedisRepository, MongoUserRepository
from app.core import FirebaseErrorViewParse, AuthBo
from app.model import CreateAccountRequest


class FirebaseService:
    @classmethod
    def init_app(cls, app):
        cls.app = app
        cls.firebase_app = cls._init_firebase()

    @staticmethod
    def _init_firebase():
        """
        Initializes pyrebase application with configuration file
        """
        try:
            current_app.logger.info("Initializing firebase app...")

            with open('instance/firebase_config.json', 'r') as config_file:
                config = json.load(config_file)

            return pyrebase.initialize_app(config)

        except json.JSONDecodeError as json_ex:
            current_app.logger.error(f"Invalid JSON configuration for Firebase: {json_ex}")
            raise ValueError("Invalid JSON configuration for Firebase.") from json_ex

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
            current_app.logger.info(f"{creds.email} signing in...")

            firebase_auth = cls.get_firebase_auth()

            response = firebase_auth.sign_in_with_email_and_password(creds.email, creds.password)
            fb_response = FirebaseParser.parse_sign_in(response)

            service_response = cls.__make_service_response(fb_response)

            current_app.logger.info(f"{creds.email} signed in.")
            return service_response

        except HTTPError as http_ex:
            error_response = FirebaseParser.parse_error(http_ex.strerror)

            if error_response is None:
                return jsonify({"message": "Internal Server Error"}), 500

            current_app.logger.error(f"Firebase API sign-in error response has occurred: {error_response.message}")
            return jsonify({"message": FirebaseErrorViewParse.view_alert_parse(error_response.message)}), 500

        except Exception as ex:
            current_app.logger.error(f"Unable to sign in to firebase {ex}")
            return jsonify({"message": "Unable to sign in to firebase"}), 500

    @classmethod
    def sign_up(cls, creds: CreateAccountRequest):
        try:
            current_app.logger.info(f"{creds.email} signing up...")

            validation_response = AuthBo.validate_user(creds)

            if not validation_response.is_valid:
                return jsonify({"message": validation_response.message}), 400

            firebase_auth = cls.get_firebase_auth()

            response = firebase_auth.create_user_with_email_and_password(creds.email, creds.password)
            fb_response = FirebaseParser.parse_sign_in(response)

            MongoUserRepository.save_user(creds.username, creds.email, int(creds.escom_id), fb_response.uid, 1)

            service_response = cls.__make_service_response(fb_response)

            current_app.logger.info(f"{creds.email} signed up.")
            return service_response

        except HTTPError as http_error:
            error_response = FirebaseParser.parse_error(http_error.strerror)

            if error_response is None:
                return jsonify({"message": "Internal Server Error"}), 500

            current_app.logger.error(f"Firebase API sign-up error response has occurred {error_response.message}")
            return jsonify({"message": FirebaseErrorViewParse.view_alert_parse(error_response.message)}), 500

        except Exception as ex:
            current_app.logger.error(f"Unable to sign up to firebase {ex}")
            return jsonify({"message": "Unable to sign up to firebase"}), 500

    @staticmethod
    def __add_cookie(response: Response, name: str, value: str, max_age: int):
        response.set_cookie(
            key=name,
            value=value,
            max_age=max_age,  # Lifetime of the cookie in seconds
            httponly=True,  # Makes the cookie inaccessible to JavaScript on the client side
            secure=current_app.config['COOKIE_SECURE'],  # Should be set to True in production to send only over HTTPS
            samesite=current_app.config['COOKIE_SAME_SITE']  # The cookie will not be sent with cross-origin requests
        )

    @classmethod
    def __make_service_response(cls, fb_response: FirebaseSignInResponse):

        # Gets expiration datetime utc (1 hour from now - 5 minutes)
        expiration_seconds = int(fb_response.expires_in) - 300
        expiration_datetime = datetime.now(timezone.utc) + timedelta(seconds=expiration_seconds)

        # Adds registry to cache
        RedisRepository.add_user(fb_response.id_token, fb_response.uid, expiration_datetime)

        # Returns only expire in seconds information
        service_response = make_response(jsonify({"expires_in": fb_response.expires_in}), 200)

        cls.__add_cookie(service_response, 'X-Access-Token', fb_response.id_token, expiration_seconds)
        cls.__add_cookie(service_response, 'X-Refresh-Token', fb_response.refresh_token, expiration_seconds)
        cls.__add_cookie(service_response, 'X-Uid', fb_response.uid, expiration_seconds)

        return service_response
