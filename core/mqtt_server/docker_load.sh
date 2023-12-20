#!/bin/bash
gunzip -f ./mqttserver_latest.tar.gz
docker load < ./mqttserver_latest.tar
docker run -p 1883:1883 -p 9001:9001 mqttserver:latest
