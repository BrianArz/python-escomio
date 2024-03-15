from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
import os, datetime

# Initialize the Flask application
app = Flask(__name__)

# Credential path
cred_path = os.path.abspath("escomio.json")

# Initialize Firebase
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Route to authenticate
@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    try:
        # Get information
        email = request.json['email']
        password = request.json['password']

        # Authenticate the user
        user = auth.get_user_by_email(email)

        # If exists, generate token
        custom_token = auth.create_custom_token(user.uid)

        # Get expiration
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

        # Convert token -> string
        custom_token_str = custom_token.decode("utf-8")

        # Return the token and expiration as a response
        response = {
            "token": custom_token_str,
            "expiration_time": expiration_time.isoformat()
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Start Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
