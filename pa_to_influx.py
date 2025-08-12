# Convert JSON from the purple air `sensors` API endpoint
# to influx line format, turning pm2.5 into AQI along the
# way.

import json
import re

def pa_to_influx(data : dict) -> str:
    sensor = data.get("sensor")
    name = sensor.get("name")
    sensor_index = sensor.get("sensor_index")
    temperature = sensor.get("temperature")
    humidity = sensor.get("humidity")
    aqi = sensor.get("aqi")
    last_seen = sensor.get("last_seen")
    return (
        "purpleair,"
        f"name={sanitize(name)},"
        f"sensor_index={sensor_index}"
        " "
        f"temperature={temperature},"
        f"humidity={humidity},"
        f"aqi={aqi}"
        " "
        f"{last_seen}000000000"  # epoch_time to nanoseconds
    )

def sanitize(s : str) -> str:
    s = re.sub(r'[ ,]', "_", s)
    return re.sub(r'_+', '_', s)


if __name__ == '__main__':
    from purpleair import sample_data
    print(pa_to_influx(sample_data()))
