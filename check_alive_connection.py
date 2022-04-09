import time

import paho.mqtt.client as mqtt

from config.settings import MQTT_BROKER, MQTT_PASSWORD, MQTT_PORT, MQTT_USER
from upstage_stats.mqtt import get_not_alive_users

if __name__ == "__main__":
    while(True):
        client_ids = get_not_alive_users()
        for client_id in client_ids:
            client = mqtt.Client(client_id)
            client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
            client.connect(MQTT_BROKER, MQTT_PORT)
            client.disconnect()
        time.sleep(60*2)
