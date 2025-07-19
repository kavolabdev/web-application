import jwt, datetime, os
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
server.config["MYSQL_UNIX_SOCKET"] = None

@server.route("/health", methods=["GET"])
def index():
    return "running"

@server.route("/login", methods=["POST"])
def login():  
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "missing credentials"}), 401
    
    email = data["email"]
    password = data["password"]

    try: 
        cur = mysql.connection.cursor()
        res = cur.execute("SELECT email, password, company_code, user_group FROM user WHERE email=%s", (email,))

        if res > 0:
            user_row = cur.fetchone()
            stored_email, stored_password, stored_company, stored_group = user_row
            
            if stored_password == password:
                token = createJWT(stored_email, os.environ.get("JWT_SECRET"), stored_company, stored_group)
                return jsonify({"token": token})

        cur.close()

    except Exception as e:
        return jsonify({"error": "internal server error", "details": str(e)}), 500
        
    return jsonify({"error": "invalid credentials"}), 401

@server.route("/validate", methods=["POST"])
def validate():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "missing credentials"}), 401
    
    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(
            token,
            os.environ.get("JWT_SECRET"),
            algorithms=["HS256"]
        )
        return jsonify(decoded), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 403

def createJWT(username, secret, company_code, user_group):
    payload = {
        "username": username,
        "user_group": user_group,
        "company": company_code,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
        "iat": datetime.datetime.now(datetime.timezone.utc)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

if __name__=="__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)          
