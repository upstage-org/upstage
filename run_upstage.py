#!/usr/bin/env python3
# -*- coding: iso8859-15 -*-
import os
import sys

projdir = os.path.abspath(os.path.dirname(__file__))
if projdir not in sys.path:
    sys.path.append(projdir)

from config.settings import FLASK_HOST,FLASK_PORT

from werkzeug.serving import run_simple
from dispatcher.main import application

if __name__ == "__main__":
    run_simple(FLASK_HOST, FLASK_PORT, application, ssl_context=None, use_reloader=False)
    #application.run()
