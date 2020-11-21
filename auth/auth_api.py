# -*- coding: iso8859-15 -*-
from datetime import datetime,timedelta
from email.utils import parseaddr
from functools import wraps
import copy
import json
import os,sys
import pdb
import pprint
import random
import re
import requests
import string
import time

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from sqlalchemy.sql.expression import func, or_

from flask_jwt_extended.exceptions import RevokedTokenError,NoAuthorizationError

from flask import jsonify,url_for
from flask_restx import Resource, abort
from flask import  request, redirect, render_template, make_response
from flask_jwt_extended import (jwt_required,get_jwt_identity,
    jwt_refresh_token_required,create_access_token,create_refresh_token,
    verify_jwt_in_request)
from flask_jwt_extended import utils as jwt_utils

from config.project_globals import DBSession,Base,metadata,engine,ScopedSession,app,db
from config.settings import (ENV_TYPE,URL_PREFIX,JWT_REFRESH_TOKEN_DAYS,
    GOOGLE_WEB_CLIENT_ID,GOOGLE_TOKEN_VERIFY,FACEBOOK_ACCESS_TOKEN_CREATE,
    FACEBOOK_TOKEN_VERIFY,APPLE_APP_ID,APPLE_APP_SECRET,APPLE_ACCESS_TOKEN_CREATE,
    APPLE_TOKEN_VERIFY,APPLE_TEAM_ID,VERSION_STRING_IOS,VERSION_STRING_ANDROID,CHECK_VERSION_STRING)

from config.signals import add_signals
from utils.formatting import to_dict

from user.models import (User,ROLES,PLAYER,MAKER,UNLIMITED_MAKER,ADMIN,CREATOR,SUPER_ADMIN)

from jwt import ExpiredSignatureError
from auth.fernet_crypto import encrypt,decrypt
from auth.models import (UserSession,GoogleProfile,FacebookProfile,AppleProfile,
    JWTNoList,get_security_code,new_security_code,SIGNUP_VALIDATION,
    SIGNUP_VALIDATION_MISSING_1ST_CODE,PUBLIC_LOGIN)

from user.totp import verify_user_totp

class LostCodeError(Exception):
    pass
class ProfileError(Exception):
    pass

class TokenNoList(object):

    def check(self,token):
        # Check if token has already been no-listed.
        origtoken = token
        if 'jti' not in token and 'token' not in token:
            token = jwt_utils.decode_token(token)
        if DBSession.query(JWTNoList).filter(
            JWTNoList.token==token['jti']).count() > 0:
            return True

        return False

    # Token looks like this:
    # {'token': {'iat': 1514613742, 'nbf': 1514613742, 'jti': '7923a09c-6d2c-42cd-a045-9385253fab8b', 'exp': 1514614342, 'identity': 43, 'fresh': False, 'type': 'access', 'user_claims': {}},

    # Tokens can be removed after the token_after datetime
    def add(self,token):

        if 'token' in token:
            orig_token = copy.deepcopy(token['token'])
            token_type=token['token']['type']
            decoded_token=token['token']
            token=token['token']['jti']
        elif 'type' in token:
            orig_token = copy.deepcopy(token)
            token_type=token['type']
            decoded_token=token
            token=token['jti']
        else:
            orig_token = copy.deepcopy(token)
            decoded_token = jwt_utils.decode_token(token)
            token_type=decoded_token['type']
            token=decoded_token['jti']

        if self.check(decoded_token):
            return

        # Already restricted.
        if DBSession.query(JWTNoList).filter(JWTNoList.token==token).first():
            return

        if token_type == 'access':
            remove_after = datetime.utcnow()+app.config['JWT_ACCESS_TOKEN_EXPIRES']
        else:
            remove_after = datetime.utcnow()+app.config['JWT_REFRESH_TOKEN_EXPIRES']

        with ScopedSession() as local_db_session:
            TokenNo = JWTNoList(
                token=token,
                token_type=token_type,
                remove_after=remove_after,
                )
            local_db_session.add(TokenNo)

    # Run this in cron
    def remove(self):
        with ScopedSession() as local_db_session:
            local_db_session.query(JWTNoList).filter(
                JWTNoList.remove_after < datetime.utcnow()).delete()

TNL=TokenNoList()
jwt.token_in_blacklist_loader(TNL.check)

@app.route('/{0}'.format(URL_PREFIX),defaults={'path': ''})
def catch_all(path):
    if not get_jwt_identity():
        abort(401,'Invalid endpoint (11)')
    return make_response(jsonify({'error':None}), 201)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/{0}site-map/".format(URL_PREFIX))
@jwt_required
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            #if url == '/':
            #    rule.endpoint = catch_all
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return make_response(jsonify(links), 201)
    #return make_response(jsonify(pprint.pformat(app.url_map._rules[0].__dict__)), 201)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#BASE_URL='/{0}access_token/'.format(URL_PREFIX)
BASE_URL='/access_token/'

# This is our portal login/logout endpoint.
# It gets an additional TOTP code from Google Authenticator.
@app.route('{0}portal/'.format(BASE_URL), methods=['POST','DELETE'])
def portal_login():
    if request.method == 'DELETE': # logout
        return call_login_logout(app_entry=False)

    #pprint.pprint(request.json)
    #pprint.pprint(request.full_path)
    #sys.stdout.flush()
    num_value = request.json.get('num_value',None)
    #if not num_value:
    #    return make_response(jsonify({"error": "Invalid access code."}), 401)
    return call_login_logout(app_entry=False,num_value=num_value)


# This is our app login/logout endpoint.
@app.route('{0}/'.format(BASE_URL), methods=['POST','DELETE'])
def login_logout():
    #print(f'HEADERS {request.headers}')
    return call_login_logout(app_entry=True)

'''
The only differences between FB/Google login and ours are:
(1) We validate the Google/FB token passed in from the front end,
    instead of requiring a usernam and password. An internal mapping
    of our user to Google/FB happens after email/phone validation.
(2) We use the TTL of the Google/FB token for the refresh token TTL,
    instead of our own TTL (which is 30 days. Theirs is an hour or so).
    The shorter TTL doesn't present a problem, since login via G/FB 
    is one-click.
'''
def call_login_logout(app_entry=True,num_value=None):
    timeout_minutes = None
    user  = None
    group = None
    groups = [group]
    #pprint.pprint(request.headers)
    if request.method == 'DELETE': # logout

        access_token = request.headers.get(app.config['JWT_HEADER_NAME'],None)
        if access_token:
            try:
                TNL.add(access_token)
            except ExpiredSignatureError:
                pass # No need to "no" list an already expired token.

            # Make sure we kill this refresh token (add to token 'no' list), even if the 
            # user can't/didn't send it.
            user_session = DBSession.query(UserSession).filter(UserSession.access_token==access_token).first()
            if user_session:
                try:
                    TNL.add(user_session.refresh_token)
                except ExpiredSignatureError:
                    pass # No need to "no" list an already expired token.

        return make_response(jsonify({'error':None}), 200)

    # If they sent an access token with this login request, kill it.
    access_token = request.headers.get(app.config['JWT_HEADER_NAME'],None)
    if access_token:
        TNL.add(access_token)
        user_session = DBSession.query(UserSession).filter(UserSession.access_token==access_token).first()

        # Make sure we kill this refresh token (add to token 'no' list), even if the 
        # user can't/didn't send it.
        if user_session:
            TNL.add(user_session.refresh_token)

    #pprint.pprint(request)

    # Login with either email or username if Upstage login.
    email = None
    username = request.json.get('username',None)
    password = request.json.get('password', None)
    profile_id = request.json.get('profile_id', None)
    from_other = request.json.get('from_other', None)
    signin_token = request.json.get('signin_token', None) # This is an auth code for Apple sign-ins.
    if (not username or len(username) <= 0 or len(username) > 100) and not profile_id:
        return make_response(jsonify({"error": "Missing/invalid username or email (12)"}), 400)
    if (not password or len(password) <= 0 or len(password) > 100) and not profile_id:
        return make_response(jsonify({"error": "Missing/invalid password parameter (13)"}), 400)

    # Regular Upstage login, from app or portal.
    if username and password:
        username = username.lower().strip()
        if '@' in username:
            email = parseaddr(username)[1]
            if not email or len(email) <= 0 or len(email) > 100:
                return make_response(jsonify({"error": "Invalid username or email (14)"}), 401)

        if email:
            user = DBSession.query(User).filter(User.email==email
                ).filter(User.active==True).first()
        else:
            user = DBSession.query(User).filter(User.username==username
                ).filter(User.active==True).first()

        if user:
            if not decrypt(user.password) == password:
                return make_response(jsonify({"error": "Bad email or password (16)"}), 401)
        else:
            if '@' in username:
                user = DBSession.query(User).filter(User.email==username
                    ).filter(User.active==False).first()
            if not user:
                user = DBSession.query(User).filter(or_(User.username==username,
                    User.email==username)).filter(User.active==False).first()

            if not user:
                return make_response(jsonify({"error": "User not found. Please verify that you have an Upstage account or contact us."}), 401)

            # User is inactive and needs to re-verify their phone or email,
            # if we are down here.
            if not decrypt(user.password) == password:
                return make_response(jsonify({"error": "Bad email or password (17)"}), 401)

            # Re-send their signup code.
            existing_code = get_security_code(user.id,SIGNUP_VALIDATION)
            if not existing_code:
                existing_code = new_security_code(user.id,SIGNUP_VALIDATION_MISSING_1ST_CODE)
                '''
                raise LostCodeError(
                    "Something weird happened in the system, and this person's code got lost: user id {}".format(user.id)
                    )
                '''

            if not send_acct_verification_code(user.phone,existing_code): # always sms
                app.logger.warning(f"Tried to send this user a verification code but their phone number is invalid: user_id {user.id} phone {user.phone} ")

            email_verification_code(user.email,existing_code)
            return make_response(jsonify({"user_id":user.id,
                "message": "User needs to verify account"}), 409)

        # Admin Logins from the portal will pass a TOTP value that must be verified.
        # Service providers will have an SMS code they have entered.

        # Kludge: uncomment the below line. remove the line after.
        if user.role in (SUPER_ADMIN,):
            if not verify_user_totp(user,num_value):
                return make_response(jsonify({"error": "Invalid code."}), 401)
            else:
                with ScopedSession() as local_db_session:
                    local_db_session.query(User).filter(
                        User.id==user.id).update(
                        {User.validated_via_portal:True},synchronize_session=False)

        elif user.role in (PLAYER,MAKER,UNLIMITED_MAKER,ADMIN,CREATOR) and not app_entry: 
            pass # password checked-out, that's all we need.

    # We may also have a fb/g login, if this is the first time a user is logging
    # in via fb/g.
    # If it's not the first time, we only have the fb/g login, and it's already mapped
    # to our user.
    if profile_id:

        with ScopedSession() as local_db_session:

            if from_other == 'apple':
                #pprint.pprint(request)
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded; UTF-8',
                }
    
                other_profile = local_db_session.query(AppleProfile).filter(
                    AppleProfile.id==profile_id).one()
    
                # Autheticate the token, match the data, and then map the accounts if they are not mapped.
                # To successfully map them, the user must have logged into ours as well, just the first time
                # they log in via FB/Google/Apple.
                # We first have to create our own access token. Then we verify the inbound token.
                refresh_token = None if not other_profile.other_profile_json else json.loads(other_profile.other_profile_json)['refresh_token']
                did_refresh = False
                if refresh_token:
                    # Refresh tokens expire in 24 hours.
                    payload = {'client_id':APPLE_APP_ID,'client_secret':apple_get_client_secret(),
                        'code':signin_token,
                        'refresh_token':refresh_token,'grant_type':'refresh_token'}
                    did_refresh = True
                else:
                    payload = {'client_id':APPLE_APP_ID,'client_secret':apple_get_client_secret(),
                        'code':signin_token,'grant_type':'authorization_code'}
    
                result = requests.post(APPLE_ACCESS_TOKEN_CREATE,headers=headers,data=payload)
    
                if not result.ok:
                    # If we tried a refresh and it failed:
                    if did_refresh:
                        payload = {'client_id':APPLE_APP_ID,'client_secret':apple_get_client_secret(),
                            'code':signin_token,grant_type:'authorization_code'}
                        result = requests.post(APPLE_ACCESS_TOKEN_CREATE,headers=headers,data=payload)
                        if not result.ok:
                            # get rid of old refresh token.
                            other_profile.other_profile_json = None
                            return make_response(jsonify({"error": "Invalid Source Sign-in (2)."}), 401)
    
                        did_refresh = False
                    else:
                        return make_response(jsonify({"error": "Invalid Source Sign-in."}), 401)
    
                #pprint.pprint(json.loads(result.text))
                response = json.loads(result.text)
                #pprint.pprint(response)
                access_token=response['access_token']
    
                if not did_refresh:
                    refresh_token=response['refresh_token']
                    other_profile.other_profile_json = json.dumps({'refresh_token':refresh_token})
    
                if 'data' in response and 'expires_at' in response['data'] and response['data']['expires_at']:
                    timeout_minutes = int( ( int(response['data']['expires_at']) - datetime.timestamp(datetime.utcnow()) ) / 60)
                    if timeout_minutes <= 0:
                        timeout_minutes = 60
                elif 'data' in response and 'expires_in' in response['data'] and response['data']['expires_in']:
                    # Apple used expires_in
                    timeout_minutes = int( ( int(response['data']['expires_in']) - datetime.timestamp(datetime.utcnow()) ) / 60)
                    if timeout_minutes <= 0:
                        timeout_minutes = 60
                else:
                    timeout_minutes = 60
    
                if user and (not other_profile.user_id):
                    other_profile.user_id=user.id
                else:
                    user = DBSession.query(User).filter(
                        User.id==other_profile.user_id).first()
                    if (not user) or (not user.active):
                        if not user:
                            user = DBSession.query(User).filter(
                                or_(User.username==email,User.email==email,User.username==username)
                                ).first()
                        if user:
                            # Re-send their signup code. They are inactive for some reason.
                            existing_code = get_security_code(user.id,SIGNUP_VALIDATION)
                            if not existing_code:
                                existing_code = new_security_code(user.id,SIGNUP_VALIDATION_MISSING_1ST_CODE,
                                    pending_a_id=profile_id,numeric=True)
                                '''
                                raise LostCodeError(
                                    "Something weird happened in the system, and this person's code got lost: user id {}".format(user.id)
                                    )
                                '''
    
                            if not send_acct_verification_code(user.phone,existing_code): # always sms
                                app.logger.warning(f"Tried to send this user a verification code but their phone number is invalid: user_id {user.id} phone {user.phone} ")
                
                            email_verification_code(user.email,existing_code)
                            return make_response(jsonify({"user_id":user.id,
                                "message": "User needs to verify account"}), 409)
                        else:
                            return make_response(jsonify({"error": "User not found. Please verify that you have an Upstage account by sign-in in directly, then retry this new sign-in method. If this does not work please contact us."}), 401)
    
                    if other_profile.user_id != user.id:
                        return make_response(jsonify({"error": "Invalid Source Match"}), 401)
    
            elif from_other == 'facebook':
                other_profile = local_db_session.query(FacebookProfile).filter(
                    FacebookProfile.id==profile_id).one()
    
                # Autheticate the token, match the data, and then map the accounts if they are not mapped.
                # To successfully map them, the user must have logged into Upstage as well, just the first time
                # they log in via FB/Google/Apple.
                # We first have to create our own access token. Then we verify the inbound token.
                result = requests.get(FACEBOOK_ACCESS_TOKEN_CREATE)
                if not result.ok:
                    return make_response(jsonify({"error": "Invalid Source Sign-in."}), 401)
                response = json.loads(result.text)
                #pprint.pprint(response)
                access_token=response['access_token']
                result = requests.get(FACEBOOK_TOKEN_VERIFY.format(signin_token,access_token))
                #pprint.pprint(FACEBOOK_TOKEN_VERIFY.format(signin_token,access_token))
                #pprint.pprint(result.text)
                if not result.ok:
                    return make_response(jsonify({"error": "Invalid Source Sign-in."}), 401)
                response = json.loads(result.text)
                #pprint.pprint(response)
                if 'data' in response and 'expires_at' in response['data'] and response['data']['expires_at']:
                    timeout_minutes = int( ( int(response['data']['expires_at']) - datetime.timestamp(datetime.utcnow()) ) / 60)
                    if timeout_minutes <= 0:
                        timeout_minutes = 60
                else:
                    timeout_minutes = 60
    
                if user and (not other_profile.user_id):
                    other_profile.user_id=user.id
                else:
                    user = DBSession.query(User).filter(
                        User.id==other_profile.user_id).first()
                    if (not user) or (not user.active):
                        if not user:
                            user = DBSession.query(User).filter(
                                or_(User.username==email,User.email==email,User.username==username)
                                ).first()
                        if user:
                            # Re-send their signup code. They are inactive for some reason.
                            existing_code = get_security_code(user.id,SIGNUP_VALIDATION)
                            if not existing_code:
                                existing_code = new_security_code(user.id,SIGNUP_VALIDATION_MISSING_1ST_CODE,
                                    pending_f_id=profile_id,numeric=True)
                                '''
                                raise LostCodeError(
                                    "Something weird happened in the system, and this person's code got lost: user id {}".format(user.id)
                                    )
                                '''
    
                            if not send_acct_verification_code(user.phone,existing_code): # always sms
                                app.logger.warning(f"Tried to send this user a verification code but their phone number is invalid: user_id {user.id} phone {user.phone} ")
                
                            email_verification_code(user.email,existing_code)
                            return make_response(jsonify({"user_id":user.id,
                                "message": "User needs to verify account"}), 409)
                        else:
                            return make_response(jsonify({"error": "User not found. Please verify that you have an Upstage account by sign-in in directly, then retry this new sign-in method. If this does not work please contact us."}), 401)
    
                    if other_profile.user_id != user.id:
                        return make_response(jsonify({"error": "Invalid Source Match"}), 401)
    
            elif from_other == 'google':
                other_profile = local_db_session.query(GoogleProfile).filter(
                    GoogleProfile.id==profile_id).one()
    
                # Autheticate the token, match the data, and then map the accounts if they are not mapped.
                # To successfully map them, the user must have logged into Upstage as well, just the first time
                # they log in via FB/Google.
                result = requests.get(GOOGLE_TOKEN_VERIFY.format(signin_token))
                if not result.ok:
                    return make_response(jsonify({"error": "Invalid Source Sign-in"}), 401)
                response = json.loads(result.text)
                #pprint.pprint(response)
                if 'expires_in' in response and response['expires_in']:
                    timeout_minutes = int(int(response['expires_in'])/60)
                    if timeout_minutes <= 0:
                        timeout_minutes = 60
                else:
                    timeout_minutes = 60
    
                if user and (not other_profile.user_id):
                    other_profile.user_id=user.id
                else:
                    user = DBSession.query(User).filter(
                        User.id==other_profile.user_id).first()
                    if (not user) or (not user.active):
                        if not user:
                            user = DBSession.query(User).filter(
                                or_(User.username==email,User.email==email,User.username==username)
                                ).first()
                        if user:
                            # Re-send their signup code. They are inactive for some reason.
                            existing_code = get_security_code(user.id,SIGNUP_VALIDATION)
                            if not existing_code:
                                existing_code = new_security_code(user.id,SIGNUP_VALIDATION_MISSING_1ST_CODE,
                                    pending_g_id=profile_id,numeric=True)
                                '''
                                raise LostCodeError(
                                    "Something weird happened in the system, and this person's code got lost: user id {}".format(user.id)
                                    )
                                '''
        
                            if not send_acct_verification_code(user.phone,existing_code): # always sms
                                app.logger.warning(f"Tried to send this user a verification code but their phone number is invalid: user_id {user.id} phone {user.phone} ")
                
                            email_verification_code(user.email,existing_code)
                            return make_response(jsonify({"user_id":user.id,
                                "message": "User needs to verify account"}), 409)
                        else:
                            return make_response(jsonify({"error": "User not found. Please verify that you have an Upstage account by sign-in in directly, then retry this new sign-in method. If this does not work please contact us."}), 401)
    
                    if other_profile.user_id != user.id:
                        return make_response(jsonify({"error": "Invalid Source Match"}), 401)
            else:
                return make_response(jsonify({"error": "Invalid Source."}), 401)


    # Generate session tokens
    access_token = create_access_token(identity=user.id)

    # Shorter token expiry for admins
    if user.role in (SUPER_ADMIN,):
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)
        print(f"User id {user.id} token timeout set to 1 day")
    else:
        print("Timeout minutes set to this: {}".format(timeout_minutes))
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=timeout_minutes) if timeout_minutes else timedelta(days=JWT_REFRESH_TOKEN_DAYS)
        print(f"User id {user.id} token timeout set to either timeout_minutes if not zero: {timeout_minutes}, or this number of days: {JWT_REFRESH_TOKEN_DAYS}")

    refresh_token = create_refresh_token(identity=user.id)

    # Session handling, no matter which login type occurred.
    '''
    NO: this breaks all the things.
    # Force logout of most recent live sessions (can't be logged in twice).
    user_sessions = DBSession.query(UserSession).filter(
        UserSession.user_id==user.id).filter(
        UserSession.recorded_time >= (datetime.utcnow() - timedelta(days=1))).all()

    # Make sure we kill this refresh token (add to token 'no' list)
    for u in user_sessions:
        # JWT reuses tokens for same identity at times, even if we set fresh=True.
        # Don't expire matches.
        if (u.access_token == access_token) or (u.refresh_token == refresh_token):
            continue
        TNL.add(u.access_token)
        TNL.add(u.refresh_token)
    '''

    user_session = UserSession(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
        app_version=request.headers.get('X-Upstage-App-Version'),
        app_os_type = request.headers.get("X-Upstage-Os-Type"),
        app_os_version = request.headers.get("X-Upstage-Os-Version"),
        app_device = request.headers.get("X-Upstage-Device-Model")
    )
    with ScopedSession() as local_db_session:
        local_db_session.add(user_session)
        local_db_session.flush()
        user_session_id = user_session.id
    
    # Determine what to show based on account type.
    title_prefix = '' if ENV_TYPE == 'Production' else 'DEV '
    default_title = title_prefix + 'Upstage'
    title  = default_title
    if user.role == SUPER_ADMIN:
        title = title_prefix + 'Super Admin'
        #groups = [g for g in DBSession.query(FunctionalGroup).all()]
        group={'id':0,'name':"test"}
        groups=[group]

    elif user.role in (PLAYER,MAKER,UNLIMITED_MAKER,ADMIN,CREATOR) and not (group):
        group={'id':0,'name':"test"}
        groups=[group]
        #raise ProfileError("Attendee {0} has no associated group. User must have a group record!".format(user_id))

    print("title:{}".format(title))

    return make_response(jsonify({'user_id':user.id,'access_token':access_token,'refresh_token':refresh_token,
        'phone':user.phone,
        #'access_bitmask':user.access_bitmask,
        'role':user.role, 'first_name':user.first_name,
        #'groups':[to_dict(g) for g in groups],
        'groups':groups,
        'username':user.username,
        'title':title}), 200)


@app.route('{0}refresh/'.format(BASE_URL), methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user_id = get_jwt_identity()
    refresh_token = request.headers[app.config['JWT_HEADER_NAME']]

    user = DBSession.query(User).filter(User.id==current_user_id
        ).filter(User.active==True).first()

    if not user:
        TNL.add(refresh_token)
        return make_response(jsonify({'error':"Your session expired. Please log in again."}), 401)

    access_token = create_access_token(identity=current_user_id)

    user_session = UserSession(
        user_id=current_user_id,
        access_token=access_token,
        refresh_token=refresh_token,
        app_version=request.headers.get('X-Upstage-App-Version'),
        app_os_type=request.headers.get("X-Upstage-Os-Type"),
        app_os_version=request.headers.get("X-Upstage-Os-Version"),
        app_device=request.headers.get("X-Upstage-Device-Model")
    )

    with ScopedSession() as local_db_session:
        local_db_session.add(user_session)
        local_db_session.flush()
        user_session_id = user_session.id
    
    return make_response(jsonify({'access_token':access_token}),200)

@app.route('/{0}prlookup/'.format(URL_PREFIX), methods=['POST'])
def g_fb_a_lookup():

    google_id = request.json.get('google_id',None)
    facebook_id = request.json.get('facebook_id',None)
    apple_id = request.json.get('apple_id',None)
    email = request.json.get('email',None)
    phone = request.json.get('phone',None)
    first_name = request.json.get('first_name',None)
    last_name = request.json.get('last_name',None)
    username = request.json.get('username',None)

    if not (google_id or facebook_id or apple_id):
        return make_response(jsonify({'error':'Missing required parameters'}), 422)

    google_id = google_id.strip().lower() if google_id else None
    facebook_id = facebook_id.strip().lower() if facebook_id else None
    apple_id = apple_id.strip().lower() if apple_id else None
    email = email.strip().lower() if email else None
    phone=clean_phone(phone)
    first_name = first_name.strip().lower() if first_name else None
    last_name = last_name.strip().lower() if last_name else None

    both = False
    found = False
    profile_id = None

    if google_id:
        google_id = str(google_id)
        profile = DBSession.query(GoogleProfile).filter(
            GoogleProfile.google_id==google_id).first()
        if profile:
            found = True
            both = True if profile.user_id else False
            profile_id = profile.id
        else:
            profile = GoogleProfile(
                google_id=google_id,
                google_phone=phone,
                google_email=email,
                google_first_name=first_name,
                google_last_name=last_name,
                google_username=username,
                )
            with ScopedSession() as local_db_session:
                local_db_session.add(profile)
                local_db_session.flush()
                profile_id = profile.id

    if facebook_id:
        facebook_id = str(facebook_id)
        profile = DBSession.query(FacebookProfile).filter(
            FacebookProfile.facebook_id==facebook_id).first()
        if profile:
            found = True
            both = True if profile.user_id else False
            profile_id = profile.id
        else:
            profile = FacebookProfile(
                facebook_id=facebook_id,
                facebook_phone=phone,
                facebook_email=email,
                facebook_first_name=first_name,
                facebook_last_name=last_name,
                facebook_username=username,
                )
            with ScopedSession() as local_db_session:
                local_db_session.add(profile)
                local_db_session.flush()
                profile_id = profile.id

    if apple_id:
        apple_id = str(apple_id)
        profile = DBSession.query(AppleProfile).filter(
            AppleProfile.apple_id==apple_id).first()
        if profile:
            found = True
            both = True if profile.user_id else False
            profile_id = profile.id
        else:
            profile = AppleProfile(
                apple_id=apple_id,
                apple_phone=phone,
                apple_email=email,
                apple_first_name=first_name,
                apple_last_name=last_name,
                apple_username=username,
                )
            with ScopedSession() as local_db_session:
                local_db_session.add(profile)
                local_db_session.flush()
                profile_id = profile.id

    #if profile_id:
    #    pprint.pprint(f"{profile_id}: {profile.__dict__}")
    return make_response(jsonify({'found':found,'both':both,'profile_id':profile_id}), 200)

# Use this instead of the flask extended decorator.
def jwt_required(fn):
    """
    Overriding built-in decorator, to catch the exception
    thrown when signature expires.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if CHECK_VERSION_STRING:
            version = request.headers.get('X-Upstage-App-Version',None)
            if (version not in (VERSION_STRING_IOS,VERSION_STRING_ANDROID)) and \
                (ENV_TYPE == 'Production') and ('/vue_admin/' not in request.referrer):
                return make_response(jsonify({'error':"Please update this app for a better user experience."}), 422)
        try:
            verify_jwt_in_request()
        except ExpiredSignatureError:
            app.logger.warning("Signature Expired")
            return make_response(jsonify({'error':"You have been logged out on this session."}), 401)
        except RevokedTokenError:
            app.logger.warning("Token Revoked")
            return make_response(jsonify({'error':"You have been logged out on this session ."}), 401)
        except NoAuthorizationError:
            app.logger.warning("Token Revoked from another login")
            return make_response(jsonify({'error':"You have been logged out on this session  ."}), 401)
        return fn(*args, **kwargs)
    return wrapper

# Use this instead of the flask extended decorator.
def admin_jwt_required(fn):
    """
    Overriding built-in decorator, to catch the exception
    thrown when signature expires.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()

            user = DBSession.query(User).options(FromCache("default")).filter(
                User.id==current_user_id).filter(
                User.active==True).first()
            if ENV_TYPE == 'Production' and (not user or not user.validated_via_portal):
                abort(403,'Invalid validation.')

            #print(request.referrer)
            if ENV_TYPE == 'Production' and '/vue_admin/' not in request.referrer:
                abort(403,'Invalid path.')

        except ExpiredSignatureError:
            app.logger.warning("Signature Expired")
            return make_response(jsonify({'error':"You have been logged out on this session."}), 401)

        except RevokedTokenError:
            app.logger.warning("Token Revoked")
            return make_response(jsonify({'error':"You have been logged out on this session ."}), 401)

        except NoAuthorizationError:
            app.logger.warning("Token Revoked from another login")
            return make_response(jsonify({'error':"You have been logged out on this session  ."}), 401)

        return fn(*args, **kwargs)
    return wrapper

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
# Specific to Apple login verification
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
def apple_get_client_secret():
    from jwt.api_jwt import encode
    kid = APPLE_APP_SECRET # kid is the id for the private key from developer.apple.com/account/resources/authkeys/list
    teamID = APPLE_TEAM_ID
    keyfile = os.path.abspath(os.path.join(projdir,'config/settings/apple_auth.p8'))
    key = ""
    with open(keyfile, 'r') as myFile:
        key = myFile.read()
    
    #print(kid)
    #print(key)
    #print(APPLE_APP_ID)
    timeNow = int(round(time.time()))
    time25Hours = timeNow + 90000

    claims = {
        'iss': teamID,
        'iat': timeNow,
        'exp': time25Hours,
        'aud': 'https://appleid.apple.com',
        'sub': APPLE_APP_ID,
    }

    secret = encode(claims, key, algorithm='ES256', headers={'kid': kid})
    #print("secret:")
    #print(secret)
    client_secret = secret.decode("utf-8")
    #print(client_secret)
    return client_secret


if __name__ == "__main__":
    #import pdb;pdb.set_trace()
    pass
    '''
    # Test disabling user via tokens
    access_token='33069e62834fa9f4fb5d3204bb0622e387f49cf1ff21e8721fb0cb67a02f16ee'
    refresh_token='8e5b1db2e3b5f939ac634d1372ac6c5d0a35aa991678e18c2e77a7fc135dbd6f'
    with app.app_context():
        import pdb;pdb.set_trace()
        with ScopedSession() as local_db_session:
            atoken = jwt_utils.decode_token(access_token)
            rtoken = jwt_utils.decode_token(refresh_token)
            TNL.add(atoken)
            TNL.add(rtoken)
    
    apple_get_client_secret()
    '''
    '''
    #payload = {'client_id':APPLE_APP_ID,'client_secret':apple_get_client_secret(),
    #    'code':signin_token,
    #    'refresh_token':refresh_token,'grant_type':'refresh_token'}
    signin_token='c100c6b28d39441a6a4c5dfd3e21d3276.0.muwz.6449BACPFrVl26RIDU57vg'
    payload = {'client_id':APPLE_APP_ID,'client_secret':apple_get_client_secret(),
        'code':signin_token,'grant_type':'authorization_code'}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; UTF-8',
    }
    #result = requests.post(APPLE_ACCESS_TOKEN_CREATE,headers=headers,data=json.dumps(payload))
    result = requests.post(APPLE_ACCESS_TOKEN_CREATE,headers=headers,data=payload)
    pprint.pprint(json.loads(result.text))

    '''
