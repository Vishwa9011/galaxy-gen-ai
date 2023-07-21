from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import datetime
import jwt

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb+srv://vishu842301:vishu842301@cluster0.zrz66q0.mongodb.net/test?retryWrites=true&w=majority'
app.config['SECRET_KEY'] = 'KNSDFABUSF39835H8NVDSBJVAS'  # Replace with a strong, random secret key
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route("/")
def home():
    return "Home Page"


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() 
    print(data)
    if not data or "username" not in data or "password" not in data or "role" not in data:
        return jsonify({"message": "Invalid data"}), 400

    username = data["username"]
    password = data["password"]
    role = data["role"]

    # Check if the username is already taken
    if mongo.db.users.find_one({"username": username}):
        return jsonify({"message": "Username already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insert the user data into the collection
    user_data = {"username": username, "password": hashed_password, "role": role}
    inserted_data = mongo.db.users.insert_one(user_data)

    return jsonify({"message": "User registered successfully", "id": str(inserted_data.inserted_id)}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print(data)
    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Invalid data"}), 400
 
    username = data["username"]
    password = data["password"]

    # Check if the user exists in the database
    user = mongo.db.users.find_one({"username": username})
    print(user)
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Create a JWT token for authentication
    token = jwt.encode({"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])

    user["_id"] = str(user["_id"])
    return jsonify({"token": token,"user":user}), 200 

# The following routes should be protected and require a valid JWT token for access
@app.route("/users", methods=["GET"])
def get_users():
    # Get the token from the request header
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing"}), 401

    try:
        # Decode the token and verify its authenticity
        jwt.decode(token, app.config['SECRET_KEY'])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

    users = list(mongo.db.users.find({}, {"_id": 0, "password": 0}))
    return jsonify(users)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
