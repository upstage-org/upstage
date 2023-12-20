# -*- coding: iso8859-15 -*-
from core.project_globals import db, Base
from sqlalchemy import Column, DateTime, String, BigInteger, Text
from datetime import datetime
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


class Config(Base, db.Model):
    """
    System configuration, such as the Terms of Service's URL, theme, global settings,...
    """

    __tablename__ = "config"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(Text, nullable=True)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
