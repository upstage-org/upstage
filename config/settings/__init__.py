# -*- coding: iso8859-15 -*-
import pprint
import copy
import os,sys
from datetime import datetime,timedelta
import secrets

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'../../'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

import socket

# ------------------------------------

# Override these in your local settings file if you wish.
# Things which must be overridden aren't listed here.

CHECK_VERSION_STRING=False
VERSION_STRING_IOS = ''
VERSION_STRING_ANDROID = ''

EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

MONGODB_PORT = 27017
#MONGODB_HOST = 'localhost'
MONGODB_QUEUE_DBNAME = 'QUEUES'

MONGODB_COLLECTION_EMAIL = 'EMAIL_OUTBOUND_QUEUE'

EMAIL_PORT = 587
#EMAIL_PORT = 25
FROM_EMAIL=''

# log file
MAX_BYTES = 50000000
BACKUP_COUNT = 10

# Data Cache default settings
MAX_URL_CACHE_SECONDS = 60*60*24

# KLUDGE: Turns off warning:
SQLALCHEMY_TRACK_MODIFICATIONS=True

SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_SIZE = 300
SQLALCHEMY_POOL_RECYCLE = 3600
PAGE_LIMIT = 100

# user content defaults
UPLOAD_USER_CONTENT_FOLDER = '/home/projectname/uploads'
MAX_BINS = 1000000

TWILIO_ACCOUNT_ID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_FROM_NUMBER = ""

if 'HARDCODED_HOSTNAME' in os.environ:
    ORIG_HOSTNAME=HOSTNAME=os.environ['HARDCODED_HOSTNAME']
    print("Loading local settings from a hard-coded env hostname: %s.py" % HOSTNAME)
else:
    ORIG_HOSTNAME = socket.gethostname( )
    HOSTNAME = socket.gethostname( ).replace('.','_').replace('-','_')
    print("Loading local settings from %s.py" % HOSTNAME)


# Read-only DB replica: we don't yet have one
#RO_DB_NAME=DB_NAME
#RO_DB_USER=DB_USER
#RO_DB_PASSWD=DB_PASSWD
#RO_DB_HOST=DB_HOST
#RO_DB_PORT=DB_PORT

hstr = "from config.settings.{0} import *".format(HOSTNAME)
exec(hstr)

# Reset this based on imported local config values
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(DB_USER,DB_PASSWD,DB_HOST,DB_PORT,DB_NAME)
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'.format(DB_USER,DB_PASSWD,DB_HOST,DB_PORT,DB_NAME)

if __name__ == '__main__':
    print("Copy-paste this secret:{}".format(secrets.token_urlsafe(64)))
