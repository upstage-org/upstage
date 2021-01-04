import logging
import json
import os
import re
import secrets
import sys

import paho.mqtt.client as paho

import config as conf
from system import event_queue


def on_connect(client, userdata, flags, rc):
    client.subscribe(conf.PERFORMANCE_TOPIC_RULE)


def on_message(client, userdata, msg):
    try:
        event_queue.put({"topic": msg.topic, "payload": msg.payload, "timestamp": msg.timestamp})
    except:
        pass


def get_client_id():
    return secrets.token_urlsafe(16)


def build_client(client_id=get_client_id(), transport=conf.MQTT_TRANSPORT):
    client = paho.Client(client_id=client_id, transport=transport)
    client.on_connect = on_connect
    client.on_message = on_message
    return client