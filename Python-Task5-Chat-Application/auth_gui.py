import tkinter as tk
from tkinter import messagebox

from database import create_tables, register_user, login_user


class AuthGUI:
    def __init__(self, root):
        self.root = root

        self.root.title("Chat Application - Login")
        self.root.geometry("420x450")
        self.root.resizable(False, False)

        create_tables()

        self.create_login_screen()

    # ---------------------------------
    # Clear Window
    # ---------------------------------

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------------------------
    # Login Screen
    # ---------------------------------

    def create_login_screen(self):

        self.clear_window()

        title = tk.Label(
            self.root,
            text="Python Chat Application",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=(35, 10))

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
        ).pack(anchor="w", padx=60)

        self.login_username = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 11)
        )

        self.login_username.pack(
            padx=60,
            pady=(5, 15)
        )

        # Password

        tk.Label(
            self.root,
            text="Password",
            font=("Arial", 11)
        ).pack(anchor="w", padx=60)

        self.login_password = tk.Entry(
            self.root,
            width=30,
            show="*",
            font=("Arial", 11)
        )

        self.login_password.pack(
            padx=60,
            pady=(5, 20)
        )

        # Login Button

        login_button = tk.Button(
            self.root,
            text="Login",
            width=20,
            height=2,
            command=self.login
        )

        login_button.pack(pady=10)

        # Register

        register_label = tk.Label(
            self.root,
            text="Don't have an account?",
            font=("Arial", 10)
        )

        register_label.pack(pady=(25, 5))

        register_button = tk.Button(
            self.root,
            text="Create Account",
            width=20,
            command=self.create_register_screen
        )

        register_button.pack()

        self.login_username.focus()

    # ---------------------------------
    # Register Screen
    # ---------------------------------

    def create_register_screen(self):

        self.clear_window()

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
        ).pack(anchor="w", padx=60)

        self.register_username = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 11)
        )

        self.register_username.pack(
            padx=60,
            pady=(5, 15)
        )

        # Password

        tk.Label(
            self.root,
            text="Password",
            font=("Arial", 11)
        ).pack(anchor="w", padx=60)

        self.register_password = tk.Entry(
            self.root,
            width=30,
            show="*",
            font=("Arial", 11)
        )

        self.register_password.pack(
            padx=60,
            pady=(5, 15)
        )

        # Confirm Password

        tk.Label(
            self.root,
            text="Confirm Password",
            font=("Arial", 11)
        ).pack(anchor="w", padx=60)

        self.register_confirm = tk.Entry(
            self.root,
            width=30,
            show="*",
            font=("Arial", 11)
        )

        self.register_confirm.pack(
            padx=60,
            pady=(5, 20)
        )

        # Register Button

        register_button = tk.Button(
            self.root,
            text="Register",
            width=20,
            height=2,
            command=self.register
        )

        register_button.pack(pady=10)

        # Back to Login

        login_button = tk.Button(
            self.root,
            text="Back to Login",
            width=20,
            command=self.create_login_screen
        )

        login_button.pack(pady=10)

        self.register_username.focus()

    # ---------------------------------
    # Register User
    # ---------------------------------

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

            self.create_login_screen()

            self.login_username.insert(
                0,
                username
            )

        else:

            messagebox.showerror(
                "Registration Failed",
                message
            )

    # ---------------------------------
    # Login User
    # ---------------------------------

    def login(self):

        username = self.login_username.get().strip()
        password = self.login_password.get()

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

            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!"
            )

            print(f"User logged in: {username}")

        else:

            messagebox.showerror(
                "Login Failed",
                message
            )


# ---------------------------------
# Start Application
# ---------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = AuthGUI(root)

    root.mainloop()