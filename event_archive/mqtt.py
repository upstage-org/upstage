import logging
import json
import os
import re
import secrets
import sys

import paho.mqtt.client as paho

from config.settings import PERFORMANCE_TOPIC_RULE, MONGO_DB, EVENT_COLLECTION, MQTT_TRANSPORT
from event_archive.db import build_mongo_client


def on_connect(client, userdata, flags, rc):
    client.subscribe(PERFORMANCE_TOPIC_RULE)
    print("Connected successfully! Waiting for new messages...")


def on_message(client, userdata, msg: paho.MQTTMessage):
    if not msg.retain:
        print(msg.topic, msg.payload)

        try:
            client = build_mongo_client()
            db = client[MONGO_DB]
            db[EVENT_COLLECTION].insert_one(
                {"topic": msg.topic, "payload": msg.payload,
                    "timestamp": msg.timestamp}
            )
            client.close()
        except Exception as e:
            logging.error(e)


def get_client_id():
    return secrets.token_urlsafe(16)


def build_client(client_id=get_client_id(), transport=MQTT_TRANSPORT):
    client = paho.Client(client_id=client_id, transport=transport)
    client.on_connect = on_connect
    client.on_message = on_message
    return client
