# 🎙️ Python Voice Assistant

A Python-based voice assistant that understands spoken commands, performs useful tasks, and responds using text-to-speech.

The project started as a basic voice assistant and was extended with natural-language intent detection, reminders, weather information, email sending, general knowledge Q&A, and configurable custom commands.

---

## 🚀 Features

### 🎤 Voice Recognition
- Captures commands through the microphone.
- Uses `SpeechRecognition`.
- Supports English speech recognition.
- Uses `en-IN` language recognition.

### 🔊 Text-to-Speech
- Uses `pyttsx3`.
- Provides audible responses to the user.
- Works locally without requiring a separate cloud TTS service.

### 🧠 Intent Recognition
The assistant identifies the user's intention instead of relying only on exact commands.

Supported intents include:

- `GREETING`
- `GET_TIME`
- `GET_DATE`
- `WEATHER`
- `SEND_EMAIL`
- `QUESTION`
- `WEB_SEARCH`
- `SET_REMINDER`
- `EXIT`

Unknown commands can also be checked against the custom command configuration.

---

## 🌤️ Weather

The assistant can fetch live weather information using a weather API.

Example:

> "What's the weather in Pune?"

The assistant returns information such as:

- Weather condition
- Temperature
- Feels-like temperature
- Humidity

---

## ⏰ Reminders

The assistant supports timed reminders.

Examples:

> "Remind me in 10 seconds."

> "Set a reminder for 5 minutes."

The reminder is stored and an audible notification is provided when the timer completes.

---

## 📧 Voice Email

The assistant can send emails using Python's `smtplib`.

Example:

> "Send email."

The assistant asks for:

1. Email address
2. Message

It can understand spoken email formats such as:

> "kishan at the rate gmail dot com"

The email is sent through Gmail SMTP using an App Password.

---

## 🌐 Web Search

The assistant can perform Google searches from spoken commands.

Examples:

> "Search for Python decorators."

> "Look up machine learning."

The default web browser opens with the search results.

---

## 📚 General Knowledge Q&A

The assistant can answer general knowledge questions using Wikipedia.

Examples:

> "What is Python?"

> "Who invented Python?"

> "Tell me about artificial intelligence."

The answer is retrieved and read aloud using text-to-speech.

---

## ⚙️ Custom Commands

Users can create their own commands using `commands.json`.

Example:

```json
{
    "open youtube": "https://www.youtube.com",
    "open github": "https://github.com",
    "open linkedin": "https://www.linkedin.com",
    "open google": "https://www.google.com"
}