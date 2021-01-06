import logging
import json
import os
import re
import secrets
import sys

import paho.mqtt.client as paho

import config as conf
from db import build_client as db_client


def on_connect(client, userdata, flags, rc):
    client.subscribe(conf.PERFORMANCE_TOPIC_RULE)


def on_message(client, userdata, msg):
    try:
        client = db_client()
        db = client[conf.MONGO_DB]
        db[conf.EVENT_COLLECTION].insert_one(
            {"topic": msg.topic, "payload": msg.payload, "timestamp": msg.timestamp}
        )
        client.close()
    except Exception as e:
        logging.error(e)


def get_client_id():
    return secrets.token_urlsafe(16)


def build_client(client_id=get_client_id(), transport=conf.MQTT_TRANSPORT):
    client = paho.Client(client_id=client_id, transport=transport)
    client.on_connect = on_connect
    client.on_message = on_message
    return client
