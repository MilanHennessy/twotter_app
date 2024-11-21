import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///twitter_clone.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "static/uploads")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    TWITTER_API_KEY = "UyfzPwRHBxNmlOW4Vpkek8ktx"
    TWITTER_API_SECRET = "KEtBwWZMC166E1989RvOxjH8W0rpDRmKRZFTxqfyrPFytmU8SQ"
    TWITTER_ACCESS_TOKEN = "949102730529959936-OJbb77zHMfKerSF5UAE8L9IFbRgQzws"
    TWITTER_ACCESS_SECRET = "Jzk1JPrPY9TnGLlJDcXYzKfE9ViqMQMaw9Z17WhD9fZzv"

