#!/bin/bash
docker build . -f Dockerfile -t mqttserver:latest --network host 
docker save -o ./mqttserver_latest.tar mqttserver:latest
gzip -f ./mqttserver_latest.tar
