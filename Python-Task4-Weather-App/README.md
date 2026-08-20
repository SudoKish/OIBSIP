# 🌤 Weather App

A modern Python GUI weather application that fetches real-time weather information and forecasts for a user-selected city or Indian PIN code.

The application uses OpenWeatherMap for current weather and 5-day forecasts, Open-Meteo for the next 6 hours, and IP-based location detection for the automatic location feature.

## ✨ Features

- 🔍 Search weather by city name
- 📍 Search weather using an Indian PIN/ZIP code
- 🌡️ Current temperature in Celsius and Fahrenheit
- 💧 Humidity percentage
- 💨 Wind speed
- 🌤️ Weather condition and weather icons
- 🕐 Next 6 hours forecast
- 📅 5-day weather forecast
- 🔄 Celsius / Fahrenheit toggle
- 📍 Automatic approximate location detection using IP
- ⚠️ GUI-based error messages
- 🌐 Network timeout and API error handling
- 📜 Scrollable modern GUI
- 🎨 Gradient background and glass-style weather cards

## 🛠️ Tech Stack

- Python
- Tkinter
- Requests
- Pillow
- python-dotenv
- OpenWeatherMap API
- Open-Meteo API
- ipinfo.io API

## 📂 Project Structure

```text
Python-Task4-Weather-App/
│
├── weather_app.py
├── weather_api.py
├── weather_utils.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt