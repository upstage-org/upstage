# -*- coding: iso8859-15 -*-
from datetime import datetime
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, String, BigInteger, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from config.project_globals import Base,metadata,DBSession
from user.models import User
from asset.models import Asset,Stage

'''
A performance is comprised of one or more Scenes. Scenes have an ordering,
and direct us on which assets are needed when, in a performance. 
Assets follow a hierarchy when rendering for a performance.
'''
class ParentStage(Base,db.Model):
    '''
    This maps all 'children' in a hierarchy of assets for a stage.
    Assets also have children.
    Not yet sure if this maps only the first tier, or all assets to a stage.
    I could see the benefit of mapping them all, for quick asset collection.
    '''
    __tablename__ = "parent_stage"
    id = Column(BigInteger, primary_key=True)
    stage_id = Column(Integer, ForeignKey(Stage.id), nullable=False, default=0)
    child_asset_id = Column(Integer, ForeignKey(Asset.id), nullable=False, default=0)
    stage = relationship(Stage, foreign_keys=[stage_id])
    child_asset = relationship(Asset, foreign_keys=[child_asset_id])

class ParentAsset(Base,db.Model):
    '''
    This maps a parent to a child asset, so that rendering can follow a hierarchy.
    The topmost parent asset is a stage.
    '''
    __tablename__ = "parent_asset"
    id = Column(BigInteger, primary_key=True)
    asset_id = Column(Integer, ForeignKey(Asset.id), nullable=False, default=0)
    child_asset_id = Column(Integer, ForeignKey(Asset.id), nullable=False, default=0)
    asset = relationship(Asset, foreign_keys=[asset_id])
    child_asset = relationship(Asset, foreign_keys=[child_asset_id])

class Scene(Base,db.Model):
    __tablename__ = "scene"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    scene_ordering = Column(Integer, nullable=False, default=0)
    owner_id = Column(Integer, ForeignKey(User.id), nullable=False, default=0)
    description = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    expires_on = Column(DateTime, nullable=False, default=None)
    parent_stage_id = Column(Integer, ForeignKey(ParentStage.id), nullable=False, default=0)
    owner = relationship(User, foreign_keys=[owner_id])
    parent_stage = relationship(ParentStage, foreign_keys=[parent_stage_id])

class Performance(Base,db.Model):
    __tablename__ = "performance"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey(User.id), nullable=False, default=0)
    description = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow())
    expires_on = Column(DateTime, nullable=False, default=None)

class ScenePerformance(Base,db.Model):
    __tablename__ = "scene_performance"
    id = Column(BigInteger, primary_key=True)
    scene_id = Column(Integer, ForeignKey(Scene.id), nullable=False, default=0)
    performance_id = Column(Integer, ForeignKey(Performance.id), nullable=False, default=0)
    description = Column(Text, nullable=False)
