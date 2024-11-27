from flask import Flask, jsonify, redirect, url_for, render_template, session, request, flash
import requests
from models import User
from extensions import db
from helpers import get_tweets, generate_random_like_count

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secure secret key for sessions

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Update with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Look for user in the local database
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Store user data in session
            session['user_id'] = user.id
            session['username'] = user.username  # Properly set the username in the session
            return redirect(url_for('home'))

        flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')


# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    username = session.get('username')  # Fetch username from session

    if request.method == 'POST':
        # Get the tweet content from the request
        content = request.json.get('content')
        if content:
            # Simulate creating a new post with the username from the session
            new_post = {
                'username': username,  # Use the logged-in user's username
                'timestamp': 'Just now',  # Mock timestamp
                'body': content,
                'likeCount': generate_random_like_count()  # Simulate like count generation
            }
            posts = get_tweets(user_id)[1]
            posts.insert(0, new_post)  # Add the new post at the beginning of the list
            return jsonify({"new_post": new_post, "posts": posts})
    
    # Fetch user and posts
    user, posts = get_tweets(user_id)
    user['username'] = username  # Ensure the correct username is displayed
    return render_template('home.html', user=user, posts=posts)


# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clears the session to log the user out
    return redirect(url_for('login'))


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another one.', 'danger')
            return redirect(url_for('register'))

        # Create a new user and hash the password
        new_user = User(username=username)
        new_user.set_password(password)  # Ensure this method hashes the password

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Profile route
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    username = session.get('username')  # Get username from session

    # Fetch user and posts
    user, posts = get_tweets(user_id)
    user['username'] = username  # Ensure the correct username is displayed

    return render_template('profile.html', user=user, posts=posts)


# Tweets route
@app.route('/tweets', methods=['GET', 'POST'])
def tweets():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('Tweet content cannot be empty.')
            return redirect(url_for('tweets'))

        # Create a new tweet via API
        response = requests.post(f"https://jsonplaceholder.typicode.com/posts", json={
            "title": "New Tweet",
            "body": content,
            "userId": session['user_id']
        })
        if response.status_code == 201:
            flash('Tweet posted successfully!', 'success')
        else:
            flash('Error posting tweet.', 'danger')

    # Fetch tweets from API
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts")
    if response.status_code == 200:
        tweets = response.json()
        return render_template('tweets.html', tweets=tweets)
    return "Error fetching tweets."


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database is initialized
    app.run(debug=True)
