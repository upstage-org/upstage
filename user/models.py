# -*- coding: iso8859-15 -*-
import os,sys
import re
import pdb
import pprint
import traceback
from datetime import datetime
appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from config.project_globals import db,Base,metadata,app,api,DBSession

from flask import  current_app, request, redirect, render_template

from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime,
    Float, ForeignKey, Index, Integer, Numeric, SmallInteger,
    String, Table, Text, Time, text, DATE, func, UniqueConstraint)
from sqlalchemy.dialects.postgresql.base import INET, TSVECTOR
from sqlalchemy.sql.expression import func, or_, not_, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

ATTENDEE = 1
PARTICIPANT = 2
ACCOUNT_ADMIN = 4
SUPER_ADMIN = 8

ADMINS = ACCOUNT_ADMIN | SUPER_ADMIN

ROLES = {
    ATTENDEE:'Attendee',
    PARTICIPANT:'Participant',
    ACCOUNT_ADMIN:'Account Admin',
    SUPER_ADMIN:'Super Admin',
}

# These limit access, they don't widen access.
ACCESS_PERFORM = 1
ACCESS_EDIT = 2
ACCESS_MODERATE = 4

ACCESS = {
    ACCESS_PERFORM:'Only perform, no edits',
    ACCESS_EDIT:'Create/edit content, no performing',
    ACCESS_MODERATE:'Moderate chat and other things',
}

def role_conv(roles_bitmask):
    role_strings = []
    #was getting an exception on local because this was nont?
    if roles_bitmask is not None:
        for r in ROLES:
            if roles_bitmask & r == r:
                role_strings.append(ROLES[r])
        return ','.join(role_strings)

class User(Base,db.Model):
    __tablename__ = 'upstage_user'
    id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False, unique=True, default='')
    password = Column(Text, nullable=False, default='')
    email = Column(Text, nullable=False, unique=True, default='')
    bin_name = Column(Text,nullable=False,default='')
    role = Column(Integer, nullable=False, default=0)
    access_bitmask = Column(BigInteger, nullable=False, default=0)
    first_name = Column(Text, default='')
    last_name = Column(Text, default='')
    display_name = Column(Text, default='')
    phone = Column(Text, default='')
    active = Column(Boolean, nullable=False, default=False)
    ok_to_sms = Column(Boolean, nullable=False, default=True)
    # This flag is for making sure
    # we're accessing the portal from a certain path, only for admins.
    validated_via_portal = Column(Boolean, nullable=False, default=False)
    agreed_to_terms = Column(Boolean, nullable=False, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    firebase_pushnot_id = Column(Text, default=None)
    deactivated_on = Column(DateTime)

    def has_access(self, required_bitmasks):
        #super admins can do all...
        if self.role==SUPER_ADMIN:
            return True
        #access_bitmask==0 you have access to everything your role allows
        if self.access_bitmask==0:
            return True
        #if required_bitmasks==0 you have to have access to everything...
        if required_bitmasks==0:
            return False
        return required_bitmasks & self.access_bitmask == required_bitmasks

    def human_redable_access(self):
        for bitmask in ACCESS:
            if bitmask & self.access_bitmask:
                print(ACCESS[bitmask])

class UserPushnot(Base,db.Model):
    __tablename__ = 'user_pushnot'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey(User.id), nullable=False, default=0)
    push_notification = Column(Text, nullable=False, default='')
    user = relationship(User, foreign_keys=[user_id])

class UserPortalConfig(Base,db.Model):
    __tablename__ = 'user_portal_config'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey(User.id), unique=True,nullable=False, default=0)
    json_config = Column(Text, nullable=False, default='{"viewing_timezone":"US/Eastern"}')
    user = relationship(User, foreign_keys=[user_id])

class NonuserInquiry(Base,db.Model):
    __tablename__ = 'nonuser_inquiry'
    id = Column(Integer, primary_key=True)
    phone_number = Column(Text, nullable=False, default='')
    access_code = Column(Text, nullable=False, default='')
    verified = Column(Boolean, nullable=False, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    first_name = Column(Text, nullable=False, default='')
    last_name = Column(Text, nullable=False, default='')
    email = Column(Text, nullable=False, default='')
    full_address = Column(Text, nullable=False, default='')
    found_match = Column(Text, nullable=True, default=None)

class OneTimeTOTPQRURL(Base, db.Model):
    __tablename__ = 'admin_one_time_totp_qr_url'

    # This is a one-time link to get the QR code for the TOTP secret, for Google Authenticator, etc.
    # Only admins use this, in the portal.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey(User.id), unique=True, nullable=False, default=0)
    url = Column(Text,nullable=False,default='')
    code = Column(Text,nullable=False,default='')
    recorded_time = Column(DateTime, nullable=False, index=True, default=datetime.utcnow)
    active = Column(Boolean, nullable=False, index=True, default=True)
    user = relationship(User, foreign_keys=[user_id])

