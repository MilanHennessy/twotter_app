# Milan Hennessy 100839808
# This project is a twitter-like social media app with basic functionaloities such as creating an acoount
# tweeting, and liking tweets. You are also able to update your username as well as delete your account.
# We use jsonplaceholder api as our external api to grab a template feed to mimic a home feed that is always
# updating. 

from datetime import datetime
import random
from flask import Flask, jsonify, redirect, url_for, render_template, session, request, flash
import requests
from models import Like, Tweet, User
from extensions import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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

    
    db_posts = Tweet.query.order_by(Tweet.created_at.desc()).limit(5).all()  

    
    liked_tweet_ids = [like.tweet_id for like in Like.query.filter_by(user_id=user_id).all()]

    
    if not db_posts:
        flash('No tweets found in your feed.', 'info')

  
    jsonplaceholder_posts = []
    posts_response = requests.get("https://jsonplaceholder.typicode.com/posts")
    users_response = requests.get("https://jsonplaceholder.typicode.com/users")

    if posts_response.status_code == 200 and users_response.status_code == 200:
        posts = posts_response.json()
        users = users_response.json()

        usernames = [user['username'] for user in users]
        random.shuffle(usernames)
        random.shuffle(posts)
        selected_posts = posts[:5]  

        for post in selected_posts:
            
            comments_response = requests.get(f"https://jsonplaceholder.typicode.com/comments?postId={post['id']}")
            comment = comments_response.json()[0] if comments_response.status_code == 200 and comments_response.json() else None

            jsonplaceholder_posts.append({
                'id': post['id'],
                'username': random.choice(usernames),
                'body': post['body'],
                'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'likeCount': random.randint(1, 10000),
                'liked': random.choice([True, False]),
                'comment': {'name':  random.choice(usernames), 'body': comment['body']} if comment else None,
            })

    
    for post in db_posts:
        post.liked_by_user = Like.query.filter_by(user_id=user_id, tweet_id=post.id).first() is not None

    
    if request.method == 'POST':
        content = request.form.get('content') or (request.json and request.json.get('content'))
        if content:
            
            new_tweet = Tweet(content=content, user_id=user_id)
            db.session.add(new_tweet)
            db.session.commit()

            
            new_post = {
                'id': new_tweet.id,
                'username': username,
                'timestamp': new_tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'body': new_tweet.content,
                'likeCount': new_tweet.like_count  
            }

            
            if request.is_json:
                return jsonify({"new_post": new_post})
            
            return redirect(url_for('home'))

        return jsonify({"error": "Content is required"}), 400

    
    return render_template(
        'home.html',
        user={'username': username},
        db_posts=db_posts,  
        jsonplaceholder_posts=jsonplaceholder_posts,
        liked_tweet_ids=liked_tweet_ids  
    )

@app.route('/update_username', methods=['POST'])
def update_username():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    new_username = request.form.get('new_username')

    
    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user:
        flash('Username already taken. Please choose another one.', 'danger')
        return redirect(url_for('profile'))  

    
    user = User.query.get(user_id)
    if user:
        user.username = new_username
        db.session.commit()

    
    session['username'] = new_username

    flash('Username updated successfully!', 'success')
    return redirect(url_for('profile'))  

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    
    tweets = Tweet.query.filter_by(user_id=user_id).all()
    for tweet in tweets:
        db.session.delete(tweet)
    
    
    likes = Like.query.filter_by(user_id=user_id).all()
    for like in likes:
        db.session.delete(like)
    
    
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
    
    db.session.commit()

    
    session.clear()
    flash('Your account has been deleted successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/tweets/<int:tweet_id>', methods=['DELETE'])
def delete_tweet(tweet_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    
    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        return jsonify({'error': 'Tweet not found'}), 404

    
    if tweet.user_id != session['user_id']:
        return jsonify({'error': 'Permission denied'}), 403

    
    db.session.delete(tweet)
    db.session.commit()

    return jsonify({'message': 'Tweet deleted successfully'})

@app.route('/tweets/<int:tweet_id>', methods=['PUT'])
def update_tweet(tweet_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    
    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        return jsonify({'error': 'Tweet not found'}), 404

    
    if tweet.user_id != session['user_id']:
        return jsonify({'error': 'Permission denied'}), 403

    
    data = request.json
    new_content = data.get('content')
    if not new_content:
        return jsonify({'error': 'Content is required'}), 400

    tweet.content = new_content
    tweet.updated_at = datetime.utcnow()  
    db.session.commit()

    return jsonify({'message': 'Tweet updated successfully', 'tweet': {'id': tweet.id, 'content': tweet.content}})


@app.route('/like/<int:tweet_id>', methods=['POST'])
def like_unlike(tweet_id):
    action = request.json.get('action')  
    tweet = Tweet.query.get(tweet_id)

    if not tweet:
        return jsonify({'error': 'Tweet not found'}), 404

    
    user_id = session.get('user_id')
    existing_like = Like.query.filter_by(user_id=user_id, tweet_id=tweet_id).first()

    if action == 'like':
        if not existing_like:
            
            like = Like(user_id=user_id, tweet_id=tweet_id)
            db.session.add(like)
            tweet.like_count += 1
        tweet.liked = True
    elif action == 'unlike':
        if existing_like:
            
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

    
    db_posts = Tweet.query.filter_by(user_id=user_id).order_by(Tweet.created_at.desc()).all()

    
    
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
