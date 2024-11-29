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

### Clone the repository:
   ```bash
   git clone [https://github.com/MilanHennessy/twotter_app.git]
   cd twitter-clone
  ```

### Create a virtual environment (optional):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Set up the database:

```bash
flask shell
>>> from extensions import db
>>> db.create_all()
>>> exit()
```

### Run the application:

```bash
flask run
```

By default, the app runs on `http://127.0.0.1:5000`.

### **Usage**

#### **User Workflow**
1. **Register**: 
   - Navigate to the `/register` page to create an account.
   - Provide a username and password.
   - Submit the form to register.

2. **Login**:
   - Navigate to the `/login` page to access your account.
   - Enter your username and password.
   - Upon successful login, you will be redirected to the home page.

3. **Home Page**:
   - The homepage displays:
     - User-created tweets.
     - Posts fetched from the JSONPlaceholder API.
   - You can create new tweets or interact with existing ones (like, update, or delete).

4. **Profile**:
   - Navigate to `/profile` to view your own tweets and liked posts.
   - Use options to update your username or delete your account.

5. **Tweet Management**:
   - Create a new tweet on the homepage or `/tweets`.
   - Update or delete your tweets by navigating to the respective tweet actions.

6. **Integration with JSONPlaceholder**:
   - Posts from the JSONPlaceholder API are displayed alongside tweets.
   - Posts include randomized usernames, timestamps, like counts, and top comments for demonstration.

---

### **Architecture**

#### **Backend**
- Built using **Flask**, a lightweight and modular Python web framework.
- Includes the following models:
  - **User**: Manages user credentials and authentication.
  - **Tweet**: Handles user-created tweets and tracks interactions.
  - **Like**: Establishes a many-to-many relationship between users and tweets.
- API integration with **JSONPlaceholder** to fetch and display placeholder posts.

#### **Frontend**
- HTML templates rendered using Flask's Jinja2 templating engine.
- Includes dynamic elements for displaying tweets and JSONPlaceholder posts.
- Utilizes Bootstrap (or custom CSS) for responsive design.

#### **Database**
- **SQLite** used as the relational database.
- Tables:
  - `users`: Stores user details (username, password hash).
  - `tweets`: Stores user-created tweets.
  - `likes`: Tracks which users liked specific tweets.

#### **Routes**
- Core functionalities are organized into routes for ease of navigation:
  - `/register`: User registration.
  - `/login`: User authentication.
  - `/`: Displays homepage with tweets and JSONPlaceholder posts.
  - `/profile`: User profile with personal tweets and liked posts.
  - `/tweets`: Create, update, or delete tweets.
  - `/like/<int:tweet_id>`: Like or unlike tweets.
  - `/update_username`: Update logged-in user’s username.
  - `/delete_account`: Delete the user account.
  - `/logout`: Log out of the application.

#### **Third-party Integration**
- The app fetches posts from the **JSONPlaceholder API** for demonstration purposes.
- Placeholder posts are enhanced with additional attributes like randomized usernames, timestamps, and comments.

---
### **Architecture Diagrams**

#### **1. UML Package Diagram**

The application follows the **Model-View-Controller (MVC)** architecture, where:

- **Model**: Handles data and database logic (e.g., `User`, `Tweet`, and `Like` models).
- **View**: Includes frontend templates rendered using Jinja2 (e.g., `index.html`, `profile.html`).
- **Controller**: Defines the application's logic and routes (e.g., Flask route handlers in `main.py`).

```plaintext
+--------------------+
|   Controller       |
|--------------------|
| - Flask Routes     |
| - JSONPlaceholder  |
+--------------------+
         |
         |
+--------------------+
|      View          |
|--------------------|
| - Jinja Templates  |
| - HTML/CSS/JS      |
+--------------------+
         |
         |
+--------------------+
|      Model         |
|--------------------|
| - User Model       |
| - Tweet Model      |
| - Like Model       |
| - Database (SQLite)|
+--------------------+

```

### **Deployment**

The application is deployed on **Render**, a modern cloud platform for hosting web applications. Render provides automatic deployment from a GitHub repository, making it easy to host and maintain the application.

#### **Screenshot**
Below is a screenshot of the live application:

![image](https://github.com/user-attachments/assets/3e6e710b-0cab-45a5-9a3e-aa634887ad60)

---

By hosting the app on Render, deployment is streamlined, and updates to the GitHub repository automatically trigger a new build and deployment, ensuring the app is always up to date.

