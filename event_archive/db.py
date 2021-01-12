import logging
import secrets
import os
import sys

import pymongo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config as conf


def build_mongo_client(host=conf.MONGO_HOST, port=conf.MONGO_PORT):
    return pymongo.MongoClient(host, port)


def build_pg_engine(connection_string=conf.PG_CONNECTION_STR):
    return create_engine(connection_string)


def build_pg_session():
    eng = build_pg_engine()
    Session = sessionmaker(bind=eng)
    return Session()