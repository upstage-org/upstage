# -*- coding: iso8859-15 -*-
import os, sys
import json
import traceback
import pprint

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)
import time, datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, g, got_request_exception, request
from flask import Response, jsonify, make_response

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from core.project_globals import get_scoped_session
from flask_jwt_extended import get_jwt_identity

from core.auth import api, app

from config import DEBUG, ENV_TYPE, HOSTNAME


def add_details(sender, exception):
    exc = traceback.format_exc()
    cid = get_jwt_identity()

    msg = """
{0}:{1}: 
Exception: {2}
User {3}

Request: {4}
    """.format(
        ENV_TYPE, HOSTNAME, exc, cid, pprint.pformat(request.__dict__)
    )

    sys.stderr.write(msg)
    if "abort(3" in exc or "abort(4" in exc:
        app.logger.warning(msg)
    else:
        app.logger.exception(msg)


def add_signals(app):
    got_request_exception.connect(add_details, app)
