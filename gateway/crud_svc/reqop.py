import os, requests
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

CRUDOP_URL = os.environ.get("CRUDOP_URL")

def send(req, data):
    try:
        res = requests.post(f"{CRUDOP_URL}/operate", json=data)
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({"error": "Operation failed", "details": str(e)}), 500