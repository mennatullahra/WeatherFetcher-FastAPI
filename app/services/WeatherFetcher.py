import logging
from app.models.Weather import Weather
import aiohttp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("weather.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WeatherFetcher:
    """Handles fetching weather data from the OpenWeatherMap API."""

    def __init__(self, api_key: str):
        """Initializes the WeatherFetcher with the given API key.

        Args:
            api_key (str): OpenWeatherMap API key.
        """
        self.api_key = api_key
        self.endpoint= "https://api.openweathermap.org/data/2.5/weather"
        logger.info("Weather Fetcher is initialized.")

    async def fetch_weather_for_city(self, city : str) -> Weather:
        """Fetches current weather data for a specified city.

        Args:
            city (str): The name of the city to fetch weather for.

        Returns:
            Weather: A Weather object containing temperature, humidity, and description.

        Raises:
            ValueError: If the API response contains incomplete weather data.
        """
        logger.info(f"Fetching weather for: {city}")
        self.params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.endpoint, params=self.params) as response:
                data = await response.json()
                
                if (str(data.get("main",{}).get("temp")) == "None") or (str(data.get("main",{}).get("humidity")) == "None"):
                    logger.warning(f"Incomplete weather data for {city}: {data}")
                    raise ValueError(f"Incomplete weather data for {city}")
                
                result = Weather(
                    city=city,
                    degree=data["main"]["temp"],
                    humidity=data["main"]["humidity"],
                    condition=data["weather"][0]["description"]
                )

                return result
