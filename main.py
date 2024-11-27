from datetime import datetime
import random
from flask import Flask, jsonify, redirect, url_for, render_template, session, request, flash
import requests
from models import Tweet, User
from extensions import db
from helpers import get_tweets, generate_random_like_count

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))

        flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    username = session.get('username')

    # Fetch only 5 most recent posts from the database
    db_posts = Tweet.query.filter_by(user_id=user_id).order_by(Tweet.created_at.desc()).limit(5).all()

    # If no posts are found, display a message
    if not db_posts:
        flash('No tweets found in your feed.', 'info')

    # Fetch posts from JSONPlaceholder
    jsonplaceholder_posts = []
    posts_response = requests.get("https://jsonplaceholder.typicode.com/posts")
    users_response = requests.get("https://jsonplaceholder.typicode.com/users")

    if posts_response.status_code == 200 and users_response.status_code == 200:
        posts = posts_response.json()
        users = users_response.json()
        
        # Extract usernames and shuffle them for randomness
        usernames = [user['username'] for user in users]
        random.shuffle(usernames)

        # Shuffle posts to simulate randomness
        random.shuffle(posts)
        selected_posts = posts[:5]  # Take the first 5 posts after shuffling

        for post in selected_posts:
            # Assign a random username from the shuffled list
            username2 = random.choice(usernames)

            jsonplaceholder_posts.append({
                'username': username2,
                'body': post['body'],
                'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),  # Use current timestamp
                'likeCount': random.randint(1, 10000)  # Generate a random like count
            })

    if request.method == 'POST':
        content = request.form.get('content') or (request.json and request.json.get('content'))
        if content:
            # Save new tweet to the database
            new_tweet = Tweet(content=content, user_id=user_id)
            db.session.add(new_tweet)
            db.session.commit()

            # Create a new post to display dynamically
            new_post = {
                'id': new_tweet.id,
                'username': username,
                'timestamp': new_tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'body': new_tweet.content,
                'likeCount': generate_random_like_count()
            }

            # If the request is from AJAX (JSON), return the new tweet data
            if request.is_json:
                return jsonify({"new_post": new_post})
            # If it's a regular form POST, redirect to avoid resubmitting the form
            return redirect(url_for('home'))

        return jsonify({"error": "Content is required"}), 400

    # Render the template with the user and post data
    return render_template(
        'home.html',
        user={'username': username},
        db_posts=db_posts,  # Ensure this is passed as a list of posts
        jsonplaceholder_posts=jsonplaceholder_posts
    )




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another one.', 'danger')
            return redirect(url_for('register'))

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
    username = session['username']

    # Query to fetch all tweets for the logged-in user
    db_posts = Tweet.query.filter_by(user_id=user_id).order_by(Tweet.created_at.desc()).all()

    return render_template('profile.html', user={'username': username}, posts=db_posts)


@app.route('/tweets', methods=['GET', 'POST'])
def tweets():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('Tweet content cannot be empty.', 'danger')
            return redirect(url_for('tweets'))

        response = requests.post(
            "https://jsonplaceholder.typicode.com/posts",
            json={"title": "New Tweet", "body": content, "userId": session['user_id']}
        )
        if response.status_code == 201:
            flash('Tweet posted successfully!', 'success')
        else:
            flash('Error posting tweet.', 'danger')

    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    tweets = response.json() if response.status_code == 200 else []

    return render_template('tweets.html', tweets=tweets)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
