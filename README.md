# Twitter Clone with JSONPlaceholder API Integration

This project is a **Twitter-like application** built with **Flask**. It features essential functionality for creating, viewing, and managing tweets while integrating with the **JSONPlaceholder API** to display external posts. The app also includes features like user authentication, likes, and account management.

## Features

- **User Authentication**: 
  - Register, login, and logout functionality.
  - Session management to protect user-specific actions.

- **Tweets**:
  - Create, update, and delete tweets.
  - Like/unlike tweets with real-time updates on like counts.

- **External Posts**: 
  - Fetch and display posts from [JSONPlaceholder](https://jsonplaceholder.typicode.com/).
  - Randomized usernames and like counts for external posts.

- **User Profile**:
  - View tweets authored by the logged-in user.
  - See tweets liked by the user.

- **Account Management**:
  - Update username.
  - Delete account and associated tweets/likes.

## Requirements

Ensure you have the following installed:

- Python 3.8 or later
- Virtualenv (optional but recommended)

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/twitter-clone.git
   cd twitter-clone
