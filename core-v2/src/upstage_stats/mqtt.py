import json
import logging
import secrets
from datetime import datetime, timedelta

import paho.mqtt.client as mqtt

from global_config import MQTT_TRANSPORT, DBSession, ScopedSession
from upstage_stats.db_models.receive_stat import ReceiveStatModel
from upstage_stats.db_models.connection_stat import ConnectionStatModel


CONNECTION_TOPIC = "upstage_stats/connections"
LIVE_CLIENT_TOPIC = "upstage_stats/live_clients"
client_messages = {}


def on_connect(client: mqtt.Client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(CONNECTION_TOPIC)
        connection_payload = {
            "connected": client._client_id.decode("utf-8"),
            "timestamp": datetime.now().isoformat(),
            "channel": CONNECTION_TOPIC,
        }
        client.publish(CONNECTION_TOPIC, payload=json.dumps(connection_payload))

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
        if "connected" in payload:
            try:
                with ScopedSession() as session:
                    connection_stat = ConnectionStatModel(
                        connected_id=payload["connected"],
                        mqtt_timestamp=payload["timestamp"],
                        topic=payload["channel"],
                        payload=payload,
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

        print(f"message_count:  {client_messages[client_id]}")
        if client_messages[client_id] == 10:
            client_messages[client_id] = 0
            try:
                with ScopedSession() as session:
                    receive_stat = session.query(ReceiveStatModel).filter(
                        ReceiveStatModel.received_id == client_id
                    )
                    if not receive_stat.first():
                        receive_stat = ReceiveStatModel(
                            received_id=client_id,
                            mqtt_timestamp=datetime.now(),
                            topic=LIVE_CLIENT_TOPIC,
                            payload=payload,
                        )
                        session.add(receive_stat)
                        session.commit()
                    else:
                        receive_stat.update(
                            {
                                ReceiveStatModel.mqtt_timestamp: datetime.utcnow(),
                                ReceiveStatModel.payload: payload,
                            },
                            synchronize_session=False,
                        )
            except Exception as error:
                logging.error(error)
            finally:
                if session is not None:
                    session.close()


def on_disconnect(client, userdata, rc):
    print("disconnect " + client._client_id.decode("utf-8"))
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
    two_minute_ago = datetime.now() - timedelta(minutes=2)
    not_alive_clients = (
        DBSession.query(ReceiveStatModel)
        .filter(ReceiveStatModel.mqtt_timestamp < two_minute_ago)
        .all()
    )
    return [x.received_id for x in not_alive_clients]
