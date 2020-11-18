# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import Flask, send_file
from config.project_globals import initialize_microservice

# Create and init app. Now you can use app.logger and such. Woo!
app = Flask(__name__)
db = initialize_microservice(app)

@app.route("/<path:filename>", methods=["GET"])
def get_file(filename):
    real_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 
            filename
        )
    )
    if os.path.isfile(real_path):
        return send_file(real_path)
    else:
        return f"Not found", 404
