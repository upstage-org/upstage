from core.event_archive.system import run
from core.event_archive.mqtt import build_client
import event_archive.actions
from config import MQTT_USER, MQTT_PASSWORD, MQTT_BROKER, MQTT_PORT

if __name__ == "__main__":
    run()
    mqtt_client = build_client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.loop_forever()
