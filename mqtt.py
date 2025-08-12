import os
import time

import paho.mqtt.client as mqtt


def on_publish(client, userdata, mid, reason_code, properties):
    try:
        userdata.remove(mid)
    except KeyError as ex:
        print(f"{ex!r}")


def publish_to_mqtt(client_name: str, topic : str, message : str):
    if os.getenv("DEBUG", '0') == '1':
        print(topic)
        print(message)
        return

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
    mqtt_client.username = os.getenv("MQTT_USER", None)
    mqtt_client.password = os.getenv("MQTT_PASSWORD", None)

    mqtt_client.on_publish = on_publish

    unacked_mids = set()
    mqtt_client.user_data_set(unacked_mids)

    mqtt_client.connect(os.getenv("MQTT_HOST"))
    mqtt_client.loop_start()

    pub = mqtt_client.publish(topic, message, qos=1)
    unacked_mids.add(pub.mid)
    pub.wait_for_publish()
    assert len(unacked_mids) == 0
   
    mqtt_client.disconnect()
    mqtt_client.loop_stop() 
