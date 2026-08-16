# BMI Calculator & Health Tracker

A Python-based BMI Calculator and Health Tracker developed as part of the **OASIS INFOBYTE Python Internship – Task 2**.

The application provides a graphical user interface for calculating Body Mass Index (BMI), classifying the result into health categories, storing BMI records using SQLite, viewing BMI history, and visualizing BMI trends over time.

## Features

* Calculate BMI using weight and height
* Classify BMI into health categories
* Input validation and error handling
* User-friendly Tkinter GUI
* Dark-themed and responsive interface
* Store BMI records using SQLite
* Automatically record date and time
* View complete BMI history
* Clear stored BMI history
* Visualize BMI trends using Matplotlib
* Display BMI reference thresholds on the trend graph

## BMI Classification

| BMI Range      | Category      |
| -------------- | ------------- |
| Below 18.5     | Underweight   |
| 18.5 – 24.9    | Normal weight |
| 25.0 – 29.9    | Overweight    |
| 30.0 and above | Obese         |

## Technologies Used

* **Python**
* **Tkinter** – Graphical User Interface
* **SQLite** – Data persistence
* **Matplotlib** – BMI trend visualization

## BMI Formula

```text
BMI = Weight (kg) / Height² (m²)
```

For example:

```text
Weight = 70 kg
Height = 1.75 m

BMI = 70 / (1.75 × 1.75)
BMI = 22.86
```

Result:

```text
Category: Normal weight
```

## Project Structure

```text
Python-Task2-BMI-Calculator/
│
├── bmi_calculator.py
├── requirements.txt
├── README.md
└── .gitignore
```

The SQLite database `bmi_data.db` is generated automatically when the application runs and is excluded from Git using `.gitignore`.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SudoKish/OIBSIP.git
```

### 2. Navigate to the project

```bash
cd OIBSIP/Python-Task2-BMI-Calculator
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

Run:

```bash
python bmi_calculator.py
```

The BMI Calculator desktop application will open.

## How It Works

1. Enter your weight in kilograms.
2. Enter your height in meters.
3. Click **Calculate BMI**.
4. The application calculates your BMI.
5. Your BMI is classified into a health category.
6. The result is automatically saved to the SQLite database.
7. Use **View BMI History** to see previous records.
8. Use **View BMI Trend** to visualize BMI changes over time.
9. Use **Clear History** to remove stored BMI records when required.

## Data Persistence

BMI records are stored locally in an SQLite database.

Each record contains:

```text
ID
Weight
Height
BMI
Category
Date
```

The database is created automatically by the application, so no manual database configuration is required.

## Trend Visualization

The application uses Matplotlib to visualize saved BMI measurements.

The graph includes:

* BMI measurements over time
* Individual BMI values
* Underweight threshold
* Overweight threshold
* Obese threshold
* Date and time of measurements

This allows users to monitor changes in their BMI over multiple measurements.

## Error Handling

The application validates user input and handles invalid values such as:

* Empty input
* Non-numeric values
* Zero values
* Negative values

Appropriate error messages are displayed using Tkinter message boxes.

## Future Improvements

Possible future improvements include:

* User profiles
* Age and gender information
* BMI recommendations
* Export BMI history to CSV
* PDF health reports
* More advanced dashboard visualizations
* Goal tracking
* Monthly and weekly BMI statistics

## Learning Outcomes

Through this project, I practiced:

* Python functions
* Exception handling
* Tkinter GUI development
* SQLite database operations
* CRUD-related database concepts
* Data persistence
* Matplotlib visualization
* File and project organization
* Git and GitHub workflow

## Author

## Author

**Kishan Wadhwa**

GitHub: [SudoKish](https://github.com/SudoKish)

---

**OASIS INFOBYTE — Python Internship**

**Task 2: BMI Calculator**
