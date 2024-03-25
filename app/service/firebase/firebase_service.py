# Packages
import json
import pyrebase
import firebase_admin
from firebase_admin import credentials


def init_firebase():
    """
    Initializes Firebase application

    :return: Firebase application instance
    """
    try:
        with open('instance/firebase_config.json', 'r') as config_file:
            config = json.load(config_file)

        return pyrebase.initialize_app(config)

    except json.JSONDecodeError:
        pass


def init_firebase_admin():
    cred = credentials.Certificate("instance/firebase_admin_key.json")
    firebase_admin.initialize_app(cred)


def get_firebase_auth():
    from app import firebase_app
    return firebase_app.auth()
