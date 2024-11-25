import os


class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///twitter_clone.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "jwtsecretkey"
    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    GITHUB_CLIENT_ID = 'your_github_client_id'
    GITHUB_CLIENT_SECRET = 'your_github_client_secret'
    GITHUB_REDIRECT_URI = 'http://localhost:5000/login/callback'  # Adjust to your needs

    # Twitter OAuth credentials (using the credentials you provided)
    TWITTER_CONSUMER_KEY = "LTg3WDZGX0VXWWs0T0hnR180VWU6MTpjaQ"
    TWITTER_CONSUMER_SECRET = "ILAqb5lSxCaVg7P9psx5C8Tt46T3Ehn42cWOimd5OJ_NX6fdUE"
    TWITTER_API_KEY = "UyfzPwRHBxNmlOW4Vpkek8ktx"
    TWITTER_API_SECRET = "KEtBwWZMC166E1989RvOxjH8W0rpDRmKRZFTxqfyrPFytmU8SQ"
    TWITTER_ACCESS_TOKEN = "949102730529959936-OJbb77zHMfKerSF5UAE8L9IFbRgQzws"
    TWITTER_ACCESS_SECRET = "Jzk1JPrPY9TnGLlJDcXYzKfE9ViqMQMaw9Z17WhD9fZzv"

    TWITTER_SIGNATURE_METHOD = 'HMAC-SHA1'  # This is the default method used by Twitter    TWITTER_SIGNATURE_METHOD = 'HMAC-SHA1'  # This is the default method used by Twitter
