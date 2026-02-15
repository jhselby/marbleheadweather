import requests
import json

LAT, LON = 42.5014, -70.8750

def fetch_weather():
    # 1. Get the Forecast in Fahrenheit and MPH
    forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m,windspeed_10m&timezone=America%2FNew_York&forecast_days=1&temperature_unit=fahrenheit&wind_speed_unit=mph"
    
    # 2. Get the Actuals from Beverly Airport
    nws_url = "https://api.weather.gov/stations/KBVY/observations/latest"
    headers = {'User-Agent': '(my-weather-app, contact@example.com)'}

    try:
        forecast_res = requests.get(forecast_url).json()
        actual_res = requests.get(nws_url, headers=headers).json()

        combined_data = {
            "forecast": forecast_res,
            "current_actual": {
                "temp": (actual_res['properties']['temperature']['value'] * 9/5) + 32,
                "wind": actual_res['properties']['windSpeed']['value'] * 0.621371
            }
        }

        with open('weather_data.json', 'w') as f:
            json.dump(combined_data, f, indent=4)
        print("Success! Fahrenheit data updated.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_weather()
