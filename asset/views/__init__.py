# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'../..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import Flask
from config.project_globals import initialize_microservice

# Create and init app. Now you can use app.logger and such. Woo!
app = Flask(__name__)
db = initialize_microservice(app)

from .assets import blueprint as assets
from .licenses import blueprint as licenses

app.register_blueprint(assets)
app.register_blueprint(licenses)
