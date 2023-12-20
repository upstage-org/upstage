# -*- coding: iso8859-15 -*-
import os, sys
import re
import pdb
import random
import string
import pprint
import traceback
from datetime import datetime

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from core.project_globals import Base, metadata, DBSession, ScopedSession, db, app

from flask import request, redirect, render_template

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Table,
    Text,
    Time,
    text,
    DATE,
    func,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql.base import INET, TSVECTOR
from sqlalchemy.sql.expression import func, or_, not_, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.user.models import User

SIGNUP_VALIDATION = 1
RESET_PASSWORD = 2
SIGNUP_VALIDATION_MISSING_1ST_CODE = 3
PROFILE_CHG = 4
PUBLIC_LOGIN = 5
SECURITY_CODE_REASONS = {
    SIGNUP_VALIDATION: "Signup Validation",
    RESET_PASSWORD: "Password Reset",
    SIGNUP_VALIDATION_MISSING_1ST_CODE: "Missing code we sent you before, account was inactive, were you banned?",
    PROFILE_CHG: "Profile change",
    PUBLIC_LOGIN: "Public-facing admin interface",
}


class JWTNoList(Base, db.Model):
    __tablename__ = "jwt_no_list"
    id = Column(BigInteger, primary_key=True)
    token = Column(Text, nullable=False, unique=True, default="")
    token_type = Column(Text, nullable=False, default="")
    remove_after = Column(DateTime, nullable=False, default=datetime.utcnow)


class UserSession(Base, db.Model):
    __tablename__ = "user_session"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey(User.id, deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    access_token = Column(Text, default=None)
    refresh_token = Column(Text, default=None)
    recorded_time = Column(
        DateTime, nullable=False, index=True, default=datetime.utcnow
    )
    app_version = Column(Text, default=None)
    app_os_type = Column(Text, default=None)
    app_os_version = Column(Text, default=None)
    app_device = Column(Text, default=None)
    user = relationship(User, foreign_keys=[user_id])


class OneTimeCode(Base, db.Model):
    __tablename__ = "user_one_time_code"

    # Unconfirmed codes are just replaced with new unconfirmed codes.
    # Confirmed codes go into history.
    id = Column(BigInteger, primary_key=True)
    user_id = Column(
        Integer, ForeignKey(User.id), unique=True, nullable=False, default=0
    )
    code = Column(Text, nullable=False, default="")
    reason = Column(Integer, nullable=False, default=0)
    pending_google_login_id = Column(Integer, nullable=False, default=0)
    pending_facebook_login_id = Column(Integer, nullable=False, default=0)
    pending_apple_login_id = Column(Integer, nullable=False, default=0)
    user = relationship(User, foreign_keys=[user_id])


class OneTimeCodeHistory(Base, db.Model):
    __tablename__ = "user_one_time_code_history"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(
        Integer, nullable=False, index=True
    )  # No foreign key in history records.
    code = Column(Text, nullable=False, default="")
    reason = Column(Integer, nullable=False, default=0)
    pending_google_login_id = Column(Integer, nullable=False, default=0)
    pending_facebook_login_id = Column(Integer, nullable=False, default=0)
    pending_apple_login_id = Column(Integer, nullable=False, default=0)
    response_time = Column(DateTime, nullable=False, default=datetime.utcnow)


class GoogleProfile(Base, db.Model):
    __tablename__ = "google_profile"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True, default=None)
    google_id = Column(Text, nullable=True, default=None)
    google_phone = Column(Text, nullable=True, default=None)
    google_email = Column(Text, nullable=True, default=None)
    google_first_name = Column(Text, nullable=True, default=None)
    google_last_name = Column(Text, nullable=True, default=None)
    google_username = Column(Text, nullable=True, default=None)
    other_profile_json = Column(Text, nullable=True, default=None)
    received_datetime = Column(DateTime, nullable=False, default=datetime.utcnow)


class FacebookProfile(Base, db.Model):
    __tablename__ = "facebook_profile"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True, default=None)
    facebook_id = Column(Text, nullable=True, default=None)
    facebook_phone = Column(Text, nullable=True, default=None)
    facebook_email = Column(Text, nullable=True, default=None)
    facebook_first_name = Column(Text, nullable=True, default=None)
    facebook_last_name = Column(Text, nullable=True, default=None)
    facebook_username = Column(Text, nullable=True, default=None)
    other_profile_json = Column(Text, nullable=True, default=None)
    received_datetime = Column(DateTime, nullable=True, default=datetime.utcnow)


class AppleProfile(Base, db.Model):
    __tablename__ = "apple_profile"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True, default=None)
    apple_id = Column(Text, nullable=True, default=None)
    apple_phone = Column(Text, nullable=True, default=None)
    apple_email = Column(Text, nullable=True, default=None)
    apple_first_name = Column(Text, nullable=True, default=None)
    apple_last_name = Column(Text, nullable=True, default=None)
    apple_username = Column(Text, nullable=True, default=None)
    other_profile_json = Column(Text, nullable=True, default=None)
    received_datetime = Column(DateTime, nullable=True, default=datetime.utcnow)


def BadSecCodeReason(Exception):
    pass


# Access codes are different from Security codes: Access codes check authorization to get in.
# Security codes check authentication: Is your phone/email genuinely yours?
# For a first-time login via google/apple/facebook, this will track the mapping
# of user to code, and hold it in a "pending" state until the code is verified.
# For all otehr one-time code use, it's just a code pending later verification.
def new_security_code(
    user_id,
    reason,
    pending_g_id=None,
    pending_f_id=None,
    pending_a_id=None,
    numeric=False,
):
    # Delete any possible existing one time urls for this user.
    if reason not in SECURITY_CODE_REASONS:
        raise BadSecCodeReason("Invalid reason id for new security code, failing")

    local_db_session = get_scoped_session()
    local_db_session.query(OneTimeCode).filter(OneTimeCode.user_id == user_id).delete()
    local_db_session.flush()
    # local_db_session.commit()

    # local_db_session = get_scoped_session()
    if numeric:
        new_code = generate_numeric_security_access_code()
    else:
        new_code = generate_security_access_code()
    otc = OneTimeCode(
        user_id=user_id,
        code=new_code,
        reason=reason,
        pending_google_login_id=pending_g_id,
        pending_facebook_login_id=pending_f_id,
        pending_apple_login_id=pending_a_id,
    )
    local_db_session.add(otc)
    local_db_session.commit()
    local_db_session.close()
    return new_code


# Needed for re-send.
def get_security_code(user_id, reason):
    if reason not in SECURITY_CODE_REASONS:
        raise BadSecCodeReason("Invalid reason id for new security code, failing")

    code = (
        DBSession.query(OneTimeCode)
        .filter(OneTimeCode.user_id == user_id)
        .filter(OneTimeCode.reason == reason)
        .first()
    )

    if code:
        return code.code


def verify_security_code(code, activate=False):
    # Verify that it exists, save history, pass back corresp. user id.
    code = code.lower().strip()

    local_db_session = get_scoped_session()
    result = (
        local_db_session.query(OneTimeCode).filter(OneTimeCode.code == code).first()
    )
    if not result:
        local_db_session.commit()
        local_db_session.close()
        return

    user_id = result.user_id
    hist = OneTimeCodeHistory(
        user_id=result.user_id,
        code=result.code,
        pending_google_login_id=result.pending_google_login_id,
        pending_facebook_login_id=result.pending_facebook_login_id,
        pending_apple_login_id=result.pending_apple_login_id,
        reason=result.reason,
    )

    local_db_session.add(hist)

    if result.pending_google_login_id:
        local_db_session.query(GoogleProfile).filter(
            GoogleProfile.id == result.pending_google_login_id
        ).update({GoogleProfile.user_id: user_id}, synchronize_session=False)

    if result.pending_facebook_login_id:
        local_db_session.query(FacebookProfile).filter(
            FacebookProfile.id == result.pending_facebook_login_id
        ).update({FacebookProfile.user_id: user_id}, synchronize_session=False)

    if result.pending_apple_login_id:
        local_db_session.query(AppleProfile).filter(
            AppleProfile.id == result.pending_apple_login_id
        ).update({AppleProfile.user_id: user_id}, synchronize_session=False)

    local_db_session.query(OneTimeCode).filter(OneTimeCode.id == result.id).delete(
        synchronize_session=False
    )

    if activate:
        local_db_session.query(User).filter(User.id == user_id).update(
            {"active": True}, synchronize_session=False
        )

    local_db_session.commit()
    local_db_session.close()
    return DBSession.query(User).filter(User.id == user_id).one()


"""
if __name__ == "__main__":
    import random
    for user in DBSession.query(User).all():
        new_security_code(user.id,random.randint(SIGNUP_VALIDATION,RESET_PASSWORD))
"""
