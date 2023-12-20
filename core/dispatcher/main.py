# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from core.asset.views import app as asset
from core.auth.auth_api import app as auth
from core.user.user_api import app as user
from ui import app as frontend

from flask import Flask, Blueprint

application = DispatcherMiddleware(
    frontend,
    {
        "/V4.0/auth": auth,
        "/V4.0/user": user,
        "asset": asset,
        "ui": frontend,
    },
)
