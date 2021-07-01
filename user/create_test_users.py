#!/usr/bin/env python3
# -*- coding: iso8859-15 -*-
import pdb
import os,sys
import pprint
import json
import string
import requests
import random
import re
appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import jsonify
from flask_restx import Resource
from flask import  abort, current_app, request, redirect, render_template, make_response
from auth.auth_api import jwt_required

from config.project_globals import (DBSession,Base,metadata,engine,get_scoped_session,
    app,api)
from config.settings import FLASK_HOST,FLASK_PORT, ENV_TYPE

from config.signals import add_signals

from auth.fernet_crypto import encrypt
from user.models import User,PLAYER,ADMIN

# System user(s)
def create_some_users():
    db_session = get_scoped_session()
    user = User(
        username='nnnn',
        password=encrypt('nnnnn'),
        email='nnnnnn',
        active=True,
        role=ADMIN,
    )
    db_session.add(user)
    db_session.commit()
    db_session.close()

def modify_user():
    db_session = get_scoped_session()
    user = db_session.query(User).filter(User.username=='nnnn').one()
    #user.password = encrypt('nnnnn')
    user.email='nnnn',
    db_session.commit()

if __name__ == "__main__":
    #create_some_users()
    #modify_user()
    pass

