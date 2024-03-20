# Packages
import json
import pyrebase


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
