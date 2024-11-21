import tweepy
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Tweet, User
from config import Config

# Initialize Tweepy API
auth = tweepy.OAuth1UserHandler(
    Config.TWITTER_API_KEY,
    Config.TWITTER_API_SECRET,
    Config.TWITTER_ACCESS_TOKEN,
    Config.TWITTER_ACCESS_SECRET
)
twitter_api = tweepy.API(auth)

tweets_bp = Blueprint('tweets', __name__)

# Create Tweet Endpoint (Authenticated)
@tweets_bp.route('/tweets', methods=['POST'])
@jwt_required()  # Ensure the user is authenticated
def create_tweet():
    data = request.get_json()  # Assuming you're sending JSON data
    
    # Validate incoming data
    if 'content' not in data:
        return jsonify({"message": "Content is required"}), 422

    content = data['content']
    user_id = get_jwt_identity()  # Get the user_id from the JWT token

    # Ensure the user exists in the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Now create and save the tweet
    tweet = Tweet(content=content, user_id=user.id)
    db.session.add(tweet)
    db.session.commit()
    
    # Optional: Tweet to Twitter
    try:
        twitter_api.update_status(content)  # Posting to Twitter
    except tweepy.TweepError as e:
        return jsonify({"message": "Tweet posted locally, but failed to post to Twitter", "error": str(e)}), 500

    return jsonify({"message": "Tweet created successfully", "tweet": {"content": content, "user_id": user.id}}), 201

# Get Tweets Endpoint (Local and Twitter)
@tweets_bp.route('/tweets', methods=['GET'])
def get_tweets():
    include_twitter = request.args.get('include_twitter', 'false').lower() == 'true'

    tweet_list = []

    # Fetch tweets from the local database
    local_tweets = Tweet.query.all()
    for tweet in local_tweets:
        tweet_data = {
            "id": tweet.id,
            "content": tweet.content,
            "author": tweet.user.username,
            "created_at": tweet.created_at
        }
        tweet_list.append(tweet_data)

    # Optionally fetch tweets from Twitter
    if include_twitter:
        try:
            twitter_timeline = twitter_api.user_timeline(count=10)  # Fetching 10 recent tweets from Twitter
            for tweet in twitter_timeline:
                tweet_data = {
                    "id": tweet.id_str,
                    "content": tweet.text,
                    "author": tweet.user.screen_name,
                    "created_at": tweet.created_at
                }
                tweet_list.append(tweet_data)
        except tweepy.TweepError as e:
            return jsonify(message="Failed to fetch tweets from Twitter", error=str(e)), 500

    return jsonify(tweet_list), 200
