import socket
import threading
from datetime import datetime

from database import (
    create_tables,
    create_rooms_table,
    create_messages_table,
    create_default_room,
    get_rooms,
    room_exists,
    save_message,
    get_message_history,
    create_room
)


HOST = "localhost"
PORT = 5556

clients = {}
lock = threading.Lock()


def timestamp():
    return datetime.now().strftime("%H:%M")


def send_message(client_socket, message):
    try:
        client_socket.send(
            (message + "\n").encode("utf-8")
        )
        return True

    except (
        ConnectionResetError,
        ConnectionAbortedError,
        OSError
    ):
        return False


def broadcast_to_room(message, room_name, sender=None):
    disconnected_clients = []

    with lock:
        current_clients = list(clients.items())

    for client_socket, client_info in current_clients:

        if client_info["room"] != room_name:
            continue

        if client_socket == sender:
            continue

        if not send_message(client_socket, message):
            disconnected_clients.append(client_socket)

    for client_socket in disconnected_clients:
        remove_client(client_socket)


def remove_client(client_socket):

    with lock:
        client_info = clients.pop(client_socket, None)

    try:
        client_socket.close()
    except OSError:
        pass

    return client_info


def handle_client(client_socket, address):

    username = None
    room_name = "General"

    try:

        # Receive username
        username = client_socket.recv(1024).decode("utf-8").strip()

        if not username:
            client_socket.close()
            return

        # Store client
        with lock:
            clients[client_socket] = {
                "username": username,
                "room": room_name
            }

        print(
            f"[{timestamp()}] "
            f"{username} connected from {address}"
        )

        # Send available rooms
        rooms = get_rooms()

        rooms_message = (
            "ROOMS:"
            + "|".join(rooms)
        )

        send_message(
            client_socket,
            rooms_message
        )

        # Join notification
        join_message = (
            f"[{timestamp()}] "
            f"{username} joined #{room_name}."
        )

        print(join_message)

        broadcast_to_room(
            join_message,
            room_name,
            client_socket
        )

        # Receive messages
        while True:

            data = client_socket.recv(4096)

            if not data:
                break

            message = data.decode("utf-8").strip()

            if not message:
                continue

            # Room command
            if message.startswith("/join "):

                requested_room = (
                    message[6:].strip()
                )

                if not room_exists(requested_room):

                    send_message(
                        client_socket,
                        "ERROR:Room does not exist."
                    )

                    continue

                old_room = room_name

                room_name = requested_room

                with lock:
                    if client_socket in clients:
                        clients[client_socket]["room"] = room_name

                leave_message = (
                    f"[{timestamp()}] "
                    f"{username} left #{old_room}."
                )

                broadcast_to_room(
                    leave_message,
                    old_room,
                    client_socket
                )

                join_message = (
                    f"[{timestamp()}] "
                    f"{username} joined #{room_name}."
                )

                send_message(
                    client_socket,
                    f"SYSTEM:{join_message}"
                )

                # Load previous messages for the room
                history = get_message_history(
                    room_name,
                    100
                )

                for username_history, message_history, time_history in history:

                    history_message = (
                        f"[{time_history}] "
                        f"{username_history}: "
                        f"{message_history}"
                    )

                    send_message(
                        client_socket,
                        f"HISTORY:{history_message}"
                    )

                broadcast_to_room(
                    join_message,
                    room_name,
                    client_socket
                )

                print(join_message)

                continue

            # Create room
            if message.startswith("/create "):

                new_room = message[8:].strip()

                if not new_room:
                    send_message(
                        client_socket,
                        "ERROR:Room name cannot be empty."
                    )
                    continue

                from database import create_room

                success, result = create_room(new_room)

                if success:

                    send_message(
                        client_socket,
                        f"ROOM_CREATED:{new_room}"
                    )

                    # Send updated room list
                    rooms = get_rooms()

                    send_message(
                        client_socket,
                        "ROOMS:"
                        + "|".join(rooms)
                    )

                    print(
                        f"[{timestamp()}] "
                        f"{username} created room #{new_room}"
                    )

                else:

                    send_message(
                        client_socket,
                        f"ERROR:{result}"
                    )

                continue

            # Room listing
            if message == "/rooms":

                rooms = get_rooms()

                send_message(
                    client_socket,
                    "ROOMS:"
                    + "|".join(rooms)
                )

                continue

            # Normal message


            message_time = timestamp()

            formatted_message = (
                f"[{message_time}] "
                f"{username}: {message}"
            )

            # Save message to SQLite
            save_message(
                room_name,
                username,
                message,
                message_time
            )

            print(
                f"#{room_name} {formatted_message}"
            )

            broadcast_to_room(
                formatted_message,
                room_name,
                client_socket
            )
    except (
        ConnectionResetError,
        ConnectionAbortedError,
        OSError
    ):
        pass

    finally:

        client_info = remove_client(
            client_socket
        )

        if client_info:

            username = client_info["username"]
            room_name = client_info["room"]

            disconnect_message = (
                f"[{timestamp()}] "
                f"{username} disconnected."
            )

            print(disconnect_message)

            broadcast_to_room(
                disconnect_message,
                room_name
            )


def start_server():

    create_tables()
    create_rooms_table()
    create_messages_table()
    create_default_room()

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (HOST, PORT)
    )

    server.listen(10)

    # Allows clean Ctrl+C handling
    server.settimeout(0.5)

    print("=" * 50)
    print("        ADVANCED CHAT SERVER")
    print("=" * 50)
    print(f"Server running on {HOST}:{PORT}")
    print("Default room: General")
    print("Waiting for clients...")
    print("Press Ctrl+C to stop the server.")
    print("=" * 50)

    try:

        while True:

            try:

                client_socket, address = (
                    server.accept()
                )

                thread = threading.Thread(
                    target=handle_client,
                    args=(
                        client_socket,
                        address
                    ),
                    daemon=True
                )

                thread.start()

            except socket.timeout:
                pass

    except KeyboardInterrupt:

        print("\nAdvanced server shutting down...")

    finally:

        with lock:
            connected_clients = list(
                clients.keys()
            )

        for client_socket in connected_clients:

            try:
                client_socket.shutdown(
                    socket.SHUT_RDWR
                )
            except OSError:
                pass

            try:
                client_socket.close()
            except OSError:
                pass

        server.close()

        print("Advanced server stopped.")


if __name__ == "__main__":

    try:
        start_server()
    except KeyboardInterrupt:
        pass