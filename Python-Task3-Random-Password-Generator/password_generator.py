import string
import secrets
import tkinter as tk
from tkinter import messagebox
import pyperclip


# Store the last 5 generated passwords only during this session
password_history = []


AMBIGUOUS_CHARACTERS = "0Ol1"


def get_character_sets():
    """Return character sets based on selected options."""

    character_sets = []

    if uppercase_var.get():
        characters = string.ascii_uppercase

        if exclude_ambiguous_var.get():
            characters = "".join(
                char for char in characters
                if char not in AMBIGUOUS_CHARACTERS
            )

        character_sets.append(("Uppercase", characters))

    if lowercase_var.get():
        characters = string.ascii_lowercase

        if exclude_ambiguous_var.get():
            characters = "".join(
                char for char in characters
                if char not in AMBIGUOUS_CHARACTERS
            )

        character_sets.append(("Lowercase", characters))

    if numbers_var.get():
        characters = string.digits

        if exclude_ambiguous_var.get():
            characters = "".join(
                char for char in characters
                if char not in AMBIGUOUS_CHARACTERS
            )

        character_sets.append(("Numbers", characters))

    if symbols_var.get():
        characters = string.punctuation
        character_sets.append(("Symbols", characters))

    return character_sets


def calculate_strength(length, number_of_types):
    """Calculate password strength."""

    score = 0

    # Length score
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    # Character diversity score
    if number_of_types >= 3:
        score += 2
    elif number_of_types == 2:
        score += 1

    if score <= 1:
        return "Weak"
    elif score <= 2:
        return "Medium"
    else:
        return "Strong"


def update_strength():
    """Update password strength indicator."""

    try:
        length = int(length_var.get())
    except ValueError:
        strength_label.config(text="Strength: -")
        return

    selected_types = get_character_sets()

    strength = calculate_strength(length, len(selected_types))

    strength_label.config(text=f"Strength: {strength}")


def generate_password():
    """Generate a secure password."""

    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror(
            "Invalid Length",
            "Please enter a valid password length."
        )
        return

    if length < 8:
        messagebox.showerror(
            "Invalid Length",
            "Password length must be at least 8 characters."
        )
        return

    selected_types = get_character_sets()

    if len(selected_types) < 2:
        messagebox.showerror(
            "Character Types Required",
            "Please select at least 2 character types."
        )
        return

    # Make sure every selected character set contains characters
    for name, characters in selected_types:
        if not characters:
            messagebox.showerror(
                "Character Error",
                f"No valid characters available for {name}."
            )
            return

    # Create combined character set
    all_characters = "".join(
        characters for _, characters in selected_types
    )

    password_characters = []

    # Guarantee at least one character from every selected type
    for _, characters in selected_types:
        password_characters.append(
            secrets.choice(characters)
        )

    # Generate remaining characters
    remaining_length = length - len(password_characters)

    for _ in range(remaining_length):
        password_characters.append(
            secrets.choice(all_characters)
        )

    # Securely shuffle password
    secrets.SystemRandom().shuffle(password_characters)

    password = "".join(password_characters)

    # Display password
    password_var.set(password)

    # Automatically copy password to clipboard
    try:
        pyperclip.copy(password)
        clipboard_status_label.config(
            text="✓ Password copied to clipboard"
        )
    except Exception:
        clipboard_status_label.config(
            text="⚠ Could not copy automatically"
        )

    # Update strength
    strength = calculate_strength(
        length,
        len(selected_types)
    )

    strength_label.config(
        text=f"Strength: {strength}"
    )

    # Add password to history
    password_history.insert(0, password)

    # Keep only last 5 passwords
    if len(password_history) > 5:
        password_history.pop()

    update_history()


def copy_password():
    """Copy current password to clipboard."""

    password = password_var.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    try:
        pyperclip.copy(password)

        clipboard_status_label.config(
            text="✓ Password copied to clipboard"
        )

    except Exception:
        messagebox.showerror(
            "Clipboard Error",
            "Unable to copy password to clipboard."
        )


def update_history():
    """Update password history display."""

    history_listbox.delete(0, tk.END)

    for index, password in enumerate(password_history, start=1):
        history_listbox.insert(
            tk.END,
            f"{index}. {password}"
        )


def clear_history():
    """Clear password history from the current session."""

    password_history.clear()
    update_history()


# ---------------------------------------------------------
# GUI SETUP
# ---------------------------------------------------------

root = tk.Tk()

root.title("Random Password Generator")
root.geometry("650x780")
root.resizable(False, False)

root.configure(bg="#f4f4f4")


# Variables
length_var = tk.IntVar(value=12)

uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

exclude_ambiguous_var = tk.BooleanVar(value=False)

password_var = tk.StringVar()


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

title_label = tk.Label(
    root,
    text="🔐 Random Password Generator",
    font=("Arial", 22, "bold"),
    bg="#f4f4f4"
)

title_label.pack(pady=(20, 5))


subtitle_label = tk.Label(
    root,
    text="Generate strong and secure passwords",
    font=("Arial", 11),
    bg="#f4f4f4"
)

subtitle_label.pack(pady=(0, 20))


# ---------------------------------------------------------
# PASSWORD LENGTH
# ---------------------------------------------------------

length_frame = tk.LabelFrame(
    root,
    text="Password Length",
    font=("Arial", 11, "bold"),
    bg="#f4f4f4",
    padx=15,
    pady=10
)

length_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


length_spinbox = tk.Spinbox(
    length_frame,
    from_=8,
    to=128,
    textvariable=length_var,
    width=10,
    font=("Arial", 12),
    command=update_strength
)

length_spinbox.pack(side="left", padx=10)


length_info = tk.Label(
    length_frame,
    text="Minimum: 8 characters",
    bg="#f4f4f4",
    font=("Arial", 10)
)

length_info.pack(side="left")


# ---------------------------------------------------------
# CHARACTER TYPES
# ---------------------------------------------------------

types_frame = tk.LabelFrame(
    root,
    text="Character Types",
    font=("Arial", 11, "bold"),
    bg="#f4f4f4",
    padx=15,
    pady=10
)

types_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


tk.Checkbutton(
    types_frame,
    text="Uppercase (A-Z)",
    variable=uppercase_var,
    bg="#f4f4f4",
    command=update_strength
).grid(row=0, column=0, sticky="w", padx=10, pady=5)


tk.Checkbutton(
    types_frame,
    text="Lowercase (a-z)",
    variable=lowercase_var,
    bg="#f4f4f4",
    command=update_strength
).grid(row=0, column=1, sticky="w", padx=10, pady=5)


tk.Checkbutton(
    types_frame,
    text="Numbers (0-9)",
    variable=numbers_var,
    bg="#f4f4f4",
    command=update_strength
).grid(row=1, column=0, sticky="w", padx=10, pady=5)


tk.Checkbutton(
    types_frame,
    text="Symbols (!@#$)",
    variable=symbols_var,
    bg="#f4f4f4",
    command=update_strength
).grid(row=1, column=1, sticky="w", padx=10, pady=5)


# ---------------------------------------------------------
# AMBIGUOUS CHARACTERS
# ---------------------------------------------------------

ambiguous_check = tk.Checkbutton(
    root,
    text="Exclude ambiguous characters (0, O, l, 1)",
    variable=exclude_ambiguous_var,
    bg="#f4f4f4",
    font=("Arial", 10)
)

ambiguous_check.pack(pady=10)


# ---------------------------------------------------------
# PASSWORD DISPLAY
# ---------------------------------------------------------

password_frame = tk.LabelFrame(
    root,
    text="Generated Password",
    font=("Arial", 11, "bold"),
    bg="#f4f4f4",
    padx=15,
    pady=15
)

password_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


password_entry = tk.Entry(
    password_frame,
    textvariable=password_var,
    font=("Consolas", 16, "bold"),
    justify="center",
    width=35,
    state="readonly"
)

password_entry.pack(
    side="left",
    padx=5
)


copy_button = tk.Button(
    password_frame,
    text="Copy",
    command=copy_password,
    font=("Arial", 10, "bold"),
    padx=10
)

copy_button.pack(side="left", padx=5)


# ---------------------------------------------------------
# STRENGTH INDICATOR
# ---------------------------------------------------------

strength_label = tk.Label(
    root,
    text="Strength: -",
    font=("Arial", 13, "bold"),
    bg="#f4f4f4"
)

strength_label.pack(pady=5)


clipboard_status_label = tk.Label(
    root,
    text="",
    font=("Arial", 10),
    bg="#f4f4f4"
)

clipboard_status_label.pack(pady=2)


# ---------------------------------------------------------
# GENERATE BUTTON
# ---------------------------------------------------------

generate_button = tk.Button(
    root,
    text="🔑 Generate Password",
    command=generate_password,
    font=("Arial", 13, "bold"),
    padx=25,
    pady=10
)

generate_button.pack(pady=15)


# ---------------------------------------------------------
# HISTORY
# ---------------------------------------------------------

history_frame = tk.LabelFrame(
    root,
    text="Generation History — Last 5",
    font=("Arial", 11, "bold"),
    bg="#f4f4f4",
    padx=10,
    pady=10
)

history_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


history_listbox = tk.Listbox(
    history_frame,
    font=("Consolas", 11),
    height=5,
    width=55
)

history_listbox.pack(
    side="left",
    fill="both",
    expand=True
)


clear_history_button = tk.Button(
    history_frame,
    text="Clear History",
    command=clear_history,
    font=("Arial", 9)
)

clear_history_button.pack(
    side="right",
    padx=5
)


# ---------------------------------------------------------
# START APPLICATION
# ---------------------------------------------------------

root.mainloop()