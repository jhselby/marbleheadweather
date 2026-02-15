import requests
import json

LAT, LON = 42.5014, -70.8750

def fetch_weather():
    # 1. Get the Forecast (Model Data)
    forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m,windspeed_10m&timezone=America%2FNew_York&forecast_days=1"
    
    # 2. Get the Actuals (NWS Beverly Airport Station)
    # NWS requires a 'User-Agent' header (just a name for your app)
    nws_url = "https://api.weather.gov/stations/KBVY/observations/latest"
    headers = {'User-Agent': '(my-weather-app, contact@example.com)'}

    try:
        forecast_res = requests.get(forecast_url).json()
        actual_res = requests.get(nws_url, headers=headers).json()

        # Combine them into one file
        combined_data = {
            "forecast": forecast_res,
            "current_actual": {
                "temp": (actual_res['properties']['temperature']['value'] * 9/5) + 32, # Convert C to F
                "wind": actual_res['properties']['windSpeed']['value'] * 0.621371 # Convert km/h to mph
            }
        }

        with open('weather_data.json', 'w') as f:
            json.dump(combined_data, f, indent=4)
        print("Success! Wyman Cove data updated with NWS actuals.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_weather()
