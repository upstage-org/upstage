import logging
import secrets
import os
import sys

import pymongo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import MONGO_HOST, MONGO_PORT, SQLALCHEMY_DATABASE_URI


def build_mongo_client(host=MONGO_HOST, port=MONGO_PORT):
    return pymongo.MongoClient(host, port)


def build_pg_engine(connection_string=SQLALCHEMY_DATABASE_URI):
    return create_engine(connection_string)


def build_pg_session():
    eng = build_pg_engine()
    Session = sessionmaker(bind=eng)
    return Session()