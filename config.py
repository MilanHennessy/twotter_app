import os


class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///twitter_clone.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "jwtsecretkey"
    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # Twitter OAuth credentials (using the credentials you provided)
    TWITTER_CONSUMER_KEY = "LTg3WDZGX0VXWWs0T0hnR180VWU6MTpjaQ"
    TWITTER_CONSUMER_SECRET = "ILAqb5lSxCaVg7P9psx5C8Tt46T3Ehn42cWOimd5OJ_NX6fdUE"
    TWITTER_API_KEY = "UyfzPwRHBxNmlOW4Vpkek8ktx"
    TWITTER_API_SECRET = "KEtBwWZMC166E1989RvOxjH8W0rpDRmKRZFTxqfyrPFytmU8SQ"
    TWITTER_ACCESS_TOKEN = "949102730529959936-OJbb77zHMfKerSF5UAE8L9IFbRgQzws"
    TWITTER_ACCESS_SECRET = "Jzk1JPrPY9TnGLlJDcXYzKfE9ViqMQMaw9Z17WhD9fZzv"
    TWITTER_REDIRECT_URI = 'https://twotter-app.onrender.com/auth/twitter/callback'
    TWITTER_SIGNATURE_METHOD = 'HMAC-SHA1'  # This is the default method used by Twitter    TWITTER_SIGNATURE_METHOD = 'HMAC-SHA1'  # This is the default method used by Twitter
