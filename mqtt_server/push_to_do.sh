#!/bin/bash
# Before running this, do:
# export DO_TOKEN=your_digital_ocean_personal_access_token
# Run the docker build script
# docker run mqttserver:latest, then look at container id. pass the container id into this script
container_id=$1
docker-machine create --digitalocean-size "s-1vcpu-2gb" --driver digitalocean --digitalocean-access-token ${DO_TOKEN} ${container_id}
