# -*- coding: iso8859-15 -*-
from datetime import datetime
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from sqlalchemy import Column, DateTime, String, BigInteger, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from config.project_globals import db,Base,metadata,app,api,DBSession
from user.models import User


class StageLicense(Base,db.Model):
    '''
    Stage is yet another asset, but broken out as the 'root' in the hierarchy.
    One can grant a license to everything under a stage, or any other asset,
    to make licensing easier.
    '''
    __tablename__ = "stage_license"
    id = Column(BigInteger, primary_key=True)
    stage_id = Column(Integer, ForeignKey('stage.id'), nullable=False, default=0)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_on = Column(DateTime, nullable=True)
    access_path = Column(String, nullable=False, unique=True)
    grant_recursively = Column(Boolean, nullable=False, default=False)
    stage = relationship('Stage', foreign_keys=[stage_id])

class AssetLicense(Base,db.Model):
    __tablename__ = "asset_license"
    id = Column(BigInteger, primary_key=True)
    asset_id = Column(Integer, ForeignKey('asset.id'), nullable=False, default=0)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    level = Column(Integer, nullable=False, default=0)
    permissions = Column(String, nullable=True)

class AssetUsage(Base,db.Model):
    __tablename__ = "asset_usage"
    id = Column(BigInteger, primary_key=True)
    asset_id = Column(Integer, ForeignKey('asset.id'), nullable=False, default=0)
    user_id = Column(Integer, ForeignKey('upstage_user.id'), nullable=False, default=0)
    approved = Column(Boolean, nullable=False, default=False)
    seen = Column(Boolean, nullable=False, default=False)
    note = Column(String, nullable=True)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    user = relationship('User', foreign_keys=[user_id])
    asset = relationship('Asset', foreign_keys=[asset_id])