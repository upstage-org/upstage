from config import MQTT_BROKER, MQTT_PASSWORD, MQTT_PORT, MQTT_USER
from upstage_stats.mqtt import build_client

if __name__ == "__main__":
    client = build_client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()
