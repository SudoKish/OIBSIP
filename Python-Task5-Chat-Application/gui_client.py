import socket
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


HOST = "localhost"
PORT = 5555


class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Chat Application")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        self.client_socket = None
        self.connected = False
        self.username = ""

        self.create_widgets()

        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

    def create_widgets(self):

        # -------------------------------
        # Header
        # -------------------------------

        header = tk.Frame(self.root, padx=10, pady=10)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Python Chat Application",
            font=("Arial", 20, "bold")
        )
        title.pack()

        # -------------------------------
        # Login Section
        # -------------------------------

        login_frame = tk.Frame(self.root, padx=10, pady=5)
        login_frame.pack(fill="x")

        tk.Label(
            login_frame,
            text="Username:"
        ).pack(side="left")

        self.username_entry = tk.Entry(
            login_frame,
            width=20
        )
        self.username_entry.pack(side="left", padx=5)

        self.connect_button = tk.Button(
            login_frame,
            text="Connect",
            width=10,
            command=self.connect_to_server
        )
        self.connect_button.pack(side="left", padx=5)

        self.disconnect_button = tk.Button(
            login_frame,
            text="Disconnect",
            width=10,
            command=self.disconnect_from_server,
            state="disabled"
        )
        self.disconnect_button.pack(side="left", padx=5)

        # -------------------------------
        # Status
        # -------------------------------

        self.status_label = tk.Label(
            self.root,
            text="Status: Disconnected",
            anchor="w",
            padx=10
        )
        self.status_label.pack(fill="x")

        # -------------------------------
        # Chat Display
        # -------------------------------

        chat_frame = tk.Frame(self.root, padx=10, pady=5)
        chat_frame.pack(fill="both", expand=True)

        self.chat_display = tk.Text(
            chat_frame,
            height=20,
            width=80,
            state="disabled",
            wrap="word",
            font=("Arial", 11)
        )
        self.chat_display.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            chat_frame,
            command=self.chat_display.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.chat_display.config(
            yscrollcommand=scrollbar.set
        )

        # -------------------------------
        # Message Section
        # -------------------------------

        message_frame = tk.Frame(
            self.root,
            padx=10,
            pady=10
        )
        message_frame.pack(fill="x")

        self.message_entry = tk.Entry(
            message_frame,
            font=("Arial", 11)
        )
        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.send_button = tk.Button(
            message_frame,
            text="Send",
            width=10,
            command=self.send_message,
            state="disabled"
        )
        self.send_button.pack(side="right")

        # Press Enter to send
        self.message_entry.bind(
            "<Return>",
            self.send_message_event
        )

    # -------------------------------
    # Connect to Server
    # -------------------------------

    def connect_to_server(self):

        username = self.username_entry.get().strip()

        if not username:
            messagebox.showwarning(
                "Username Required",
                "Please enter a username."
            )
            return

        try:
            self.client_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.client_socket.connect(
                (HOST, PORT)
            )

            self.client_socket.send(
                username.encode("utf-8")
            )

            self.username = username
            self.connected = True

            self.status_label.config(
                text=f"Status: Connected as {username}"
            )

            self.username_entry.config(
                state="disabled"
            )

            self.connect_button.config(
                state="disabled"
            )

            self.disconnect_button.config(
                state="normal"
            )

            self.send_button.config(
                state="normal"
            )

            self.add_message(
                f"Connected to chat as {username}."
            )

            receive_thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )

            receive_thread.start()

            self.message_entry.focus()

        except ConnectionRefusedError:

            messagebox.showerror(
                "Connection Error",
                "Could not connect to the server.\n\n"
                "Make sure server.py is running."
            )

        except Exception as error:

            messagebox.showerror(
                "Connection Error",
                f"An error occurred:\n{error}"
            )

            self.close_socket()

    # -------------------------------
    # Receive Messages
    # -------------------------------

    def receive_messages(self):

        while self.connected:

            try:

                message = self.client_socket.recv(
                    1024
                ).decode("utf-8")

                if not message:
                    break

                self.root.after(
                    0,
                    self.add_message,
                    message
                )

            except (
                ConnectionResetError,
                ConnectionAbortedError,
                OSError
            ):
                break

        if self.connected:

            self.root.after(
                0,
                self.server_disconnected
            )

    # -------------------------------
    # Send Message
    # -------------------------------

    def send_message(self):

        if not self.connected:
            return

        message = self.message_entry.get().strip()

        if not message:
            return

        try:

            self.client_socket.send(
                message.encode("utf-8")
            )

            self.message_entry.delete(
                0,
                tk.END
            )

        except (
            ConnectionResetError,
            ConnectionAbortedError,
            OSError
        ):

            self.server_disconnected()

    def send_message_event(self, event):

        self.send_message()

    # -------------------------------
    # Display Message
    # -------------------------------

    def add_message(self, message):

        self.chat_display.config(
            state="normal"
        )

        self.chat_display.insert(
            tk.END,
            message + "\n"
        )

        self.chat_display.see(
            tk.END
        )

        self.chat_display.config(
            state="disabled"
        )

    # -------------------------------
    # Disconnect
    # -------------------------------

    def disconnect_from_server(self):

        if not self.connected:
            return

        self.connected = False

        try:
            self.client_socket.shutdown(
                socket.SHUT_RDWR
            )
        except OSError:
            pass

        self.close_socket()

        self.status_label.config(
            text="Status: Disconnected"
        )

        self.username_entry.config(
            state="normal"
        )

        self.connect_button.config(
            state="normal"
        )

        self.disconnect_button.config(
            state="disabled"
        )

        self.send_button.config(
            state="disabled"
        )

        self.add_message(
            "You disconnected from the chat."
        )

    # -------------------------------
    # Server Disconnected
    # -------------------------------

    def server_disconnected(self):

        self.connected = False

        self.close_socket()

        self.status_label.config(
            text="Status: Server disconnected"
        )

        self.username_entry.config(
            state="normal"
        )

        self.connect_button.config(
            state="normal"
        )

        self.disconnect_button.config(
            state="disabled"
        )

        self.send_button.config(
            state="disabled"
        )

        self.add_message(
            "Server connection closed."
        )

    # -------------------------------
    # Close Socket
    # -------------------------------

    def close_socket(self):

        if self.client_socket:

            try:
                self.client_socket.close()
            except OSError:
                pass

            self.client_socket = None

    # -------------------------------
    # Close Application
    # -------------------------------

    def close_application(self):

        if self.connected:
            self.connected = False

            try:
                self.client_socket.shutdown(
                    socket.SHUT_RDWR
                )
            except OSError:
                pass

            self.close_socket()

        self.root.destroy()


# -------------------------------
# Start GUI
# -------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = ChatGUI(root)

    root.mainloop()