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
from auth import app as auth_app
from user import app as user_app
from ui import app as frontend

application = DispatcherMiddleware(frontend, {
    "/asset": asset,
    "/auth": auth_app,
    "/user": user_app,
    "/ui": frontend,
})
