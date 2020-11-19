# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from asset.views import app as asset 
from auth.auth_api import app as auth
from user.user_api import app as user
from ui import app as frontend

application = DispatcherMiddleware(frontend, {
    "/V2.0/auth": auth,
    "asset": asset,
    "user": user,
    "ui": frontend,
})
