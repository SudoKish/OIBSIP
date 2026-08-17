# 🔐 Random Password Generator

A secure Python password generator with a graphical user interface (GUI). The application allows users to create strong random passwords based on customizable length and character-type requirements.

## 🎯 Objective

The objective of this project is to build a secure password generator that allows users to define password requirements while ensuring that the generated password follows the selected security rules.

## ✨ Features

### Advanced Features

- GUI built using Tkinter
- Password length control using Spinbox
- Minimum password length of 8 characters
- Uppercase letters selection
- Lowercase letters selection
- Numbers selection
- Symbols selection
- At least two character types are required
- Uses Python's `secrets` module for cryptographically secure generation
- Guarantees at least one character from every selected character type
- Password strength indicator:
  - Weak
  - Medium
  - Strong
- Automatically copies generated password to clipboard
- Manual "Copy" button
- Uses `pyperclip` for clipboard integration
- Option to exclude ambiguous characters:
  - `0`
  - `O`
  - `l`
  - `1`
- Generation history displaying the last 5 generated passwords
- History is stored only during the current application session
- History is not saved to any file for security reasons
- Clear History button
- Input validation and error handling

## 🛠️ Technologies Used

- Python
- Tkinter
- secrets
- string
- pyperclip

## 📂 Project Structure

```text
Python-Task3-Random-Password-Generator/
│
├── password_generator.py
├── README.md
└── .gitignore