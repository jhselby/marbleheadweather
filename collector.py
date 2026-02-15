ximport requests
import json

# Marblehead, MA Coordinates
LAT, LON = 42.5048, -70.8578

def fetch_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m,precipitation_probability,windspeed_10m&timezone=America%2FNew_York&forecast_days=3"
    response = requests.get(url)
    if response.status_code == 200:
        with open('weather_data.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
        print("Updated Marblehead data successfully.")

if __name__ == "__main__":
    fetch_weather()
