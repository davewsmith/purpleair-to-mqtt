# Fetch data from a PurpleAir sensor, and calculate
# the AQI
# 
# Assumes PURPLEAIR_READ_KEY is in the environment

import json
import os

import requests

from aqi import pm25_to_aqi


def pa_data(sensor_index: int) -> dict:
    data = sensor_data(sensor_index)
    # print(json.dumps(data, indent=2))

    if "error" not in data:
        # Augment with calculated AQI
        sensor = data.get("sensor")
        pm25 = sensor.get("pm2.5")
        humidity = sensor.get("humidity")
        sensor["aqi"] = pm25_to_aqi(pm25, humidity)
    return data


def sensor_data(sensor_index: int) -> dict:
    if os.getenv("DEBUG", '0') == '1':
        return sample_data()

    headers = {
       "X-API-Key": os.getenv('PURPLEAIR_READ_KEY'),
    }
    r = requests.get(
        f'https://api.purpleair.com/v1/sensors/{sensor_index}',
        headers=headers
    )
    if r.status_code == 200:
        return r.json()
    else:
        return {"error": r.status_code}


def sample_data() -> dict:
    return json.loads(
"""
{
  "api_version": "V1.0.10-0.0.17",
  "time_stamp": 1629824214,
  "data_time_stamp": 1629824174,
  "sensor": {
    "sensor_index": 9999,
    "last_seen": 1629824174,
    "name": "My Test Sensor",
    "location_type": 0,
    "private": 0,
    "latitude": 34.0522,
    "longitude": -118.2437,
    "altitude": 200,
    "position_rating": 5,
    "last_check_in": 1629824174,
    "is_owner": 0,
    "stats": {
      "pm2.5": 12.3,
      "pm2.5_10minute": 12.0,
      "pm2.5_30minute": 11.5,
      "pm2.5_60minute": 11.0,
      "pm2.5_6hour": 10.0,
      "pm2.5_24hour": 9.0,
      "pm2.5_1week": 8.0,
      "pm1.0": 5.0,
      "pm10.0": 15.0,
      "humidity": 45.0,
      "temperature": 72,
      "pressure": 1012.0,
      "voc": 0.5,
      "ozone1": 40.0,
      "scattering_coefficient": 100.0
    }
  }
}
""")
