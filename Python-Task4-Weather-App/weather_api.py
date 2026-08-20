import requests


# API URLs

CURRENT_WEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)

FORECAST_URL = (
    "https://api.openweathermap.org/data/2.5/forecast"
)

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
)

OPENWEATHER_GEO_URL = (
    "https://api.openweathermap.org/geo/1.0/zip"
)

IP_LOCATION_URL = (
    "https://ipinfo.io/json"
)


# Current weather

def get_current_weather(location, api_key):
    """Fetch current weather from OpenWeatherMap."""

    if location.isdigit():

        location_data = get_location_from_pincode(
            location,
            api_key
        )

        params = {
            "lat": location_data["lat"],
            "lon": location_data["lon"],
            "appid": api_key,
            "units": "metric"
        }

    else:

        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }

    try:

        response = requests.get(
            CURRENT_WEATHER_URL,
            params=params,
            timeout=10
        )

    except requests.exceptions.Timeout:
        raise TimeoutError(
            "Weather request timed out."
        )

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Unable to connect to the weather service."
        )

    if response.status_code == 404:
        raise ValueError(
            "Location not found. Please check the city or PIN code."
        )

    if response.status_code == 401:
        raise ValueError(
            "Invalid or inactive API key."
        )

    if response.status_code == 429:
        raise ValueError(
            "API request limit reached."
        )

    response.raise_for_status()

    return response.json()


# PIN code geocoding

def get_location_from_pincode(pincode, api_key):
    """Convert an Indian PIN code to coordinates."""

    params = {
        "zip": f"{pincode},IN",
        "appid": api_key
    }

    try:

        response = requests.get(
            OPENWEATHER_GEO_URL,
            params=params,
            timeout=10
        )

    except requests.exceptions.Timeout:
        raise TimeoutError(
            "PIN code request timed out."
        )

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Unable to connect to the location service."
        )

    if response.status_code == 404:
        raise ValueError(
            "PIN code not found."
        )

    if response.status_code == 401:
        raise ValueError(
            "Invalid or inactive API key."
        )

    response.raise_for_status()

    data = response.json()

    if "lat" not in data or "lon" not in data:
        raise ValueError(
            "Unable to determine coordinates for this PIN code."
        )

    return data


# Five-day forecast

def get_five_day_forecast(latitude, longitude, api_key):
    """Fetch five-day forecast from OpenWeatherMap."""

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric"
    }

    try:

        response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=10
        )

    except requests.exceptions.Timeout:
        raise TimeoutError(
            "Forecast request timed out."
        )

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Unable to connect to the forecast service."
        )

    if response.status_code == 401:
        raise ValueError(
            "Invalid or inactive API key."
        )

    if response.status_code == 429:
        raise ValueError(
            "API request limit reached."
        )

    response.raise_for_status()

    return response.json()


# Six-hour forecast

def get_hourly_forecast(latitude, longitude):
    """Fetch the next six hours from Open-Meteo."""

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": (
            "temperature_2m,"
            "weather_code,"
            "is_day"
        ),
        "forecast_hours": 6,
        "timezone": "auto"
    }

    try:

        response = requests.get(
            OPEN_METEO_URL,
            params=params,
            timeout=10
        )

    except requests.exceptions.Timeout:
        raise TimeoutError(
            "Hourly forecast request timed out."
        )

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Unable to connect to the hourly forecast service."
        )

    response.raise_for_status()

    return response.json()


# Automatic IP location

def get_location_from_ip():
    """Get approximate location from the user's IP address."""

    try:

        response = requests.get(
            IP_LOCATION_URL,
            timeout=10
        )

    except requests.exceptions.Timeout:
        raise TimeoutError(
            "Location request timed out."
        )

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Unable to connect to the location service."
        )

    response.raise_for_status()

    data = response.json()

    city = data.get("city")

    if not city:
        raise ValueError(
            "Unable to detect your location."
        )

    return city