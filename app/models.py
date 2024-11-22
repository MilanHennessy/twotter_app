from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# models.py
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    # Add the to_dict method
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password_hash
        }

    # Add other methods like password checking here
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        """Hash the password and save it to the database."""
        self.password_hash = generate_password_hash(password)


class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # backref='author' makes the user accessible via tweet.author
    user = db.relationship('User', backref='tweets', lazy=True)