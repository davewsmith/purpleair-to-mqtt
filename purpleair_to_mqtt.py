import os
import sys

import dotenv

from mqtt import publish_to_mqtt
from pa_to_influx import pa_to_influx
from purpleair import pa_data

dotenv.load_dotenv()


def purpleair_to_mqtt(sensor_index : int):
    """Fetch data from a PurpleAir sensor and publish to MQTT
    """
    data = pa_data(sensor_index)

    if "error" in data:
        print(f"PurpleAir API returned {data.get('error')}")
    else:
        topic = os.getenv("MQTT_TOPIC", "aqi")
        message = pa_to_influx(data)
        publish_to_mqtt("purpleair", topic, message)


if __name__ == '__main__':
    sensor_indexes = sys.argv[1:]
    if len(sensor_indexes) == 0:
        print(f"usage: {sys.argv[0]} sensor_index ...")
        sys.exit(0)
    for sensor_index in sensor_indexes:
        try:
            purpleair_to_mqtt(int(sensor_index))
        except exception as ex:
            print(f"{ex!r}")
