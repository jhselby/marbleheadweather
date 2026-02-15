import requests
import json
from datetime import datetime

LAT, LON = 42.5014, -70.8750

def fetch_weather():
    # 1. Weather & Sun Data
    forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m&daily=sunrise,sunset&timezone=America%2FNew_York&forecast_days=1&temperature_unit=fahrenheit"
    
    # 2. Tide Data (Salem, MA station 8442668)
    tide_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=8442668&product=predictions&datum=MLLW&time_zone=lst_ldt&units=english&format=json"

    try:
        f_res = requests.get(forecast_url).json()
        t_res = requests.get(tide_url).json()

        temps = f_res['hourly']['temperature_2m']
        
        combined_data = {
            "forecast": f_res,
            "high_low": {"high": max(temps), "low": min(temps)},
            "tides": [float(p['v']) for p in t_res['predictions'][::6]], # Sample every hour
            "sun_times": {
                "sunrise": f_res['daily']['sunrise'][0],
                "sunset": f_res['daily']['sunset'][0]
            }
        }

        with open('weather_data.json', 'w') as f:
            json.dump(combined_data, f, indent=4)
        print("Success! Tides and High/Low added.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_weather()
