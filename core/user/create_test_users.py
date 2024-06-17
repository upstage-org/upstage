#!/usr/bin/env python3
# -*- coding: iso8859-15 -*-
import pdb
import os, sys
import pprint
import json
import string
import requests
import random
import re

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import jsonify
from flask_restx import Resource
from flask import abort, current_app, request, redirect, render_template, make_response
from core.auth.auth_api import jwt_required

from core.project_globals import (
    DBSession,
    Base,
    metadata,
    engine,
    get_scoped_session,
    app,
    api,
)
from config import FLASK_HOST, FLASK_PORT, ENV_TYPE

from core.signals import add_signals

from core.auth.fernet_crypto import encrypt
from core.user.models import User, PLAYER, ADMIN


# System user(s)
def create_some_users():
    db_session = get_scoped_session()
    for i in range(1,11):
        user = User(
            username=f"testuser{i}",
            password=encrypt(f"qmu_test~!_user{i}"),
            email=f"testuser{i}@no.none",
            active=True,
            role=ADMIN,
        )
        db_session.add(user)
    db_session.commit()
    db_session.close()


def modify_user():
    db_session = get_scoped_session()
    user = db_session.query(User).filter(User.username == "gloria2").one()
    user.password = encrypt('QMUtestingH8W*n1~')
    #user.email = ("",)
    db_session.commit()


if __name__ == "__main__":
     create_some_users()
    #modify_user()
    #pass
