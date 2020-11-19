# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from config.project_globals import initialize_microservice
from flask import Flask, Blueprint

global app
global db
global jwt
global api
app = None

if not app:
    app = Flask(__name__)
    db,jwt,api = initialize_microservice(app)
    
    blueprint = Blueprint("user", __name__)
    app.register_blueprint(blueprint)
