from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from flask_cors import CORS
import tweepy
from config import Config

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)  # Load configuration from Config class
CORS(app)

# Twitter API Authentication Setup
auth = tweepy.OAuthHandler(Config.TWITTER_CONSUMER_KEY, Config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(Config.TWITTER_ACCESS_TOKEN, Config.TWITTER_ACCESS_SECRET)

api = tweepy.API(auth)

@app.route("/")
def home():
    """Default homepage route"""
    if 'user_id' in session:
        # If user is logged in, show their Twitter profile and a welcome message
        user = api.me()
        return render_template("index.html", user=user)
    else:
        # If user is not logged in, redirect to Twitter login
        return redirect(url_for("login"))

@app.route("/login")
def login():
    """Redirect user to Twitter login page"""
    try:
        auth_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
        return redirect(auth_url)
    except tweepy.TweepyException as e:  # Change to TweepyException
        return jsonify({"message": f"Failed to get request token from Twitter: {str(e)}"}), 400

@app.route("/callback")
def callback():
    """Handle the callback after user authorizes Twitter"""
    request_token = session.pop('request_token', None)
    if request_token:
        auth.request_token = request_token
        try:
            auth.get_access_token(request.args['oauth_verifier'])
            session['access_token'] = auth.access_token
            session['access_token_secret'] = auth.access_token_secret

            # Get user's details
            user = api.me()

            # Save user info to session
            session['user_id'] = user.id
            session['username'] = user.screen_name
            session['profile_image'] = user.profile_image_url

            # Redirect to homepage after login
            return redirect(url_for('home'))

        except tweepy.TweepyException as e:  # Change to TweepyException
            return jsonify({"message": f"Failed to get access token from Twitter: {str(e)}"}), 400
    return jsonify({"message": "Request token missing."}), 400

@app.route("/logout")
def logout():
    """Logout the user and clear session"""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('profile_image', None)
    session.pop('access_token', None)
    session.pop('access_token_secret', None)
    return redirect(url_for('home'))

@app.route("/tweet", methods=["POST"])
def tweet():
    """Post a tweet to the user's Twitter account"""
    if 'user_id' not in session:
        return jsonify({"message": "Login required."}), 401
    
    tweet_content = request.form.get("tweet_content")
    if tweet_content:
        try:
            api.update_status(tweet_content)
            return jsonify({"message": "Tweet posted successfully!"})
        except tweepy.TweepyException as e:  # Change to TweepyException
            return jsonify({"message": f"Error posting tweet: {str(e)}"}), 400
    else:
        return jsonify({"message": "No content provided for the tweet."}), 400

if __name__ == "__main__":
    app.run(debug=True)
