import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("weather.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Weather:
    """Represents weather data for a specific city.

    Attributes:
        city (str): Name of the city.
        degree (int): Temperature in Celsius.
        humidity (int): Humidity percentage.
        condition (str): Weather condition description (e.g., 'Sunny', 'Rainy').
    """

    def __init__(self, city : str, degree : int, humidity : int, condition : str):
        """Initializes a Weather object with city, temperature, humidity, and condition.

        Args:
            city (str): Name of the city.
            degree (int): Temperature in Celsius.
            humidity (int): Humidity percentage.
            condition (str): Weather condition description.
        """
        self.city = city
        self.degree = degree
        self.humidity = humidity
        self.condition = condition
        logger.info("Weather is initialized.")
    
    def __str__(self):
        """Returns a formatted string representation of the weather data.

        Returns:
            str: A human-readable summary of the weather information.
        """
        logger.info(f"City: {self.city} | Degree: {self.degree}°C | "
                f"Condition: {self.condition} | Humidity: {self.humidity}%")
        
        return (f"City: {self.city} | Degree: {self.degree}°C | "
                f"Condition: {self.condition} | Humidity: {self.humidity}%")
    