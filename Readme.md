# 🌦️ Weather Reporter — CLI & FastAPI

A modular Python app to fetch, record, and analyze weather data using OpenWeatherMap. Built with async API calls, input validation, logging, FastAPI endpoints, and CSV export. Features include async weather fetching with retry logic, input validation for city names, FastAPI RESTful endpoints, weather history tracking (in-memory), CSV export (downloadable via API), statistical summary via Pandas, modular architecture with docstrings and type hints, and a CLI interface for local usage.


To set up the project:
first clone the repo using: git clone https://github.com/mennatullahra/WeatherFetcher-FastAPI.git and cd into the project folder. 
Create and activate a virtual environment using: python -m venv venvName 
followed by venvName\Scripts\activate on Windows or source venvName/bin/activate on macOS/Linux. Then install dependencies with: pip install -r requirements.txt.

To run the CLI, execute: python app.main.py. 
You’ll be presented with a menu: 
    1. Check Weather
    2. View History
    3. Export to CSV
    4. Exit. 
Example interaction: Enter city name: Cairo 
  City: Cairo | Degree: 32°C | Condition: Sunny | Humidity: 40%.

To run the FastAPI server, use: python -m uvicorn app.main:app --reload. 
Visit Swagger UI at http://127.0.0.1:8000/docs. 
Available routes include: 
  GET /weather/city/{city} to fetch weather for a single city, 
  GET /weather/multi?cities=a,b,c to fetch weather for multiple cities, 
  GET /weather/summary to return statistical summary, 
  GET /weather/export to download weather history as CSV.

The app uses OpenWeatherMap as its data provider. 
The API endpoint is https://api.openweathermap.org/data/2.5/weather with parameters: q for city name, appid for your API key, and units for metric or imperial.

Project structure includes: app/main.py, WeatherRouter.py, WeatherFetcher.py, WeatherRecorder.py, Weather.py, RetryMechanism.py, Validator.py, cli/CLI.py, weather.csv, weather.log, requirements.txt, and README.md.

Made by Mennatullah (https://github.com/mennatullahra)
