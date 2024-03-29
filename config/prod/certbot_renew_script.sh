#!/bin/bash

CERTBOT=`whereis certbot | awk '{print $2}'`
DOMAIN=SET_THIS_TO_THE_FULL_DOMAIN_NAME_NOT_HOSTNAME

#STREAMING_SERVER=
#STREAMING_SERVER=1
#SVC_SERVER=
#SVC_SERVER=1
#APP_SERVER=
APP_SERVER=1

CERTCHECK_FILE=/etc/letsencrypt/live/${DOMAIN}/cert.pem
if [[ -n ${SVC_SERVER} ]]
then
    OTHER_COPY=/etc/mosquitto/ca_certificates/cert.pem
else
    OTHER_COPY=
fi

now_seconds=`date +%s`
sleep 2
$CERTBOT renew

# See if certs were updated. certbot doesn't always return a 0 status when expected.
# So ignore return code issued by certbot and do our own check.
mod_seconds=`/usr/bin/stat -c %Y $CERTCHECK_FILE`

if [[ $now_seconds -lt $mod_seconds ]]
then
    echo "Updating..."
    systemctl reload nginx
    if [[ -n ${SVC_SERVER} ]]
    then
        other_seconds=`/usr/bin/stat -c %Y $OTHER_COPY`
        if [[ $other_seconds -lt $mod_seconds ]]
        then
            cd /etc/letsencrypt/live/${DOMAIN}
            cp * /etc/mosquitto/ca_certificates
            chown -R mosquitto:mosquitto /etc/mosquitto/ca_certificates
            systemctl reload mosquitto.service >> /var/log/le-renew.log 2>&1
        fi
    fi
else
    echo "No update."
fi

if [[ -n ${APP_SERVER} ]]
then
    echo "Restarting anyway in case the svc1 server certs were updated."
    systemctl restart upstage.service >> /var/log/le-renew.log 2>&1
    systemctl restart event_archive.service >> /var/log/le-renew.log 2>&1
elif [[ -n ${STREAMING_SERVER} ]]
then
    echo "Restarting our nodejs streaming service, in case streaming1 server certs were updated. This does not restart jitsi-videobridge, which uses its own cert files"
    systemctl restart upstage-streaming.service >> /var/log/le-renew.log 2>&1
fi
