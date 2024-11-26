from flask import Flask, redirect, url_for, render_template, session, request, flash
import requests
from models import User
from extensions import db
from helpers import get_tweets, generate_random_like_count, generate_random_username

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for sessions

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Update this with your actual database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    # Fetch user and posts
    user, posts = get_tweets(user_id)

    return render_template('home.html', user=user, posts=posts)

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
            session['username'] = user.username
            return redirect(url_for('home'))

        flash('Invalid username or password. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Clears the session to log the user out
    return redirect(url_for('home'))

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

        # If username is unique, create a new user and hash the password
        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    # Simulate fetching posts and user data
    response_user = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    response_posts = requests.get(f"https://jsonplaceholder.typicode.com/posts", params={"userId": user_id})
    
    user = None
    posts = []
    
    if response_user.status_code == 200:
        user = response_user.json()

    if response_posts.status_code == 200:
        posts = response_posts.json()

    return render_template('profile.html', user=user, posts=posts)

@app.route('/tweets', methods=['GET', 'POST'])
def tweets():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('Tweet content cannot be empty.')
            return redirect(url_for('tweets'))

        # Create a new tweet
        response = requests.post(f"https://jsonplaceholder.typicode.com/posts", json={
            "title": "New Tweet",
            "body": content,
            "userId": session['user_id']
        })
        if response.status_code == 201:
            flash('Tweet posted successfully!')
        else:
            flash('Error posting tweet.')

    response = requests.get(f"https://jsonplaceholder.typicode.com/posts")
    if response.status_code == 200:
        tweets = response.json()
        return render_template('tweets.html', tweets=tweets)
    return "Error fetching tweets."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database is initialized
    app.run(debug=True)
