import pandas as pd
import os
import requests
from datetime import datetime

# ✅ Step 1: Set your API keys manually
OPENWEATHER_API_KEY = "ee88310481e99a7843bdedc0cca27fd1"
AQICN_API_TOKEN = "2eb7e59a27fec6826892da8d9b3f9ff95e6c573e"


LAT, LON = 24.8607, 67.0011
CSV_FILE = "data/karachi_aqi_data.csv"

def fetch_openweather():
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}&units=metric"
    r = requests.get(url).json()
    return {
        "temp": r["main"]["temp"],
        "humidity": r["main"]["humidity"],
        "pressure": r["main"]["pressure"],
        "wind_speed": r["wind"]["speed"]
    }

def fetch_aqicn():
    url = f"https://api.waqi.info/feed/geo:{LAT};{LON}/?token={AQICN_API_TOKEN}"
    r = requests.get(url).json()
    iaqi = r["data"]["iaqi"]
    return {
        "aqi": r["data"]["aqi"],
        "pm25": iaqi.get("pm25", {}).get("v"),
        "pm10": iaqi.get("pm10", {}).get("v"),
        "co": iaqi.get("co", {}).get("v"),
        "no2": iaqi.get("no2", {}).get("v"),
        "so2": iaqi.get("so2", {}).get("v"),
        "o3": iaqi.get("o3", {}).get("v")
    }

def get_data_row():
    now = datetime.utcnow()
    time_features = {
        "datetime": now,
        "hour": now.hour,
        "day": now.day,
        "month": now.month,
        "weekday": now.weekday()
    }
    return {**time_features, **fetch_openweather(), **fetch_aqicn()}

def main():
    os.makedirs("data", exist_ok=True)
    row = get_data_row()
    df_new = pd.DataFrame([row])

    # ✅ Append to old file if exists
    if os.path.exists(CSV_FILE):
        df_old = pd.read_csv(CSV_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(CSV_FILE, index=False)
    print("✅ Appended new row to CSV")

if __name__ == "__main__":
    main()

















