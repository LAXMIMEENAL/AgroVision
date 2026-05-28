import requests


API_KEY = "e83898eed92628ab1d28b6fe23343c62"


def get_weather(lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    data = response.json()

    weather = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "rainfall": (
    data.get("rain", {}).get("1h")
    or data.get("rain", {}).get("3h")
    or 0)
    }

    return weather