import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

server = Flask(__name__)
CORS(server)

MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
if MONGO_USER and MONGO_PASSWORD:
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"
else:
    MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

client = MongoClient(MONGO_URI)

@server.route("/operate", methods=["POST"])
def operate():
    try:
        data = request.get_json()

        database_name = data.get("database")
        table_name = data.get("table")
        operation = data.get("operation")
        payload = data.get("payload", {})

        if not all([database_name, table_name, operation]):
            return jsonify({"error": "Missing 'database', 'table', or 'operation'"}), 400

        db = client[database_name]
        collection = db[table_name]

        if operation == "insertOne":
            result = collection.insert_one(payload)
            return jsonify({"inserted_id": str(result.inserted_id)}), 200

        elif operation == "find":
            filter_ = payload.get("filter", {})
            projection = payload.get("projection")
            cursor = collection.find(filter_, projection)
            results = [doc for doc in cursor]
            for doc in results:
                doc["_id"] = str(doc["_id"])
            return jsonify(results), 200

        else:
            return jsonify({"error": "Unsupported operation", "data": data}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route("/health", methods=["GET"])
def health():
    return jsonify({"message": "CRUD service running"}), 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5002, debug=True)