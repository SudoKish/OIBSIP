import tkinter as tk
from tkinter import messagebox
import socket
import threading

from database import create_tables, register_user, login_user


HOST = "localhost"
PORT = 5555


class AdvancedChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Chat Application")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        self.client_socket = None
        self.connected = False
        self.username = ""

        create_tables()

        self.show_login_screen()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    # ==========================================
    # Clear Window
    # ==========================================

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================
    # LOGIN SCREEN
    # ==========================================

    def show_login_screen(self):

        self.clear_window()

        self.root.title("Chat Application - Login")

        title = tk.Label(
            self.root,
            text="Python Chat Application",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(40, 10))

        subtitle = tk.Label(
            self.root,
            text="Login to your account",
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 25))

        # Username

        tk.Label(
            self.root,
            text="Username",
            font=("Arial", 11)
        ).pack(anchor="w", padx=150)

        self.username_entry = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 11)
        )
        self.username_entry.pack(
            padx=150,
            pady=(5, 15)
        )

        # Password

        tk.Label(
            self.root,
            text="Password",
            font=("Arial", 11)
        ).pack(anchor="w", padx=150)

        self.password_entry = tk.Entry(
            self.root,
            width=30,
            show="*",
            font=("Arial", 11)
        )
        self.password_entry.pack(
            padx=150,
            pady=(5, 20)
        )

        # Login

        tk.Button(
            self.root,
            text="Login",
            width=20,
            height=2,
            command=self.login
        ).pack(pady=10)

        # Register

        tk.Label(
            self.root,
            text="Don't have an account?",
            font=("Arial", 10)
        ).pack(pady=(25, 5))

        tk.Button(
            self.root,
            text="Create Account",
            width=20,
            command=self.show_register_screen
        ).pack()

        self.username_entry.focus()

    # ==========================================
    # REGISTER SCREEN
    # ==========================================

    def show_register_screen(self):

        self.clear_window()

        self.root.title("Chat Application - Register")

        title = tk.Label(
            self.root,
            text="Create Account",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(35, 25))

        # Username

        tk.Label(
            self.root,
            text="Username",
            font=("Arial", 11)
        ).pack(anchor="w", padx=150)

        self.register_username = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 11)
        )
        self.register_username.pack(
            padx=150,
            pady=(5, 15)
        )

        # Password

        tk.Label(
            self.root,
            text="Password",
            font=("Arial", 11)
        ).pack(anchor="w", padx=150)

        self.register_password = tk.Entry(
            self.root,
            width=30,
            show="*",
            font=("Arial", 11)
        )
        self.register_password.pack(
            padx=150,
            pady=(5, 15)
        )

        # Confirm Password

        tk.Label(
            self.root,
            text="Confirm Password",
            font=("Arial", 11)
        ).pack(anchor="w", padx=150)

        self.register_confirm = tk.Entry(
            self.root,
            width=30,
            show="*",
            font=("Arial", 11)
        )
        self.register_confirm.pack(
            padx=150,
            pady=(5, 20)
        )

        # Register

        tk.Button(
            self.root,
            text="Register",
            width=20,
            height=2,
            command=self.register
        ).pack(pady=10)

        # Back

        tk.Button(
            self.root,
            text="Back to Login",
            width=20,
            command=self.show_login_screen
        ).pack(pady=10)

        self.register_username.focus()

    # ==========================================
    # REGISTER
    # ==========================================

    def register(self):

        username = self.register_username.get().strip()
        password = self.register_password.get()
        confirm_password = self.register_confirm.get()

        if not username or not password or not confirm_password:

            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )

            return

        if password != confirm_password:

            messagebox.showerror(
                "Password Error",
                "Passwords do not match."
            )

            return

        if len(password) < 6:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 6 characters."
            )

            return

        success, message = register_user(
            username,
            password
        )

        if success:

            messagebox.showinfo(
                "Registration Successful",
                "Account created successfully!"
            )

            self.show_login_screen()

            self.username_entry.insert(
                0,
                username
            )

        else:

            messagebox.showerror(
                "Registration Failed",
                message
            )

    # ==========================================
    # LOGIN
    # ==========================================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )

            return

        success, message = login_user(
            username,
            password
        )

        if success:

            self.username = username

            self.show_chat_screen()

        else:

            messagebox.showerror(
                "Login Failed",
                message
            )

    # ==========================================
    # CHAT SCREEN
    # ==========================================

    def show_chat_screen(self):

        self.clear_window()

        self.root.title(
            f"Python Chat Application - {self.username}"
        )

        # Header

        header = tk.Frame(
            self.root,
            padx=10,
            pady=10
        )
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Python Chat Application",
            font=("Arial", 20, "bold")
        )
        title.pack()

        # User information

        user_label = tk.Label(
            header,
            text=f"Logged in as: {self.username}",
            font=("Arial", 10)
        )
        user_label.pack()

        # Chat area

        chat_frame = tk.Frame(
            self.root,
            padx=10,
            pady=5
        )
        chat_frame.pack(
            fill="both",
            expand=True
        )

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
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.chat_display.config(
            yscrollcommand=scrollbar.set
        )

        # Message section

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
            command=self.send_message
        )
        self.send_button.pack(side="right")

        self.message_entry.bind(
            "<Return>",
            self.send_message_event
        )

        # Bottom buttons

        bottom_frame = tk.Frame(
            self.root,
            pady=5
        )
        bottom_frame.pack(fill="x")

        tk.Button(
            bottom_frame,
            text="Logout",
            width=12,
            command=self.logout
        ).pack()

        # Connect to existing server

        self.connect_to_server()

    # ==========================================
    # CONNECT TO EXISTING SERVER
    # ==========================================

    def connect_to_server(self):

        try:

            self.client_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.client_socket.connect(
                (HOST, PORT)
            )

            self.client_socket.send(
                self.username.encode("utf-8")
            )

            self.connected = True

            self.add_message(
                f"Connected to chat as {self.username}."
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

            self.logout()

        except Exception as error:

            messagebox.showerror(
                "Connection Error",
                f"An error occurred:\n{error}"
            )

            self.logout()

    # ==========================================
    # RECEIVE MESSAGES
    # ==========================================

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

    # ==========================================
    # SEND MESSAGE
    # ==========================================

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

    # ==========================================
    # DISPLAY MESSAGE
    # ==========================================

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

    # ==========================================
    # SERVER DISCONNECTED
    # ==========================================

    def server_disconnected(self):

        self.connected = False

        self.close_socket()

        self.add_message(
            "Server connection closed."
        )

    # ==========================================
    # LOGOUT
    # ==========================================

    def logout(self):

        self.connected = False

        self.close_socket()

        self.username = ""

        self.show_login_screen()

    # ==========================================
    # CLOSE SOCKET
    # ==========================================

    def close_socket(self):

        if self.client_socket:

            try:
                self.client_socket.shutdown(
                    socket.SHUT_RDWR
                )
            except OSError:
                pass

            try:
                self.client_socket.close()
            except OSError:
                pass

            self.client_socket = None

    # ==========================================
    # CLOSE APPLICATION
    # ==========================================

    def close_application(self):

        self.connected = False

        self.close_socket()

        self.root.destroy()


# ==============================================
# START APPLICATION
# ==============================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AdvancedChatApp(root)

    root.mainloop()