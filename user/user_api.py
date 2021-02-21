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

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask import jsonify
from flask_restx import Resource, Api, fields, marshal_with, reqparse, abort
from flask import request, redirect, render_template, make_response
from sqlalchemy import func

from auth.auth_api import jwt_required
from config.project_globals import DBSession,Base,metadata,engine,ScopedSession,app,db,api
from config.settings import ENV_TYPE, URL_PREFIX

from config.signals import add_signals

from auth.fernet_crypto import encrypt,decrypt

from user.models import User
from user.user_utils import current_user
from auth.models import (UserSession,
    new_security_code,verify_security_code,SIGNUP_VALIDATION,
    RESET_PASSWORD,PROFILE_CHG,FacebookProfile,GoogleProfile,AppleProfile)

from auth import fernet_crypto
from auth.auth_api import TNL

BASE_URL='/{0}user'.format(URL_PREFIX)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/{0}crash/'.format(URL_PREFIX),methods=['GET'])
def always_crash():
    raise Exception("Test")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Only accessible to Admin users.
@app.route('/{0}pick_a_group/'.format(URL_PREFIX),methods=['POST'])
@jwt_required
def admin_pick_a_group():
    code,error,user,buildings,groups,timezone = current_user(admin_initial=True)
    if code != 200:
        abort(code,error)

    if user.role in (ACCOUNT_ADMIN,SUPER_ADMIN):
        post_args = request.get_json(force=True)
        if 'group_id' not in post_args or not post_args['group_id']:
            return make_response(jsonify({'error':'Permission denied.'}),403)

        group_id = post_args['group_id']

        alg = AdminLatestGroup(
            user_id = user.id,
            group_id = group_id,
            )
        with ScopedSession() as local_db_session:
            local_db_session.add(alg)

        group = DBSession.query(FunctionalGroup).filter(
            FunctionalGroup.id==group_id).first()

        title_prefix = '' if ENV_TYPE == 'Production' else 'DEV '
        if user.role == SUPER_ADMIN:
            title = title_prefix + 'Super Admin ' + group.group_name
        elif user.role == ACCOUNT_ADMIN:
            title = title_prefix + 'Admin ' + group.group_name

        return make_response(jsonify({'title':title}),200)

    return make_response(jsonify({'error':'Permission denied.'}),403)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/{0}logged_in/'.format(URL_PREFIX),methods=['GET'])
@jwt_required
def current_user_info():
    #pprint.pprint(request.headers)
    code,error,user,buildings,groups,timezone = current_user()
    if code != 200:
        abort(code,error)

    access_token = request.headers.get(app.config['JWT_HEADER_NAME'],None)
    #app.logger.info("access token:{0}".format(access_token))

    # If latest user session access token doesn't match, kick them out.
    user_session = DBSession.query(UserSession).filter(
        UserSession.user_id==user.id).order_by(
        UserSession.recorded_time.desc()).first()

    if not user_session:
        return make_response(jsonify({'error':'Bad user session (3)'}),403)

    if (user_session.access_token != access_token):
        TNL.add(access_token)
        # No. user session may be valid, from a newer login on a different device.
        #TNL.add(user_session.refresh_token)
        #TNL.add(user_session.access_token)
        return make_response(jsonify({'error':'Access token is invalid (4)'}),403)

    address = None

    return make_response(jsonify({'user_id':user.id,'role':user.role,
        'phone':user.phone,
        'first_name':user.first_name, 'last_name': user.last_name, 
        'email':user.email,
        'timezone':timezone if timezone != pytz.UTC else None,
        'groups':[],
        'username':user.username,
        }),200)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/{0}password_reset/'.format(URL_PREFIX),methods=['POST'])
def reset_password():
    # Consider blocking too many requests to this URL.

    post_args = request.get_json(force=True)
    code = post_args['code']
    if (len(code) > 100) or (len(code) == 0):
        return make_response(jsonify({'error':'Bad code (5)'}),403)

    if len(post_args['password']) > 50 or len(post_args['password']) == 0:
        return make_response(jsonify({'error':'Bad password (6)'}),403)

    if post_args['password'] != post_args['password2']:
        return make_response(jsonify({'error':'New passwords do not match, rejected.'}),422)

    user = verify_security_code(code)
    if not user:
        return make_response(jsonify({'error':'Bad code (7)'}),403)

    with ScopedSession() as local_db_session:
        app.logger.info("Resetting password for user {}".format(user.__dict__))
        local_db_session.query(User).filter(
            User.id==user.id).update({
            'password':fernet_crypto.encrypt(post_args['password'])})

    return make_response(jsonify({'error':None}),200)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/{0}forgot_password/'.format(URL_PREFIX),methods=['POST'])
def forgot_password():

    # This sends out the N digit reset code. After this, call '/password_reset/<string:code>/',
    # POSTing new password. See above.
    # Consider blocking too many requests to this URL.
    post_args = request.get_json(force=True)
    post_args['email'] = post_args['email'].lower().strip()
    if len(post_args['email']) <= 0 or len(post_args['email']) > 100:
        #maybe keep this one, someone putting bad emails in could be possible attack
        app.logger.error("User can't see this: User sent this email to forgot password, it failed: {}".format(
            post_args['email']))
        abort(403,'Bad user (8)')

    user = DBSession.query(User).filter(
        User.active==True).filter(
        User.email==post_args['email']).first()
    if not user:
        user = DBSession.query(User).filter(
            User.active==True).filter(
            func.lower(User.username)==post_args['email']).first()
    if not user:
        #downgrading to warning...
        app.logger.warning("User can't see this: User sent this email to forgot password, user is either inactive or nonexistent: {}".format(
            post_args['email']))
        abort(403,'Bad user (9)')

    new_code = new_security_code(user.id,RESET_PASSWORD,numeric=True)
    #if user.ok_to_sms:
    email_password_reset_code(user.email,new_code)
    if not send_reset_code(user.phone,new_code): # always sms
        return make_response(jsonify({'error':'SMS failed. Is your phone number valid?'}),403)

    return make_response(jsonify({'error':None}),200)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class NonuserInquiryPage1(Resource):
    def __init__(self,*args,**kwargs):
        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('first_name', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('last_name', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('phone', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('email', type = str, required = True, location = 'json')
        super(NonuserInquiryPage1, self).__init__(*args,**kwargs)

    def post(self):
        args = self.post_reqparse.parse_args()
        #pprint.pprint(args)
        args['phone'] = clean_phone(args['phone'])
        if (len(args['phone']) < 10):
            return make_response(jsonify({'error':'Bad phone i'}),422)

        ni = NonuserInquiry(
            phone_number = args['phone'], #cleaned above
            first_name = args['first_name'].strip(),
            last_name = args['last_name'].strip(),
            email = args['email'].strip(),
            access_code = generate_numeric_security_access_code(),
            )

        try:
            email_bldg_inqury_code(ni.email,ni.access_code)
        except:
            return make_response(jsonify({'error':"Email to {} failed".format(ni.email)}),422)

        with ScopedSession() as local_db_session:
            local_db_session.add(ni)
            local_db_session.flush()
            ni_access_code = ni.access_code
            ni_id = ni.id

        return make_response(jsonify({'id':ni_id,'access_code':ni_access_code}),201)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class NonuserInquiryCodeValidation(Resource):
    def __init__(self,*args,**kwargs):
        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('user_id', type = int, required = True, location = 'json')
        self.post_reqparse.add_argument('access_code', type = str, required = True, location = 'json')
        super(NonuserInquiryCodeValidation, self).__init__(*args,**kwargs)

    def post(self):
        args = self.post_reqparse.parse_args()
        #pprint.pprint(args)

        with ScopedSession() as local_db_session:
            ni = local_db_session.query(NonuserInquiry).filter(
                NonuserInquiry.id==args['user_id']).filter(
                NonuserInquiry.access_code==args['access_code'].strip()).first()

            if not ni:
                return make_response(jsonify({'error':"No matching inquiry 1"}),422)

            ni.verified = True

        return make_response(jsonify({'error':None}),200)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class NonuserInquiryCodeResend(Resource):
    def __init__(self,*args,**kwargs):
        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('user_id', type = int, required = True, location = 'json')
        self.post_reqparse.add_argument('email', type = str, required = True, location = 'json')
        super(NonuserInquiryCodeResend, self).__init__(*args,**kwargs)

    def post(self):
        args = self.post_reqparse.parse_args()
        #pprint.pprint(args)

        with ScopedSession() as local_db_session:
            ni = local_db_session.query(NonuserInquiry).filter(
                NonuserInquiry.id==args['user_id']).filter(
                NonuserInquiry.email==args['email'].strip()).first()

            if not ni:
                return make_response(jsonify({'error':"No matching inquiry 2"}),422)

            # Generate and email a new code.
            ni.access_code = generate_numeric_security_access_code()
            email_bldg_inqury_code(ni.email,ni.access_code)

            return make_response(jsonify({'error':None}),200)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class NonuserInquiryPage2(Resource):
    def __init__(self,*args,**kwargs):
        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('user_id', type = int, required = True, location = 'json')
        self.post_reqparse.add_argument('full_address', type = str, required = True, location = 'json')
        super(NonuserInquiryPage2, self).__init__(*args,**kwargs)

    def post(self):
        args = self.post_reqparse.parse_args()
        #pprint.pprint(args)

        with ScopedSession() as local_db_session:
            ni = local_db_session.query(NonuserInquiry).filter(
                NonuserInquiry.id==args['user_id']).first()

            if not ni:
                return make_response(jsonify({'error':"No matching inquiry 3"}),422)

            ni.full_address = args['full_address']

            found,result = match_full_address_string(ni.full_address)
            if found:
                ni.found_match = result
                local_db_session.flush()
                d_ni = to_dict(ni)
                email_admins_inquiry_match(d_ni)
                return make_response(jsonify({'address_found':True}),200)
            else:
                local_db_session.flush()
                d_ni = to_dict(ni)
                email_admins_inquiry_match(d_ni)
                return make_response(jsonify({'address_found':False}),200)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ResidentProfile(Resource):

    def __init__(self,*args,**kwargs):
        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('username', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('password', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('password2', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('apartment', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('first_name', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('last_name', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('display_name', type = str, location = 'json')
        self.post_reqparse.add_argument('phone', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('email', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('ok_to_sms', type = bool, required = True, location = 'json')
        self.post_reqparse.add_argument('agreed_to_terms', type = bool, required = True, location = 'json')
        self.post_reqparse.add_argument('access_code', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('profile_id', type = int, required = False, location = 'json')
        self.post_reqparse.add_argument('from_other', type = str, required = False, location = 'json')

        self.put_reqparse = reqparse.RequestParser()
        self.put_reqparse.add_argument('id', type = int, required = True, location = 'json')
        self.put_reqparse.add_argument('display_name', type = str, required=False, location = 'json')
        self.put_reqparse.add_argument('phone', type = str, required = False, location = 'json')
        self.put_reqparse.add_argument('email', type = str, required = False, location = 'json')
        self.put_reqparse.add_argument('ok_to_sms', type = bool, required = False, location = 'json')
        #self.put_reqparse.add_argument('username', type = str, required = False, location = 'json')
        #self.put_reqparse.add_argument('password', type = str, required = False, location = 'json')
        #self.put_reqparse.add_argument('password2', type = str, required = False, location = 'json')
        #self.put_reqparse.add_argument('first_name', type = str, required = False, location = 'json')
        #self.put_reqparse.add_argument('last_name', type = str, required = False, location = 'json')

        super(ResidentProfile, self).__init__(*args,**kwargs)


    def post(self):
        # Create new user and profile.
        # This saves a profile as unverified. Verification happens in a different endpoint,
        # for email and/or phone.
        args = self.post_reqparse.parse_args()
        #pprint.pprint(args)
        new_user = User()
        access_code = None
        profile_id = None
        from_other = None

        if args['password'].strip() != args['password2'].strip():
            return make_response(jsonify({'error':"Passwords don't match"}),422)

        if not args['agreed_to_terms']:
            return make_response(jsonify({'error':"User did not agree to terms"}),422)

        if args['profile_id']:
            profile_id = args['profile_id']
            from_other = args['from_other']
            del args['profile_id']
            del args['from_other']

        args['phone']=clean_phone(args.get('phone'))
        if len(args['phone']) < 10:
            return make_response(jsonify({'error':'Invalid phone number, please enter a valid number.'}),422)

        for k, v in args.items():
            if k in ('apartment','username','first_name','last_name','display_name','phone',
                'email','ok_to_sms','agreed_to_terms'):
                setattr(new_user, k, v.strip() if (v and type(v) != bool) else v)
            elif k in ('password','password2'):
                if len(v) > 100 or len(v) < 8:
                    if profile_id:
                        return make_response(jsonify({'error':'Please enter a backup password for your new account.'}),422)
                    else:
                        return make_response(jsonify({'error':'Bad password'}),422)
                if k=='password':
                    setattr(new_user,k,fernet_crypto.encrypt(v.strip()))
            elif k == 'access_code':
                if (len(v) < 8):
                    return make_response(jsonify({'error':'Bad access code'}),422)
                access_code = v.strip()

        # Access code = 6 chars for group access, and last N chars for building.
        building_code = access_code[GROUP_ACCESS_CODE_LENGTH:]

        building = DBSession.query(Building).filter(Building.building_code==building_code).first()
        if not building:
            return make_response(jsonify({'error':'Invalid building code'}),422)

        #pprint.pprint("User's building, based on code:{}".format(building.__dict__))

        access_code_obj = DBSession.query(GroupAccessCode).filter(
            GroupAccessCode.access_code==access_code[0:GROUP_ACCESS_CODE_LENGTH]).filter(
            GroupAccessCode.active==True).first()

        # This is the building and group access code. It was already looked up prior to this function,
        # but we double-check it to be sure no hacking is happening.
        if not access_code_obj:
            return make_response(jsonify({'error':'Invalid access code'}),422)

        new_user.email = new_user.email.lower().strip()
        new_user.apartment = new_user.apartment.lower().strip()
        new_user.username = new_user.username.lower().strip()
        new_user.phone = clean_phone(new_user.phone)
        if (len(new_user.phone) < 10):
            return make_response(jsonify({'error':'Invalid phone number, please enter a valid number.'}),422)

        # Check for user, active or not.
        with ScopedSession() as local_db_session:
            existing_user = local_db_session.query(User).filter(
                User.email==new_user.email).first()
    
            if not existing_user:
                existing_user = local_db_session.query(User).filter(User.username==new_user.username).first()
            if existing_user:
                local_db_session.remove()
                if existing_user.active:
                    return make_response(jsonify({'error':'User name or email already exists. Please try another.'}),422)
                else:
                    # Another account matches, even though they tried to set up a new account.
                    return make_response(jsonify({'error':'User forbidden'}),422) 

            new_user.active=False
            new_user.role=RESIDENT

            local_db_session.add(new_user)
            local_db_session.flush()
            new_user_id = new_user.id
            new_user_ok_to_sms = new_user.ok_to_sms

            group = access_code_obj.group
    
            if not group:
                local_db_session.remove()
                return make_response(jsonify({'error':'No matching building or group'}),422)
            
            bu = BuildingUser(
                user_id = new_user.id,
                building_id = building.id,
                )
            local_db_session.add(bu)

            gu = GroupUser(
                user_id = new_user.id,
                group_id = group.id,
                access_code_id = access_code_obj.id,
                )
            local_db_session.add(gu)

            # Always sms and email
            # We check sms failures in another endpoint.
            new_code = new_security_code(new_user.id,SIGNUP_VALIDATION,numeric=True)
            send_acct_verification_code(new_user.phone,new_code)
            email_account_verification_code(new_user.email,new_code)

            if profile_id:
                #print(f"Updating profile {profile_id} with user {new_user.id}")
                profile = None
                if from_other == 'google':
                    profile = local_db_session.query(GoogleProfile).filter(
                        GoogleProfile.id==profile_id).first()
                elif from_other == 'facebook':
                    profile = local_db_session.query(FacebookProfile).filter(
                        FacebookProfile.id==profile_id).first()
                elif from_other == 'apple':
                    profile = local_db_session.query(AppleProfile).filter(
                        AppleProfile.id==profile_id).first()
                else:
                    # invalid from_other value
                    return make_response(jsonify({"error": "Invalid Source."}), 403)

                if not profile:
                    # because of a bug, try to find it in the apple profile.
                    profile = local_db_session.query(AppleProfile).filter(
                        AppleProfile.id==profile_id).first()
                    if profile and (not profile.user_id) and (profile.apple_email == new_user.email) and \
                            (profile.apple_username == new_user.username):
                        from_other = 'apple'
                    else:
                        app.logger.error(f"We could not find this profile id: {profile_id} for this profile: {from_other} this user: {new_user_id}, user can't log in.")
                        return make_response(jsonify({"error": "Invalid Source. We were just made aware of this error, and we'll hunt it down."}), 403)

                profile.user_id = new_user.id
                local_db_session.flush()

        #pprint.pprint("Added building user entry:{}".format(bu.__dict__))

        return make_response(jsonify({'id':new_user_id,
            'sms':new_user_ok_to_sms}),201)

    def put(self):
        put_args = self.put_reqparse.parse_args()
        new_user_id = put_args['id']
        phone = put_args.get('phone', None)
        email = put_args.get('email', None)

        new_user = DBSession.query(User).filter(User.id==new_user_id).first()
        if not new_user:
            return make_response(jsonify({'error':'Nope'}),403)
        if new_user.active:
            return make_response(jsonify({'error':'Not allowed'}),403)

        with ScopedSession() as local_db_session:
            if phone:
                local_db_session.query(User).filter(
                    User.id==new_user_id).update(
                    {User.phone:clean_phone(phone)},synchronize_session=False)
            else:
                phone = new_user.phone
    
            if email:
                email = email.strip().lower()
    
                dup_user = DBSession.query(User).filter(
                    func.lower(User.email)==email).first()
    
                if dup_user and dup_user.id != new_user.id:
                    app.logger.error(f"User can't see this: User {new_user.id}, {new_user.first_name} {new_user.last_name} is trying to create a new account, used an existing email address: {email}, it failed.")
                    return make_response(jsonify({'error':'Invalid email address'}),403)
    
                local_db_session.query(User).filter(
                    User.id==new_user_id).update(
                    {User.email:email},synchronize_session=False)
            else:
                email = new_user.email

        new_code = new_security_code(new_user.id,SIGNUP_VALIDATION,numeric=True)
        email_account_verification_code(email,new_code)
        if not send_acct_verification_code(phone,new_code): # always sms and email
            code=422
            if email:
                code=403
            return make_response(jsonify({'error':'SMS failed. Either enter a new number or verify with email'}),code)
        return make_response(jsonify({'error':None}),200)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ProviderProfile(Resource):

    def __init__(self,*args,**kwargs):
        # Address is required.

        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('username', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('password', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('password2', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('first_name', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('last_name', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('address', type = str, location = 'json')
        self.post_reqparse.add_argument('city', type = str, location = 'json')
        self.post_reqparse.add_argument('state', type = str, location = 'json')
        self.post_reqparse.add_argument('zip_code', type = str, location = 'json')
        self.post_reqparse.add_argument('phone', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('email', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('ok_to_sms', type = bool, required = True, location = 'json')

        self.put_reqparse = reqparse.RequestParser()
        self.put_reqparse.add_argument('id', type = int, required = False, location = 'json')
        #self.put_reqparse.add_argument('username', type = str, required = False, location = 'json')
        self.put_reqparse.add_argument('password', type = str, required = False, location = 'json')
        self.put_reqparse.add_argument('password2', type = str, required = False, location = 'json')
        #self.put_reqparse.add_argument('first_name', type = str, required = False, location = 'json')
        #self.put_reqparse.add_argument('last_name', type = str, required = False, location = 'json')
        self.put_reqparse.add_argument('address', type = str, location = 'json')
        self.put_reqparse.add_argument('city', type = str, location = 'json')
        self.put_reqparse.add_argument('state', type = str, location = 'json')
        self.put_reqparse.add_argument('zip_code', type = str, location = 'json')
        self.put_reqparse.add_argument('phone', type = str, required = False, location = 'json')
        self.put_reqparse.add_argument('email', type = str, required = False, location = 'json')
        self.put_reqparse.add_argument('ok_to_sms', type = bool, required = False, location = 'json')

        super(ProviderProfile, self).__init__(*args,**kwargs)


    @jwt_required
    def put(self):
        args = self.put_reqparse.parse_args()

    def post(self):
        # Create new service provider and profile
        # Provider won't be in a building. They will, however, be added to
        # building groups, so we know what area they can serve. 
        args = self.post_reqparse.parse_args()
        new_user = User()
        new_address = Address() 

        if args['password'] != args['password2']:
            return make_response(jsonify({'error':"Passwords don't match"}),422)

        args['phone'] = clean_phone(args['phone'])

        if (len(args['phone']) < 10):
            return make_response(jsonify({'error':'Bad phone l'}),422)

        for k, v in args.items():
            if k in ('username','first_name','last_name','phone','email','ok_to_sms'):
                setattr(new_user, k, v)
            elif k in ('password','password2'):
                if (len(v) > 100 or len(v) < 8):
                    return make_response(jsonify({'error':'Bad password'}),422)
                if k=='password':
                    setattr(new_user,k,fernet_crypto.encrypt(v))
            else:
                setattr(new_address, k, v)

        # Check for user, active or not.
        with ScopedSession() as local_db_session:
            existing_user = local_db_session.query(User).filter(User.email==new_user.email).first()
            if not existing_user:
                existing_user = local_db_session.query(User).filter(User.username==new_user.username).first()
            if existing_user:
                local_db_session.remove()
                return make_response(jsonify({'error':'User name or email already exists. Use PUT request to update.'}),422)
    
            if not args['address']:
                local_db_session.remove()
                return make_response(jsonify({'error':'Missing address'}),422)
    
            new_user.active=False
            new_user.role=PROVIDER
    
            local_db_session.add(new_user)
            local_db_session.flush()
    
            new_address.user_id = new_user.id
            local_db_session.add(new_address)
            local_db_session.flush()
                
            new_code = new_security_code(new_user.id,SIGNUP_VALIDATION,numeric=True)
            email_account_verification_code(new_user.email,new_code)
            if not send_acct_verification_code(new_user.phone,new_code): # always sms
                local_db_session.rollback()
                return make_response(jsonify({'error':'SMS failed.'}),403)
    
        return make_response(jsonify({'id':new_user.id,'sms':new_user.ok_to_sms}),201)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PushnotTokenUpdate(Resource):
    def __init__(self,*args,**kwargs):
        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('token', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('macs', type = str, required = False, location = 'json')
        super(PushnotTokenUpdate, self).__init__(*args,**kwargs)

    @jwt_required
    def post(self):
        code,error,user,x,y,timezone = current_user()
        if code != 200:
            abort(code,error)

        # Phone/device generates Firebase Cloud Messaging 
        # Push Notification token on the device, then sends it to us.
        args = self.post_reqparse.parse_args()
        if (args['token'] == None) or (len(args['token']) > 200) or (len(args['token']) == 0):
            return make_response(jsonify({'error':'Bad Token'}),422)
        token = args['token'].strip()

        with ScopedSession() as local_db_session:
            local_db_session.query(User).filter(User.id==user.id).update({
                'firebase_pushnot_id':token},synchronize_session=False)
      
            # Opportinity to update mac addrs.
            if 'macs' in args and args['macs']:
                # We're excpecting [{'addr':aa.aa.aa.aa.aa,'type':'bluetooth'},{'addr':aa.aa.aa.aa.aa,'type':'wifi'}]
                macs = json.loads(args['macs'])
                for addr,mtype in macs:
                    uhm = UserHardwareMap(
                        user_mac_addr = addr,
                        connection_type = ROUTER_TYPES[mtype],
                        user_id = user.id,
                        )
                    local_db_session.add(uhm)

        return make_response(jsonify({'error':None}),200)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ValidateSignup(Resource):
    def __init__(self,*args,**kwargs):
        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('user_id', type = int, required = True, location = 'json')
        self.post_reqparse.add_argument('code', type = str, required = True, location = 'json')
        self.post_reqparse.add_argument('via_email', type = bool, required = True, location = 'json')
        super(ValidateSignup, self).__init__(*args,**kwargs)

    def post(self):
        # This is a validation code sent via email or SMS, to activate the account.
        args = self.post_reqparse.parse_args()
        code = args['code'].strip()
        user_id = args['user_id']
        verified_via_email = args['via_email']

        ruser = verify_security_code(code,activate=True)
        if ruser and ruser.id == user_id:
            ok_to_sms = True
            if verified_via_email:
                ok_to_sms = False
            with ScopedSession in local_db_session:
                local_db_session.query(User).filter(User.id==user_id).update({
                    'active':True,'ok_to_sms':ok_to_sms})
            welcome_email(ruser.email)
            return make_response(jsonify({'error':None}),200)

        # Consider account lock based on IP or user, if this happens more than N times.
        abort(422,'Invalid security code')
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ModifyProfileParams(Resource):
    def __init__(self,*args,**kwargs):
        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('new_username', type = str, required = False, location = 'json')
        self.post_reqparse.add_argument('new_email', type = str, required = False, location = 'json')
        self.post_reqparse.add_argument('new_phone', type = str, required = False, location = 'json')
        self.post_reqparse.add_argument('new_apartment', type = str, required = False, location = 'json')
        self.post_reqparse.add_argument('code', type = str, required = False, location = 'json')
        self.post_reqparse.add_argument('user_id', type = int, required = True, location = 'json')
        super(ModifyProfileParams, self).__init__(*args,**kwargs)

    @jwt_required
    def post(self):
        code,error,ruser,x,y,timezone = current_user()
        if code != 200:
            abort(code,error)

        args = self.post_reqparse.parse_args()
        user_id = args['user_id']
        if user_id != ruser.id:
            return make_response(jsonify({'error':'Invalid update attempt'}),422)

        phone = ruser.phone
        email = ruser.email

        if 'code' in args and args['code']:
            # This is a validation code sent via email or SMS, to activate the account.
            code = args['code'].strip()
            ruser = verify_security_code(code)

            profile_update = {}
            if data['new_email']:
                profile_update['email'] = data['new_email']
            if data['new_phone']:
                profile_update['phone'] = data['new_phone']
            if data['new_apartment']:
                profile_update['apartment'] = data['new_apartment']
            if data['new_username']:
                profile_update['username'] = data['new_username']

            with ScopedSession in local_db_session:
                local_db_session.query(User).filter(User.id==user_id).update(profile_update)
            return make_response(jsonify({'error':None}),200)

        else:
            if not args['new_phone'] and not args['new_email'] and not args['new_apartment'] and not args['new_username']:
                return make_response(jsonify({'error':'No change'}),422)

            if args['new_phone']:
                args['new_phone'] = clean_phone(args['new_phone'])
                if (len(args['new_phone']) < 10):
                    return make_response(jsonify({'error':'Bad phone (u)'}),422)
                phone = args['new_phone']

            if args['new_email']:
                args['new_email'] = args['new_email'].lower().strip()
                if len(args['new_email']) <= 0 or len(args['new_email']) > 100:
                    #maybe keep this one, someone putting bad emails in could be possible attack
                    app.logger.error("User can't see this: User sent this email to forgot password, it failed: {}".format(
                        post_args['new_email']))
                    return make_response(jsonify({'error':'Invalid email (8)'}),422)
                email = args['new_email']

            data = args
            data['user_id'] = user_id
            data['data_type'] = 'profile_update'

            new_code = new_security_code(user_id,PROFILE_CHG,numeric=True)
            email_account_verification_code(email,new_code)
            if ruser.ok_to_sms and not send_acct_verification_code(phone,new_code):
                return make_response(jsonify({'message':'We sent you an account verification code via email and SMS. The SMS send failed.'}),200)

            return make_response(jsonify({'message':'We sent you an account verification code via email and SMS.'}),200)

        # Consider account lock based on IP or user, if this happens more than N times.
        return make_response(jsonify({'error':'Invalid security code'}),422)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
api.add_resource(ResidentProfile, '/{0}profile/resident/'.format(URL_PREFIX),
    endpoint='profile_crud_r')

api.add_resource(ProviderProfile, '/{0}profile/provider/'.format(URL_PREFIX),
    endpoint='profile_crud_p')

api.add_resource(ValidateSignup, '/{0}profile/validate/'.format(URL_PREFIX),
    endpoint='profile_validate')

api.add_resource(PushnotTokenUpdate, '/{0}profile/pushnotid/'.format(URL_PREFIX),
    endpoint='update_pushnot_token')

api.add_resource(ModifyProfileParams, '/{0}profile/'.format(URL_PREFIX),
    endpoint='update_profile')

api.add_resource(NonuserInquiryPage1, '/{0}bldg_inquiry/contact/'.format(URL_PREFIX),
    endpoint='bldg_inquiry_1')

api.add_resource(NonuserInquiryCodeValidation, '/{0}bldg_inquiry/validate/'.format(URL_PREFIX),
    endpoint='bldg_inquiry_code_validation')

api.add_resource(NonuserInquiryCodeResend, '/{0}bldg_inquiry/resend/'.format(URL_PREFIX),
    endpoint='bldg_inquiry_code_resend')

api.add_resource(NonuserInquiryPage2, '/{0}bldg_inquiry/address/'.format(URL_PREFIX),
    endpoint='bldg_inquiry_2')


#if __name__ == "__main__":
#    print(current_user(1255))
