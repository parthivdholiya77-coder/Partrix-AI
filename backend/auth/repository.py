from backend.database.connection import conn
from werkzeug.security import generate_password_hash, check_password_hash

def signup(username, email, password):
    """
    Create a new user account.
    Returns (True, user_id) on success.
    Returns (False, error_message) on failure.
    """

    cur = conn.execute(
        """
        SELECT id
        FROM users
        WHERE username = ? OR email = ?
        """,
        (username, email),
    )

    if cur.fetchone():
        return False, "Username or email already exists."

    hashed_password = generate_password_hash(password)

    cur = conn.execute(
        """
        INSERT INTO users(username, email, password)
        VALUES (?, ?, ?)
        """,
        (username, email, hashed_password),
    )

    conn.commit()

    return True, cur.lastrowid

def login(email, password):
    """
    Login using email.
    Returns (True, user_data) on success.
    Returns (False, message) on failure.
    """

    cur = conn.execute(
        """
        SELECT id, username, email, password
        FROM users
        WHERE email = ?
        """,
        (email,),
    )

    user = cur.fetchone()

    if not user:
        return False, "User not found."

    user_id, username, email, hashed_password = user

    if not check_password_hash(hashed_password, password):
        return False, "Incorrect password."

    return True, {
        "id": user_id,
        "username": username,
        "email": email,
    }