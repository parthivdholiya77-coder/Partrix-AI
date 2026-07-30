import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

API_KEY = os.getenv("WEATHERAPI_API_KEY")


@tool
def weather(city: str) -> str:
    """
    Get the current weather for any city.

    Use this tool when the user asks about:
    - Current weather
    - Temperature
    - Humidity
    - Wind speed
    - Weather conditions
    """

    if not API_KEY:
        return "Weather API key is not configured."

    url = "https://api.weatherapi.com/v1/current.json"

    params = {
        "key": API_KEY,
        "q": city,
        "aqi": "yes"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        location = data["location"]
        current = data["current"]

        return f"""
📍 {location['name']}, {location['country']}

🌡 Temperature : {current['temp_c']}°C
🥵 Feels Like : {current['feelslike_c']}°C
☁ Condition : {current['condition']['text']}
💧 Humidity : {current['humidity']}%
💨 Wind : {current['wind_kph']} km/h
👁 Visibility : {current['vis_km']} km
🧭 Pressure : {current['pressure_mb']} mb
🌤 UV Index : {current['uv']}
""".strip()

    except requests.exceptions.HTTPError:
        try:
            error = response.json()["error"]["message"]
        except Exception:
            error = "Unable to fetch weather."

        return f"Weather Error: {error}"

    except requests.exceptions.RequestException as e:
        return f"Network Error: {e}"

    except Exception as e:
        return f"Unexpected Error: {e}"