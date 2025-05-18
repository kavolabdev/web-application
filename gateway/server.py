import os, json
from flask import Flask, request, jsonify
from auth_svc import access
from auth import validate


server = Flask(__name__)


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
    
    user_data = json.loads(decoded_token)
    if user_data.get("admin"):
        return jsonify({"message": "Admin access granted!"}), 200
    else:
        return jsonify({"error": "Not authorized"}), 403


if __name__=="__main__":
    server.run(host="0.0.0.0", port=8080)