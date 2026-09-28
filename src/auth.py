"""
auth.py
-------
User authentication and favorites management using SQLite.

Features:
- Secure SHA-256 password hashing
- User Registration & Login
- Guest Mode support
- Bookmark / Save Favorite Recipes
"""

import hashlib
import os
import sqlite3
from typing import List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "users.db")


def hash_password(password: str) -> str:
    """Returns SHA-256 hash of password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_connection():
    """Returns a connection to the SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn


def init_db():
    """Initializes users and favorites tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            recipe_name TEXT NOT NULL,
            category TEXT,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, recipe_name)
        )
    """)
    conn.commit()
    conn.close()


def register_user(username: str, password: str, full_name: str) -> Tuple[bool, str]:
    """Registers a new user."""
    if not username or not password or not full_name:
        return False, "All fields are required."

    username = username.strip().lower()
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."

    pwd_hash = hash_password(password)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, full_name) VALUES (?, ?, ?)",
            (username, pwd_hash, full_name.strip())
        )
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose another."
    except Exception as e:
        return False, f"Registration error: {e}"


def login_user(username: str, password: str) -> Tuple[bool, Optional[dict], str]:
    """Logs in an existing user."""
    if not username or not password:
        return False, None, "Please enter both username and password."

    username = username.strip().lower()
    pwd_hash = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, full_name, password_hash FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, None, "User not found. Please sign up first."

    if row[3] != pwd_hash:
        return False, None, "Incorrect password."

    user_data = {
        "id": row[0],
        "username": row[1],
        "full_name": row[2]
    }
    return True, user_data, "Login successful!"


def toggle_favorite(username: str, recipe_name: str, category: str = "") -> bool:
    """Toggles bookmarking a recipe for a user."""
    if not username or username == "guest":
        return False

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM favorites WHERE username = ? AND recipe_name = ?",
        (username, recipe_name)
    )
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            "DELETE FROM favorites WHERE username = ? AND recipe_name = ?",
            (username, recipe_name)
        )
        is_fav = False
    else:
        cursor.execute(
            "INSERT INTO favorites (username, recipe_name, category) VALUES (?, ?, ?)",
            (username, recipe_name, category)
        )
        is_fav = True

    conn.commit()
    conn.close()
    return is_fav


def get_favorites(username: str) -> List[str]:
    """Returns list of favorite recipe names for a user."""
    if not username or username == "guest":
        return []

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT recipe_name FROM favorites WHERE username = ? ORDER BY saved_at DESC",
        (username,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]


# Initialize DB upon module load
init_db()
