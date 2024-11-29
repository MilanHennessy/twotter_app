from flask import session
import pytest
from main import app, db
from models import User, Tweet, Like

# Fixture to create the app context and client
@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client

# Fixture to initialize the database
@pytest.fixture(scope='function')
def init_db():
    # Create the tables in the test database
    db.create_all()

    # Setup: Create a test user in the database
    user = User(username="testuser", password_hash="hashedpassword")
    user.set_password("testpassword")  # Use set_password to hash the password
    db.session.add(user)
    db.session.commit()

    # Create a test tweet for the user
    tweet1 = Tweet(content="Test tweet 1", user_id=user.id)
    tweet2 = Tweet(content="Test tweet 2", user_id=user.id)
    db.session.add(tweet1)
    db.session.add(tweet2)
    db.session.commit()

    # Yield the DB session for use in tests
    yield db

    # Teardown: Clean up after each test
    db.session.remove()
    db.drop_all()

def test_login(client, init_db):
    # Make a POST request with login credentials
    response = client.post('/login', data=dict(username="testuser", password="testpassword"))

    # Check if the response status code is 302 (Redirect)
    assert response.status_code == 302

    # Check if the redirect location is /home
    assert response.headers['Location'] == '/'


def test_update_username(client, init_db):
    # Simulate a user login by adding the user to the session
    user = User.query.filter_by(username="testuser").first()
    # Directly manipulate the session
    with client.session_transaction() as sess:
        sess['user_id'] = user.id  # Simulate setting the session with the logged-in user's ID
        sess['username'] = user.username  # Simulate setting the username in session

    # Make a POST request with the new username
    response = client.post('/update_username', data=dict(new_username="new_username"))
    
    # Check if the response is a redirect (302)
    assert response.status_code == 302

    # Check if the username has been updated in the DB
    user = User.query.filter_by(id=user.id).first()
    assert user.username == "new_username"

    # Optionally check if session is updated
    with client.session_transaction() as sess:
        assert sess['username'] == "new_username"


# Test delete account functionality
def test_delete_account(client, init_db):
    # Simulate a user login by adding the user to the session
    user = User.query.filter_by(username="testuser").first()
    # Directly manipulate the session
    with client.session_transaction() as sess:
        sess['user_id'] = user.id  # Simulate setting the session with the logged-in user's ID
        sess['username'] = user.username  # Simulate setting the username in session

    # Make a POST request to delete the account
    response = client.post('/delete_account')
    
    # Assert that the response redirects to the login page (status code 302)
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'

    # Ensure the user has been deleted from the database
    deleted_user = User.query.get(user.id)
    assert deleted_user is None

    # Ensure the user's tweets have been deleted
    deleted_tweets = Tweet.query.filter_by(user_id=user.id).all()
    assert len(deleted_tweets) == 0

    # Ensure the user's likes have been deleted
    deleted_likes = Like.query.filter_by(user_id=user.id).all()
    assert len(deleted_likes) == 0

    # Ensure the session has been cleared (user is logged out)
    with client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'username' not in sess
        
# Test liking a tweet
def test_like_tweet(client, init_db):
    # Simulate a user login by adding the user to the session
    user = User.query.filter_by(username="testuser").first()
    tweet = Tweet.query.first()
    
    # Directly manipulate the session
    with client.session_transaction() as sess:
        sess['user_id'] = user.id  # Simulate setting the session with the logged-in user's ID

    # Make a POST request to like the tweet
    response = client.post(f'/like/{tweet.id}', json={'action': 'like'})
    
    # Assert that the tweet's like count has increased by 1
    tweet = Tweet.query.get(tweet.id)  # Get the tweet again after the action
    assert tweet.like_count == 1
    assert tweet.liked is True  # Check that the tweet's liked status is True
    
    # Check the response
    assert response.status_code == 200
    assert response.json['like_count'] == tweet.like_count
    assert response.json['liked'] is True


# Test unliking a tweet
def test_unlike_tweet(client, init_db):
    # Simulate a user login by adding the user to the session
    user = User.query.filter_by(username="testuser").first()
    tweet = Tweet.query.first()
    
    # Simulate liking the tweet first
    with client.session_transaction() as sess:
        sess['user_id'] = user.id
    client.post(f'/like/{tweet.id}', json={'action': 'like'})

    # Now, simulate unliking the tweet
    response = client.post(f'/like/{tweet.id}', json={'action': 'unlike'})
    
    # Assert that the tweet's like count has decreased by 1
    tweet = Tweet.query.get(tweet.id)
    assert tweet.like_count == 0
    assert tweet.liked is False  # Check that the tweet's liked status is False
    
    # Check the response
    assert response.status_code == 200
    assert response.json['like_count'] == tweet.like_count
    assert response.json['liked'] is False
    
# Test logout functionality
def test_logout(client, init_db):
    # Simulate a user login by adding the user to the session
    user = User.query.filter_by(username="testuser").first()
    
    # Directly manipulate the session
    with client.session_transaction() as sess:
        sess['user_id'] = user.id  # Simulate setting the session with the logged-in user's ID
    
    # Make a GET request to logout
    response = client.get('/logout')
    
    # Check if the session is cleared
    with client.session_transaction() as sess:
        assert 'user_id' not in sess  # Ensure the session no longer contains 'user_id'
    
    # Check if the user is redirected to the login page
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'
    
    # Test registration with a new username
def test_register_new_user(client, init_db):
    # Make a POST request with new user data
    response = client.post('/register', data=dict(username="newuser", password="testpassword"))
    
    # Check if the registration was successful and redirected to login
    assert response.status_code == 302  # Should redirect
    assert response.headers['Location'] == '/login'
    
    # Check if the new user exists in the database
    user = User.query.filter_by(username="newuser").first()
    assert user is not None
    assert user.username == "newuser"

# Test registration with an already existing username
def test_register_existing_user(client, init_db):
    # Add a user to the database manually for testing
    user = User(username="existinguser")
    user.set_password("testpassword")
    db.session.add(user)
    db.session.commit()

    # Try to register with the same username
    response = client.post('/register', data=dict(username="existinguser", password="newpassword"))
    
    # Check if it redirects back to the registration page with an error message
    assert response.status_code == 302  # Should redirect
    assert response.headers['Location'] == '/register'
    

    # Ensure the existing user is still in the database
    user = User.query.filter_by(username="existinguser").first()
    assert user is not None
    
# Test if the profile page is accessible by a logged-in user
def test_profile_logged_in(client, init_db):
    # Simulate logging in by adding user info to the session
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Assuming the user with ID 1 is the test user
        sess['username'] = "testuser"

    # Make a GET request to the /profile route
    response = client.get('/profile')
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the correct username is displayed on the profile page
    assert b"testuser" in response.data
