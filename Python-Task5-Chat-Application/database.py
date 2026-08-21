import sqlite3
import hashlib
from datetime import datetime


DATABASE_NAME = "chat.db"


def connect_database():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def register_user(username, password):

    connection = connect_database()
    cursor = connection.cursor()

    password_hash = hash_password(password)
    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, password_hash, created_at)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, created_at)
        )

        connection.commit()

        return True, "Registration successful."

    except sqlite3.IntegrityError:

        return False, "Username already exists."

    finally:

        connection.close()


def login_user(username, password):

    connection = connect_database()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        AND password_hash = ?
        """,
        (username, password_hash)
    )

    user = cursor.fetchone()

    connection.close()

    if user:
        return True, "Login successful."

    return False, "Invalid username or password."

def create_rooms_table():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_default_room():
    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO rooms (room_name, created_at)
            VALUES (?, ?)
        """, (
            "General",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        connection.commit()

    except sqlite3.IntegrityError:
        # General room already exists
        pass

    finally:
        connection.close()


def create_room(room_name):

    room_name = room_name.strip()

    if not room_name:
        return False, "Room name cannot be empty."

    connection = connect_database()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO rooms (room_name, created_at)
            VALUES (?, ?)
        """, (
            room_name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        connection.commit()

        return True, "Room created successfully."

    except sqlite3.IntegrityError:

        return False, "Room already exists."

    finally:

        connection.close()


def get_rooms():

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT room_name
        FROM rooms
        ORDER BY room_name
    """)

    rooms = cursor.fetchall()

    connection.close()

    return [room[0] for room in rooms]


def room_exists(room_name):

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM rooms
        WHERE room_name = ?
    """, (room_name,))

    room = cursor.fetchone()

    connection.close()

    return room is not None
def create_messages_table():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_message(room_name, username, message, timestamp):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages (
            room_name,
            username,
            message,
            timestamp
        )
        VALUES (?, ?, ?, ?)
    """, (
        room_name,
        username,
        message,
        timestamp
    ))

    connection.commit()
    connection.close()


def get_message_history(room_name, limit=100):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT username, message, timestamp
        FROM messages
        WHERE room_name = ?
        ORDER BY id ASC
        LIMIT ?
    """, (
        room_name,
        limit
    ))

    messages = cursor.fetchall()

    connection.close()

    return messages


if __name__ == "__main__":
    create_tables()
    create_rooms_table()
    create_messages_table()
    create_default_room()

    print("Database initialized successfully.")