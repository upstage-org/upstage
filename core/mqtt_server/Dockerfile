FROM alpine:3.12

# Install packages
RUN apk --no-cache add mosquitto mosquitto-clients

RUN mkdir /var/log/mosquitto && chown mosquitto /var/log/mosquitto

COPY ./pw.txt /etc/mosquitto/pw.txt
COPY ./mosquitto.conf /etc/mosquitto/mosquitto.conf
RUN mosquitto_passwd  -U /etc/mosquitto/pw.txt

# Expose MQTT port
EXPOSE 1883
EXPOSE 9001
#EXPOSE 22

ENV PATH /usr/sbin:$PATH

ENTRYPOINT ["/usr/sbin/mosquitto","-c","/etc/mosquitto/mosquitto.conf"]
