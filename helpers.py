import random
import requests
from datetime import datetime

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
    # Create a random number between 0 and 10000
    likes = random.randint(0, 10000)
    # You can append random suffixes or modify it to your liking
    return f"{likes}"  # Returns a string like "12K" or "99M"


def generate_random_username():
    # A pool of random usernames for diversity
    return random.choice([
        "SkyDiver12", "CoolCat", "SpaceExplorer", "SunsetLover", "OceanBreeze",
        "MountainClimber", "TechGuru", "FoodieLife", "GameMaster", "ArtisticSoul"
    ])

def get_tweets(num_posts=5):
    try:
        # Fetch all posts from JSONPlaceholder
        response_posts = requests.get(f"{API_BASE_URL}/posts")
        if response_posts.status_code != 200:
            print("Failed to fetch posts. Returning an empty list.")
            return []

        posts = response_posts.json()
        # Shuffle posts to randomize their order
        random.shuffle(posts)
        selected_posts = posts[:num_posts]

        # Enrich posts with random usernames, like counts, and timestamps
        enriched_posts = []
        for post in selected_posts:
            enriched_posts.append({
                'username': generate_random_username(),
                'body': post['body'],
                'likeCount': generate_random_like_count(),
                'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            })

        return enriched_posts

    except Exception as e:
        print(f"An error occurred: {e}")
        return []