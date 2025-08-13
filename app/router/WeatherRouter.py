from fastapi import APIRouter, HTTPException, Query
from app.services.WeatherFetcher import WeatherFetcher
from app.services.RetryMechanism import RetryMechanism
from app.utils.Validator import Validator
from app.services.WeatherRecorder import WeatherRecorder
from fastapi.responses import FileResponse
from app.models.Weather import Weather
import asyncio
import logging
import pandas as pd



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("weather.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

router = APIRouter()
weather_fetcher = WeatherFetcher("73d760cb69bfbdb74b29850c6043bac6")
weather_recorder = WeatherRecorder()
city_validator = Validator()


@router.get("/weather/city/{city}", response_model=Weather)
async def get_weather(city: str):
    if not city_validator.validate_city_name(city):
        raise HTTPException(status_code=400, detail="Invalid city name. Only letters and spaces are allowed.")
    try:
        result = await RetryMechanism.retry_async(
            weather_fetcher.fetch_weather_for_city, city, retries=3, delay=2
        )
        weather_recorder.new_record(result)
        return result  
    except Exception:
        return {"error": f"Failed to fetch weather for {city}. Please try again later."}

@router.get("/weather/history", response_model=None)
async def get():
    return weather_recorder.export_to_dicts()


@router.get("/weather/multiple")
async def get_multiple_cities(cities: str):
    logger.info(f"Received cities: {cities}")
    cities_list = [city.strip() for city in cities.split(",")]
    results = {}

    async def fetch(city: str):
        try:
            logger.info(f"Validating city: {city}")
            if not Validator().validate_city_name(city):
                logger.warning(f"Invalid city: {city}")
                results[city] = {"status": "invalid", "data": None}
                return

            logger.info(f"Fetching weather for: {city}")
            weather = await RetryMechanism.retry_async(
                weather_fetcher.fetch_weather_for_city, city, retries=3, delay=2
            )
            weather_recorder.new_record(weather)
            results[city] = {"status": "success", "data": weather.dict()}
        except Exception as e:
            logger.error(f"Error fetching weather for {city}: {e}")
            results[city] = {"status": "failed", "data": None}

    try:
        async with asyncio.TaskGroup() as group:
            for city in cities_list:
                group.create_task(fetch(city))
    except Exception as e:
        logger.critical(f"TaskGroup failed: {e}")
        raise HTTPException(status_code=500, detail="Internal error during weather fetch")

    return results

@router.get("/weather/summary")
async def get_weather_summary():
    if not weather_recorder.history:
        return {"message": "No weather data recorded yet."}

    df = pd.DataFrame([w.dict() for w in weather_recorder.history])

    summary = {
        "total_cities": len(df),
        "average_temperature": round(df["degree"].mean(), 2),
        "min_temperature": df["degree"].min(),
        "max_temperature": df["degree"].max(),
        "most_frequent_condition": df["condition"].mode()[0] if not df["condition"].mode().empty else None
    }
    return summary


@router.get("/weather/export")
async def export_weather_history():
    if not weather_recorder.history:
        return {"message": "No weather records to export."}

    filepath = weather_recorder.export_to_csv()

    return FileResponse(
        path=filepath,
        media_type="text/csv",
        filename="weather_history.csv"
    )