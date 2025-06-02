import os, json
from flask import Flask, request, jsonify, send_from_directory
from auth_svc import access
from auth import validate
from flask_cors import CORS
from types import SimpleNamespace
from dotenv import load_dotenv

load_dotenv()

server = Flask(__name__, static_folder='static', static_url_path='')
CORS(server)

@server.route("/", methods=["GET"])
def main():

    username = os.environ.get("TEST_ADMIN"),
    password = os.environ.get("TEST_PASSWORD")

    mock_req = SimpleNamespace()
    mock_req.authorization = SimpleNamespace(username=username, password=password)

    token, error = access.login(mock_req)

    if error:
        return jsonify({"error": "login failed", "details": error}), 401
    
    # return jsonify({
    #     "message": f"Access granted for mock user",
    #     "token": token
    # }), 200

    return send_from_directory('static', 'index.html')

@server.route("/login", methods=["POST"])
def login():
    token, error = access.login(request)

    if not error:
        return token
    else:
        return error
    
@server.route("/operation", methods=["POST"])
def operation():
    access, error = validate.token(request)
    decoded_token = json.loads(access)

    if error:
        return error
    
    if decoded_token.get("admin"):
        return jsonify({"message": "Admin access granted!"}), 200
    else:
        return jsonify({"error": "Not authorized"}), 403


if __name__=="__main__":
    server.run(host="0.0.0.0", port=8005, debug=True)