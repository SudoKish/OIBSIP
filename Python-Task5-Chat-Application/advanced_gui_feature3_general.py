import socket
import threading
import tkinter as tk
from tkinter import messagebox

from database import create_tables, login_user


HOST = "localhost"
PORT = 5556


class AdvancedChatGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Advanced Python Chat")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.client_socket = None
        self.connected = False
        self.username = ""
        self.current_room = "General"

        create_tables()

        self.show_login_screen()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    # ==========================================
    # CLEAR WINDOW
    # ==========================================

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================
    # LOGIN SCREEN
    # ==========================================

    def show_login_screen(self):

        self.clear_window()

        self.root.title(
            "Advanced Chat - Login"
        )

        title = tk.Label(
            self.root,
            text="Advanced Python Chat",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=(50, 10))

        subtitle = tk.Label(
            self.root,
            text="Login to continue",
            font=("Arial", 12)
        )

        subtitle.pack(pady=(0, 30))

        # Username

        tk.Label(
            self.root,
            text="Username",
            font=("Arial", 11)
        ).pack(anchor="w", padx=220)

        self.username_entry = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 11)
        )

        self.username_entry.pack(
            padx=220,
            pady=(5, 15)
        )

        # Password

        tk.Label(
            self.root,
            text="Password",
            font=("Arial", 11)
        ).pack(anchor="w", padx=220)

        self.password_entry = tk.Entry(
            self.root,
            width=30,
            show="*",
            font=("Arial", 11)
        )

        self.password_entry.pack(
            padx=220,
            pady=(5, 20)
        )

        # Login button

        tk.Button(
            self.root,
            text="Login",
            width=20,
            height=2,
            command=self.login
        ).pack(pady=10)

        self.username_entry.focus()

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

        if not success:

            messagebox.showerror(
                "Login Failed",
                message
            )

            return

        self.username = username

        self.connect_to_advanced_server()

    # ==========================================
    # CONNECT TO ADVANCED SERVER
    # ==========================================

    def connect_to_advanced_server(self):

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

            self.show_chat_screen()

            receive_thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )

            receive_thread.start()

        except ConnectionRefusedError:

            messagebox.showerror(
                "Connection Error",
                "Could not connect to the advanced server.\n\n"
                "Make sure advanced_server.py is running."
            )

            self.close_socket()

        except Exception as error:

            messagebox.showerror(
                "Connection Error",
                str(error)
            )

            self.close_socket()

    # ==========================================
    # CHAT SCREEN
    # ==========================================

    def show_chat_screen(self):

        self.clear_window()

        self.root.title(
            f"Advanced Chat - {self.username}"
        )

        # ======================================
        # HEADER
        # ======================================

        header = tk.Frame(
            self.root,
            padx=10,
            pady=10
        )

        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Advanced Python Chat",
            font=("Arial", 20, "bold")
        )

        title.pack()

        user_label = tk.Label(
            header,
            text=f"Logged in as: {self.username}",
            font=("Arial", 10)
        )

        user_label.pack()

        # ======================================
        # MAIN AREA
        # ======================================

        main_frame = tk.Frame(
            self.root,
            padx=10,
            pady=5
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ======================================
        # ROOM PANEL
        # ======================================

        room_frame = tk.Frame(
            main_frame,
            width=180,
            relief="groove",
            borderwidth=1
        )

        room_frame.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        room_frame.pack_propagate(False)

        tk.Label(
            room_frame,
            text="CHAT ROOMS",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        self.room_listbox = tk.Listbox(
            room_frame,
            width=20,
            height=20,
            font=("Arial", 11)
        )

        self.room_listbox.pack(
            padx=10,
            pady=5,
            fill="both",
            expand=True
        )

        # ======================================
        # CHAT AREA
        # ======================================

        chat_frame = tk.Frame(
            main_frame
        )

        chat_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.room_title = tk.Label(
            chat_frame,
            text="# General",
            font=("Arial", 14, "bold"),
            anchor="w"
        )

        self.room_title.pack(
            fill="x",
            pady=(0, 5)
        )

        self.chat_display = tk.Text(
            chat_frame,
            height=20,
            width=60,
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

        # ======================================
        # MESSAGE INPUT
        # ======================================

        message_frame = tk.Frame(
            self.root,
            padx=10,
            pady=10
        )

        message_frame.pack(
            fill="x"
        )

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

        self.send_button.pack(
            side="right"
        )

        self.message_entry.bind(
            "<Return>",
            self.send_message_event
        )

        self.message_entry.focus()

        # ======================================
        # BOTTOM
        # ======================================

        bottom_frame = tk.Frame(
            self.root,
            pady=5
        )

        bottom_frame.pack(
            fill="x"
        )

        self.status_label = tk.Label(
            bottom_frame,
            text="Connected | Room: General",
            anchor="w",
            padx=10
        )

        self.status_label.pack(
            side="left"
        )

        tk.Button(
            bottom_frame,
            text="Logout",
            width=12,
            command=self.logout
        ).pack(
            side="right",
            padx=10
        )

    # ==========================================
    # RECEIVE MESSAGES
    # ==========================================

    def receive_messages(self):

        while self.connected:

            try:

                message = self.client_socket.recv(
                    4096
                ).decode("utf-8")

                if not message:
                    break

                self.root.after(
                    0,
                    self.process_server_message,
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
    # PROCESS SERVER MESSAGE
    # ==========================================

    def process_server_message(self, message):

        # Room list
        if message.startswith("ROOMS:"):

            rooms = message[6:].split("|")

            self.room_listbox.delete(
                0,
                tk.END
            )

            for room in rooms:

                if room:
                    self.room_listbox.insert(
                        tk.END,
                        room
                    )

            return

        # System message
        if message.startswith("SYSTEM:"):

            self.add_message(
                message[7:]
            )

            return

        # Error
        if message.startswith("ERROR:"):

            messagebox.showerror(
                "Room Error",
                message[6:]
            )

            return

        # Normal message

        self.add_message(message)

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
            "Advanced server connection closed."
        )

        self.status_label.config(
            text="Disconnected"
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

    app = AdvancedChatGUI(root)

    root.mainloop()