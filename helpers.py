import random
import requests

# JSONPlaceholder API Base URL
API_BASE_URL = "https://jsonplaceholder.typicode.com"

# Function to fetch a random username from JSONPlaceholder users
def generate_random_username():
    response = requests.get(f"{API_BASE_URL}/users")
    users = []
    if response.status_code == 200:
        users = response.json()

    # Pick a random user from the list
    random_user = random.choice(users)
    return random_user['username']  # Return the username


# Function to generate random like counts
def generate_random_like_count():
    # Create a random number between 0 and 100
    likes = random.randint(0, 10000)
    # You can append random suffixes or modify it to your liking
    return f"{likes}"  # Returns a string like "12K" or "99M"


# Fetch posts with usernames
def get_tweets(user_id):
    # Fetch user data (usernames) from JSONPlaceholder
    response_user = requests.get(f"{API_BASE_URL}/users/{user_id}")
    user = None
    if response_user.status_code == 200:
        user = response_user.json()

    # Fetch posts (tweets) from JSONPlaceholder API
    response_posts = requests.get(f"{API_BASE_URL}/posts", params={"userId": user_id})
    posts = []
    if response_posts.status_code == 200:
        posts = response_posts.json()
        for post in posts:
            # Assign the correct username to each post
            post['username'] = generate_random_username()
            post['likeCount'] = generate_random_like_count()  # Using the new function for random like count
            post['timestamp'] = '2024-11-26 12:00:00'  # Mock timestamp

    return user, posts
