from flask import Flask, redirect, request, session, url_for, render_template
import tweepy
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Twitter API credentials (replace with your actual credentials)
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://127.0.0.1:5000/twitter_callback'

# Set the API URLs
AUTHORIZATION_URL = "https://twitter.com/i/oauth2/authorize"
TOKEN_URL = "https://api.twitter.com/oauth2/token"

# Set up Tweepy client (without authentication initially)
client = tweepy.Client(bearer_token="your-bearer-token")

@app.route('/')
def home():
    if 'twitter_token' in session:
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    # Construct authorization URL with the necessary query parameters
    auth_url = f"{AUTHORIZATION_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=tweet.read users.read"
    return redirect(auth_url)

@app.route('/callback')
def twitter_callback():
    # Twitter redirects here with the authorization code
    code = request.args.get('code')

    if not code:
        return "Error: No code returned"

    # Exchange the authorization code for an access token
    token_data = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=token_data)
    if response.status_code == 200:
        # Save the token to the session
        session['twitter_token'] = response.json()['access_token']

        # Redirect to the custom HTML page (home.html)
        return redirect(url_for('home_page'))
    else:
        return "Error during token exchange"

@app.route('/home')
def home_page():
    # This will render the home.html template
    return render_template('index.html')

@app.route('/profile')
def profile():
    if 'twitter_token' not in session:
        return redirect(url_for('login'))

    # Create a Tweepy client with the access token
    access_token = session['twitter_token']
    client = tweepy.Client(bearer_token=access_token)

    try:
        # Fetch the authenticated user's profile
        user = client.get_me()
        return f'Hello {user.data["name"]}, your Twitter handle is @{user.data["username"]}.'
    except tweepy.TweepyException as e:
        return f'Error fetching user info: {e}'

if __name__ == '__main__':
    app.run(debug=True)
