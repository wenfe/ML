"""OpenWeatherMap current-weather lookup."""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from src.utils.config import get_openweather_api_key


def get_weather(city: str) -> dict[str, object]:
    """Fetch current weather for a city using the OpenWeatherMap API."""
    if not city.strip():
        raise ValueError("City cannot be empty.")

    params = urlencode(
        {"q": city, "appid": get_openweather_api_key(), "units": "metric"}
    )
    url = f"https://api.openweathermap.org/data/2.5/weather?{params}"
    try:
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Weather service returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError("Could not connect to the weather service.") from exc
