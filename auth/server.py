import jwt, datetime, os, bcrypt
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS


server = Flask(__name__)
CORS(server)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))
server.config["MYSQL_UNIX_SOCKET"] = None

@server.route("/", methods=["GET"])
def index():
    return "hello from index"

@server.route("/login", methods=["POST"])
def login():  
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "missing credentials"}), 401
    
    email = data["email"]
    password = data["password"]

    try: 
        cur = mysql.connection.cursor()
        res = cur.execute("SELECT email, password FROM user WHERE email=%s", (email,))

        if res > 0:
            user_row = cur.fetchone()
            stored_email, stored_password = user_row
            
            if stored_password == password:
                token = createJWT(stored_email, os.environ.get("JWT_SECRET"), True)
                return jsonify({"token": token})
    
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

def createJWT(username, secret, is_admin):
    payload = {
        "username": username,
        "admin": is_admin,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
        "iat": datetime.datetime.now(datetime.timezone.utc)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

if __name__=="__main__":
    server.run(host="0.0.0.0", port=5000)       
