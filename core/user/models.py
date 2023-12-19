# -*- coding: iso8859-15 -*-
import os, sys
import re
import pdb
import pprint
import traceback
from datetime import datetime

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

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

from core.project_globals import Base, DBSession, db, app

PLAYER = 1
GUEST = 4
ADMIN = 8
SUPER_ADMIN = 32

ROLES = {
    PLAYER: "Player",  # Player access to on-stage tools
    GUEST: "Guest",  # Can play a stage if granted player permission, cannot create or edit media
    ADMIN: "Admin",  # Admin access to edit media, players, content
    SUPER_ADMIN: "Super Admin",  # Internal Upstage staff access to all
}


def role_conv(roles_bitmask):
    role_strings = []
    # was getting an exception on local because this was nont?
    if roles_bitmask is not None:
        for r in ROLES:
            if roles_bitmask & r == r:
                role_strings.append(ROLES[r])
        return ",".join(role_strings)


class User(Base, db.Model):
    __tablename__ = "upstage_user"
    id = Column(BigInteger, primary_key=True)
    username = Column(Text, nullable=False, unique=True, default="")
    password = Column(Text, nullable=False, default="")
    email = Column(Text, nullable=True, default="")
    bin_name = Column(Text, nullable=True, default="")
    role = Column(Integer, nullable=False, default=0)
    first_name = Column(Text, default="")
    last_name = Column(Text, default="")
    display_name = Column(Text, default="")
    active = Column(Boolean, nullable=False, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    firebase_pushnot_id = Column(Text, default=None)
    deactivated_on = Column(DateTime)
    upload_limit = Column(Integer, default=1024 * 1024)
    intro = Column(Text, default="")
    can_send_email = Column(Boolean, default=False)


class UserPushnot(Base, db.Model):
    __tablename__ = "user_pushnot"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, default=0)
    push_notification = Column(Text, nullable=False, default="")
    user = relationship(User, foreign_keys=[user_id])


class UserPortalConfig(Base, db.Model):
    __tablename__ = "user_portal_config"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(
        Integer, ForeignKey(User.id), unique=True, nullable=False, default=0
    )
    json_config = Column(
        Text, nullable=False, default='{"viewing_timezone":"US/Eastern"}'
    )
    user = relationship(User, foreign_keys=[user_id])


class OneTimeTOTP(Base, db.Model):
    __tablename__ = "admin_one_time_totp_qr_url"

    # This is a one-time link to get the QR code for the TOTP secret, for Google Authenticator, etc.
    # Only admins use this, in the portal.
    id = Column(BigInteger, primary_key=True)
    user_id = Column(
        Integer, ForeignKey(User.id), unique=True, nullable=False, default=0
    )
    url = Column(Text, nullable=False, default="")
    code = Column(Text, nullable=False, default="")
    recorded_time = Column(
        DateTime, nullable=False, index=True, default=datetime.utcnow
    )
    active = Column(Boolean, nullable=False, index=True, default=True)
    user = relationship(User, foreign_keys=[user_id])
