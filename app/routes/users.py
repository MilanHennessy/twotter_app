# users.py
from flask import Blueprint, request, jsonify
from extensions import db  # Import db from extensions, not from main
from models import User  # Assuming User model is in models.py

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def get_users():
    # Example endpoint
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])  # Convert users to dicts for JSON response

# Define other routes for users, like user profile, etc.
