# PurpleAir-to-MQTT

Pull data from a PurpleAir sensor, derive the AQI that their web interface
shows, and publish to MQTT.

The MQTT topic is configurable. The message conforms to influx line procotol,
and includes the sensor index and name as tags, and the temperature,
humidity, and derived AQI as fields.

**Unlicensed, use-at-your-own-riskware.**
I pulled this together from pieces to scratch a personal itch.

## Usage

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

Copy `env.template` to `.env`, and fill it in with a PurpleAir API key that has READ permission,
details for accessing an MQTT server, and the MQTT topic to publish on.

Then,

     python purpleair_to_mqtt.py <sensorindex>

Setting DEBUG=1 in `.env` loads sample data and prints the MQTT topic and message instead
of requiring a server.
