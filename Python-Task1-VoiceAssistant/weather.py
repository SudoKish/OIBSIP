import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):

    if not API_KEY:
        return "Weather API key is not configured."

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 404:
            return f"I could not find the city {city}."

        if response.status_code == 401:
            return "The weather API key is invalid."

        response.raise_for_status()

        data = response.json()

        city_name = data["name"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        return (
            f"The weather in {city_name} is {description}. "
            f"The temperature is {temperature:.1f} degrees Celsius, "
            f"feels like {feels_like:.1f} degrees Celsius, "
            f"with {humidity}% humidity."
        )

    except requests.exceptions.Timeout:

        return "The weather service took too long to respond."

    except requests.exceptions.ConnectionError:

        return "I could not connect to the weather service."

    except requests.exceptions.RequestException:

        return "There was a problem getting the weather."


if __name__ == "__main__":

    city = input("Enter city name: ")

    result = get_weather(city)

    print("\nWeather:")
    print(result)