import requests
import json

LAT, LON = 42.5014, -70.8750

def fetch_weather():
    # Weather Data
    f_url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m&timezone=America%2FNew_York&forecast_days=1&temperature_unit=fahrenheit"
    # Tide Data (Salem, MA)
    t_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=8442668&product=predictions&datum=MLLW&time_zone=lst_ldt&units=english&format=json"

    try:
        f_res = requests.get(f_url).json()
        t_res = requests.get(t_url).json()

        # Clean Tides: Get one point per hour to match weather
        raw_tides = t_res.get('predictions', [])
        clean_tides = [float(p['v']) for p in raw_tides[::10]][0:24]
        
        # Get High/Low from the forecast
        temps = f_res['hourly']['temperature_2m']

        combined_data = {
            "forecast": f_res,
            "tide_values": clean_tides,
            "high": max(temps),
            "low": min(temps)
        }

        with open('weather_data.json', 'w') as f:
            json.dump(combined_data, f, indent=4)
        print("Success: Data Synced")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_weather()
