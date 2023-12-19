import json
import logging
import secrets
from datetime import datetime, timedelta

import paho.mqtt.client as mqtt
from config.settings import MQTT_TRANSPORT

from upstage_stats.db import DBSession, get_scoped_session
from upstage_stats.models import ConnectionStat, ReceiveStat

CONNECTION_TOPIC = "upstage_stats/connections"
LIVE_CLIENT_TOPIC = "upstage_stats/live_clients"
client_messages = {}


def on_connect(client: mqtt.Client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(CONNECTION_TOPIC)
        connection_payload = {"connected": client._client_id.decode("utf-8"),
                              "timestamp": datetime.utcnow().isoformat(),
                              "channel": CONNECTION_TOPIC}
        client.publish(CONNECTION_TOPIC,
                       payload=json.dumps(connection_payload))

        client.subscribe(LIVE_CLIENT_TOPIC)
        print("Connected successfully! Waiting for new messages...")


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    global client_messages

    if not msg.retain:
        client_id = client._client_id.decode("utf-8")
        print(msg.topic, msg.payload)
        payload = json.loads(msg.payload)
        if client_id not in client_messages:
            client_messages[client_id] = 0
        if 'connected' in payload:
            try:
                session = get_scoped_session()
                connection_stat = ConnectionStat(
                    connected_id=payload['connected'],
                    mqtt_timestamp=payload['timestamp'],
                    topic=payload['channel'],
                    payload=payload
                )
                session.add(connection_stat)
                session.commit()
            except Exception as error:
                logging.error(error)
            finally:
                if session is not None:
                    session.close()
        else:
            client_messages[client_id] = client_messages[client_id] + 1

        print(f'message_count:  {client_messages[client_id]}')
        if client_messages[client_id] == 10:
            client_messages[client_id] = 0
            try:
                session = get_scoped_session()
                receive_stat = session.query(ReceiveStat).filter(
                    ReceiveStat.received_id == client_id)
                if not receive_stat.first():
                    receive_stat = ReceiveStat(
                        received_id=client_id,
                        mqtt_timestamp=datetime.utcnow(),
                        topic=LIVE_CLIENT_TOPIC,
                        payload=payload
                    )
                    session.add(receive_stat)
                    session.commit()
                else:
                    receive_stat.update(
                        {ReceiveStat.mqtt_timestamp: datetime.utcnow(), ReceiveStat.payload: payload}, synchronize_session=False)
            except Exception as error:
                logging.error(error)
            finally:
                if session is not None:
                    session.close()


def on_disconnect(client, userdata, rc):
    print('disconnect ' + client._client_id.decode("utf-8"))
    client.connected_flag = False
    client.disconnect_flag = True


def get_client_id():
    return secrets.token_urlsafe(16)


def build_client(client_id=get_client_id(), transport=MQTT_TRANSPORT):
    client = mqtt.Client(client_id=client_id, transport=transport)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    return client


def get_not_alive_users():
    two_minute_ago = datetime.utcnow() - timedelta(minutes=2)
    not_alive_clients = DBSession.query(ReceiveStat).filter(
        ReceiveStat.mqtt_timestamp < two_minute_ago).all()
    return [x.received_id for x in not_alive_clients]
