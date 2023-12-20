#!/usr/bin/env python
# -*- coding: iso8859-15 -*-
import pdb
import os, sys
import pprint
import json
import string
import requests
import random
import re
import pytz
import psycopg2

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import jsonify
from flask_restx import Resource, Api, fields, marshal_with, reqparse, abort
from flask import request, redirect, render_template, make_response
from core.auth.auth_api import jwt_required, get_jwt_identity

from core.project_globals import DBSession, Base, metadata, engine, app, db
from config import ENV_TYPE, URL_PREFIX

from core.signals import add_signals

from core.user.models import User
from core.auth.models import UserSession, SIGNUP_VALIDATION, RESET_PASSWORD

from core.auth import fernet_crypto
from core.auth.auth_api import TNL


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def current_user(user_id=None, admin_initial=False, internal_use=False):
    current_user_id = get_jwt_identity() if not user_id else user_id

    user = (
        DBSession.query(User)
        .filter(User.id == current_user_id)
        .filter(User.active == True)
        .first()
    )
    if not user:
        return 403, "Invalid user (1)", None, None, None, None

    if not user_id:
        user_session = (
            DBSession.query(UserSession)
            .filter(UserSession.user_id == user.id)
            .order_by(UserSession.recorded_time.desc())
            .first()
        )

        if not user_session and not internal_use:
            return 403, "Bad user session (2)", None, None, None, None

    # TODO: Get user timezone from front end.
    timezone = "UTC"
    return 200, None, user, timezone
