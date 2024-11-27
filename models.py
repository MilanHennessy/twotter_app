from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        # Hash and set password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Check hashed password
        return check_password_hash(self.password_hash, password)


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    like_count = db.Column(db.Integer, default=0)  # New column to store the number of likes
    
    # Removed backref from here, as it's already defined in the User model
    user = db.relationship('User')  # No backref needed here

    def __repr__(self):
        return f'<Tweet {self.id}>'

    def increment_likes(self):
        self.like_count += 1
        db.session.commit()

    def decrement_likes(self):
        if self.like_count > 0:
            self.like_count -= 1
            db.session.commit()
