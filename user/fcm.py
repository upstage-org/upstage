# -*- coding: iso8859-15 -*-
####
#### Run this asynchronously!
####
import os,sys
import pytz
import arrow
import json
#from pyfcm import FCMNotification
import requests
import pprint
import asyncio

import firebase_admin
from firebase_admin import messaging,credentials

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from config.project_globals import DBSession,app

cred = credentials.Certificate(os.path.join(projdir,'config/settings/firebase.json'))
fbapp = firebase_admin.initialize_app(cred)

async def send_pushnot(user,event_item_dict):

    # Maybe this user turned off push notifications.
    if not user['firebase_pushnot_id']:
        return

    # Push notifications don't depend on phone numbers. Google identifies the device itself.
    event_item_dict['event_date_time'] = event_item_dict['event_date_time'].isoformat()

    headers = {
        'Content-Type': 'application/json; UTF-8',
        'Authorization': 'Bearer ' + cred.get_access_token().access_token,
        }
    data = {
        "message": {
            "token" : user['firebase_pushnot_id'],
            "notification": {
                "title": event_item_dict['title'],
                "body": event_item_dict['message'],
                #"channel": 'projectname',
            },
            "data": {
                "color":"#00ACD4",
                "priority":"high",
                "channel":"projectname",
                "icon":"ic_notif",
                "group": "GROUP",
                "sound": "default",
                "id": "id",
                "show_in_foreground": "true",
                "event":json.dumps(event_item_dict),
            },
        }
    }
    s = requests.Session()
    pprint.pprint(data)
    result = s.post('https://fcm.googleapis.com/v1/projects/projectname/messages:send', data=json.dumps(data),
        headers=headers)
    if not result:
        app.logger.error("Not visible to user:Push notification failed for user:{}:{}".format(user['id'],result.text))
    print("Push Notification Response: {}".format(pprint.pformat(result.text)))

