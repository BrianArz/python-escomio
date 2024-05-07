from flask import request, jsonify, Blueprint
from pymongo import MongoClient

import app.config as config
from app.core import authorize


class MongoDBService:
    def __init__(self, mongo_host, mongo_port, mongo_database, mongo_collection):
        self.client = MongoClient(mongo_host, mongo_port)
        self.db = self.client[mongo_database]
        self.collection = self.db[mongo_collection]

    def add_user(self, uid, username, name, lastname, career):
        user_data = {
            '_id': uid,
            'username': username,
            'name': name,
            'lastname': lastname,
            'career': career
        }
        inserted_user_id = self.collection.insert_one(user_data).inserted_id
        return inserted_user_id

    def get_user(self, uid):
        user_data = self.collection.find_one({'_id': uid})
        return user_data


mongo_service = MongoDBService(config.MONGO_HOST, config.MONGO_PORT, config.MONGO_DATABASE, config.MONGO_COLLECTION)

user_bp = Blueprint('user', __name__)


@user_bp.route('/add_user', methods=['POST'])
@authorize
def add_user():
    """
    Creates a new user in MongoDB

    :parameter: User, name, last name, mail and career
    :return: SignInResponse object
    """

    if request.method == 'POST':
        # UID = request.form.get('uid')
        username = request.form.get('username')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        career = request.form.get('career')

        if not (username and name and lastname and career):
            return jsonify({'error': 'Todos los campos son obligatorios'})

        # Get UID
        uid = request.user['uid']

        # Checkout if UID exists
        existing_user = mongo_service.get_user(uid)
        if existing_user:
            return jsonify({'error': 'El usuario ya esta registrado'})

        # Insert document into MongoDB collection
        inserted_user_id = mongo_service.add_user(uid, username, name, lastname, career)

        return jsonify({'message': 'Usuario agregado correctamente', 'inserted_id': str(inserted_user_id)})
    else:
        return jsonify({'error': 'Solo se permiten solicitudes POST'})


@user_bp.route('/get_user', methods=['GET'])
@authorize
def get_user():
    """
    Retrieves user data from MongoDB

    :parameter: UID
    :return: UserData object
    """
    # Get the UID
    uid = request.user['uid']

    # Get Data from de UID
    user_data = mongo_service.get_user(uid)

    if user_data:
        user_data['_id'] = str(user_data['_id'])
        return jsonify({'message': 'Usuario encontrado', 'user_data': user_data})
    else:
        return jsonify({'error': 'Usuario no encontrado'})
