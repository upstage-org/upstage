#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

ADMINS = []

DB_NAME=""
DB_USER=""
DB_PASSWD=""
DB_HOST=""
DB_PORT=5432

MONGO_HOST = "10.116.0.5"
MONGO_PORT = 27018
MONGO_DB = "upstage"
EVENT_COLLECTION = "events"

MQTT_BROKER = "10.116.0.5"
MQTT_PORT = 1884
MQTT_TRANSPORT = "tcp"
MQTT_USER = "performance"
MQTT_PASSWORD = "z48FCTsJVEUkYmtUw5S9"
PERFORMANCE_TOPIC_RULE = "#"

FLASK_HOST='127.0.0.1'
FLASK_PORT=8000
FLASK_CHAT_WEBSOCKET_PORT=8002
RUNFROM_PORT=None

ESEARCH_HOST = "127.0.0.1"
ESEARCH_PORT = 9200

ENV_TYPE="LOCAL_laptop"

UPLOAD_USER_CONTENT_FOLDER = '/tmp'

# SqlAlchemy caching defaults. Use file caching in your
# local settings file to override.
DOGPILE_CACHE_REGION='default'
DOGPILE_CACHE_CONFIG = {
    DOGPILE_CACHE_REGION + "backend":"dogpile.cache.pylibmc",
    DOGPILE_CACHE_REGION + "arguments.url":"127.0.0.1",
}

MAX_URL_CACHE_SECONDS = 60*60*24

JWT_ACCESS_TOKEN_MINUTES = 15
JWT_REFRESH_TOKEN_DAYS = 30

DIRECT_MEMCACHED_ADDR='127.0.0.1'
DIRECT_MEMCACHED_PORT='11211'

# Data Cache settings (matched on URL)
URL_CACHE = {
    'CACHE_TYPE':'memcached',
    #'CACHE_TYPE':'filesystem',   # Not for servers.
    #'CACHE_DIR':'/tmp/URLCache', # Not for servers.
    'CACHE_KEY_PREFIX':'URLCache',
    'CACHE_MEMCACHED_SERVERS':('127.0.0.1',),
    'CACHE_DEFAULT_TIMEOUT':MAX_URL_CACHE_SECONDS
    }

BLOCK_DISPOSABLE_EMAIL_KEY='' # only on web server
BLOCK_DISPOSABLE_URL='' # only on web server

MAX_SESSION_SECONDS = (60 * 30)

DEBUG = True

VERSION='V4.0'

# log file
LOG_FILENAME = f'/var/log/uwsgi/upstage_{VERSION}.log'

# We derive domain, unless we need it in crontab.
# Don't use this unless you have to.
HTTP_PROTOCOL='http://'
DOMAIN = str(FLASK_HOST) + ':' + str(FLASK_PORT)
SUBDOMAIN = ''
API_SUBDOMAIN = ''

FULL_DOMAIN = HTTP_PROTOCOL + SUBDOMAIN + DOMAIN
URL_PREFIX='{}/'.format(VERSION)
DEFAULT_STATIC_CONTENT='{}/static_content/default/{}'.format(FULL_DOMAIN,URL_PREFIX)
RELATIVE_STATIC_CONTENT='/static_content/default/{}'.format(URL_PREFIX)

# Only for admin pages.
DEFAULT_ADMIN_STATIC_CONTENT='{}/static'.format(FULL_DOMAIN)
DEFAULT_ADMIN_STATIC_DIR=os.path.abspath(os.path.join(basedir,'../../static'))
RELATIVE_ADMIN_STATIC_CONTENT='/static/'

print("Static content URL:{}\nAdmin static URL:{}\ndirectory:{}\n".format(
    DEFAULT_STATIC_CONTENT,DEFAULT_ADMIN_STATIC_CONTENT,DEFAULT_ADMIN_STATIC_DIR))

INTERNAL_QR_HOST_DIR='/tmp'
EXTERNAL_QR_HOST_URL='http://localhost'
UPLOADED_IMAGES_DIR='/tmp'
FIREBASE_API_KEY=''
GOOGLE_WEB_CLIENT_ID=''
GOOGLE_TOKEN_VERIFY='https://oauth2.googleapis.com/tokeninfo?access_token={}'
FACEBOOK_APP_ID=''
FACEBOOK_APP_SECRET=''
FACEBOOK_ACCESS_TOKEN_CREATE=f"https://graph.facebook.com/oauth/access_token?client_id={FACEBOOK_APP_ID}&client_secret={FACEBOOK_APP_SECRET}&grant_type=client_credentials"
FACEBOOK_TOKEN_VERIFY='https://graph.facebook.com/debug_token?input_token={}&access_token={}'
APPLE_APP_ID=''
APPLE_APP_SECRET=''
APPLE_TEAM_ID=''
APPLE_ACCESS_TOKEN_CREATE='https://appleid.apple.com/auth/token'
APPLE_TOKEN_VERIFY='https://appleid.apple.com/auth/token'

GOOGLE_RECAPTCHA_KEY = ''
GOOGLE_RECAPTCHA_SECRET = ''

WEATHER_API_KEY=""

CIPHER_KEY='' # Paste the result from fernet_crypto.py
SECRET_KEY='' # Paste the result from running __init__.py
