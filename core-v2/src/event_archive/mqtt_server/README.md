## Docker build of Mosquitto Server (does not deal with deployment)
* Change the passwords in the pw.txt file
* Check the config in the mosquitto.conf
* Run docker_build.sh. Note that it saves a copy to disk, called mqttserver_latest.tar.gz
* Copy this disk image to the destination machine where you wish to run the container. 
* Deploy this as you see fit. Keep in mind, the host machine needs ports 9001 and 1883 open, and able to pass traffic through to this image. This can be accomplished with:
** docker run -p 9001:9001 -p 1883:1883 mqttserver:latest
