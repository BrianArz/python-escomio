# Packages
import json
import pyrebase
import firebase_admin
from firebase_admin import credentials


class FirebaseService:
    @classmethod
    def init_app(cls, app):
        cls.app = app
        cls.firebase_app = cls.init_firebase()
        cls.firebase_admin = cls.init_firebase_admin()

    @staticmethod
    def init_firebase():
        """
        Initializes pyrebase application with configuration file

        :return: pyrebase app
        """
        try:
            with open('instance/firebase_config.json', 'r') as config_file:
                config = json.load(config_file)
            return pyrebase.initialize_app(config)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON configuration for Firebase.") from e

    @staticmethod
    def init_firebase_admin():
        """
        Initializes firebase sdk admin app

        :return: Firebase sdk admin app
        """
        try:
            cred = credentials.Certificate("instance/firebase_admin_key.json")
            return firebase_admin.initialize_app(cred)
        except FileNotFoundError:
            raise FileNotFoundError("Firebase admin credentials file not found.")

    @staticmethod
    def get_firebase_auth():
        """
        Gets firebase sdk admin auth application

        :return: Firebase sdk admin auth application
        """
        if hasattr(FirebaseService, 'firebase_app'):
            return FirebaseService.firebase_app.auth()
        else:
            raise Exception("Firebase app is not initialized.")
