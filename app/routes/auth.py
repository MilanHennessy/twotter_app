from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

# Registration Route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate incoming data
    if 'username' not in data or 'password' not in data:
        return jsonify({"message": "Username and password are required"}), 422

    username = data['username']
    password = data['password']

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409

    # Create new user
    new_user = User(username=username)
    new_user.set_password(password)

    # Save user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully. Please log in to continue."}), 201

# Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate incoming data
    if 'username' not in data or 'password' not in data:
        return jsonify({"message": "Username and password are required"}), 422

    username = data['username']
    password = data['password']

    # Check if user exists
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Create JWT token after successful login
    access_token = create_access_token(identity=user.id)

    return jsonify({"message": "Login successful", "access_token": access_token}), 200