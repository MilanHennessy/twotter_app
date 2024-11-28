from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship to Tweets
    tweets = db.relationship('Tweet', backref='user', lazy=True)

    def set_password(self, password):
        # Hash and set password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Check hashed password
        return check_password_hash(self.password_hash, password)

# Tweet Model
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    like_count = db.Column(db.Integer, default=0)  # Number of likes

    # Relationship to Likes
    likes = db.relationship('Like', backref='tweet_association', lazy=True)

    def __repr__(self):
        return f'<Tweet {self.id}>'

    def increment_likes(self):
        """ Increment like count when a tweet is liked """
        self.like_count += 1
        db.session.commit()

    def decrement_likes(self):
        """ Decrement like count when a tweet is unliked """
        if self.like_count > 0:
            self.like_count -= 1
            db.session.commit()

    def toggle_like(self, user):
        """ Toggle like status (like or unlike) for a tweet """
        existing_like = Like.query.filter_by(user_id=user.id, tweet_id=self.id).first()

        if existing_like:
            # If the user already liked this tweet, unlike it
            self.decrement_likes()
            db.session.delete(existing_like)
            db.session.commit()
            return False  # Return False indicating it was unliked
        else:
            # If the user hasn't liked this tweet, like it
            self.increment_likes()
            new_like = Like(user_id=user.id, tweet_id=self.id)
            db.session.add(new_like)
            db.session.commit()
            return True  # Return True indicating it was liked

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=False)

    # Enforce that each user can only like a tweet once
    __table_args__ = (db.UniqueConstraint('user_id', 'tweet_id', name='unique_user_tweet_like'),)

    # Relationships
    user = db.relationship('User', backref='liked_tweets', lazy=True)
    tweet = db.relationship('Tweet', backref='likes_association', lazy=True)  # Changed to avoid conflict
