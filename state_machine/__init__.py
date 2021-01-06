import logging
import os
import sys

from system import run
from mqtt import build_client
import config as conf
import actions


if __name__ == "__main__":
    run()
    broker, port = None, None
    args = sys.argv[1:]
    if len(args):
        broker = args.pop(0)
    if len(args):
        port = args.pop(0)
    if broker is None:
        broker = conf.MQTT_BROKER
    if port is None:
        port = conf.MQTT_PORT
    mqtt_client = build_client()
    mqtt_client.connect(broker, port)
    mqtt_client.loop_forever()
