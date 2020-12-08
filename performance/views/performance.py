# -*- coding: iso8859-15 -*-
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'../..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import Flask, Blueprint, jsonify, request, url_for, send_file
from config.project_globals import app,DBSession,ScopedSession


'$SYS/broker/clients/connected'
