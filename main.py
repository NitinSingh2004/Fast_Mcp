from mcp.server.fastmcp import FastMCP
import requests
import os

mcp = FastMCP("Weather Server")

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@mcp.tool()
def get_weather(city: str) -> dict:
    """
    Get current weather for a city.
    """

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

if __name__ == "__main__":
    mcp.run()
