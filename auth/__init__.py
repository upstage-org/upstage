# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from config.project_globals import initialize_microservice,app,api,jwt,db
from flask import Flask, Blueprint

app = Flask(__name__,instance_relative_config=True)
initialize_microservice(app)

blueprint = Blueprint("auth", __name__)
app.register_blueprint(blueprint)
