import logging
import os
import csv
from app.models.Weather import Weather


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("weather.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WeatherRecorder:
    """Stores and manages a history of Weather records.

    Attributes:
        history (List[Weather]): A list of recorded Weather objects.
    """

    def __init__(self):
        """Initializes an empty WeatherRecorder."""
        self.history = []
        logger.info("Weather Recorder is initialized.")

    def new_record(self, data : Weather):
        """Adds a new Weather record to the history.

        Args:
            data (Weather): A Weather object containing weather data to record.
        """
        logger.info("Adding Record")
        if not any(record.city.lower() == data.city.lower() for record in self.history):
            self.history.append(data)

    
    def export_to_dicts(self) -> list[dict]:
        """Exports all recorded weather data as a list of dictionaries.

        Returns:
            list[dict]: A list of dictionaries, each representing a weather record.
        """
        return [
            {
                "City": w.city,
                "Degree (°C)": w.degree,
                "Humidity (%)": w.humidity,
                "Description": w.condition
            }
            for w in self.history
        ]


    def export_to_csv(self) -> str:
        """Exports all recorded weather data to a CSV file and returns the file path.

        Returns:
            str: The full path to the exported CSV file.
        """
        if not self.history:
            logger.warning("No weather records to export.")
            return "No weather records to export."

        filename = "weather.csv"
        filepath = os.path.join(os.getcwd(), filename)

        with open(filepath, "w", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["City", "Degree (°C)", "Humidity (%)", "Description"])
            writer.writeheader()
            writer.writerows(self.export_to_dicts())

        logger.info(f"Weather history exported to {filepath}")
        return filepath


    def __str__(self)-> str:
        """Returns a formatted string of all recorded weather data.

        Returns:
            str: A human-readable summary of all weather records.
        """
        if not self.history:
            return "No weather records yet."
        return "-----------------------------------------\n"+"\n".join(
            f"{w.city}: {w.degree}°C, {w.humidity}%, {w.condition}"
            for w in self.history
        )+"\n-----------------------------------------"