from datetime import datetime
import random
from flask import Flask, jsonify, redirect, url_for, render_template, session, request, flash
import requests
from models import Like, Tweet, User
from extensions import db

# Initialize OAuth (commented out for now)
# oauth = OAuth(app)

# OAuth provider configuration (example with Twitter)
# twitter = oauth.remote_app(
#     'twitter',
#     consumer_key='your_consumer_key',
#     consumer_secret='your_consumer_secret',
#     request_token_params={
#         'scope': 'email',
#     },
#     base_url='https://api.twitter.com/1.1/',
#     request_token_url='https://api.twitter.com/oauth/request_token',
#     access_token_method='POST',
#     access_token_url='https://api.twitter.com/oauth/access_token',
#     authorize_url='https://api.twitter.com/oauth/authorize',
# )

# OAuth callback route
# @app.route('/oauth/callback')
# def oauth_callback():
#     response = twitter.authorized_response()
#     if response is None or response.get('oauth_token') is None:
#         return 'Access denied: reason={} error={}'.format(
#             request.args['reason'],
#             request.args['error_reason']
#         )
#     session['oauth_token'] = (response['oauth_token'], response['oauth_token_secret'])
#     user_info = twitter.get('account/verify_credentials.json')
#     session['user_id'] = user_info.data['id']
#     session['username'] = user_info.data['screen_name']
#     return redirect(url_for('home'))

# OAuth protected login route
# @app.route('/login_oauth')
# def login_oauth():
#     return twitter.authorize(callback=url_for('oauth_callback', _external=True))

# OAuth logout route
# @app.route('/logout_oauth')
# def logout_oauth():
#     session.clear()
#     return redirect(url_for('login'))
