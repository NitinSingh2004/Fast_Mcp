import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("Weather Server")

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@mcp.tool()
def get_weather(city: str) -> dict:
    """
    Get current weather information for a city.
    """

    if not API_KEY:
        return {
            "error": "OPENWEATHER_API_KEY is not configured"
        }

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature_celsius": data["main"]["temp"],
            "feels_like_celsius": data["main"]["feels_like"],
            "humidity_percent": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed_mps": data["wind"]["speed"]
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }
