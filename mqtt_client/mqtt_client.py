#!/usr/bin/env python3
# -*- coding: iso8859-15 -*-
from paho.mqtt import client as mqtt
import ssl
import os, sys
import time
import subprocess
import pprint
import uuid

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import jsonify
from flask_restx import abort, Resource, Api, fields, marshal_with, reqparse
from flask import current_app, request, redirect, render_template, make_response
from auth.auth_api import jwt_required

path_to_root_cert = str(projdir) + "/some.cert"
domain_name = "some_domain.org"

class MQTTClient(object):
    countDisconnects = 0

    def __init__(self,client_id):
        self.client_id = client_id
        self.client = None
        self.nonzero_count = 0
        self.unacked_messages = []

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:                                                                             
            msg = "Connected successfully: {0}, Port: {1}".format(pprint.pformat(client),pprint.pformat(flags))
            logger.info(msg)

        elif rc == 5:
            msg = "Not authorized to connect, or hub time is wrong: (return code 5) ({0}, {1}, {2})".format(pprint.pformat(client),pprint.pformat(userdata),pprint.pformat(flags))
            logger.error(msg)
        else:
            msg = "Connection failed: return code {0}".format(rc)
            logger.error(msg)

        #client.subscribe("client/" + self.client_id + "/messages/devicebound/#")

    def on_disconnect(self, client, userdata, rc):
        if rc == 1:                                                                             
            msg = "Unexpected Connection fail: return code 1"
            logger.error(msg)
        else:
            msg = "Disconnected from the Platform"
            logger.error(msg)

        self.countDisconnects+=1
        if self.countDisconnects > 10:
            msg = "Process unexpectedly disconnected more than 10 times, killing and restarting the process."
            logger.error(msg)
            sys.exit(-1)

    def on_message(self, client, userdata, msg):
        msg = " - ".join((msg.topic, str(msg.payload)))
        logger.info(msg)

    def on_publish(self, client, userdata, mid):
        msg = "Publish Callback message ID for internal: {0}".format(mid)
        logger.info(msg)
        self.countDisconnects = 0
        if mid in self.unacked_messages:
            self.unacked_messages.remove(mid)

    def on_log(self, client, userdata, level, buffer):
        msg = "Log entry from device {0}: {1}, {2}, {3}".format(self.client_id,level,buffer,userdata)
        logger.info(msg)

    def client_start(self,on_message=None,mqtt_user_param=None,mqtt_password=None):
        self.client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv5)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = on_message if on_message else self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_log = self.on_log
        '''
        self.client.tls_set(ca_certs=path_to_root_cert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
        self.client.tls_insecure_set(False)

        self.client.connect(domain_name, port=9876)
        print("Connected as {0}".format(mqtt_user))
        '''
        self.client.loop_start()

    def client_publish(self, json_payload):
        result,message_id = self.client.publish("devices/" + self.client_id + "/messages/events/data", payload=json_payload, qos=1, retain=False)
        if result != 0:
            msg = "Published message ID {0}: return code is not zero: {1}".format(message_id,result)
            logger.error(msg)
            self.nonzero_count += 1
            if self.nonzero_count >= 10:
                msg = "Process for device {0} had greater than 10 publish failures, killing and restarting the process.".format(self.client_id)
                logger.error(msg,extra=get_logger_extras(__file__,__name__))
                sys.exit(-1)
        else:
            msg = "Published message ID {0}: {1}".format(message_id,result)
            logger.info(msg)
            self.unacked_messages.append(message_id)


    def client_shutdown(self):
        self.client.loop_stop()
        self.client.disconnect()


if __name__ == "__main__":
    # Each client id has to be unique, so the origin can be identified.
    #client_id = configdata['gid'][8:].upper() + '_' + str(int(time.time()))
    client_id = str(uuid.uuid4())

    if sys.argv[1] == 'publish':
        x=MQTTClient(client_id)
        x.client_start()
        count = 0
        try:
            while True:
                count += 1
                outbound = "{\"test\":\"one\",\"test2\":\"%d\"}" % count
                x.client_publish(outbound)
                time.sleep(5)
                print('Publishing: {0}'.format(count))
        finally:
            x.client_shutdown()

    elif sys.argv[1] == 'subscribe':
        x=MQTTClient(client_id)
        x.client_start()
        try:
            # Subscribe to a device other than your own: user prompt.client_id
            x.client.subscribe("devices/" + sys.argv[2] + "/messages/events/data")
            while True:
                time.sleep(5)
        finally:
            x.client_shutdown()

