import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///twitter_clone.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "static/uploads")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
