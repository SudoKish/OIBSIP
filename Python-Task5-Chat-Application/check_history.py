from database import get_message_history


print("\n===== GENERAL ROOM HISTORY =====")

messages = get_message_history("General")

if not messages:
    print("No messages found.")

else:
    for username, message, timestamp in messages:
        print(
            f"[{timestamp}] {username}: {message}"
        )


print("\n===== PYTHON ROOM HISTORY =====")

messages = get_message_history("Python")

if not messages:
    print("No messages found.")

else:
    for username, message, timestamp in messages:
        print(
            f"[{timestamp}] {username}: {message}"
        )