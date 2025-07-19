import os, json
from flask import Flask, request, jsonify
from auth_svc import access
from auth import validate
from crud_svc import reqop
from flask_cors import CORS
from types import SimpleNamespace
from dotenv import load_dotenv

load_dotenv()

server = Flask(__name__)
CORS(server)


@server.route("/health", methods=["GET"])
def main():

    username = os.environ.get("TEST_USER"),
    password = os.environ.get("TEST_PASSWORD")

    mock_req = SimpleNamespace()
    mock_req.authorization = SimpleNamespace(username=username, password=password)

    token, error = access.login(mock_req)

    if error:
        return jsonify({"error": "login failed", "details": error}), 401
    
    return jsonify({"message": "ok"}), 200

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

    if error:
        return error
    
    decoded_token = json.loads(access)
    company = decoded_token.get("company")
    group = decoded_token.get("user_group")

    if not company:
        return jsonify({"error": "Company missing"}), 403
    
    try:
        original_data = request.get_json(force=True)

        modified_payload = original_data.copy()
        modified_payload["database"] = company
        modified_payload["company"] = company
        if group:
            modified_payload["group"] = group
        
        return reqop.send(request, modified_payload)
    
    except Exception as e:
        return jsonify({"error": "Failed to prepare operation", "details": str(e)}), 500

    
@server.route("/admin", methods=["POST"])
def admin():
    access, error = validate.token(request)
    decoded_token = json.loads(access)

    if error:
        return error
    
    if decoded_token.get("user_group"):
        group = decoded_token.get("user_group")
        if group=="admin":
            return jsonify({"message": "Admin access granted!"}), 200
        else:
            return jsonify({"error": "Not authorized"}), 403
    else:
        return jsonify({"error": "Not authorized"}), 403


if __name__=="__main__":
    server.run(host="0.0.0.0", port=8005, debug=True)