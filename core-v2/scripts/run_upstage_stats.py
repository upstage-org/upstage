from src.global_config import MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD
from src.upstage_stats.mqtt import build_client
if __name__ == "__main__":
    print(f"Connecting to {MQTT_BROKER}:{MQTT_PORT} as {MQTT_USER}")
    client = build_client()
    print('Built client successful')
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, int(MQTT_PORT))
    client.loop_forever()
