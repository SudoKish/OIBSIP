import socket
import threading
from datetime import datetime

HOST = "localhost"
PORT = 5555

clients = {}
lock = threading.Lock()


def timestamp():
    return datetime.now().strftime("%H:%M")


def broadcast(message, sender=None):
    with lock:
        disconnected_clients = []

        for client in list(clients.keys()):
            if client != sender:
                try:
                    client.send(message.encode("utf-8"))
                except (ConnectionResetError, ConnectionAbortedError, OSError):
                    disconnected_clients.append(client)

        for client in disconnected_clients:
            clients.pop(client, None)


def handle_client(client_socket, address):
    username = None

    try:
        username = client_socket.recv(1024).decode("utf-8").strip()

        if not username:
            return

        with lock:
            clients[client_socket] = username

        join_message = f"[{timestamp()}] {username} joined the chat."
        print(join_message)
        broadcast(join_message, client_socket)

        while True:
            message = client_socket.recv(1024).decode("utf-8")

            if not message:
                break

            formatted_message = f"[{timestamp()}] {username}: {message}"
            print(formatted_message)
            broadcast(formatted_message, client_socket)

    except (ConnectionResetError, ConnectionAbortedError, OSError):
        pass

    finally:
        with lock:
            clients.pop(client_socket, None)

        try:
            client_socket.close()
        except OSError:
            pass

        if username:
            disconnect_message = f"[{timestamp()}] {username} disconnected."
            print(disconnect_message)
            broadcast(disconnect_message)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)

    # Short timeout allows clean Ctrl+C handling
    server.settimeout(0.5)

    print("=" * 45)
    print("        CHAT APPLICATION SERVER")
    print("=" * 45)
    print(f"Server running on {HOST}:{PORT}")
    print("Waiting for clients...")
    print("Press Ctrl+C to stop the server.")
    print("=" * 45)

    try:
        while True:
            try:
                client_socket, address = server.accept()

                thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, address),
                    daemon=True
                )

                thread.start()

            except socket.timeout:
                pass

    except KeyboardInterrupt:
        print("\nServer shutting down...")

    finally:
        with lock:
            connected_clients = list(clients.keys())

        for client in connected_clients:
            try:
                client.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

            try:
                client.close()
            except OSError:
                pass

        server.close()

        print("Server stopped.")


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        pass