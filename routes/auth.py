# import tweepy
# from flask import Blueprint, jsonify, redirect, request, url_for, session
# from config import Config

# auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# @auth_bp.route('/twitter', methods=['GET'])
# def twitter_login():
#     try:
#         auth = tweepy.OAuth1UserHandler(
#             Config.TWITTER_CONSUMER_KEY,
#             Config.TWITTER_CONSUMER_SECRET,
#             Config.TWITTER_REDIRECT_URI
#         )
#         redirect_url = auth.get_authorization_url()
#         session['request_token'] = auth.request_token
#         return redirect(redirect_url)
#     except tweepy.TweepyException as e:  # Updated exception handling
#         return {"message": "Failed to authenticate with Twitter", "error": str(e)}, 500

# @auth_bp.route('/twitter/callback', methods=['GET'])
# def twitter_callback():
#     verifier = request.args.get('oauth_verifier')
#     token = session.get('request_token')
#     session.pop('request_token', None)

#     if not token:
#         return {"message": "Missing request token"}, 400

#     try:
#         auth = tweepy.OAuth1UserHandler(
#             Config.TWITTER_CONSUMER_KEY,
#             Config.TWITTER_CONSUMER_SECRET,
#             Config.TWITTER_REDIRECT_URI
#         )
#         auth.request_token = token
#         auth.get_access_token(verifier)

#         api = tweepy.API(auth)
#         user_info = api.verify_credentials()

#         # Handle user information
#         return jsonify({"message": f"Welcome {user_info.screen_name}!"})
#     except tweepy.TweepyException as e:  # Updated exception handling
#         return {"message": "Failed to retrieve access token or user info", "error": str(e)}, 500
