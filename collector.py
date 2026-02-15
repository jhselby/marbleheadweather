import requests
import json

LAT, LON = 42.5014, -70.8750

def fetch_weather():
    # 1. Get Weather
    f_url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m&timezone=America%2FNew_York&forecast_days=1&temperature_unit=fahrenheit"
    # 2. Get Tides (Salem, MA)
    t_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=8442668&product=predictions&datum=MLLW&time_zone=lst_ldt&units=english&format=json"

    try:
        f_res = requests.get(f_url).json()
        t_res = requests.get(t_url).json()

        # Extract temperature list
        temps = f_res['hourly']['temperature_2m']
        
        # Extract and clean tide list (one per hour)
        raw_tides = t_res.get('predictions', [])
        clean_tides = [float(p['v']) for p in raw_tides[::10]][0:24]

        # Save everything in a flat, easy-to-read structure
        combined_data = {
            "temp_labels": [t.split("T")[1] for t in f_res['hourly']['time'][0:24]],
            "temp_values": temps[0:24],
            "tide_values": clean_tides,
            "high": max(temps),
            "low": min(temps)
        }

        with open('weather_data.json', 'w') as f:
            json.dump(combined_data, f, indent=4)
        print("Success: Data Synced!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_weather()
