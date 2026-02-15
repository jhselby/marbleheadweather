import requests
import json

LAT, LON = 42.5014, -70.8750

def fetch_weather():
    # We added &daily=sunrise,sunset to the URL here
    forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m,windspeed_10m&daily=sunrise,sunset&timezone=America%2FNew_York&forecast_days=1&temperature_unit=fahrenheit&wind_speed_unit=mph"
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
            },
            # This is the "bridge" that sends sun times to your HTML
            "sun_times": {
                "sunrise": forecast_res['daily']['sunrise'][0],
                "sunset": forecast_res['daily']['sunset'][0]
            }
        }

        with open('weather_data.json', 'w') as f:
            json.dump(combined_data, f, indent=4)
        print("Success! Sun times are now in the data.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_weather()
