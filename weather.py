from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests
import os

#API_KEY = os.getenv("OPENWEATHER_API_KEY") 

@tool
def weather(user_input: str) -> dict:
    """
    Fetch weather for a city given as a string.
    User can enter "City" or "City, Country".
    """
    if not user_input or not user_input.strip():
        raise ValueError("City must be provided as input.")
    
    user_input = user_input.strip()
    parts = user_input.split(",")
    city = parts[0].strip()
    country = parts[1].strip() if len(parts) > 1 else ""

    query = f"{city},{country}" if country else city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={API_KEY}&units=metric"
    
    resp = requests.get(url, timeout=8)
    if resp.status_code != 200:
        raise RuntimeError(f"Weather API error {resp.status_code}: {resp.text[:200]}")

    data = resp.json()
    return {
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"]
    }
