import io
import requests
from PIL import Image, ImageTk


# Temperature conversion

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""

    return (celsius * 9 / 5) + 32


def get_temperature_text(temperature, unit):
    """Return formatted temperature based on selected unit."""

    if unit == "C":
        return f"{temperature:.1f}°C"

    return f"{celsius_to_fahrenheit(temperature):.1f}°F"


# OpenWeatherMap icon

def get_weather_icon(icon_code, size=(70, 70)):
    """Download and return an OpenWeatherMap weather icon."""

    icon_url = (
        f"https://openweathermap.org/img/wn/"
        f"{icon_code}@2x.png"
    )

    try:
        response = requests.get(
            icon_url,
            timeout=10
        )

        response.raise_for_status()

        image = Image.open(
            io.BytesIO(response.content)
        )

        image = image.resize(
            size,
            Image.Resampling.LANCZOS
        )

        return ImageTk.PhotoImage(image)

    except requests.exceptions.RequestException:
        return None

def get_openweather_icon_code(code, is_day):
    """Convert Open-Meteo weather code to OpenWeatherMap icon code."""

    if code == 0:
        return "01d" if is_day else "01n"

    if code == 1:
        return "02d" if is_day else "02n"

    if code == 2:
        return "03d" if is_day else "03n"

    if code == 3:
        return "04d" if is_day else "04n"

    if code in [45, 48]:
        return "50d" if is_day else "50n"

    if code in [51, 53, 55, 56, 57]:
        return "09d" if is_day else "09n"

    if code in [61, 63, 65, 66, 67, 80, 81, 82]:
        return "10d" if is_day else "10n"

    if code in [71, 73, 75, 77, 85, 86]:
        return "13d" if is_day else "13n"

    if code in [95, 96, 99]:
        return "11d" if is_day else "11n"

    return "02d" if is_day else "02n"


# Open-Meteo weather description

def get_weather_description(code):
    """Convert Open-Meteo weather code to a description."""

    weather_codes = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime Fog",
        51: "Light Drizzle",
        53: "Drizzle",
        55: "Heavy Drizzle",
        56: "Freezing Drizzle",
        57: "Heavy Freezing Drizzle",
        61: "Light Rain",
        63: "Rain",
        65: "Heavy Rain",
        66: "Freezing Rain",
        67: "Heavy Freezing Rain",
        71: "Light Snow",
        73: "Snow",
        75: "Heavy Snow",
        77: "Snow Grains",
        80: "Light Rain Showers",
        81: "Rain Showers",
        82: "Heavy Rain Showers",
        85: "Light Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Hail",
        99: "Heavy Thunderstorm with Hail"
    }

    return weather_codes.get(
        code,
        "Unknown"
    )


# Open-Meteo weather emoji

def get_weather_emoji(code):
    """Return an emoji based on Open-Meteo weather code."""

    if code == 0:
        return "☀️"

    if code in [1, 2]:
        return "🌤️"

    if code == 3:
        return "☁️"

    if code in [45, 48]:
        return "🌫️"

    if code in [51, 53, 55, 56, 57]:
        return "🌦️"

    if code in [61, 63, 65, 66, 67, 80, 81, 82]:
        return "🌧️"

    if code in [71, 73, 75, 77, 85, 86]:
        return "🌨️"

    if code in [95, 96, 99]:
        return "⛈️"

    return "🌤️"