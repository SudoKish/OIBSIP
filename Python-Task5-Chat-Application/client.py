import socket
import threading
from datetime import datetime

HOST = "localhost"
PORT = 5555


def timestamp():
    return datetime.now().strftime("%H:%M")


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")

            if not message:
                print("\nServer connection closed.")
                break

            print(f"\n{message}")
            print("You: ", end="", flush=True)

        except (ConnectionResetError, ConnectionAbortedError, OSError):
            print("\nDisconnected from the server.")
            break


def start_client():
    username = input("Enter your username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))

        client_socket.send(username.encode("utf-8"))

        print("=" * 45)
        print("       WELCOME TO THE CHAT")
        print("=" * 45)
        print(f"Connected as: {username}")
        print("Type your message and press Enter.")
        print("Type 'exit' to leave the chat.")
        print("=" * 45)

        receive_thread = threading.Thread(
            target=receive_messages,
            args=(client_socket,)
        )

        receive_thread.daemon = True
        receive_thread.start()

        while True:
            message = input("You: ")

            if message.lower() == "exit":
                print("Leaving the chat...")
                break

            if message.strip():
                client_socket.send(message.encode("utf-8"))

    except ConnectionRefusedError:
        print("Could not connect to the server.")
        print("Make sure server.py is running first.")

    except KeyboardInterrupt:
        print("\nLeaving the chat...")

    finally:
        client_socket.close()
        print("Connection closed.")


if __name__ == "__main__":
    start_client()