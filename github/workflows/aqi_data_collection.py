import pandas as pd
import os
import requests
from datetime import datetime

# ✅ Step 1: Set your API keys manually
OPENWEATHER_API_KEY = "ee88310481e99a7843bdedc0cca27fd1"
AQICN_API_TOKEN = "2eb7e59a27fec6826892da8d9b3f9ff95e6c573e"

# ✅ Step 2: Karachi Location
LAT, LON = 24.8607, 67.0011

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
        "datetime_utc": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.date(),
        "day": now.day,
        "month": now.month,
        "weekday": now.weekday()
    }
    return {**time_features, **fetch_openweather(), **fetch_aqicn()}

def main():
    # ✅ Prepare daily folder path
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    folder_path = f"data/{today_str}"
    os.makedirs(folder_path, exist_ok=True)
    csv_file_path = os.path.join(folder_path, "karachi.csv")

    # ✅ Fetch data and save to daily CSV
    row = get_data_row()
    df = pd.DataFrame([row])
    df.to_csv(csv_file_path, index=False)

    print(f"✅ Saved daily data to: {csv_file_path}")

if __name__ == "__main__":
    main()

















