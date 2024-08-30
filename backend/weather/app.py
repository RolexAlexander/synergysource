from flask import Flask, jsonify, request
import requests
import pandas as pd

app = Flask(__name__)

# Replace with your actual API key and base URL
WEATHER_API_KEY = "a3a196f898853f6c894e5c066f8af5c0"
BASE_URL = "http://api.openweathermap.org/data/2.5/onecall"

@app.route('/weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Please provide latitude and longitude"}), 400

    params = {
        'lat': lat,
        'lon': lon,
        'appid': WEATHER_API_KEY,
        'units': 'metric',  # Change to 'imperial' for Fahrenheit
        'exclude': 'minutely'  # Example to exclude minutely data
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data"}), 500

    weather_data = response.json()
    return jsonify(process_weather_data(weather_data)), 200

def process_weather_data(data):
    # Convert current weather data to DataFrame
    current_df = pd.DataFrame([{
        "temperature": data["current"]["temp"],
        "description": data["current"]["weather"][0]["description"],
        "humidity": data["current"]["humidity"],
        "wind_speed": data["current"]["wind_speed"],
        "wind_gust": data["current"].get("wind_gust", None),
        "pressure": data["current"]["pressure"],
        "visibility": data["current"]["visibility"],
        "uvi": data["current"]["uvi"],
        "clouds": data["current"]["clouds"],
        "sunrise": data["current"]["sunrise"],
        "sunset": data["current"]["sunset"],
    }])

    # Convert daily forecast to DataFrame
    daily_df = pd.DataFrame([
        {
            "date": day["dt"],
            "summary": day.get("summary", ""),
            "temperature": day["temp"]["day"],
            "weather": day["weather"][0]["description"],
            "humidity": day["humidity"],
            "wind_speed": day["wind_speed"],
            "clouds": day["clouds"],
            "rain": day.get("rain", 0),
            "uvi": day["uvi"]
        } for day in data["daily"]
    ])

    # Convert alerts to DataFrame
    alerts_df = pd.DataFrame([
        {
            "event": alert["event"],
            "start": alert["start"],
            "end": alert["end"],
            "description": alert["description"]
        } for alert in data.get("alerts", [])
    ])

    # Convert DataFrames to JSON
    return {
        "current": current_df.to_dict(orient='records'),
        "daily_forecast": daily_df.to_dict(orient='records'),
        "alerts": alerts_df.to_dict(orient='records')
    }

if __name__ == '__main__':
    app.run(debug=True)
