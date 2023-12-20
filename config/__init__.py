# -*- coding: iso8859-15 -*-
import pprint
import copy
import os
import sys
import secrets
import socket
from datetime import datetime, timedelta

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../../"))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


# ------------------------------------

# Override these in your local settings file if you wish.
# Things which must be overridden aren't listed here.

ADMINS = ["support@upstage.org"]
SUPPORT_EMAILS = ["support@upstage.org"]

# A list of developers who should receive email crash reports in dev.
# In prod, they should all go to the support address.
DEVS = []

DB_NAME = ""
DB_USER = ""
DB_PASSWD = ""
DB_HOST = ""
DB_PORT = 5432

FLASK_HOST = "127.0.0.1"
FLASK_PORT = 8000
FLASK_CHAT_WEBSOCKET_PORT = 8002
RUNFROM_PORT = None

ENV_TYPE = ""

CHECK_VERSION_STRING = False
VERSION_STRING_IOS = ""
VERSION_STRING_ANDROID = ""

EMAIL_USE_TLS = True
EMAIL_HOST = ""
EMAIL_PORT = 465
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_DISPLAY_NAME = ""
EMAIL_TIME_TRIGGER_SECONDS = 60 * 1  # 1 minute
EMAIL_TIME_EXPIRED_TOKEN = 60 * 10  # 10 minute
ACCEPT_SERVER_SEND_EMAIL_EXTERNAL = [
    "https://dev-app1.upstage.live"
]  # All client server endpoints. Only config on upstage server
SEND_EMAIL_SERVER = "https://upstage.live"  # Send email server endpoint
ACCEPT_EMAIL_HOST = ["app1"]

MONGO_HOST = ""
MONGO_PORT = 0
MONGO_DB = ""
EVENT_COLLECTION = ""

MQTT_BROKER = ""
MQTT_PORT = 0
MQTT_TRANSPORT = "tcp"
MQTT_USER = ""
MQTT_PASSWORD = ""
PERFORMANCE_TOPIC_RULE = "#"

MONGODB_COLLECTION_EMAIL = "EMAIL_OUTBOUND_QUEUE"
MONGODB_COLLECTION_TOKEN = "EMAIL_ACCEPT_TOKEN"

EMAIL_PORT = 587
# EMAIL_PORT = 25
FROM_EMAIL = ""

# log file
MAX_BYTES = 50000000
BACKUP_COUNT = 10

# Data Cache default settings
MAX_URL_CACHE_SECONDS = 60 * 60 * 24

# KLUDGE: Turns off warning:
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_SIZE = 300
SQLALCHEMY_POOL_RECYCLE = 3600
PAGE_LIMIT = 100
URL_PREFIX = "api/"

# payment
STRIPE_KEY = ""
STRIPE_PRODUCT_ID = ""

# user content defaults
UPLOAD_USER_CONTENT_FOLDER = "/home/upstage/assets_all_releases"
MAX_BINS = 1000000

TWILIO_ACCOUNT_ID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_FROM_NUMBER = ""

STREAM_EXPIRY_DAYS = 180

if "HARDCODED_HOSTNAME" in os.environ:
    ORIG_HOSTNAME = HOSTNAME = os.environ["HARDCODED_HOSTNAME"]
    print("Loading local settings from a hard-coded env hostname: %s.py" % HOSTNAME)
else:
    ORIG_HOSTNAME = socket.gethostname()
    HOSTNAME = socket.gethostname().replace(".", "_").replace("-", "_")
    print("Loading local settings from %s.py" % HOSTNAME)


# Read-only DB replica: we don't yet have one
# RO_DB_NAME=DB_NAME
# RO_DB_USER=DB_USER
# RO_DB_PASSWD=DB_PASSWD
# RO_DB_HOST=DB_HOST
# RO_DB_PORT=DB_PORT

hstr = "from config.{0} import *".format(HOSTNAME)
exec(hstr)

# Reset this based on imported local config values
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
    DB_USER, DB_PASSWD, DB_HOST, DB_PORT, DB_NAME
)
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'.format(DB_USER,DB_PASSWD,DB_HOST,DB_PORT,DB_NAME)
NGINX_CONFIG_FILE = "config/dev/dev_app1_nginx_upstage.conf"

CLOUDFLARE_CAPTCHA_VERIFY_ENDPOINT = (
    "https://challenges.cloudflare.com/turnstile/v0/siteverify"
)

if __name__ == "__main__":
    print("Copy-paste this secret:{}".format(secrets.token_urlsafe(64)))
