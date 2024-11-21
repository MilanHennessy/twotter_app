from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_cors import CORS
from config import Config
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from models import User  # Assuming the User model is in 'models.py'

def create_app():
    app = Flask(
        __name__,
        static_folder="static",  # Folder for CSS, JS, and images
        template_folder="templates"  # Folder for HTML files
    )
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    # Register blueprints (if applicable)
    from routes.auth import auth_bp
    from routes.tweets import tweets_bp
    from routes.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tweets_bp)
    app.register_blueprint(users_bp)

    # Route for the login page
    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            data = request.get_json()  # Get the JSON data from the request

            # Check if JSON has username and password fields
            if not data or "username" not in data or "password" not in data:
                return jsonify({"message": "Missing username or password"}), 400

            username = data["username"]
            password = data["password"]

            # Check if the username exists
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):  # Check if password matches
                # Successful login, no need for JWT, just start the session
                session["user_id"] = user.id  # Store user ID in session

                # Debug: Print the session to verify user ID storage
                print("User ID stored in session:", session.get("user_id"))

                # Return success response
                return jsonify({"message": "Login successful"}), 200

            # If login failed
            return jsonify({"message": "Invalid username or password. Please try again."}), 401

        # If it's a GET request, render the login form
        return render_template("login.html")

    # Route to handle user registration
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            data = request.get_json()  # Get the JSON data from the request

            # Validate data
            if not data or "username" not in data or "password" not in data:
                return jsonify({"message": "Missing username or password"}), 400

            username = data["username"]
            password = data["password"]

            # Check if the username already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return jsonify({"message": "Username already exists. Please choose another one."}), 400

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create the new user and save to the database
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            # Return success message
            return jsonify({"message": "User successfully registered."}), 201

        # If it's a GET request, render the registration form
        return render_template("register.html")

    # Index Route - Home page, requires user to be authenticated via session
    @app.route("/index")
    def index():
        user_id = session.get("user_id")  # Get user ID from session
        
        if not user_id:
            return jsonify({"message": "You must be logged in to view this page."}), 401

        # Get the user details from the database
        user = User.query.filter_by(id=user_id).first()

        if user:
            # User is authenticated, render the index page
            return render_template("index.html", username=user.username)  # pass username or any user info to the page
        else:
            return jsonify({"message": "User not found!"}), 404

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
