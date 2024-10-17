import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from src.global_config import MQTT_USER, MQTT_PASSWORD, MQTT_BROKER, MQTT_PORT
from src.event_archive.systems.system import run
from src.event_archive.messages.mqtt import build_client

if __name__ == "__main__":
    print(f"Connecting to {MQTT_BROKER}:{MQTT_PORT} as {MQTT_USER}, {MQTT_PASSWORD}")
    run()
    print('Running event archive')
    mqtt_client = build_client()
    print('Built client successful')
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.loop_forever()
