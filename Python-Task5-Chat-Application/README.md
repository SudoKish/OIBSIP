# Python Chat Application

A real-time chat application developed in Python as part of the Oasis Infobyte Python Programming Internship — Task 5.

The project includes both a beginner socket-based command-line implementation and an advanced GUI-based chat application with authentication, multiple rooms, persistent message history, desktop notifications, and emoji shortcode support.

## Features

### Beginner Version

* Socket-based client-server communication
* Real-time bidirectional messaging
* Two-user chat support
* Timestamped messages
* Username identification
* Join and disconnect notifications
* Graceful client disconnection
* Localhost support
* Thread-based concurrent client handling

### Advanced Version

* Tkinter graphical chat interface
* User registration and login
* SQLite database
* Password hashing
* Multiple chat rooms
* Room creation and joining
* Room-specific messaging
* Persistent message history
* Automatic message history loading
* Desktop notifications for new messages
* Emoji shortcode conversion
* Security transparency documentation

## Technologies Used

* Python
* Socket Programming
* Threading
* Tkinter
* SQLite3
* hashlib
* Plyer
* datetime

## Project Structure

```text
Python-Task5-Chat-Application/
│
├── server.py
├── client.py
│
├── advanced_server.py
├── advance_gui.py
├── advanced_app.py
├── auth_gui.py
│
├── database.py
├── notifications.py
├── emoji.py
│
├── test_database.py
├── test_rooms.py
├── test_messages.py
├── test_notifications.py
├── test_emoji.py
├── check_history.py
│
├── README.md
├── .gitignore
└── chat.db
```

> `chat.db` is generated locally and is excluded from Git using `.gitignore`.

## Beginner Application

The beginner application uses:

```text
server.py
client.py
```

The server listens on:

```text
localhost:5555
```

### Run the server

```bash
python server.py
```

### Run a client

Open another terminal:

```bash
python client.py
```

Open a second terminal for another user:

```bash
python client.py
```

Enter different usernames and begin chatting.

## Advanced Application

The advanced application uses a separate server and port so that the original beginner implementation remains preserved.

```text
Advanced Server
localhost:5556
```

### Start the advanced server

```bash
python advanced_server.py
```

### Start the advanced GUI

Open another terminal:

```bash
python advance_gui.py
```

Register or log in using an existing account.

## Authentication

User registration and login are implemented using SQLite.

The database contains a `users` table with:

```text
id
username
password_hash
created_at
```

Passwords are not stored directly as plain-text passwords. The application stores a SHA-256 hash of the password.

## Multiple Chat Rooms

Users can create and join named chat rooms.

The default room is:

```text
General
```

Users can create additional rooms such as:

```text
Python
Projects
Random
```

Messages are associated with their respective rooms.

## Message History

Messages are stored in the SQLite database so that room history can be retrieved later.

The `messages` table contains:

```text
id
room_name
username
message
timestamp
```

When a user joins a room, previously stored messages from that room are loaded into the GUI.

## Desktop Notifications

The application uses `plyer` to provide desktop notifications.

When the chat window is not focused and a new message arrives, a desktop notification can be displayed.

Install the dependency with:

```bash
pip install plyer
```

## Emoji Support

Common emoji shortcodes are converted to Unicode emoji.

Examples:

```text
:smile:      → 😄
:heart:      → ❤️
:fire:       → 🔥
:thumbsup:   → 👍
:rocket:     → 🚀
:party:      → 🎉
```

For example:

```text
Hello :smile: :rocket:
```

is displayed as:

```text
Hello 😄 🚀
```

## Security Transparency

### Password Storage

Passwords are not stored as plain-text values in the database.

The current implementation hashes passwords using SHA-256 before storing the resulting hash.

For a production authentication system, a dedicated password hashing algorithm such as Argon2, bcrypt, or scrypt would be preferable.

### Message Storage

Chat messages are stored in the local SQLite database to provide persistent message history.

The stored message data includes:

* Room name
* Username
* Message content
* Timestamp

### What Is Not Encrypted

This project does **not implement end-to-end encryption**.

Messages stored in the SQLite database are not encrypted. Anyone who obtains access to the database file may potentially read the stored messages.

The socket communication is also not protected with TLS/SSL in the current implementation.

Therefore, this project should be considered an educational/demo application rather than a production-grade secure messaging platform.

### Database Security

The local database file contains application data and should not be publicly shared.

For this reason:

```text
*.db
```

is included in `.gitignore`.

## Requirements

Python 3.x is required.

The project primarily uses Python standard-library modules.

The advanced notification feature additionally requires:

```text
plyer
```

Install it using:

```bash
pip install plyer
```

## Testing

The project contains separate test scripts for major components:

```text
test_database.py
test_rooms.py
test_messages.py
test_notifications.py
test_emoji.py
check_history.py
```

These were used to verify the database, authentication, rooms, message history, notifications, and emoji conversion features independently.

## Advanced Feature Checklist

* [x] GUI chat window built with Tkinter
* [x] User registration and login
* [x] Username and password stored using SQLite
* [x] Password hashing
* [x] Multiple chat rooms
* [x] Users can create rooms
* [x] Users can join rooms
* [x] Room-specific messaging
* [x] Message history
* [x] Previous messages loaded when joining a room
* [x] Desktop notifications for new messages when the window is not focused
* [x] Emoji shortcode support
* [x] Security transparency documentation
* [x] Documentation of message storage
* [x] Documentation of what is not encrypted

## Learning Outcomes

This project demonstrates practical implementation of:

* Python socket programming
* Client-server architecture
* Multithreading
* GUI development with Tkinter
* SQLite database management
* User authentication
* Password hashing
* Persistent data storage
* Real-time communication
* Room-based messaging
* Desktop notifications
* Unicode and emoji handling
* Basic security awareness
