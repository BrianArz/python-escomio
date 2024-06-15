import json
import pyrebase

from datetime import datetime, timedelta, timezone
from flask import jsonify, current_app, make_response, Response
from requests.exceptions import HTTPError

from app.core import FirebaseParser, FirebaseErrorViewParse, AuthBo, UserBo
from app.schema import FirebaseCredentialsRequest, FirebaseSignInResponse
from app.respository import RedisRepository, MongoUserRepository
from app.model import CreateAccountRequest, UserViewInfo


class FirebaseService:
    @classmethod
    def init_app(cls, app):
        cls.app = app
        cls.firebase_app = cls._init_firebase()

    @staticmethod
    def _init_firebase():
        """Initializes pyrebase application with configuration file"""
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
        """Gets firebase sdk admin auth application"""
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

            user = MongoUserRepository.get_user_by_uid(fb_response.uid)
            user_view_info = UserViewInfo(username=user.username, role=user.role)

            service_response = cls._make_service_response(fb_response, user_view_info)
            current_app.logger.info(f"{creds.email} signed in.")
            return service_response

        except HTTPError as http_ex:
            return cls._handle_http_error(http_ex, "Firebase API sign-in error response has occurred")
        except Exception as ex:
            return cls._handle_general_error(ex, "Unable to sign in to firebase")

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

            mongo_user = UserBo.create_user(creds.username, creds.escom_id, fb_response.uid, 1)
            MongoUserRepository.save_user(mongo_user)

            user_view_info = UserViewInfo(username=creds.username, role=1)

            service_response = cls._make_service_response(fb_response, user_view_info)
            current_app.logger.info(f"{creds.email} signed up.")
            return service_response
        
        except HTTPError as http_error:
            return cls._handle_http_error(http_error, "Firebase API sign-up error response has occurred")
        except Exception as ex:
            return cls._handle_general_error(ex, "Unable to sign up to firebase")

    @classmethod
    def refresh_token(cls, refresh_token: str):
        try:
            firebase_auth = cls.get_firebase_auth()

            response = firebase_auth.refresh(refresh_token)

            fb_response = FirebaseParser.parse_refresh(response)

            service_response = cls._make_service_response(fb_response, None)
            return service_response
        
        except HTTPError as http_error:
            return cls._handle_http_error(http_error, "Firebase API refresh token error response has occurred")
        except Exception as ex:
            return cls._handle_general_error(ex, "Unable to refresh token from firebase")

    @staticmethod
    def _add_cookie(response: Response, name: str, value: str, max_age: int):
        response.set_cookie(
            key=name,
            value=value,
            max_age=max_age,
            httponly=True,
            secure=current_app.config['COOKIE_SECURE'],
            samesite=current_app.config['COOKIE_SAME_SITE']
        )

    @classmethod
    def _make_service_response(cls, fb_response: FirebaseSignInResponse, user_view_info: UserViewInfo = None):
        expiration_seconds = int(fb_response.expires_in) - 300
        expiration_datetime = datetime.now(timezone.utc) + timedelta(seconds=expiration_seconds)

        RedisRepository.add_user(fb_response.id_token, fb_response.uid, expiration_datetime)

        service_response = make_response('', 200)
        
        if user_view_info is not None:
            user_view_info.set_expires_in(fb_response.expires_in)
            service_response = make_response(jsonify(user_view_info.__dict__), 200)
            
        cls._add_cookie(service_response, 'X-Access-Token', fb_response.id_token, expiration_seconds)
        cls._add_cookie(service_response, 'X-Refresh-Token', fb_response.refresh_token, expiration_seconds)
        cls._add_cookie(service_response, 'X-Uid', fb_response.uid, expiration_seconds)
        
        return service_response

    @staticmethod
    def _handle_http_error(http_error: HTTPError, log_message: str):
        error_response = FirebaseParser.parse_error(http_error.strerror)
        if error_response is None:
            return jsonify({"message": "Internal Server Error"}), 500
        current_app.logger.error(f"{log_message}: {error_response.message}")
        return jsonify({"message": FirebaseErrorViewParse.view_alert_parse(error_response.message)}), 500

    @staticmethod
    def _handle_general_error(ex: Exception, log_message: str):
        current_app.logger.error(f"{log_message} {ex}")
        return jsonify({"message": log_message}), 500
