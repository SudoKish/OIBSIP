import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt



# =========================
# DATABASE
# =========================

def create_database():
    """Create the BMI database and table if they don't exist."""

    connection = sqlite3.connect("bmi_data.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# =========================
# BMI CALCULATION
# =========================

def calculate_bmi(weight, height):
    """Calculate BMI using weight in kg and height in meters."""
    return weight / (height ** 2)


def classify_bmi(bmi):
    """Classify BMI into a health category."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# =========================
# CALCULATE BUTTON
# =========================

def calculate():
    """Read inputs, calculate BMI and display result."""

    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Weight and height must be greater than 0."
            )
            return

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        save_record(weight, height, bmi, category)

        bmi_value_label.config(
            text=f"{bmi:.2f}"
        )

        category_label.config(
            text=category
        )

        # Change category appearance
        if category == "Underweight":
            category_label.config(
                fg="#3498DB"
            )

        elif category == "Normal weight":
            category_label.config(
                fg="#2ECC71"
            )

        elif category == "Overweight":
            category_label.config(
                fg="#F39C12"
            )

        else:
            category_label.config(
                fg="#E74C3C"
            )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers."
        )


# =========================
# RESET BUTTON
# =========================

def reset():
    """Clear all fields and reset the result."""

    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    bmi_value_label.config(
        text="--"
    )

    category_label.config(
        text="Enter your details",
        fg="#B0B0B0"
    )

def get_history():
    """Retrieve all BMI records from the database."""

    connection = sqlite3.connect("bmi_data.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, weight, height, bmi, category, date
        FROM bmi_records
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records

def clear_history():
    """Delete all BMI records from the database."""

    result = messagebox.askyesno(
        "Clear History",
        "Are you sure you want to delete all BMI history?"
    )

    if result:
        connection = sqlite3.connect("bmi_data.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM bmi_records")

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "History Cleared",
            "All BMI history has been deleted."
        )

def show_trend():
    """Display a clean BMI trend graph using saved records."""

    records = get_history()

    if not records:
        messagebox.showinfo(
            "BMI Trend",
            "No BMI records available to display."
        )
        return

    # Reverse records so oldest comes first
    records.reverse()

    dates = []
    bmi_values = []

    for record in records:
        # Convert database timestamp into datetime
        date = datetime.strptime(
            record[5],
            "%Y-%m-%d %H:%M:%S"
        )

        dates.append(date)
        bmi_values.append(record[3])

    # Create figure
    plt.figure(figsize=(11, 6))

    # BMI trend
    plt.plot(
        dates,
        bmi_values,
        marker="o",
        linewidth=2,
        label="Your BMI"
    )

    # BMI reference lines
    plt.axhline(
        y=18.5,
        linestyle="--",
        linewidth=1,
        label="Underweight: 18.5"
    )

    plt.axhline(
        y=25,
        linestyle="--",
        linewidth=1,
        label="Overweight: 25"
    )

    plt.axhline(
        y=30,
        linestyle="--",
        linewidth=1,
        label="Obese: 30"
    )

    # Add BMI values to points
    for date, bmi in zip(dates, bmi_values):

        plt.annotate(
            f"{bmi:.2f}",
            (date, bmi),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9
        )

    # Title
    plt.title(
        "BMI Trend Over Time",
        fontsize=16,
        fontweight="bold"
    )

    # Axis labels
    plt.xlabel(
        "Date and Time",
        fontsize=12
    )

    plt.ylabel(
        "BMI",
        fontsize=12
    )

    # Rotate date labels
    plt.xticks(
        rotation=45,
        ha="right"
    )

    # Grid
    plt.grid(
        True,
        linestyle="--",
        alpha=0.3
    )

    # Legend
    plt.legend()

    # Prevent labels from being cut off
    plt.tight_layout()

    # Display graph
    plt.show()

def show_history():
    """Display BMI history in a separate window."""

    history_window = tk.Toplevel(root)

    history_window.title("BMI History")
    history_window.geometry("800x500")
    history_window.configure(bg="#121212")

    title = tk.Label(
        history_window,
        text="BMI HISTORY",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#121212"
    )

    title.pack(pady=20)

    records = get_history()

    if not records:
        empty_label = tk.Label(
            history_window,
            text="No BMI records found.",
            font=("Arial", 14),
            fg="#AAAAAA",
            bg="#121212"
        )

        empty_label.pack(pady=50)
        return

    header_frame = tk.Frame(
        history_window,
        bg="#1E1E1E"
    )

    header_frame.pack(
        padx=20,
        fill="x"
    )

    headers = [
        "ID",
        "Weight",
        "Height",
        "BMI",
        "Category",
        "Date"
    ]

    for column, header in enumerate(headers):

        label = tk.Label(
            header_frame,
            text=header,
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#1E1E1E",
            width=14
        )

        label.grid(
            row=0,
            column=column,
            padx=2,
            pady=10
        )

    for record in records:

        row_frame = tk.Frame(
            history_window,
            bg="#2A2A2A"
        )

        row_frame.pack(
            padx=20,
            fill="x"
        )

        values = [
            record[0],
            f"{record[1]:.1f} kg",
            f"{record[2]:.2f} m",
            f"{record[3]:.2f}",
            record[4],
            record[5]
        ]

        for column, value in enumerate(values):

            label = tk.Label(
                row_frame,
                text=value,
                font=("Arial", 10),
                fg="white",
                bg="#2A2A2A",
                width=14
            )

            label.grid(
                row=0,
                column=column,
                padx=2,
                pady=8
            )


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("BMI Calculator")
root.geometry("500x820")
root.resizable(False, False)

root.configure(bg="#121212")


# =========================
# MAIN CONTAINER
# =========================

main_frame = tk.Frame(
    root,
    bg="#121212"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=25
)


# =========================
# HEADER
# =========================

header_frame = tk.Frame(
    main_frame,
    bg="#121212"
)

header_frame.pack(
    fill="x",
    pady=(0, 18)
)


title_label = tk.Label(
    header_frame,
    text="BMI CALCULATOR",
    font=("Arial", 27, "bold"),
    fg="white",
    bg="#121212"
)

title_label.pack()


subtitle_label = tk.Label(
    header_frame,
    text="Health & Fitness Tracker",
    font=("Arial", 12),
    fg="#AAAAAA",
    bg="#121212"
)

subtitle_label.pack(
    pady=(4, 0)
)


# =========================
# INPUT CARD
# =========================

input_frame = tk.Frame(
    main_frame,
    bg="#1E1E1E",
    padx=30,
    pady=20
)

input_frame.pack(
    fill="x",
    pady=(0, 15)
)


# Weight

weight_label = tk.Label(
    input_frame,
    text="Weight (kg)",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#1E1E1E"
)

weight_label.pack(
    anchor="w"
)


weight_entry = tk.Entry(
    input_frame,
    font=("Arial", 13),
    bg="#2A2A2A",
    fg="white",
    insertbackground="white",
    relief="flat"
)

weight_entry.pack(
    fill="x",
    ipady=7,
    pady=(7, 15)
)


# Height

height_label = tk.Label(
    input_frame,
    text="Height (meters)",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#1E1E1E"
)

height_label.pack(
    anchor="w"
)


height_entry = tk.Entry(
    input_frame,
    font=("Arial", 13),
    bg="#2A2A2A",
    fg="white",
    insertbackground="white",
    relief="flat"
)

height_entry.pack(
    fill="x",
    ipady=7,
    pady=(7, 0)
)


# =========================
# CALCULATE BUTTON
# =========================

calculate_button = tk.Button(
    main_frame,
    text="Calculate BMI",
    font=("Arial", 13, "bold"),
    bg="#3498DB",
    fg="white",
    activebackground="#2980B9",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=calculate
)

calculate_button.pack(
    fill="x",
    ipady=9,
    pady=(0, 15)
)


# =========================
# RESULT CARD
# =========================

result_frame = tk.Frame(
    main_frame,
    bg="#1E1E1E",
    padx=25,
    pady=18
)

result_frame.pack(
    fill="x",
    pady=(0, 15)
)


result_title = tk.Label(
    result_frame,
    text="YOUR BMI RESULT",
    font=("Arial", 11, "bold"),
    fg="#AAAAAA",
    bg="#1E1E1E"
)

result_title.pack()


bmi_value_label = tk.Label(
    result_frame,
    text="--",
    font=("Arial", 36, "bold"),
    fg="white",
    bg="#1E1E1E"
)

bmi_value_label.pack(
    pady=(2, 0)
)


category_label = tk.Label(
    result_frame,
    text="Enter your details",
    font=("Arial", 16, "bold"),
    fg="#B0B0B0",
    bg="#1E1E1E"
)

category_label.pack(
    pady=(2, 0)
)


# =========================
# ACTION BUTTONS
# =========================

button_frame = tk.Frame(
    main_frame,
    bg="#121212"
)

button_frame.pack(
    fill="x",
    pady=(0, 12)
)


# Make both columns equal width
button_frame.columnconfigure(
    0,
    weight=1
)

button_frame.columnconfigure(
    1,
    weight=1
)


# Reset

reset_button = tk.Button(
    button_frame,
    text="Reset",
    font=("Arial", 11, "bold"),
    bg="#333333",
    fg="white",
    activebackground="#444444",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=reset
)

reset_button.grid(
    row=0,
    column=0,
    padx=(0, 6),
    pady=5,
    sticky="ew",
    ipady=7
)


# Clear History

clear_button = tk.Button(
    button_frame,
    text="Clear History",
    font=("Arial", 11, "bold"),
    bg="#E74C3C",
    fg="white",
    activebackground="#C0392B",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=clear_history
)

clear_button.grid(
    row=0,
    column=1,
    padx=(6, 0),
    pady=5,
    sticky="ew",
    ipady=7
)


# View History

history_button = tk.Button(
    button_frame,
    text="View BMI History",
    font=("Arial", 11, "bold"),
    bg="#333333",
    fg="white",
    activebackground="#444444",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=show_history
)

history_button.grid(
    row=1,
    column=0,
    padx=(0, 6),
    pady=5,
    sticky="ew",
    ipady=7
)


# View Trend

trend_button = tk.Button(
    button_frame,
    text="View BMI Trend",
    font=("Arial", 11, "bold"),
    bg="#3498DB",
    fg="white",
    activebackground="#2980B9",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=show_trend
)

trend_button.grid(
    row=1,
    column=1,
    padx=(6, 0),
    pady=5,
    sticky="ew",
    ipady=7
)


# =========================
# FOOTER
# =========================

footer_label = tk.Label(
    main_frame,
    text="BMI Calculator • Python Project",
    font=("Arial", 9),
    fg="#666666",
    bg="#121212"
)

footer_label.pack(
    pady=(0, 2)
)


# =========================
# DATABASE INITIALIZATION
# =========================

create_database()

def save_record(weight, height, bmi, category):
    """Save a BMI record into the database."""

    connection = sqlite3.connect("bmi_data.db")
    cursor = connection.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO bmi_records
        (weight, height, bmi, category, date)
        VALUES (?, ?, ?, ?, ?)
    """, (weight, height, bmi, category, current_date))

    connection.commit()
    connection.close()



# =========================
# START APPLICATION
# =========================

root.mainloop()