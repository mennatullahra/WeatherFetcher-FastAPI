import sys
import re
import logging
import asyncio
from RetryMechanism import RetryMechanism
from WeatherFetcher import WeatherFetcher
from WeatherRecorder import WeatherRecorder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("weather.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

weather_fetcher = WeatherFetcher("73d760cb69bfbdb74b29850c6043bac6")
weather_recorder = WeatherRecorder()

async def check_weather(city : str):
    """Fetches weather for a given city and records it.

    Args:
        city (str): Name of the city to check weather for.

    Raises:
        Exception: If weather fetching fails after retries.
    """
    print("Checking weather...")
    logger.info("Checking weather...")
    
    try:
        result = await RetryMechanism.retry_async(
            weather_fetcher.fetch_weather_for_city, city, retries=3, delay=2
        )
        print(result)
        weather_recorder.new_record(result)
    except Exception:
        print(f"Failed to fetch weather for {city}. Please try again later.")
        logger.error("Weather fetch failed after retries.", exc_info=True)

def view_history():
    """Displays the recorded weather history."""
    print("Viewing history...")
    logger.info("Viewing history...")
    print(weather_recorder)

def export_to_csv():
    """Exporting weather history to CSV."""
    print("Exporting to CSV...")
    logger.info("Exporting to CSV...")
    print(weather_recorder.export_to_csv())

def show_menu():
    logger.info("Menu Loading")
    print("Welcome to Weather Reporter\nChoose an option:")
    print("1. Check Weather")
    print("2. View History")
    print("3. Export to CSV")
    print("4. Exit")

def validate_city_name(city: str) -> bool:
    if not city.strip():
        return False
    if re.search(r'[^a-zA-Z\s]', city):
        return False
    return True

def get_location():
    while True:
        city = input("Enter city name: ").strip()
        if validate_city_name(city):
            return city
        else:
            print("""Invalid City Name!\nTry Again..""")
            logger.warning("""Invalid City Name!\nTry Again..""")

async def main():
    while True:
        
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            city = get_location()
            await check_weather(city)
        elif choice == "2":
            view_history()
        elif choice == "3":
            export_to_csv()
        elif choice == "4":
            print("End!")
            sys.exit()
        else:
            print("Invalid choice. Please enter a number 1-4.")

if __name__ == "__main__":
    asyncio.run(main())

