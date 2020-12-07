# -*- coding: iso8859-15 -*-
from datetime import datetime
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from sqlalchemy import Column, DateTime, String, BigInteger, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from config.project_globals import db,Base,metadata,app,api,DBSession
from user.models import User

class AssetType(Base,db.Model):
    '''
    Asset type is Prop, Avatar/Sprite, Backdrop, for example. 
    Over time we should be able to add more types or variations on 
    existing types.
    '''
    __tablename__ = "asset_type"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    file_location = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())

class Asset(Base,db.Model):
    __tablename__ = "asset"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    asset_type_id = Column(Integer, ForeignKey(AssetType.id), nullable=False, default=0)
    owner_id = Column(Integer, ForeignKey(User.id), nullable=False, default=0)
    description = Column(Text, nullable=False)
    file_location = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    asset_type = relationship(AssetType, foreign_keys=[asset_type_id])
    owner = relationship(User, foreign_keys=[owner_id])

class Stage(Base,db.Model):
    '''
    Stage is yet another asset type, with its own attributes, 
    but is broken out for convenience of group licensing/permissions.
    '''
    __tablename__ = "stage"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey(User.id), nullable=False, default=0)
    file_location = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    owner = relationship(User, foreign_keys=[owner_id])

class AssetAttribute(Base,db.Model):
    '''
    Attributes are the abilities of the asset: What the asset can do or be. 
    For example, flip, rotate, draw, overlay, be opaque, dissolve, loop.
    Breaking out attributes and actions seemed like splitting hairs, and
    seems much easier in one table.
    '''
    __tablename__ = "asset_attribute"
    id = Column(BigInteger, primary_key=True)
    asset_id = Column(Integer, ForeignKey(Asset.id), nullable=False, default=0)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    asset = relationship(Asset, foreign_keys=[asset_id])

class StageAttribute(Base,db.Model):
    __tablename__ = "stage_attribute"
    id = Column(BigInteger, primary_key=True)
    stage_id = Column(Integer, ForeignKey(Stage.id), nullable=False, default=0)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    stage = relationship(Stage, foreign_keys=[stage_id])
