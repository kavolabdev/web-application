import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

server = Flask(__name__)
CORS(server)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DATABASE")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))
server.config["MYSQL_CURSORCLASS"] = "DictCursor"
server.config["MYSQL_UNIX_SOCKET"] = None

@server.route("/operate", methods=["POST"])
def operate():
    try:
        data = request.get_json()
        company = data.get("company")
        operation = data.get("operation")
        database = data.get("database")
        table = data.get("table")
        payload = data.get("payload", {})

        if not company or not operation:
            return jsonify({"error": "Missing 'company' or 'operation'"}), 400

        cursor = mysql.connection.cursor()
        cursor.execute(f"USE `{database}`")

        if operation == "insert":
            columns = ', '.join(payload.keys())
            placeholders = ', '.join(['%s'] * len(payload))
            values = list(payload.values())
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
            mysql.connection.commit()
            return jsonify({"message": "Insert successful"}), 200

        elif operation == "select":
            where_clause = payload.get("where", "1=1")
            query = f"SELECT * FROM {table} WHERE {where_clause}"
            cursor.execute(query)
            rows = cursor.fetchall()
            return jsonify(rows), 200

        else:
            return jsonify({"error": "Unsupported operation"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@server.route("/health", methods=["GET"])
def health():
    return jsonify({"message": "CRUD service running"}), 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5002, debug=True)