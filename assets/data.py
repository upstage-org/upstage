from datetime import datetime
import os
import sys

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class Asset(db.Model):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    file_location = Column(Text, nullable=False, index=True)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow(), index=True)


class AssetLicense(db.Model):
    __tablename__ = "asset_licenses"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey(Asset.id), nullable=False, index=True)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow(), index=True)
    expires_on = Column(DateTime, nullable=False, default=datetime.utcnow(), index=True)
    access_path = Column(String, nullable=False, unique=True, index=True)
    asset = relationship(Asset, foreign_keys=[asset_id])
