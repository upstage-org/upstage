# -*- coding: iso8859-15 -*-
from datetime import datetime
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from config.project_globals import initialize_microservice

import os

from asset.views import app,db

app.config["UPLOAD_DIR"] = os.path.abspath(os.getenv("UPLOAD_DIR", "./uploads"))
if not os.path.isdir(app.config["UPLOAD_DIR"]):
    app.logger.info(f"{app.config['UPLOAD_DIR']} doesn't exist.  Creating...")
    os.makedirs(app.config["UPLOAD_DIR"])
