from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from extensions import db, jwt

def create_app():
    app = Flask(
        __name__,
        static_folder="static",  # Folder for CSS, JS, and images
        template_folder="templates"  # Folder for HTML files
    )
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.tweets import tweets_bp
    from routes.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tweets_bp)
    app.register_blueprint(users_bp)

    # Route to serve index.html at the root URL
    @app.route("/")
    def serve_index():
        return render_template("index.html")  # Loads from templates/index.html

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
