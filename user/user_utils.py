#!/usr/bin/env python
# -*- coding: iso8859-15 -*-
import pdb
import os,sys
import pprint
import json
import string
import requests
import random
import re
import pytz
import psycopg2
appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import jsonify
from flask_restx import Resource, Api, fields, marshal_with, reqparse, abort
from flask import current_app, request, redirect, render_template, make_response
from auth.auth_api import jwt_required,get_jwt_identity

from config.project_globals import (DBSession,Base,metadata,engine,get_scoped_session,
    app,api)
from config.settings import ENV_TYPE, URL_PREFIX

from config.signals import add_signals

from user.models import (User)
from auth.models import (UserSession,
    ROLES,SIGNUP_VALIDATION,RESET_PASSWORD)

from auth import fernet_crypto
from auth.auth_api import TNL

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def maintenance_resident_user_groups(user):
    # Maintenance resident sits between the world: They live in one building and can see services only there,
    # but may do maintenance in multiple buildings and groups.
    if user.role == MAINTENANCE_RESIDENT:
        groups_user = list(set([x.group for x in DBSession.query(GroupUser).filter(GroupUser.user_id==user.id).all()]))
        buildings_from_groups = list(set([x.building for x in DBSession.query(
            BuildingGroup).filter(BuildingGroup.group_id.in_([x.id for x in groups_user])).all()]))
        return groups_user,buildings_from_groups
    return None,None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def current_user(user_id=None,admin_initial=False,internal_use=False):
    current_user_id = get_jwt_identity() if not user_id else user_id

    user = DBSession.query(User).filter(
        User.id==current_user_id).filter(
        User.active==True).first()
    if not user:
        return 401,"Invalid user (1)",None,None,None,None

    if not user_id:
        user_session = DBSession.query(UserSession).filter(
            UserSession.user_id==user.id).order_by(
            UserSession.recorded_time.desc()).first()

        if not user_session and not internal_use:
            return 403, 'Bad user session (2)',None,None,None,None

    error,buildings,buildings_from_groups,groups,timezone = buildings_and_groups_for_user(user)
    if error:
        return 403,error,None,None,None,None

    if user.role in (ACCOUNT_ADMIN,SUPER_ADMIN) and not buildings:
        print("Admin needs to pick a group first")
        return 403, 'Admin needs to pick a group first',None,None,None,None
       
    #print("User: {}, id:{}, groups: {}".format(user.username,user.id,pprint.pformat([x.group_name for x in groups])))

    return 200,None,user,[],[],timezone


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def log_users_off(user_id=None,building_id=None):
    # One of these parameters must be set.
    if user_id:
        user_sessions = DBSession.query(UserSession).filter(
            UserSession.user_id==user.id).all()
    else:
        results = DBSession.query(UserSession,BuildingUser).join(
            UserSession,UserSession.user_id==BuildingUser.user_id).filter(
            BuildingUser.building_id==building_id).all();
        user_sessions = list(set([x[0] for x in results]))

    for user_session in user_sessions:
        try:
            TNL.add(user_session.access_token)
        except psycopg2.errors.UniqueViolation:
            pass
        try:
            TNL.add(user_session.refresh_token)
        except psycopg2.errors.UniqueViolation:
            pass

