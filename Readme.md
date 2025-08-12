# 🌦️ Weather Reporter CLI

A command-line tool to fetch and record weather data using OpenWeatherMap. Built with async API calls, input validation, logging, and CSV export.

## 🚀 Features

- Async weather fetching with retry logic
- Input validation for city names
- Rotating log files
- Weather history tracking
- CSV export
- Modular codebase with docstrings and type hints

## 🛠️ Setup

1. Clone the repo:
```bash
git clone https://github.com/yourusername/weather-reporter-cli.git
cd weather-reporter-cli

python -m venv venvName
source venvName/Scripts/activate 

pip install -r requirements.txt


### 4. **Usage Instructions**
```markdown
## 🧪 Usage

Run the app:
```bash
python main.py

Choose from the menu:

1. Check Weather
2. View History
3. Export to CSV
4. Exit

Example:

Enter city name: Cairo
City: Cairo | Degree: 32°C | Condition: Sunny | Humidity: 40%


### 5. **API Info**
```markdown
## 🌐 API Info

- Provider: OpenWeatherMap
- Endpoint: `https://api.openweathermap.org/data/2.5/weather`
- Parameters:
  - `q`: City name
  - `appid`: Your API key
  - `units`: metric or imperial

