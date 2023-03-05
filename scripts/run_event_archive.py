import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from core.event_archive.system import run
from core.event_archive.mqtt import build_client
import core.event_archive.actions
from config import MQTT_USER, MQTT_PASSWORD, MQTT_BROKER, MQTT_PORT

if __name__ == "__main__":
    run()
    mqtt_client = build_client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.loop_forever()
