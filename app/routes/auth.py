from flask import Blueprint, request, jsonify
from extensions import db  # Import db from extensions
from models import User  # Assuming User model is in models.py

auth_bp = Blueprint("auth", __name__)

# Define your routes here, e.g., login, signup
@auth_bp.route("/signup", methods=["POST"])
def signup():
    # Example signup logic
    data = request.get_json()
    # Use db to interact with the database
    return jsonify({"message": "User signed up"})
