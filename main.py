from datetime import datetime
import random
from flask import Flask, jsonify, redirect, url_for, render_template, session, request, flash
import requests
from models import Like, Tweet, User
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

    # Fetch tweets from all users in the database, ordered by most recent
    db_posts = Tweet.query.order_by(Tweet.created_at.desc()).limit(5).all()  # No filtering by user_id

    # Check if the user has already liked a tweet
    liked_tweet_ids = [like.tweet_id for like in Like.query.filter_by(user_id=user_id).all()]

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

        usernames = [user['username'] for user in users]
        random.shuffle(usernames)
        random.shuffle(posts)
        selected_posts = posts[:5]  # Take the first 5 posts

        for post in selected_posts:
            # Fetch only the first comment for the post
            comments_response = requests.get(f"https://jsonplaceholder.typicode.com/comments?postId={post['id']}")
            comment = comments_response.json()[0] if comments_response.status_code == 200 and comments_response.json() else None

            jsonplaceholder_posts.append({
                'id': post['id'],
                'username': random.choice(usernames),
                'body': post['body'],
                'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'likeCount': random.randint(1, 100),
                'liked': random.choice([True, False]),
                'comment': {'name':  random.choice(usernames), 'body': comment['body']} if comment else None,
            })

    # Check which posts the user has liked (use db_posts here as a safe reference)
    for post in db_posts:
        post.liked_by_user = Like.query.filter_by(user_id=user_id, tweet_id=post.id).first() is not None

    # Handle form submission to post a new tweet
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
                'likeCount': new_tweet.like_count  # Use the like_count from the database
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
        db_posts=db_posts,  # Now this will display posts from any user
        jsonplaceholder_posts=jsonplaceholder_posts,
        liked_tweet_ids=liked_tweet_ids  # Pass the liked tweet IDs to the template
    )


@app.route('/like/<int:tweet_id>', methods=['POST'])
def like_unlike(tweet_id):
    action = request.json.get('action')  # "like" or "unlike"
    tweet = Tweet.query.get(tweet_id)

    if not tweet:
        return jsonify({'error': 'Tweet not found'}), 404

    # Check if the user has already liked the tweet
    user_id = session.get('user_id')
    existing_like = Like.query.filter_by(user_id=user_id, tweet_id=tweet_id).first()

    if action == 'like':
        if not existing_like:
            # Add like to the tweet
            like = Like(user_id=user_id, tweet_id=tweet_id)
            db.session.add(like)
            tweet.like_count += 1
        tweet.liked = True
    elif action == 'unlike':
        if existing_like:
            # Remove like from the tweet
            db.session.delete(existing_like)
            tweet.like_count -= 1
        tweet.liked = False

    db.session.commit()
    return jsonify({'like_count': tweet.like_count, 'liked': tweet.liked})



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

    # Query to fetch all tweets for the logged-in user (tweets they've created)
    db_posts = Tweet.query.filter_by(user_id=user_id).order_by(Tweet.created_at.desc()).all()

    # Query to fetch all tweets liked by the logged-in user, including the username of the person who posted it
    # Ensuring proper join with Like and User models
    liked_tweets = db.session.query(Tweet, User.username).join(Like, Like.tweet_id == Tweet.id).join(User, User.id == Tweet.user_id).filter(Like.user_id == user_id).all()

    return render_template('profile.html', user={'username': username}, posts=db_posts, liked_tweets=liked_tweets)



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
