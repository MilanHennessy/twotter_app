from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Tweet

tweets_bp = Blueprint('tweets', __name__)

@tweets_bp.route('/tweets', methods=['POST'])
@jwt_required()
def create_tweet():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_tweet = Tweet(content=data['content'], user_id=user_id)
    db.session.add(new_tweet)
    db.session.commit()
    return jsonify(message="Tweet created successfully"), 201

@tweets_bp.route('/tweets', methods=['GET'])
def get_tweets():
    tweets = Tweet.query.all()
    tweet_list = [{"id": tweet.id, "content": tweet.content, "author": tweet.author.username} for tweet in tweets]
    return jsonify(tweet_list), 200
