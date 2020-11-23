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

from user.models import User
from assets.data import Asset,Stage

'''
Group permissions/licensing can be done at the group, stage, or asset level.
A user belonging to a group can see all assets/stages belonging to that group.
'''
class Group(Base,db.Model):
    __tablename__ = 'upstage_group'
    id = Column(BigInteger, primary_key=True)
    description = Column(Text)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())

class AssetGroup(Base,db.Model):
    __tablename__ = 'asset_group'
    id = Column(BigInteger, primary_key=True)
    description = Column(Text)
    group_id = Column(Integer,ForeignKey(Group.id), nullable=False, default=0)
    asset_id = Column(Integer,ForeignKey(Asset.id), nullable=False, default=0)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    group = relationship(Group, foreign_keys=[group_id])
    asset = relationship(Asset, foreign_keys=[asset_id])

class StageGroup(Base,db.Model):
    __tablename__ = 'stage_group'
    id = Column(BigInteger, primary_key=True)
    description = Column(Text)
    group_id = Column(Integer,ForeignKey(Group.id), nullable=False, default=0)
    stage_id = Column(Integer,ForeignKey(Stage.id), nullable=False, default=0)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    group = relationship(Group, foreign_keys=[group_id])
    stage = relationship(Stage, foreign_keys=[stage_id])

class UserGroup(Base,db.Model):
    __tablename__ = 'user_group'
    id = Column(BigInteger, primary_key=True)
    notes = Column(Text)
    group_id = Column(Integer,ForeignKey(Group.id), nullable=False, default=0)
    user_id = Column(Integer,ForeignKey(User.id), nullable=False, default=0)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    group = relationship(Group, foreign_keys=[group_id])
    user = relationship(User, foreign_keys=[user_id])

class UserAsset(Base,db.Model):
    __tablename__ = 'user_asset'
    id = Column(BigInteger, primary_key=True)
    notes = Column(Text)
    asset_id = Column(Integer,ForeignKey(Asset.id), nullable=False, default=0)
    user_id = Column(Integer,ForeignKey(User.id), nullable=False, default=0)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    asset = relationship(Asset, foreign_keys=[asset_id])
    user = relationship(User, foreign_keys=[user_id])

class UserStage(Base,db.Model):
    __tablename__ = 'user_stage'
    id = Column(BigInteger, primary_key=True)
    notes = Column(Text)
    stage_id = Column(Integer,ForeignKey(Stage.id), nullable=False, default=0)
    user_id = Column(Integer,ForeignKey(User.id), nullable=False, default=0)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    stage = relationship(Stage, foreign_keys=[stage_id])
    user = relationship(User, foreign_keys=[user_id])

