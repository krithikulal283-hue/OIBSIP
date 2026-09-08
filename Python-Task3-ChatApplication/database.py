import sqlite3
import hashlib
from datetime import datetime


DATABASE_NAME = "chat.db"


def get_connection():
    return sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Rooms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            room TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # Create default room
    cursor.execute("""
        INSERT OR IGNORE INTO rooms (name)
        VALUES (?)
    """, ("General",))

    connection.commit()
    connection.close()


def register_user(username, password):

    if not username or not password:
        return False, "Username and password are required."

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (
            username,
            hash_password(password)
        ))

        connection.commit()

        return True, "Registration successful."

    except sqlite3.IntegrityError:

        return False, "Username already exists."

    finally:

        connection.close()


def login_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT username
        FROM users
        WHERE username = ? AND password = ?
    """, (
        username,
        hash_password(password)
    ))

    user = cursor.fetchone()

    connection.close()

    if user:
        return True

    return False


def create_room(room_name):

    if not room_name.strip():
        return False, "Room name cannot be empty."

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO rooms (name)
            VALUES (?)
        """, (room_name.strip(),))

        connection.commit()

        return True, "Room created successfully."

    except sqlite3.IntegrityError:

        return False, "Room already exists."

    finally:

        connection.close()


def get_rooms():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM rooms
        ORDER BY name
    """)

    rooms = [
        row[0]
        for row in cursor.fetchall()
    ]

    connection.close()

    return rooms


def save_message(username, room, message):

    connection = get_connection()
    cursor = connection.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO messages
        (username, room, message, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        username,
        room,
        message,
        timestamp
    ))

    connection.commit()
    connection.close()


def get_messages(room, limit=50):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT username, message, timestamp
        FROM messages
        WHERE room = ?
        ORDER BY id DESC
        LIMIT ?
    """, (
        room,
        limit
    ))

    messages = cursor.fetchall()

    connection.close()

    # Return oldest first
    return list(reversed(messages))