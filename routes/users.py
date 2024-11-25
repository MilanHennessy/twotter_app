# routes/users.py
from flask import Blueprint, jsonify
from models import User

users_bp = Blueprint('users', __name__)

# Route to get all users
@users_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()  # Query all users from the database
    users_list = [user.to_dict() for user in users]  # Use the to_dict method

    return jsonify(users_list), 200  # Return the users as a JSON response