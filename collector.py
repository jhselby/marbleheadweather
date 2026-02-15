import requests
import json

LAT, LON = 42.5014, -70.8750

def fetch_weather():
    # 1. Weather, High/Low, and Sun times
    f_url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m&daily=sunrise,sunset&timezone=America%2FNew_York&forecast_days=1&temperature_unit=fahrenheit"
    # 2. Tides (Salem, MA)
    t_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=8442668&product=predictions&datum=MLLW&time_zone=lst_ldt&units=english&format=json"

    try:
        f_data = requests.get(f_url).json()
        t_data = requests.get(t_url).json()

        # Extract temperature list and sun times
        temps = f_data['hourly']['temperature_2m'][0:24]
        sunrise = f_data['daily']['sunrise'][0].split("T")[1]
        sunset = f_data['daily']['sunset'][0].split("T")[1]
        
        # CLEAN TIDES: Convert from "predictions list" to "list of numbers"
        # We take every 10th prediction (every hour) to match the 24 weather hours
        raw_predictions = t_data.get('predictions', [])
        clean_tides = [float(p['v']) for p in raw_predictions[::10]][0:24]

        combined_data = {
            "temp_labels": [t.split("T")[1] for t in f_data['hourly']['time'][0:24]],
            "temp_values": temps,
            "tide_values": clean_tides,
            "high": max(temps),
            "low": min(temps),
            "sunrise": sunrise,
            "sunset": sunset
        }

        with open('weather_data.json', 'w') as f:
            json.dump(combined_data, f, indent=4)
        print("Success! Data fully synced.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_weather()
